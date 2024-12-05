import sqlite3
import csv

DATABASE = 'src/verbs.db'

# Connect to the database
with sqlite3.connect(DATABASE) as conn:
    cursor = conn.cursor()

    # Create table if it doesn't exist, and ensure dictionary_form is unique
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verbs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dictionary_form TEXT NOT NULL UNIQUE,  -- Ensure uniqueness of dictionary_form
        kanji_form TEXT NOT NULL,
        translation TEXT NOT NULL,
        lesson_num INTEGER NOT NULL,
        verb_class TEXT NOT NULL,
        book TEXT NOT NULL,
        class_name TEXT NOT NULL
    )
    """)

    # Load data from CSV and insert into the database
    with open('src/verbs.csv', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        # Skip the header row
        next(csvreader)

        # Insert each row into the database, using INSERT OR IGNORE to avoid duplicates
        for row in csvreader:
            cursor.execute("""
                INSERT OR IGNORE INTO verbs (dictionary_form, kanji_form, translation, lesson_num, verb_class, book, class_name) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, row)

    # Commit changes
    conn.commit()

print("Database populated with verb data from CSV!")

