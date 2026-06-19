#!/usr/bin/env python3
import sys
from pathlib import Path

def sair():
    sys.exit(0)

#pergunta ao usuário, se não escrever nada, usa os valores padrões, se não tiver padrão, repete a pergunta
def perguntar(prompt, padrao=None):
    sufixo = f" [{padrao}]" if padrao else ""
    while True:
        resposta = input(f"{prompt}{sufixo}: ").strip()
        if resposta or padrao or resposta.lower() == "sair": 
            if resposta.lower() == "sair":
                sair()
            return resposta or padrao
        print(" Campo obrigatório.")

#configurações do cabeçalho: nprocshared, mem, rwf, método, opções extras, maxdisk e scf
def defCabecalho():
    print("\n" + "="*60 + "\n  CONFIGURAÇÃO DO CABEÇALHO GAUSSIAN\n" + "="*60)
    
    while True:
        nproc = perguntar("  %nprocshared", "40")
        if nproc.isdigit() and int(nproc) > 0:
            break
        print("  Valor inválido: %nprocshared deve ser um número inteiro.")
    
    while True:
        mem = perguntar("  %mem", "120000MB")
        unidade = mem[-2:]
        numero = mem[:-2]
        if unidade in ("MB", "GB", "TB") and numero.isdigit():
            break
        print("  Valor inválido: use um inteiro seguido de MB, GB ou TB (ex: 120000MB).")

    rwf = perguntar("  %rwf") 
    route = perguntar("  Parâmetros")
    if not route.startswith("#"):
        route = "#" + route

    
    return {"nproc": nproc, "mem": mem, "rwf": rwf, "route": route}

#lê as coordenadas, procura linhas com 4 ou mais colunas. tenta converter as 3 ultimas em float; se forem -> considera como válida, se não, ignora.
def ler_coordenadas(caminho):
    coords = []
    for linha in caminho.read_text().splitlines(): #divide linha por linha
        p = linha.split() #divide cada linha em partes, por espaço
        if len(p) >= 4:
            try:
                [float(x) for x in p[1:4]]
                coords.append(f" {linha.strip()}")
            except ValueError:
                pass
                
                
    if not coords: 
        raise ValueError(f"Nenhuma coordenada válida encontrada.")
    return "\n".join(coords)

def main():

    info = (
        "\n" + "="*60 + "\n"
        " Digite sair a qualquer momento para encerrar o programa.\n"
        "\n" + "="*60
    )
    print(info)

    #pasta de entrada
    pasta_input = Path(perguntar("\n[1/3] Caminho da pasta com arquivos .com")).expanduser() #



    arquivos_com = sorted(pasta_input.glob("*.com")) #procura os arquivos .com e ordena por nome/numero
    if not arquivos_com:
        sys.exit(f"\n  ERRO: nenhum arquivo .com em: {pasta_input}") #sai do programa se nao encontrar nenhum arquivo .com
    
    print(f"\n{len(arquivos_com)} arquivo(s) .com encontrado(s).")

    # arquivo de rodapé
    rodape_path = Path(perguntar("\n[2/3] Caminho do rodapé .txt")).expanduser()
    if not rodape_path.is_file():
        sys.exit(f"\n  ERRO: arquivo de rodapé não encontrado: {rodape_path}") #sai do programa se nao encontrar

    rodape_str = rodape_path.read_text().lstrip('\n')
    print(f"\nRodapé carregado.")

    #cabeçalho
    print("\n[3/3] Configuração do cabeçalho:")
    cabecalho = defCabecalho()

    #criação da subpasta
    pasta_saida = pasta_input / "Resultados_Script" #cria resultados dentro da pasta de entrada
    pasta_saida.mkdir(exist_ok=True)
    print(f"\nPasta de saída: {pasta_saida}")

    #processamento
    print("\n" + "="*60 + "\n  PROCESSANDO ARQUIVOS...\n" + "="*60)
    erros = []

    for idx, caminho in enumerate(arquivos_com, start=1):
        nome_base = caminho.stem
        nome_saida = f"{nome_base}.gjf" #para evitar sobrescrever o .com original
        nome_chk = f"{nome_base}.chk"

        try:
            coords_str = ler_coordenadas(caminho)
            
            conteudo = ( #para cada arquivo, monta o cabeçalho e rodpé
                f"%nprocshared={cabecalho['nproc']}\n"
                f"%mem={cabecalho['mem']}\n"
                f"%chk={nome_chk}\n"
                f"%rwf={cabecalho['rwf']}\n"
                f"{cabecalho['route']}\n\n"
                "Title Card Required\n\n"
                "0 1\n"
                f"{coords_str}\n\n"
                f"{rodape_str}\n"
            )
            
            (pasta_saida / nome_saida).write_text(conteudo) #salva na pasta de saída
            print(f"  [{idx:>4}]  {caminho.name:45s}  →  {nome_saida}") #mostra o progresso e nome do arquivo original/resultado

        except Exception as e:
            erros.append((caminho.name, str(e)))
            print(f"  [{idx:>4}]  ERRO em {caminho.name}: {e}") 

    print("\n" + "="*60)
    total_ok = len(arquivos_com) - len(erros) #
    print(f"  Concluído!  {total_ok}/{len(arquivos_com)} arquivo(s) gerado(s).")
    
    if erros:
        print(f"  {len(erros)} erro(s):") 
        for arq, msg in erros:
            print(f"    - {arq}: {msg}") #mostra os erros encontrados
            
    print(f"  Salvos em: {pasta_saida}\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()