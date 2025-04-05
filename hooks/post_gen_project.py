import os

GREEN = "\033[92m"
BOLD = "\033[1m"
RESET = "\033[0m"

message = f"""
{BOLD}{GREEN}Project generated:{RESET} {os.getcwd()}
    
Useful links:{GREEN}
 * Installing Poetry: https://python-poetry.org/docs/#installation
 *     Documentation: https://id-translation.readthedocs.io/
 *   Asking for help: https://github.com/rsundqvist/id-translation-project/issues/new
 *    Reporting bugs: https://github.com/rsundqvist/id-translation/issues/new{RESET}

To continue, start the test database:
  {GREEN}docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres{RESET}

then execute the setup script:
  {GREEN}{os.getcwd()}/setup-and-verify.sh{RESET}

The `setup-and-generate.sh` script will:{GREEN}
  1. Lint the generated project (`ruff`)
  2. Run the included unit tests against the test database (`pytest`).
  3. Run static type checking (`mypy`).
  4. Generate documentation for the new project (`sphinx`).{RESET}

Thank you for using the {BOLD}id-translation-project{RESET} template!
"""
message = message.strip()

print(message)
