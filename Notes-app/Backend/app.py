from http.client import HTTPException
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
conn = psycopg2.connect(database="note_app",
                        user="admin",
                        password="admin",
                        host="localhost",
                        port="5432",
                        sslmode="disable")
cur = conn.cursor()


@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        return e
    return


@app.route('/', methods=['GET'])
def get_notes():
    try:
        cur.execute("SELECT * FROM NoteTable")
        data = cur.fetchall()
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify({"error": "Error while fetching data"})


@app.route('/push', methods=['POST'])
def push_notes():
    print("pushing...")
    try:
        data = request.get_json()
        print(data)
        title = data['titleValue']
        text = data['noteValue']
        id_to_update = data.get('id', None)

        if id_to_update:
            update_query = "UPDATE NoteTable SET text = %s WHERE id = %s"
            cur.execute(update_query, (text, id_to_update))
        else:
            insert_query = "INSERT INTO NoteTable (title, text) VALUES (%s, %s)"
            cur.execute(insert_query, (title, text))
        conn.commit()
        return jsonify({"success": "Data pushed successfully"})
    except Exception as e:
        print(e)
        return jsonify({"error": "Error while pushing data"})


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5000)
