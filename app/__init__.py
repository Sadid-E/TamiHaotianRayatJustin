from flask import Flask, render_template, request, session, redirect
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/', methods=['GET', 'POST'])
def display_home():
    return 'Hello'

@app.route('/login', methods=['GET', 'POST'])
def display_login():
    return 'Hello'

@app.route('/blog/<user_id>', methods=['GET', 'POST'])
def display_user_blog():
    return 'Hello'

@app.route('/entry/<blog_entry_id>', methods=['GET', 'POST'])
def display_entry():
    return 'Hello'

@app.route('/entry/<blog_entry_id>/edit', methods=['GET', 'POST'])
def display_entry_edit():
    return 'Hello'

if __name__ == '__main__':
    app.debug = True
    app.run()
