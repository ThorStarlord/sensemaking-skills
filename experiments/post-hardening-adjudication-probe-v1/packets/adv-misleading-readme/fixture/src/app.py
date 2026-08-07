def ingest(path):
    return open(path).read()

if __name__ == '__main__':
    import sys
    ingest(sys.argv[1])
