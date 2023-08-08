from flask import Flask, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from cs50 import SQL
from helpers import sort_semesters

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///gradebook.db")

@app.route("/")
def index():
    if session.get("user_id") is None:
        return redirect("/login")

    "CREATE TABLE grades (id INTEGER, semester TEXT, course_id TEXT, credit_count INTEGER, gpa REAL)"
    user_data = db.execute("SELECT * FROM grades WHERE id = ?", session["user_id"])
    if len(user_data) == 0:
        return render_template("index.html", no_user_data=True)

    #CGPA calculation
    cgpa = 0
    done_credit = 0
    for course in user_data:
        if course["gpa"] >= 1 and course["credit_count"] >= 1:
            cgpa = cgpa + course["gpa"] * course["credit_count"]
            done_credit = done_credit + course["credit_count"]

    cgpa = cgpa / done_credit

    #user_data = [{} {} {}]
    #page_data = [{semester : , gpa : , cources : }]

    #Getting all the unique semesters
    semester_list_of_dict = db.execute("SELECT semester FROM grades WHERE id = ?", session["user_id"])
    semester_list = []
    for i in semester_list_of_dict:
        semester_list.append(i["semester"])
    semester_list = set(semester_list)

    #Sort the semester list
    semester_list = list(semester_list)
    semester_list = sorted(semester_list, key=sort_semesters)

    #Saving semesters to page_data
    page_data = []
    for i in semester_list:
        total_grade_point = 0
        total_credit_count = 0
        semester_data = db.execute("SELECT * FROM grades WHERE id = ? AND semester = ?", session["user_id"], i)
        for j in semester_data:
            total_grade_point = total_grade_point + (j["gpa"]  * j["credit_count"])
            total_credit_count = total_credit_count + j["credit_count"]

        gpa = total_grade_point / total_credit_count
        page_data.append({
            "semester" : i,
            "gpa" : round(gpa, 2),
            "cources" : []
        })

    for i in page_data:
        for j in user_data:
            if i["semester"] == j["semester"]:
                i["cources"].append(j)

    return render_template("index.html", cgpa=round(cgpa, 2), done_credit=done_credit, data=page_data)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        password_again = request.form.get("password_again")

        if not password or not password_again or not name:
            session["error_massage"] = "Please fill out all the required fields."
            return redirect("/apology")

        if password != password_again:
            session["error_massage"] = "Confirmation password doesn't match"
            return redirect("/apology")

        rows = db.execute("SELECT * FROM users WHERE username = ?", name)
        if len(rows) > 0:
            session["error_massage"] = "Username taken"
            return redirect("/apology")

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, generate_password_hash(password))
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            session["error_massage"] = "Must provide username"
            return redirect("/apology")

        if not request.form.get("password"):
            session["error_massage"] = "Must provide password"
            return redirect("/apology")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(rows) == 0:
            session["error_massage"] = "invalid username"
            return redirect("/apology")

        if check_password_hash(rows[0]["hash"], request.form.get("password")):
            session["user_id"] = rows[0]["id"]

        else:
            session["error_massage"] = "incorrect password"
            return redirect("/apology")

        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/apology")
def apology():
    error_massage = session.get("error_massage", "Missing")
    session["error_massage"] = None
    return render_template("apology.html", error_massage=error_massage)


@app.route("/add", methods=["GET", "POST"])
def add():
    if session.get("user_id") is None:
        return redirect("/login")

    if request.method == "POST":
        try:
            course_count = int(request.form.get("course_count"))
        except ValueError:
            session["error_massage"] = "Course count must be an single digit number (Ex : 1, 2, 3, 4)"
            return redirect("/apology")
        session["semester"] = request.form.get("semester")
        session["course_count"] = course_count
        return render_template("add.html", course_count=course_count)

    return render_template("add.html", course_count=False)


@app.route("/pack", methods=["GET", "POST"])
def pack():
    if session.get("user_id") is None:
        return redirect("/login")

    if request.method == "POST":
        courses = []
        for i in range(session["course_count"]):
            course_id = request.form.get("course_id_"+str(i))
            try:
                credit_count = int(request.form.get("credit_count_"+str(i)))
            except ValueError:
                session["error_massage"] = "Credit count must be an single digit number (Ex : 1, 2, 3, 4)"
                return redirect("/apology")
            try:
                grade = float(request.form.get("grade_"+str(i)))
                if grade > 4 or grade < 1:
                    raise ValueError
            except ValueError:
                session["error_massage"] = "Grade must be in a scale of 4(1-4) (Ex : 1.1, 2, 4.0, 3.3)"
                return redirect("/apology")

            globals () ["course_" + str(i)] = {
                "course_id" : course_id,
                "credit_count" : credit_count,
                "grade" : grade
            }

            courses.append( globals () ["course_" + str(i)])

        session["courses"] = courses

        return redirect("/database")

    return redirect("/")


@app.route("/database")
def database():
    if session.get("user_id") is None:
        return redirect("/login")

    try:
        semester = session["semester"]
        courses = session["courses"]
        course_count = session["course_count"]
        id = session["user_id"]
    except KeyError:
        session["error_massage"] = "Oh dear good sir hackerman pls dont hack me"
        return redirect("/apology")

    if not semester or not courses or not course_count:
        return redirect("/")

    "CREATE TABLE grades (id INTEGER, semester TEXT, course_id TEXT, credit_count INTEGER, gpa REAL)"
    for count in range(course_count):

        course_id = courses[count]["course_id"]
        credit_count = courses[count]["credit_count"]
        gpa = courses[count]["grade"]

        db.execute("INSERT INTO grades (id, semester, course_id, credit_count, gpa) VALUES(?, ?, ?, ?, ?)", id, semester, course_id, credit_count, gpa)

    semester = None
    courses = None
    course_count = None

    return redirect("/")


@app.route("/remove", methods=["GET", "POST"])
def remove():


    if request.method == "POST":
        rm = request.form.get("rm").strip()
        if not rm:
            session["error_massage"] = "Please provide a name"
            return redirect("/apology")

        if request.form.get("choice") == "semester":
            db.execute("DELETE FROM grades WHERE id = ? AND semester = ?", session["user_id"], rm)
            #Donno how to handel SQLight errors using python, Lets hope for the best
        else:
            db.execute("DELETE FROM grades WHERE id = ? AND course_id = ?", session["user_id"], rm)

        return redirect("/")

    return render_template("remove.html")


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        if request.form.get("choice") == "semester":
            return redirect("/chnage_semester")
        else:
            return redirect("/chnage_course")

    return render_template("edit.html")


@app.route("/chnage_semester", methods=["GET", "POST"])
def chnage_semester():
    if request.method == "POST":
        change_from = request.form.get("from").strip()
        change_to = request.form.get("to").strip()

        if not change_from or not change_to:
            session["error_massage"] = "Please provide all the requred fileds"
            return redirect("/apology")

        db.execute("UPDATE grades SET semester = ? WHERE id = ? AND semester = ?", change_to, session["user_id"], change_from)
        return redirect("/")

    return render_template("chnage_semester.html")


@app.route("/chnage_course", methods=["GET", "POST"])
def chnage_course():
    if request.method == "POST":
        choice = request.form.get("choice")

        return render_template("chnage_course.html", choice=choice)

    return render_template("chnage_course.html")


@app.route("/chnage_course_action", methods=["GET", "POST"])
def chnage_course_action():
    if request.method == "GET":
        session["error_massage"] = "Nice hack hackerman"
        return redirect("/apology")

    choice = request.form.get("choice")
    semester = request.form.get("semester")
    course_id = request.form.get("course_id")
    chnage_to = request.form.get("to")

    if choice == "gpa":
        chnage_to = float(chnage_to)

    if choice == "gpa":
        if chnage_to < 1 or chnage_to >  4:
            session["error_massage"] = "Grade must be between (1-4)"
            return redirect("/apology")

    db.execute("UPDATE grades SET ? = ? WHERE id = ? AND semester = ? AND course_id = ?", choice, chnage_to, session["user_id"], semester, course_id)

    return redirect("/")


@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        password = request.form.get("password")
        password_again = request.form.get("password_again")
        password_new = request.form.get("password_new")

        if not password or not password_again or not password_new:
            session["error_massage"] = "Please fill all the requred fileds"
            return redirect("/apology")

        if password_new != password_again:
            session["error_massage"] = "Confirming Password dose not match"
            return redirect("/apology")

        hash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["hash"]
        if check_password_hash(hash, password):
            db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(password_new), session["user_id"])
            return redirect("/")

        else:
            session["error_massage"] = "Invalid password"
            return redirect("/apology")

    return render_template("change_password.html")
