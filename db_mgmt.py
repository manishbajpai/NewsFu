import sqlite3

def add_column_to_table(db_file, table_name, new_column, column_type='TEXT'):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    c = conn.cursor()

    # Construct and execute the SQL statement to add a new column
    sql = f'ALTER TABLE {table_name} ADD COLUMN {new_column} {column_type}'
    try:
        c.execute(sql)
        conn.commit()
        print(f"Column '{new_column}' added successfully to '{table_name}'.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the database connection
        conn.close()

# Usage example
db_file = 'example.db'
table_name = 'articles'
new_column = 'category'
add_column_to_table(db_file, table_name, new_column)
