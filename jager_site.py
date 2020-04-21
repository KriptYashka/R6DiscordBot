from flask import Flask, jsonify, render_template, request

application = Flask(__name__)

@application.route('/')
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    from os import environ
    application.run(host='0.0.0.0', port=int(environ['PORT']))