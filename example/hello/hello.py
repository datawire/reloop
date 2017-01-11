#!/usr/bin/env python

import pg8000
from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello(name):
    setup()
    conn = get_db("counter")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM counter FOR UPDATE")
    [counter] = cursor.fetchone()
    cursor.execute("UPDATE counter SET hits = hits + 1")
    conn.commit()
    return "Hello! You are hit #{}.".format(name, counter + 1)


def setup():
    conn = get_db("postgres")
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'counter'")
    results = cursor.fetchall()
    if not results:
        cursor.execute("CREATE DATABASE counter")
    conn.commit()
    conn.close()
    conn = get_db("counter")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS counter (hits INTEGER)")
    conn.commit()
    cursor.execute("SELECT * FROM counter FOR UPDATE")
    results = cursor.fetchall()
    if not results:
        cursor.execute("INSERT INTO counter VALUES (0)")
    conn.commit()
    conn.close()


def get_db(database):
    return pg8000.connect(user="postgres", password="postgres",
                          database=database,
                          host="mydatabase")


def main():
    app.run(debug=True)


if __name__ == '__main__':
    setup()
    main()
