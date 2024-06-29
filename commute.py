from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.datastructures import ImmutableMultiDict
from helpers import apology, login_required

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///commute.db")

@app.route('/', methods=["GET", "POST"])
@login_required
def index():

    usr_info = db.execute('SELECT * FROM users WHERE id=?', session["user_id"])
    user_commute_days = db.execute('SELECT * FROM commute_days WHERE user_id=?', session["user_id"])
    user_commute_times = db.execute('SELECT * FROM commute_times WHERE user_id=?', session["user_id"])

    if request.method == "POST":

        usr_submit =  ImmutableMultiDict(request.form)
        res_commute_days = usr_submit.getlist('commute_days[]')
        usr_depart_time = usr_submit.getlist('usr_departTime')
        usr_return_time = usr_submit.getlist('usr_returnTime')
        usr_home_pc = usr_submit.getlist("u_home_pc")
        usr_work_pc = usr_submit.getlist("u_work_pc")

        print(usr_home_pc)
        print(usr_work_pc)

        if usr_home_pc:
            DB_homePost_count = db.execute("SELECT COUNT(*) FROM ca_postcodes WHERE postalCode = ?", usr_home_pc)
            DB_homePost_count = DB_homePost_count[0]['COUNT(*)']
            if  DB_homePost_count > 0:
                db.execute("UPDATE users SET home_postCode=? WHERE id=?", usr_home_pc, session["user_id"])
            # else:
            #     db.execute("INSERT INTO users(id, home_postCode) VALUE(?, ?)", session["user_id"], usr_home_pc)

        if usr_work_pc:
            DB_WorkPost_count = db.execute("SELECT COUNT(*) FROM ca_postcodes WHERE postalCode = ?", usr_work_pc)
            DB_WorkPost_count = DB_WorkPost_count[0]['COUNT(*)']
            if DB_WorkPost_count > 0:
                db.execute("UPDATE users SET work_postCode=? WHERE id=?", usr_work_pc, session["user_id"])
            # else:
            #     db.execute("INSERT INTO users(id,work_postCode) VALUE(?, ?)", session["user_id"], usr_work_pc)

        if res_commute_days:
            # Check if user in DB
            DB_check_usr = db.execute("SELECT COUNT(*) FROM commute_days WHERE user_id = ?", session["user_id"])
            DB_check_usr = DB_check_usr[0]['COUNT(*)']
            usr_commute_days = {'monday': 0, 'tuesday': 0, 'wednesday': 0, 'thursday': 0, 'friday': 0, 'saturday': 0, 'sunday': 0}

            for day in res_commute_days:
                for key in usr_commute_days:
                    if day == key:
                        usr_commute_days[key] = 1

            if DB_check_usr == 0:
                db.execute("INSERT INTO commute_days(user_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", session["user_id"], usr_commute_days['monday'], usr_commute_days['tuesday'], usr_commute_days['wednesday'], usr_commute_days['thursday'], usr_commute_days['friday'], usr_commute_days['saturday'], usr_commute_days['sunday'])
            else:
                db.execute("UPDATE commute_days SET monday=?, tuesday=?, wednesday=?, thursday=?, friday=?, saturday=?, sunday=? WHERE user_id=?", usr_commute_days['monday'], usr_commute_days['tuesday'], usr_commute_days['wednesday'], usr_commute_days['thursday'], usr_commute_days['friday'], usr_commute_days['saturday'], usr_commute_days['sunday'], session["user_id"])

        if usr_depart_time:
            # Check if user in DB
            DB_check_usr = db.execute("SELECT COUNT(*) FROM commute_times WHERE user_id = ?", session["user_id"])
            DB_check_usr = DB_check_usr[0]['COUNT(*)']
            if DB_check_usr == 0:
                db.execute("INSERT INTO commute_times(user_id, Out_travel) VALUES(?, ?)", session["user_id"], usr_depart_time[0])
            else:
                db.execute("UPDATE commute_times SET Out_travel=? WHERE user_id=?", usr_depart_time[0], session["user_id"])

        if usr_return_time:
            # Check if user in DB
            DB_check_usr = db.execute("SELECT COUNT(*) FROM commute_times WHERE user_id = ?", session["user_id"])
            DB_check_usr = DB_check_usr[0]['COUNT(*)']
            if DB_check_usr == 0:
                db.execute("INSERT INTO commute_times(user_id, in_travel) VALUES(?, ?)", session["user_id"], usr_return_time[0])
            else:
                db.execute("UPDATE commute_times SET in_travel=? WHERE user_id=?", usr_return_time[0], session["user_id"])

        return redirect("/")


    else:
        if user_commute_days and user_commute_times:
            return render_template("index.html", user=usr_info, commute_days=user_commute_days, commute_times=user_commute_times)
        else:
            return render_template("index.html", user=usr_info)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash_pw"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        username = request.form.get("username")
        hash_pw = generate_password_hash(request.form.get("password"))
        usernamecheck = db.execute("SELECT COUNT(*) FROM users WHERE username = ?", username)
        usernamecheck = usernamecheck[0]['COUNT(*)']

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Checking if username already exists in database
        if not usernamecheck == 0:
            return apology("Username already exists", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password matches confirmation field
        if request.form.get("password") != request.form.get("pword-confirm"):
            return apology("Password doesn't match confirmation", 400)

        db.execute("INSERT INTO users (username, hash_pw) VALUES (?, ?)", username, hash_pw)

        # Redirect user to index/home
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/commute")
@login_required
def commute():
    """Show request to carpool with the user aas the driver"""

    usr_info = db.execute('SELECT * FROM users WHERE id=?', session["user_id"])
    DB_usr_commuting_days = db.execute('SELECT monday, tuesday, wednesday, thursday, friday, saturday, sunday FROM commute_days WHERE user_id=?', session["user_id"])
    DB_usr_commuting_times = db.execute("SELECT Out_travel, in_travel FROM commute_times WHERE user_id=?", session["user_id"])
    usr_info[0]['commute_days'] = DB_usr_commuting_days[0]
    usr_info[0]['commute_times'] = DB_usr_commuting_times[0]

    print(usr_info[0]['commute_days'])

    DB_commute_buddies = db.execute("SELECT id, username, home_postCode, work_postCode FROM users WHERE home_postCode=? AND work_postCode=? AND id !=?", usr_info[0]['home_postCode'], usr_info[0]['work_postCode'], session["user_id"])
    commute_buddies = []

    for buddy in DB_commute_buddies:
        DB_commuting_days = db.execute("SELECT monday, tuesday, wednesday, thursday, friday, saturday, sunday FROM commute_days WHERE user_id=?", buddy['id'])
        DB_commuting_times = db.execute("SELECT Out_travel, in_travel FROM commute_times WHERE user_id=?", buddy['id'])
        buddy['commute_days'] = DB_commuting_days[0]
        buddy['commute_times'] = DB_commuting_times[0]
        buddy['buddy_match'] = False

        for budDay in buddy['commute_days']:
            for uDay in usr_info[0]['commute_days']:
                if buddy['commute_days'].get(budDay) == usr_info[0]['commute_days'].get(uDay) and buddy['commute_times'].get('Out_travel') == usr_info[0]['commute_times'].get('Out_travel') and buddy['commute_times'].get('in_travel') == usr_info[0]['commute_times'].get('in_travel'):
                    buddy['buddy_match'] = True


        if buddy['buddy_match'] == True:
            commute_buddies.append(buddy)

    print('commute_buddies List:')
    print(commute_buddies)

    return render_template("commute.html", user=usr_info, buddies=commute_buddies)