from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = 'agent.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# --- NEW: Database Initialization Function ---
def init_db():
    """Creates the tables if they do not exist already."""
    conn = get_db_connection()
    # Create the reviews table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            summary TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Create the learned_standards table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS learned_standards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            standard_name TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

@app.route('/')
def index():
    try:
        conn = get_db_connection()
        reviews = conn.execute('SELECT * FROM reviews ORDER BY created_at DESC').fetchall()
        
        memory_row = conn.execute('SELECT COUNT(*) as count FROM learned_standards').fetchone()
        memory_count = memory_row['count'] if memory_row else 0
        
        conn.close()
        return render_template('index.html', 
                               reviews=reviews, 
                               stats={'total': len(reviews), 'memory': memory_count})
    except Exception as e:
        print(f"SQL Error: {e}")
        return f"Database Error: {str(e)}", 500

@app.route('/new_review', methods=['POST'])
def new_review():
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO reviews (title, status, summary) 
            VALUES (?, ?, ?)
        ''', ("New Code Review", "Pending", "SQL Agent is analyzing..."))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Insert Error: {e}")
        return f"Database Error: {str(e)}", 500

if __name__ == '__main__':
    # Initialize the database before starting the web server
    init_db()
    app.run(debug=True, port=5000)