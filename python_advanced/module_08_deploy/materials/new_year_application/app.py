import os
from flask import Flask, render_template, send_from_directory

root_dir = os.path.dirname(os.path.abspath(__file__))
static_directory = os.path.join(root_dir, "static")
print(f"Static directory: {static_directory}")
print(f"Static exists: {os.path.exists(static_directory)}")

app = Flask(__name__, template_folder='templates')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/static/<path:filename>")
def send_static(filename):
    print(f"Serving: {filename}")
    return send_from_directory(static_directory, filename)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
#