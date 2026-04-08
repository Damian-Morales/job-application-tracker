import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


def get_db_connection():
    connection = sqlite3.connect("applications.db")
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def home():
    connection = get_db_connection()
    applications = connection.execute(
        "SELECT * FROM applications ORDER BY id DESC"
    ).fetchall()
    connection.close()
    return render_template("index.html", applications=applications)


@app.route("/add", methods=["GET", "POST"])
def add_application():
    if request.method == "POST":
        company = request.form["company"]
        job_title = request.form["job_title"]
        status = request.form["status"]
        date_applied = request.form["date_applied"]
        notes = request.form["notes"]

        connection = get_db_connection()
        connection.execute(
            "INSERT INTO applications (company, job_title, status, date_applied, notes) VALUES (?, ?, ?, ?, ?)",
            (company, job_title, status, date_applied, notes)
        )
        connection.commit()
        connection.close()

        return redirect(url_for("home"))

    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_application(id):
    connection = get_db_connection()
    application = connection.execute(
        "SELECT * FROM applications WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":
        company = request.form["company"]
        job_title = request.form["job_title"]
        status = request.form["status"]
        date_applied = request.form["date_applied"]
        notes = request.form["notes"]

        connection.execute(
            """
            UPDATE applications
            SET company = ?, job_title = ?, status = ?, date_applied = ?, notes = ?
            WHERE id = ?
            """,
            (company, job_title, status, date_applied, notes, id)
        )
        connection.commit()
        connection.close()

        return redirect(url_for("home"))

    connection.close()
    return render_template("edit.html", application=application)


@app.route("/delete/<int:id>", methods=["POST"])
def delete_application(id):
    connection = get_db_connection()
    connection.execute("DELETE FROM applications WHERE id = ?", (id,))
    connection.commit()
    connection.close()

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)