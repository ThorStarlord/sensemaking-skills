from db import get_conn

def poll():
    conn = get_conn()
    print('polling')

if __name__ == '__main__':
    poll()
