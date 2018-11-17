# plik gdzie testuje wysyłanie zmian na Githuba
# można modyfikowac :) LM
from flask import Flask

app = Flask(__name__)
counter = 0

@app.route('/')
def hello():
        global counter
        counter += 1
        return f'Hello, World! odwiedzono: {counter} razy.'

@app.route('/')
def cos ():
    return "A"

if __name__ == "__main__":
    app.run()