# Flask MVC & REST Example App
*Example database application for my favorite students.*

## An application that stores users with email addresses and safe passwords.
- Supports multiple views and interchangeable models.
- Users can be created and accessed by id. 
- Users can login using their password and username.


## This demo shows the following:
- Creating a simple Flask app
- Using SQLAlchemy with Flask to create models
- "Safely" storing passwords to a database (note that there are many more considerations when working securely with passwords, this merely shows how to securely store them in a database)
- The possibility to use many different views with a single model and controller
- Templating with Jinja
- Using different REST endpoints for different client purposes
- Writing a simple terminal application to access REST endpoints
