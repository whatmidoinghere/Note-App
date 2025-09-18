from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tag TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    search = request.args.get('search')
    tag = request.args.get('tag')
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    
    if search:
        c.execute("SELECT * FROM notes WHERE title LIKE ? OR content LIKE ?", 
                  (f'%{search}%', f'%{search}%'))
    elif tag:
        c.execute("SELECT * FROM notes WHERE tag=?", (tag,))
    else:
        c.execute("SELECT * FROM notes ORDER BY created_at DESC")
    
    notes = c.fetchall()
    conn.close()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['GET', 'POST'])
def add_note():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tag = request.form['tag']
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('notes.db')
        c = conn.cursor()
        c.execute("INSERT INTO notes (title, content, tag, created_at) VALUES (?, ?, ?, ?)", 
                  (title, content, tag, created_at))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        tag = request.form['tag']
        c.execute("UPDATE notes SET title=?, content=?, tag=? WHERE id=?", 
                  (title, content, tag, note_id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    c.execute("SELECT * FROM notes WHERE id=?", (note_id,))
    note = c.fetchone()
    conn.close()
    return render_template('edit.html', note=note)

@app.route('/delete/<int:note_id>')
@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True) 