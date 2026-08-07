def save(data, path):
    with open(path, 'w') as f:
        f.writelines(data)
