import os
from utils.CleverDict import CleverDict

def load_queries():
    Queries = CleverDict({})
    dirname, _, files = next(os.walk('./queries/gql'))
    for gql in files:
        with open(os.path.join(dirname, gql), 'r') as f:
            Queries[os.path.splitext(gql)[0]] = f.read()
    return Queries