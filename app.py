
from flask import Flask, render_template, request, redirect
import sqlite3

from database import connect_db, create_tables
from algorithms import (
    linear_search,
    binary_search,
    bubble_sort,
    merge_sort
)

app = Flask(__name__)

# Create database tables
create_tables()


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# STUDENT RECORDS PAGE
@app.route("/students", methods=["GET", "POST"])
def students():

    error = ""

    if request.method == "POST":

        student_id = request.form["student_id"].strip()
        name = request.form["name"].strip()
        department = request.form["department"].strip()
        year = request.form["year"]

        if not student_id or not name or not department:
            error = "Please fill in all student details."

        else:
            conn = connect_db()

            try:
                conn.execute(
                    "INSERT INTO students VALUES (?, ?, ?, ?)",
                    (student_id, name, department, year)
                )

                conn.commit()

            except sqlite3.IntegrityError:
                error = "This Student ID already exists."

            finally:
                conn.close()

            if not error:
                return redirect("/students")

    conn = connect_db()

    student_list = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    return render_template(
        "students.html",
        students=student_list,
        error=error
    )


# ATTENDANCE PAGE
@app.route("/attendance", methods=["GET", "POST"])
def attendance():

    message = ""

    if request.method == "POST":

        student_id = request.form["student_id"]
        date = request.form["date"]
        status = request.form["status"]

        conn = connect_db()

        student = conn.execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,)
        ).fetchone()

        if student:

            try:
                conn.execute(
                    """
                    INSERT INTO attendance
                    (student_id, date, status)
                    VALUES (?, ?, ?)
                    """,
                    (student_id, date, status)
                )

                conn.commit()

                message = "Attendance saved successfully!"

            except sqlite3.IntegrityError:
                message = "Could not save attendance."

        else:
            message = "Student not found."

        conn.close()

    conn = connect_db()

    student_list = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    records = conn.execute(
        "SELECT * FROM attendance ORDER BY date DESC"
    ).fetchall()

    conn.close()

    return render_template(
        "attendance.html",
        students=student_list,
        records=records,
        message=message
    )


# ALGORITHM EXPLORER PAGE
@app.route("/explorer", methods=["GET", "POST"])
def explorer():

    result = None
    steps = []
    selected_algorithm = ""
    complexity = ""

    # Get student attendance information
    conn = connect_db()

    rows = conn.execute("""
        SELECT
            s.id,
            s.name,
            s.department,
            s.year,
            COUNT(a.record_id) AS total,
            SUM(
                CASE
                    WHEN a.status = 'Present' THEN 1
                    ELSE 0
                END
            ) AS present

        FROM students s

        LEFT JOIN attendance a
        ON s.id = a.student_id

        GROUP BY s.id
    """).fetchall()

    conn.close()

    # Calculate attendance percentages
    student_data = []

    for row in rows:

        total = row["total"]
        present = row["present"] or 0

        percentage = (
            present / total * 100
            if total else 0
        )

        student_data.append({
            "id": row["id"],
            "name": row["name"],
            "department": row["department"],
            "year": row["year"],
            "percentage": round(percentage, 2)
        })

    # Run selected algorithm
    if request.method == "POST":

        selected_algorithm = request.form["algorithm"]

        # 1. LINEAR SEARCH
        if selected_algorithm == "linear":

            target = request.form["student_id"].strip()

            result, steps = linear_search(
                student_data,
                target
            )

            complexity = "Time: O(n) | Space: O(1)"

        # 2. BINARY SEARCH
        elif selected_algorithm == "binary":

            target = request.form["student_id"].strip()

            # Sort student IDs before binary search
            sorted_students = sorted(
                student_data,
                key=lambda s: s["id"]
            )

            result, steps = binary_search(
                sorted_students,
                target
            )

            complexity = (
                "Search: O(log n) | "
                "Pre-sorting: O(n log n)"
            )

        # 3. BUBBLE SORT
        elif selected_algorithm == "bubble":

            result, steps = bubble_sort(student_data)

            complexity = "Time: O(n²) | Space: O(1)"

        # 4. MERGE SORT
        elif selected_algorithm == "merge":

            result, steps = merge_sort(student_data)

            complexity = "Time: O(n log n) | Space: O(n)"

    return render_template(
        "explorer.html",
        students=student_data,
        result=result,
        steps=steps,
        selected_algorithm=selected_algorithm,
        complexity=complexity
    )


# RUN APPLICATION
if __name__ == "__main__":
    app.run(debug=True)
