#!/usr/bin/python3
"""
script that starts a Flask web application
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    A route that displays 'Hello HBNB!' when accessed.
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    A route that displays 'HBNB' when accessed
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """
    A route that displays 'C ' followed by the value of the text variable.
    """
    text = text.replace("_", " ")
    return "C " + text


@app.route('/python/<text>', strict_slashes=False)
def python(text="is_cool"):
    """
    A route that displays 'Python ' followed by the value of the text variable
    """
    text = text.replace("_", " ")
    return "Python " + text


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """
    A route that displays 'n is a number' only if n is an integer.
    """
    return f"{n} is a number"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
