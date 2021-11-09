from sqlite3.dbapi2 import IntegrityError
from flask import Flask, render_template, request, session, redirect
import os
import database

app = Flask(__name__)
app.secret_key = os.urandom(32)
database.create_tables()

@app.route('/', methods=['GET', 'POST'])
def display_login():
    if (not session.get("user_id")):
        return redirect("/login")
    return render_template(
        'home.html', user_id=session.get("user_id"),
    )

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if(session.get("user_id")):
        return redirect("/")
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user_id = database.authenticate(username, password)
        if(user_id):
            session["user_id"] = user_id #Cookie based authentication (user is identified by his client id)
            return redirect("/")
        else:
            return render_template('login.html', error=True)

    return render_template(
        'login.html'
    )

@app.route('/register', methods=['GET','POST'])
def register_user():
    if(session.get("user_id")):
        return redirect("/")
    password = ''
    confirm = ''
    if(request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        if(str(password) != str(confirm) or password == '' or confirm == ''):
            return render_template('register.html', error = True,
                error_message="Your passwords didn't match :(")
        elif(str(password) == str(confirm)):
            try:
                session['user_id'] = database.create_user(username, password)
                return redirect("/")
            except IntegrityError:
                return render_template('register.html', error = True,
                error_message="That username is already taken. Please pick another one.")
            except Exception:
                return render_template('register.html', error = True,
                error_message="Sorry, something went wrong on our end. Please try registering later.")

    return render_template(
        'register.html'
    )
@app.route('/blog/<int:user_id>', methods=['GET', 'POST'])
def display_user_blog(user_id):

    templateArgs = {
        "entries" : database.get_entries_of_user(user_id, 0, 50),
        "username" : database.get_username_from_id(user_id),
        "lookingAtOwnBlog": session.get("user_id") == user_id
    }
    return render_template(
        'blog.html',
        **templateArgs
    )

@app.route('/entry/<int:entry_id>', methods=['GET', 'POST'])
def display_entry(entry_id):
    template_args = database.get_entry(entry_id)
    template_args["username"] = database.get_username_from_id(template_args["user_id"])
    template_args["original_author"] = session.get("user_id") == template_args["user_id"]
    print(session.get("user_id"))
    return render_template(
        'entry.html',
        **template_args
    )

@app.route('/blog/newBlogEntry', methods=['GET', 'POST'])
def create_new_entry():
    if(session.get("user_id") == None):
        return redirect("/")
    if(request.method == 'POST'):
        user_id = session.get("user_id")
        new_entry_text = request.form.get('entry_text')
        new_title = request.form.get('title')
        database.add_entry(new_title, new_entry_text, user_id)

        #This assumes that the entry_id of the one we just added to the database, is the user's most recent entry
        assumed_entry_id = database.getMostRecentEntry(user_id)["entry_id"]
        return redirect(f"/entry/{assumed_entry_id}")
    return render_template("newBlogEntry.html", user_id=session.get("user_id"))

@app.route('/entry/<int:entry_id>/edit', methods=['GET', 'POST'])
def display_entry_edit(entry_id):
    if(session.get("user_id") == None):
        return redirect("/")
    if request.method == 'POST':
        author_id = database.get_entry(entry_id)["user_id"]
        if(not author_id == session.get("user_id")):
            return "Sorry, you can't modify this blog post if you aren't its author."
        new_entry_text = request.form.get('entry_text')
        new_title = request.form.get('title')
        database.edit_entry(entry_id, new_entry_text, new_title)
        return redirect(f"/entry/{entry_id}")
    if request.method == 'GET':
        templateArgs = database.get_entry(entry_id)
        return render_template('entry_edit.html', **templateArgs)

@app.route('/entry/delete', methods=['POST'])
def delete():
    if(session.get("user_id") == None):
        return redirect("/")
    entry_id = request.form["entry_id"]
    author_id = database.get_entry(entry_id)["user_id"]
    user_id = session.get("user_id")
    if(not author_id == user_id):
        return "Sorry, you can't modify this blog post if you aren't its author."

    database.delete_entry(entry_id)
    return redirect(f"/blog/{user_id}")


if __name__ == '__main__':
    app.debug = True
    app.run()
