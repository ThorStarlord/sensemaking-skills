import os

def load_plugins(directory):
    for name in os.listdir(directory):
        if name.endswith('.py'):
            exec(open(os.path.join(directory, name)).read())
