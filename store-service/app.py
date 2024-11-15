import sqlite3
from flask import Flask, render_template, request, redirect, url_for

DB_PATH = 'database/test.db'
app = Flask(__name__)

@app.route('/add_item', methods=['POST'])
def add_item():
    # validate mew records 
    a = request.form.get('a')
    b = request.form.get('b')
    if a is None or b is None:
        abort(400)
    try:
        a = int(a)
    except ValueError:
        abort(400)
    # insert new record
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute('INSERT INTO t1(a, b) VALUES (?,?)', (a, b))
        con.commit()
    #redirect to the main page
    return redirect(url_for('main_page'))

@app.route('/')
def main_page():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM sqlite_master')
        print(cur.fetchall())
        cur.execute('SELECT * FROM t1')
        return render_template('index.html',
                               columns=[x[0] for x in cur.description],
                               data=cur.fetchall())

if __name__ == '__main__':
    app.run('0.0.0.0', port=5010, debug=True)

