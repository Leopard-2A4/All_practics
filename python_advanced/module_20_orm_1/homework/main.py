from routes import app

if __name__ == '__main__':
    from db import init_test_data
    init_test_data()
    app.run(debug=True)