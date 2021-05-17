from logging import debug
from types import MethodType
from flask import Flask, app, render_template, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def process():
    email = request.form['email']
    name = request.form['name']

    if name and email:
        newName = name[::-1]
        return jsonify({'name' : newName})
    return jsonify({'error' : 'Missing Name!'})

if __name__ == '__main__':
    app.run(debug=True)
