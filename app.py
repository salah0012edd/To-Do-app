from flask import Flask, render_template ,redirect, request ,url_for 
from tasks import *

app =Flask(__name__ ,template_folder='templates')

def db_connection():
    conn = sqlite3.connect('tasks.db')
    # telling SQLite to return the results as Row objects instead of tuples
    # make it easy to access the values in tasks
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = db_connection()
    todos = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template("index.html", todoe=todos)
 
@app.route("/add", methods=["POST"])
def add_todo():
    # Give me the value of the form field named title that was submitted with this request"
    title = request.form['title']
    date = request.form['date'] 
    description = request.form['description'] 
    conn = db_connection()
    insertDB(title, description, date)
    conn.close()    
    return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["POST"])
def update_todo(id):
    status = request.form['status']
    conn = db_connection()
    updateDB(status, id)
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete_todo(id):
    conn = db_connection()
    deleteDB(id)
    return redirect(url_for('index'))

    
if __name__ == "__main__": 
    createDB()
    app.run(debug=True)
