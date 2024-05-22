from flask import Flask, send_from_directory
import os

app = Flask(__name__)
output_dir = 'output_graphs'

@app.route('/', methods=['GET'])
def index():
    return "Welcome to Contractor Performance Analysis!"

@app.route('/graph/<filename>', methods=['GET'])
def get_graph(filename):
    try:
        return send_from_directory(output_dir, filename)
    except FileNotFoundError:
        return "File not found", 404
    
if __name__ == '__main__':
    app.run(debug=True)