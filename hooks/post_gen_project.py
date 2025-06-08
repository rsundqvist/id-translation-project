import os

GREEN = "\033[92m"
BOLD = "\033[1m"
RESET = "\033[0m"

message = f"""
{BOLD}Project generated{RESET}.
{GREEN} * Location:{RESET} '{os.getcwd()}'
{GREEN} *     Name:{RESET} '{{cookiecutter.project_slug}}'
{GREEN} *   Module:{RESET} '{{cookiecutter.namespace}}.id_translation'
{GREEN} *  Version:{RESET} 'id-translation {{cookiecutter.id_translation_version}}'
Useful links:
{GREEN} * Installing Poetry:{RESET} https://python-poetry.org/docs/#installation
{GREEN} *     Documentation:{RESET} https://id-translation.readthedocs.io/
{GREEN} *   Asking for help:{RESET} https://github.com/rsundqvist/id-translation-project/issues/new
{GREEN} *    Reporting bugs:{RESET} https://github.com/rsundqvist/id-translation/issues/new
To continue, start the test database:
  {GREEN}docker run -p 5002:5432 --rm rsundqvist/sakila-preload:postgres{RESET}
then execute the setup script:
  {GREEN}{os.getcwd()}/setup-and-verify.sh{RESET}
Thank you for using the {BOLD}{GREEN}id-translation-project{RESET} template!
"""
message = message.strip()

print(message)
