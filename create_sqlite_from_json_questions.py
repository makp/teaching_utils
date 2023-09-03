import json
import sqlite3

def create_sqlite_from_json(json_path, db_path):
    # Read JSON file
    with open(json_path, 'r') as f:
        questions = json.load(f)

    # Connect to SQLite db
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table if not exists
    c.execute("""
    CREATE TABLE IF NOT EXISTS questions(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      question_type TEXT,
      question TEXT,
      mc_options TEXT,
      correct_answer TEXT,
      subject TEXT,
      notes TEXT
    );
    """)

    # Insert questions from JSON into SQLite
    for q in questions:
        c.execute("INSERT INTO questions (question_type, question, mc_options, correct_answer, subject, notes) VALUES (?, ?, ?, ?, ?, ?)",
                  (q['question_type'], q['question'], json.dumps(q['mc_options']), q['correct_answer'], json.dumps(q['subject']), q['notes']))

    # Commit and close
    conn.commit()
    conn.close()
