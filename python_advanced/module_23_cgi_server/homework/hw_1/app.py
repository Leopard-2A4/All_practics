from wsgiref.simple_server import make_server

from routes import application

if __name__ == '__main__':
    srv = make_server('127.0.0.1', 8000, application)
    print("Serving on http://127.0.0.1:8000")
    srv.serve_forever()
