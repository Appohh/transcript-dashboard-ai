import mysql.connector

def run_query(sql):
    # Connect to MySQL (MAMP defaults)
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",   # default MAMP password
        database="call_transcripts",
        port=3306          # MAMP MySQL port
    )

    cursor = conn.cursor()
    cursor.execute(sql)

    # Fetch results if it's a SELECT
    if sql.strip().lower().startswith("select"):
        result = cursor.fetchall()
        for row in result:
            print(row)

    # Commit if needed (INSERT, UPDATE, DELETE)
    conn.commit()
    cursor.close()
    conn.close()


# Example usage:
run_query("SELECT * FROM calls LIMIT 5;")