#For running and tseting python code and SQLLight qurres without running the flask app
from cs50 import SQL
import pprint
pp = pprint.PrettyPrinter(indent=4)

db = SQL("sqlite:///gradebook.db")

user_data = db.execute("SELECT * FROM grades WHERE id = ?", 2)

semester_list_of_dict = db.execute("SELECT semester FROM grades WHERE id = ?", 2)
semester_list = []
for i in semester_list_of_dict:
    semester_list.append(i["semester"])
semester_list = set(semester_list)

#Saving semesters to page_data
page_data = []
for i in semester_list:
    total_grade_point = db.execute("SELECT SUM(gpa) FROM grades WHERE id = ? AND semester = ?", 2, i)[0]["SUM(gpa)"]
    number_of_course_taken = db.execute("SELECT COUNT(gpa) FROM grades WHERE id = ? AND semester = ?", 2, i)[0]["COUNT(gpa)"]
    gpa = total_grade_point / number_of_course_taken
    page_data.append({
        "semester" : i,
        "gpa" : gpa,
        "cources" : []
    })

for i in page_data:
    for j in user_data:
        if i["semester"] == j["semester"]:
            i["cources"].append(j)

pp.pprint(page_data)