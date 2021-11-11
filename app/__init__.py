from sqlite3.dbapi2 import IntegrityError
from flask import Flask, render_template, request, session, redirect
import os
import database

app = Flask(__name__)
app.secret_key = os.urandom(32)
database.create_tables()

@app.route('/', methods=['GET', 'POST'])
def display_login():
    """Initial page, redirects user to their homepage if they are logged in, to the login page if they are not"""
    if(session.get("user_id") == None):
        return redirect("/login")
    return render_template(
        'home.html', user_id=session.get("user_id"), random_users=database.get_random_users()
    )

@app.route('/logout', methods=['GET'])
def logout():
    """Removes session info, user won't see generally"""
    session.clear()
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page for user to log in to their blog, initializes cookie authentication, displays incorrect info message if user info is not present"""
    try:
        if(session.get("user_id")):
            return redirect("/")
        if request.method == 'POST':
            username = request.form.get("username")
            password = request.form.get("password")
            user_id = database.authenticate(username, password) #Checks login against database info -- see authenticate in database.py
            if(user_id):
                session["user_id"] = user_id #Cookie based authentication (user is identified by his client id)
                return redirect("/")
            else:
                return render_template('login.html', error=True) #displays to the user if the login info doesn't match any entry

        return render_template(
            'login.html'
        )
    except Exception:
        return 'Something went wrong on our end. Please try again later'

@app.route('/register', methods=['GET','POST'])
def register_user():
    """Allows user to register an account with a username and password. Error handling for passwords not matching,
    username already being taken"""
    if(session.get("user_id")):
        return redirect("/") #send them to the homepage if they are logged in
    password = ''
    confirm = ''
    if(request.method == 'POST'):
        username = request.form.get('username', default='')
        password = request.form.get('password', default='')
        confirm = request.form.get('confirm')
        #Exception handling for blank or taken usernames, blank passwords, passwords not matching, or general errors
        if(str(password) != str(confirm) or password == '' or confirm == ''):
            return render_template('register.html', error = True,
                error_message="Your passwords didn't match or were blank :(")
        if(username == ''):
            return render_template('register.html', error = True, error_message="Blank usernames are not allowed")
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
    """Displays all entires of a user. Tracks if the user is the same one that is logged in"""
    templateArgs = {}
    try:
        templateArgs = {
            "entries" : database.get_entries_of_user(user_id, 0, 50), #see get_entries_of_user in database.py
            "username" : database.get_username_from_id(user_id),#see get_username_from_id in database.py
            "lookingAtOwnBlog": session.get("user_id") == user_id #session authentication for the user
        }
    except Exception:
        return render_template("404.html")
    return render_template(
        'blog.html',
        **templateArgs
    )

@app.route('/entry/<int:entry_id>', methods=['GET', 'POST'])
def display_entry(entry_id):
    """Displays an entry of another user's blog to the user"""
    template_args = {}
    try:
        template_args = database.get_entry(entry_id) #see get_entry in database.py
        template_args["username"] = database.get_username_from_id(template_args["user_id"])
        template_args["original_author"] = session.get("user_id") == template_args["user_id"] #logic check if the user currently viewing a blog is viewing their own blog
    except Exception:
        return render_template("404.html")
    return render_template(
        'entry.html',
        **template_args
    )

@app.route('/blog/newBlogEntry', methods=['GET', 'POST'])
def create_new_entry():
    """Allows the user to create a new blog entry"""
    try:
        if(session.get("user_id") == None):
            return redirect("/") #if a non-logged in user gets here, redirect them to the login page
        if(request.method == 'POST'):
            user_id = session.get("user_id")
            new_entry_text = request.form.get('entry_text')
            new_title = request.form.get('title')
            if(new_title != ''): #can't have blank title
                database.add_entry(new_title, new_entry_text, user_id) #see add_entry in database.py
            else:
                return redirect('/blog/newBlogEntry')

            #This assumes that the entry_id of the one we just added to the database, is the user's most recent entry
            assumed_entry_id = database.getMostRecentEntry(user_id)["entry_id"]
            return redirect(f"/entry/{assumed_entry_id}")
        return render_template("newBlogEntry.html", user_id=session.get("user_id"))
    except Exception:
        return "Something went wrong on our end. Please try again later."

@app.route('/entry/<int:entry_id>/edit', methods=['GET', 'POST'])
def display_entry_edit(entry_id):
    """Allows a user to edit their own entry"""
    try:
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
            return render_template('entry_edit.html', **templateArgs) #displays the text boxes with current text and title of the post already displayed
    except Exception:
        return render_template("404.html")

@app.route('/entry/delete', methods=['POST'])
def delete():
    """Removes a user's blog entry"""
    try: 
        if(session.get("user_id") == None):
            return redirect("/")
        entry_id = request.form["entry_id"]
        author_id = database.get_entry(entry_id)["user_id"] #see get_entry in database.py
        user_id = session.get("user_id")
        if(not author_id == user_id):
            return "Sorry, you can't modify this blog post if you aren't its author."

        database.delete_entry(entry_id) #see delete_entry in database.py
        return redirect(f"/blog/{user_id}")
    except Exception:
        return render_template("404.html")


if __name__ == '__main__':
    app.debug = True
    app.run()
