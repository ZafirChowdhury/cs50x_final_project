# GRADE TRACKER
#### Video Demo:  https://youtu.be/fgkI9mjhSCY
#### Description:

GradeTracker is a user-friendly web application designed to keep a record of their academic performance, semester by semester.

Key Features:
Semester-Based Organization.
Automatic GPA Calculation.
Edit and deletion.

In this app you can add what course(Course Id/Name, Credit count, grade). The app will show you all your cources seperated by semester in the home page. The app will autometaclly calculate your gpa and cgpa based on your grade and credit count. You can also edit or remove a semester or grade if needed.

This project also has proper login by hashing by werkzeug.security. So passwords are safely secured.

What did I use to make this project -
Python/Flaks at the backend.
Html/Jinja for the forentned.
Some CSS.
Finally Sqlight3 for the database.

Why this project -
At first I was thinking about making a web version of my CS50P final project(Grade calculator) but it was too simple. So I decited to make this.

Things I learned -
Got a better idea about how Flask works.
Python sorting with sorted() using keys.
Dynamically make input form using input form the user.
Dynamically taking variable input form the user.
Using Python "globals ()" to make dynamic variable names.
Transfering data between web pages.

To be honest I am not that proud of this project. Becasue the idea is not so good. I did not think trought it well enough. But I am satisfied with what I built. Learned a lot of things and had a lot of fun doing it.

I dont meet the propoer readme len, so I guss a more proper discription -

## Features

- User registration and authentication system.
- View and manage course data for different semesters.
- Calculate and display cumulative GPA (CGPA).
- Add, edit, and remove course information.
- Change password functionality.

Usage
Register: Sign up for an account with a unique username and password.
Log In: Log in with your registered username and password.
Home Page: View your CGPA, semester-wise GPAs, and course data.
Add Course: Add new courses along with credit counts and grades.
Edit Course: Edit existing course information.
Remove Course: Remove courses from the gradebook.
Change Password: Change your account password.
Log Out: Log out of your account.

Routes and Views:

/: This is the main page of the application. If a user is not logged in, they are redirected to the login page. If a user is logged in, their grade data is retrieved from the database, and their cumulative GPA (CGPA) and semester-wise GPA information are calculated and displayed.

/register: This route handles user registration. It checks for valid input, hashes the password, and inserts the user's information into the database.

/login: Handles user login. It checks the entered credentials against the database, and if they match, the user is logged in by storing their user ID in the session.

/logout: Clears the user session, effectively logging them out.

/add: Allows users to add courses to their gradebook. Users must be logged in to access this route. The user selects the semester and the number of courses they want to add.

/pack: Collects data for the courses being added and inserts them into the database.

/remove: Allows users to remove courses or entire semesters from their gradebook.

/edit: Provides options to either change semesters or edit courses.

/change_password: Allows users to change their account password.

/apology: Displays error messages that are stored in the session and clears them.

