from .utils.constants import DOCS_PATH

def print_docs():
    with open(DOCS_PATH, 'r') as fh:
        docs = fh.read()
        print(docs)
        fh.close()
