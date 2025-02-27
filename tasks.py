import sqlite3

ts_name = 'tasks.db'
conn = None 
cursor = None

def open():
    global conn, cursor 
    conn = sqlite3.connect(ts_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query, params=None):
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    conn.commit()

def createDB():
    open()
    cursor.execute('PRAGMA foreign_keys=ON')
    
    do('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date DATE,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
    
    close()

def insertDB(title, description, date):
    open()
    do("INSERT INTO tasks (title, description, date) VALUES (?, ?, ?)", (title, description, date)) 
    close()
    
def showDB(table):
    query = f'SELECT * FROM {table}'
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tablesDB():
    showDB('tasks')  # Only show actual data table

def updateDB(status, id):
    open()
    do("UPDATE tasks SET status = ? WHERE id = ?", (status ,id))
    close()

def deleteDB(id):
    open()
    do("DELETE FROM tasks WHERE id = ? ", (id,))
    close()

def clearIds():
    open()
    do("DELETE FROM sqlite_sequence WHERE name='tasks'")  # Add a comma to make it a tuple
    close()

def clearAll():
    open()
    do("DELETE FROM tasks")
    clearIds()
    close()
