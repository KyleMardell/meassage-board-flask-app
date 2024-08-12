# Message Board Flask App

Link - [Message Board App](https://message-board-app-07d4b12315a8.herokuapp.com/)

This is a simple message board app i made in a weekend to learn more about flask and postgres.
Login is basic only requiring a username and password. Passwords are encrypted.
You can create a post with a topic or comment on another post.
Admin can delete comments and posts.

If i were to build it again i would only use 1 relationship per database table, for example using only the user id attached to posts and comments rather than using both id and username to make it easier to edit your username. Its all learning and i had fun building it.






## Build and workspace details

Due to using gitpod and the CI template, you must run "set_pg" in the terminal every time you open the workspace.
If the workspace is completely closed, the database must be re-created initialized and populated, any previous data will be lost.

### Set up instructions
- install packages
  - Flask-SQLAlchemy (flask and sql alchemy in 1 install)
  - psycopg2 (to use postegresql database)
  - flask-login (to use the login package)
  - flask-bcrypt (for password encryption)

- Create initial files required for flask
  - run.py
  - env.py (add to gitignore as it contains a secret-key, these variables are added to heroku for deployment)
  - messageboard folder (create a folder for the package, contains the following)
    - __init__.py (initializes the application and database from inside the package)
    - routed.py (contains all the routes or each page urls, and any variables required)
    - templates folder (must be named templates for flask to recognize all contained html pages)
      - base.html (the base html template, all other html pages extend from this template using jinja)
    - static folder (contains folders such as js, css, images etc)
  - Once all files are created, check the base template runs with "python(3) run.py"

- Create the database schema
  - models.py (contains the database schema to initialize after creating the database)

- Create the database using postgresql
  - Type "psql" in the terminal to login to the postgres CLI
  - Type "CREATE DATABASE database-name" to create the database, the database name in this case is messageboard, to match our package
  - Type "\c database-name" to connect to the new database, again named messageboard in this case
  - Type "\q" to exit the postgres CLI once the database is creates and connected

- Initialize the database
  - create_db.py (imports the app and database from the messagebaord and run.py files)
