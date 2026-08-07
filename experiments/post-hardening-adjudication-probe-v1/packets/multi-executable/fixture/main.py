from db import get_conn

def serve():
    conn = get_conn()
    print('serving', conn)

if __name__ == '__main__':
    serve()
