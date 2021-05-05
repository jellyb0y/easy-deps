from pathlib import Path
from os import getcwd

ROOT_DIR = Path(__file__).resolve().parent.parent
CUR_DIR = getcwd()

DOCS_PATH = f'{ROOT_DIR}/resources/docs.txt'
PACKAGE_FILE = f'{CUR_DIR}/.ezdeps.json'
RC_FILE = f'~/.ezdepsrc'
