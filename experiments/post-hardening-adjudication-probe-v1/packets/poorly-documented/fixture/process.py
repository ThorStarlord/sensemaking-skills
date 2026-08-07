def run(path):
    with open(path) as f:
        return [line.strip() for line in f]

def filter_empty(items):
    return [i for i in items if i]
