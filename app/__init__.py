from flask import Flask, render_template, request, session, redirect
import os

app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/', methods=['GET', 'POST'])
def display_home():
    return 'Hello'

@app.route('/login', methods=['GET', 'POST'])
def display_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form

    return render_template(
        'login.html'
    )

@app.route('/blog/<user_id>', methods=['GET', 'POST'])
def display_user_blog(user_id):
    return render_template(
        'blog.html',
        username = 'Test Username',
        entries = [{'name': 'Name 0', 'text': 'Test text', 'url': '/entry/0'}, {'name': 'Name 1', 'text': 'stuff', 'url': '/entry/1'}]
    )

@app.route('/entry/<blog_entry_id>', methods=['GET', 'POST'])
def display_entry(blog_entry_id):
    return render_template(
        'entry.html',
        entry_name = 'Test Name',
        entry_user = 'Test User',
        full_entry = ['Line 0', 'Line 1', 'Line 2']
    )

@app.route('/entry/<blog_entry_id>/edit', methods=['GET', 'POST'])
def display_entry_edit(blog_entry_id):
    if request.method == 'POST':
        text = request.form['entry']
        # write_entry_to_db(text, request.args['blog_entry_id'])
        redirect('/entry/' + blog_entry_id)
    # return render_template('entry_edit.html', text = get_entry_from_db(request.args['blog_entry_id']))
    return 'Hello'

if __name__ == '__main__':
    app.debug = True
    app.run()
