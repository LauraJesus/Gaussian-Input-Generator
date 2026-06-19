# Gaussian Input Generator

A command-line Python utility to automate the creation of Gaussian input files (`.gjf`). It efficiently batch-processes multiple structure files (`.com`), extracts coordinate geometries, and merges them with a custom computational header and footer configuration.

## Features
- **Batch Processing:** Scans and processes all `.com` files inside a target folder sequentially.
- **Smart Geometry Extraction:** Automatically filters and grabs only valid atomic coordinate blocks.
- **Interactive Configuration:** Prompts for key parameters (`%nprocshared`, `%mem`, `%rwf`, and `# route`) with quick default options.
- **Safe Outputs:** Places new files under a dedicated `Resultados_Script/` folder to prevent data overwrites.

## Prerequisites
- Python 3.6+ (No external dependencies required).

## Usage

1. Place your `.com` coordinate templates in a directory.
2. Create a `.txt` file containing any calculation instructions/bases you want to append as a footer.
3. Run the script:

```bash
python3 script.py
