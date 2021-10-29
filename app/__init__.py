from flask import Flask, render_template, request, session, redirect
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/', methods=['GET', 'POST'])
def display_home():
    return 'Hello'

if __name__ == '__main__':
    app.debug = True
    app.run()
