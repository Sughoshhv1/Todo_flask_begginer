from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# shell code
# -> from app import db
# -> db.create_all()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)       #port change can be done here


import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



# need to create a context to create a db...this code shd be put in shell
# from app import app, db
# with app.app_context():
#     db.create_all()





# Use an absolute path for the database ..will create db in same directry with app.py
# base_dir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(base_dir, 'todo.db')}"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# example for search of title of todo
# from flask import Flask, render_template, request
# from models import db, Todo  # Assuming you have a Todo model and db setup

# app = Flask(__name__)

# @app.route('/', methods=['GET', 'POST'])
# def hello_world():
#     if request.method == 'POST':
#         # Handle the POST request if needed (e.g., adding new to-do)
#         title = request.form['title']
#         desc = request.form['desc']
#         todo = Todo(title=title, desc=desc)
#         db.session.add(todo)
#         db.session.commit()

#     elif request.method == 'GET':
#         # Retrieve the title from the form's GET request (if any)
#         title_query = request.args.get('title', '')  # Default to empty string if no title is provided

#         if title_query:
#             # If a title was provided, filter the to-dos by title
#             allTodo = Todo.query.filter(Todo.title.like(f'%{title_query}%')).all()
#         else:
#             # If no title is provided, show all to-dos
#             allTodo = Todo.query.all()

#     return render_template('index.html', allTodo=allTodo)


# if __name__ == '__main__':
#     app.run(debug=True)


# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Todo App</title>
# </head>
# <body>
#     <h1>Search for a Todo</h1>
    
#     <!-- Search Form (GET method) -->
#     <form method="GET" action="/">
#         <label for="title">Title:</label>
#         <input type="text" name="title" id="title" placeholder="Enter title to search">
#         <button type="submit">Search</button>
#     </form>

#     <h2>All Todos</h2>
#     <ul>
#         {% for todo in allTodo %}
#             <li>{{ todo.title }}: {{ todo.desc }}</li>
#         {% endfor %}
#     </ul>
# </body>
# </html>
