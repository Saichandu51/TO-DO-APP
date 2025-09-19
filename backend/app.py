from flask import Flask, request, jsonify
import mysql.connector
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load DB config from env vars
db_config = {
    "host": os.environ.get("DATABASE_HOST", "db"),
    "user": os.environ.get("DATABASE_USER", "myuser"),
    "password": os.environ.get("DATABASE_PASSWORD", "mypassword"),
    "database": os.environ.get("DATABASE_NAME", "mydb")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    task = data.get("task")
    if not task:
        return jsonify({"error": "Task is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (task) VALUES (%s)", (task,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task added successfully"}), 201

@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task deleted successfully"})

if __name__ == "__main__":
    # Initialize DB table if not exists
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(255) NOT NULL
    )
    """)
    conn.commit()
    conn.close()

    app.run(host="0.0.0.0", port=5000)
