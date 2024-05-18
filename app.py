from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__)
output_dir = 'output_graphs'

@app.route('/graph/<filename>', methods=['GET'])
def get_graph(filename):
    try:
        return send_from_directory(output_dir, filename)
    except FileNotFoundError:
        return "File not found", 404

@app.route('/show_graph/<filename>', methods=['GET'])
def show_graph(filename):
    try:
        with open(os.path.join(output_dir, filename), 'r', encoding='utf-8') as f:
            graph_html = f.read()
        return render_template_string('<html><body>{{ graph_html|safe }}</body></html>', graph_html=graph_html)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)