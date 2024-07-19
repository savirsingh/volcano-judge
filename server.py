# Volcano Judge Server
# Originally written between October 2022 and January 2023 by Savir Singh.
# volcanojudge.pythonanywhere.com

from flask import *
from flask_login import login_required, logout_user, current_user, login_user, UserMixin, current_user
from datetime import datetime, timedelta
from flask_sqlalchemy import *
from werkzeug.security import *
from flask_login import LoginManager
from flask_admin import *
from flask_admin.contrib.sqla import ModelView
import random
import string
from flask_migrate import Migrate
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
import requests
import subprocess
import re
from subprocess import Popen, PIPE
from threading import Timer
import tempfile
import venv
import difflib

def find_string_differences(string1, string2):
    differ = difflib.Differ()
    diff = differ.compare(string1.splitlines(keepends=True), string2.splitlines(keepends=True))
    diff_list = list(diff)

    differences = []
    for line in diff_list:
        if line.startswith('-') or line.startswith('+'):
            differences.append(line)

    return ''.join(differences)


# ASH SUBSCRIBERS
ash=["admin"]

# example custom checkers
cgc1=['cgc1p1', 'cgc1p2', 'cgc1p3', 'cgc1p4']

upload_profile = "./static/images/profile"
app = Flask(__name__, static_folder='./static')
app.secret_key = "YOUR_SECRET_KEY"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['UPLOAD_PROFILE'] = upload_profile
login_manager = LoginManager()
login_manager.init_app(app)
db=SQLAlchemy(app)
migrate = Migrate(app, db)

class news(db.Model):
    __tablename__="News"
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String, default="volcano's Next Post")
    body=db.Column(db.String)
    authors=db.Column(db.String, default="N/A")
    date=db.Column(db.DateTime, default=datetime.now)

class problems(db.Model):
    __tablename__="Problem"
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String, default="volcano's Next Problem")
    body=db.Column(db.String)
    testcase=db.Column(db.Text)
    output=db.Column(db.Text)
    timelimit=db.Column(db.Integer)
    authors=db.Column(db.String, default="N/A")
    samplein=db.Column(db.String, default="N/A")
    sampleout=db.Column(db.String, default="N/A")
    sampleex=db.Column(db.String, default="N/A")
    code=db.Column(db.String)
    points=db.Column(db.Integer)
    contestfor=db.Column(db.String, default="None")

class contests(db.Model):
    __tablename__="Contest"
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String, default="volcano's Next Contest")
    about=db.Column(db.Text)
    problemcount=db.Column(db.Integer)
    timelimit=db.Column(db.Integer)
    setter=db.Column(db.String, default="N/A")
    date=db.Column(db.DateTime, default=datetime.now)
    end_date=db.Column(db.String)
    code=db.Column(db.String)
    rated=db.Column(db.Integer, default=0)
    p1=db.Column(db.String, default="None")
    p2=db.Column(db.String, default="None")
    p3=db.Column(db.String, default="None")
    p4=db.Column(db.String, default="None")
    p5=db.Column(db.String, default="None")
    registered=db.Column(db.String, default=" ")
    problems=db.Column(db.String, default=" ")

class comments(db.Model):
    __tablename__="Comment"
    id=db.Column(db.Integer, primary_key=True)
    body=db.Column(db.Text)
    author=db.Column(db.String)
    username=db.Column(db.String)
    problem=db.Column(db.String)
    date=db.Column(db.DateTime, default=datetime.now)
    votes=db.Column(db.Integer, default=0)
    voted=db.Column(db.String, default=" ")

class User(db.Model, UserMixin):
    __tablename__="Login"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String, unique=True)
    password=db.Column(db.String)
    email=db.Column(db.String, unique=True)
    org = db.Column(db.String(140), default="None")
    profile_pic = db.Column(db.String, default="/static/images/profile/404.jpg")
    isverified = db.Column(db.Integer, default = 0)
    rating = db.Column(db.Integer, default=0)
    maxrating = db.Column(db.Integer, default=0)
    contestsauthored = db.Column(db.Integer, default=0)
    totalpoints = db.Column(db.Integer, default=0)
    completedproblems = db.Column(db.String, default=" ")
    darkmode=db.Column(db.Integer, default=0)
    bio=db.Column(db.String, default="This user seems to be quite boring.")
    incontest=db.Column(db.Integer, default=0)
    currcontest=db.Column(db.String, default="None")
    currscore=db.Column(db.Integer, default=-1)
    timestarted=db.Column(db.DateTime, default=datetime.now())
    colour=db.Column(db.String, default="#525252")


    def __repr__(self):
        return "Registered User " + str(self.id)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)

class unverified(db.Model, UserMixin):
    __tablename__="Unverified"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String)
    password=db.Column(db.String)
    email=db.Column(db.String, unique=True)
    org = db.Column(db.String(140), default="None")
    timeadded=db.Column(db.DateTime, default=datetime.now())
    code=db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@app.before_request
def before_request_function():
    if current_user.is_authenticated:
        if current_user.username!="admin" and current_user.isverified==0 and request.path!="/update-email" and ".css" not in request.path and ".js" not in request.path and request.path!="/update-email/result" and request.path!="/signup/finish/second" and request.path!="/signup/finish/second/result":
            return redirect("/update-email")
    u=unverified.query.order_by(unverified.timeadded.desc()).all()
    for person in u:
        diff=datetime.now()-person.timeadded
        minutes = divmod(diff.total_seconds(), 60)
        ans=2880-minutes[0]
        if ans<=0:
            db.session.delete(person)
            db.session.commit()


@app.route("/feedback")
def feedback_page():
    return render_template("feedback.html")

@app.route("/")
def start():
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    if current_user.is_authenticated:
        p=problems.query.order_by(problems.title.desc()).all()
        c=comments.query.order_by(comments.date.desc()).all()
        c=c[:4]
        news1=news.query.order_by(news.date.desc()).all()
        return render_template("index.html", User=User, problems=problems, comments=c, prob=p, news=news1[:3], problemcount=problemcount, contestcount=contestcount, contests=contests.query.order_by(contests.date))
    else:
        return render_template("index_no.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0)

@app.route("/update-email")
@login_required
def update_email():
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    return render_template("update_email.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0)

@app.route("/update-email/result", methods=["GET","POST"])
def update_the_email():
    global passmsg
    email = request.form["email"]
    existing_user = User.query.filter_by(email=email).first()
    existing_user1 = unverified.query.filter_by(email=email).first()
    if existing_user is None and existing_user1 is None:
        the_code=random.randint(100000, 999999)
        user=unverified(email=email, username=current_user.username, org=current_user.org, password=current_user.password, code=the_code)
        if True:
            text = f"""\
            Hello {user.username},
            Someone used this email address to sign up for Volcano Judge.
            Use this code to finish signup: {the_code}
            If you didn't try to sign up for Volcano Judge, disregard this message.
            """
            html = f"""\
            <html>
              <body style="color: #626266; background-color: #d1d5eb; font-family: Cambria; font-size: 16px">
                <p>Hello {user.username},<br>
                   This is your ONLY chance to verify your email.<br>
                   <b style="padding: 8px; font-size: 20px">Use this code to verify it: {the_code}</b><br>
                   If you didn't try to sign up for Volcano Judge, disregard this message.<br><br>
                   <img src="https://raw.githubusercontent.com/volcanojudge/online-judge/main/static/favicon-3.png" alt="Volcano Judge"><br><br>
                   - Volcano Judge Staff<br>
                   <small>Do not reply to this email; if you have a question for staff, please email volcanojudge@gmail.com.</small>
                </p>
              </body>
            </html>
            """
            sender_email = "business_email@domain.com"
            receiver_email = user.email
            password = "email_password"
            message = MIMEMultipart("alternative")
            message["Subject"] = "Verify your email address for Volcano Judge!"
            message["From"] = sender_email
            message["To"] = receiver_email
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")
            message.attach(part1)
            message.attach(part2)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
            )
            db.session.add(user)
            db.session.commit()
            return redirect("/signup/finish/second")
    else:
        return redirect(request.referrer)

@app.route("/signup", methods=["GET","POST"])
def register():
    global passmsg
    username = request.form['username']
    email = request.form["email"]
    password = request.form["password"]
    org = request.form["org"]
    existing_user = User.query.filter_by(email=email).first()
    #existing_user_ = unverified.query.filter_by(email=email).first()
    existing_user_ = None
    existing_user1 = User.query.filter_by(username=username).first()
    #existing_user_1 = unverified.query.filter_by(username=username).first()
    existing_user_1 = None
    if existing_user is None and existing_user_ is None:
        if existing_user1 is None and existing_user_1 is None:
            # the_code=random.randint(100000, 999999) # for email verification
            user=User(email=email, username=username, org=org, password=password)
            user.set_password(password)
            user.isverified=1
            if not (user.username).isalnum() or len(user.org)>64:
                return redirect(request.referrer)
            else:
                # text = f"""\
                # Hello {user.username},
                # Someone used this email address to sign up for Volcano Judge.
                # Use this code to finish signup: {the_code}
                # If you didn't try to sign up for Volcano Judge, disregard this message.
                # """
                # html = f"""\
                # <html>
                #   <body style="color: #626266; background-color: #d1d5eb; font-family: Cambria; font-size: 16px">
                #     <p>Hello {user.username},<br>
                #        Someone used this email address to sign up for Volcano Judge.<br>
                #        <b style="padding: 8px; font-size: 20px">Use this code to finish signup: {the_code}</b><br>
                #        If you didn't try to sign up for Volcano Judge, disregard this message.<br><br>
                #        <img src="https://raw.githubusercontent.com/volcanojudge/online-judge/main/static/favicon-3.png" alt="Volcano Judge"><br><br>
                #        - Volcano Judge Staff<br>
                #        <small>Do not reply to this email; if you have a question for staff, please email volcanojudge@gmail.com.</small>
                #     </p>
                #   </body>
                # </html>
                # """
                # sender_email = "business_email@domain.com"
                # receiver_email = user.email
                # password = "email_password"
                # message = MIMEMultipart("alternative")
                # message["Subject"] = "Finish signing up for Volcano Judge!"
                # message["From"] = sender_email
                # message["To"] = receiver_email
                # part1 = MIMEText(text, "plain")
                # part2 = MIMEText(html, "html")
                # message.attach(part1)
                # message.attach(part2)
                # context = ssl.create_default_context()
                # with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                #     server.login(sender_email, password)
                #     server.sendmail(
                #         sender_email, receiver_email, message.as_string()
                # )
                login_user(user)
                db.session.add(user)
                db.session.commit()
                return redirect("/")
        else:
            return redirect(request.referrer)
    else:
        return redirect(request.referrer)

@app.route("/signup/finish")
def register_page_finish():
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    return render_template("finish_register.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0)

@app.route("/signup/finish/result", methods=["GET","POST"])
def register_finish():
    global passmsg
    email=request.form['email']
    code=request.form['code']
    wesay=unverified.query.filter_by(email=email).first()
    if wesay is None:
        return "Invalid email!"
    email=wesay.email
    username=wesay.username
    password=wesay.password
    org=wesay.org
    actual_code=wesay.code
    existing_user = User.query.filter_by(email=email).first()
    existing_user1 = User.query.filter_by(username=username).first()
    if existing_user is None:
        if existing_user1 is None:
            user=User(email=email, username=username, org=org)
            user.set_password(password)
            if int(code)!=actual_code:
                return "Invalid code!"
            else:
                user.isverified=1
                db.session.add(user)
                db.session.delete(wesay)
                db.session.commit()
                login_user(user)
                return redirect("/")
        else:
            return redirect(request.referrer)
    else:
        return redirect(request.referrer)

@app.route("/signup/finish/second")
def register_page_finish_sec():
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    return render_template("finish_register_chance.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0)

@app.route("/signup/finish/second/result", methods=["GET","POST"])
def register_finish_chance():
    global passmsg
    email=request.form['email']
    code=request.form['code']
    wesay=unverified.query.filter_by(email=email).first()
    if wesay is None:
        return "Invalid email!"
    email=wesay.email
    username=wesay.username
    password=wesay.password
    org=wesay.org
    actual_code=wesay.code
    existing_user = User.query.filter_by(email=email).first()
    if existing_user is None:
        user=User(email=email, username=username, org=org, rating=current_user.rating, maxrating=current_user.maxrating, totalpoints=current_user.totalpoints, currscore=current_user.currscore, password=current_user.password, colour=current_user.colour, completedproblems=current_user.completedproblems, darkmode=current_user.darkmode, currcontest=current_user.currcontest)
        if int(code)!=actual_code:
            return "Invalid code!"
        else:
            user.isverified=1
            db.session.delete(current_user)
            db.session.commit()
            db.session.add(user)
            db.session.delete(wesay)
            db.session.commit()
            logout_user()
            login_user(user)
            return redirect("/")
    else:
        return redirect(request.referrer)

@app.route("/edit-profile")
@login_required
def edit_profile1():
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    return render_template("edit_profile.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0)

@app.route("/edit-profile-admin")
@login_required
def edit_profile_admin1():
    if current_user.username=="admin":
        problemcount=problems.query.count()
        contestcount=contests.query.count()
        return render_template("edit_profile_admin.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0)

@app.route("/edit-profile/submit", methods=["GET", "POST"])
@login_required
def edit_profile2():
    org = request.form['in1']
    bio = request.form['in2']
    if (current_user.org).isalnum() and len(org)<65:
        current_user.org=org
    if bio.isalnum() and len(bio)<241:
        current_user.bio=bio.replace("\n", "<br>")
    db.session.commit()
    return redirect(request.referrer)

@app.route("/edit-profile-admin/submit", methods=["GET", "POST"])
@login_required
def edit_profile_admin2():
    if current_user.username=="admin":
        username = org = request.form['in3']
        user=User.query.filter_by(username=username).first()
        org = request.form['in1']
        bio = request.form['in2']
        user.org=org
        user.bio=bio
        db.session.commit()
        return redirect(request.referrer)

@app.route("/comment/<id>/delete", methods=['GET', 'POST'])
@login_required
def delete_comment_1(id):
    if current_user.username=="admin":
        comm=comments.query.filter_by(id=id).first()
        db.session.delete(comm)
        db.session.commit()
        return "success"
    else:
        abort(403)

@app.errorhandler(401)
def page_not_found(e):
    return render_template('401.html'), 401

@app.errorhandler(403)
def page_not_found(e):
    return render_template('401.html'), 403


@app.route("/comment/<id>/upvote", methods=['GET', 'POST'])
@login_required
def comment_upvote(id):
    comm=comments.query.filter_by(id=id).first()
    if (current_user.username in comm.voted or current_user.username==comm.username) and current_user.username!="admin":
        return redirect(request.referrer)
    else:
        comm.votes+=1
        if current_user.username!="admin":
            comm.voted=comm.voted+current_user.username+" "
        db.session.commit()
        return redirect(request.referrer)

@app.route("/comment/<id>/downvote", methods=['GET', 'POST'])
@login_required
def comment_downvote(id):
    comm=comments.query.filter_by(id=id).first()
    if (current_user.username in comm.voted or current_user.username==comm.username) and current_user.username!="admin":
        return redirect(request.referrer)
    else:
        comm.votes-=1
        if current_user.username!="admin":
            comm.voted=comm.voted+current_user.username+" "
        if comm.votes<-12:
            db.session.delete(comm)
        db.session.commit()
        return redirect(request.referrer)

@app.route("/delete-account")
@login_required
def delete_account():
    if current_user.username=="admin":
        return render_template("delete_account.html")
    else:
        abort(403)

@app.route("/delete-account/result", methods=['GET', 'POST'])
@login_required
def delete_account_1():
    if current_user.username=="admin":
        username=request.form["in1"]
        id=request.form["in2"]
        if username!="":
            user=User.query.filter_by(username=username).first()
            comm=comments.query.filter_by(username=username).all()
            for c in comm:
                db.session.delete(c)
            db.session.delete(user)
        else:
            user=User.query.filter_by(id=id).first()
            username=user.username
            comm=comments.query.filter_by(username=username).all()
            for c in comm:
                db.session.delete(c)
            db.session.delete(user)
        db.session.commit()
        return "success"
    else:
        abort(403)

@app.route("/login",methods=['GET','POST'])
def login1():
    msg = ''
    if current_user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        user1 = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=user1).first()
        if user and user1!="":
            if user.check_password(password):
                login_user(user)
                next = request.args.get('next')
                return redirect(next or "/")
        else:
            return redirect(request.referrer)
        try:
            return redirect(request.referrer)
        except:
            return redirect("/")
    return redirect("/")

@app.route("/login_page")
def login_p():
    if current_user.is_authenticated:
        return redirect("/")
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    return render_template("login.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0)

@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    return redirect("/")

@app.route("/create-contest")
@login_required
def create_contest():
    return render_template("create_contest.html")

@app.route("/user/<username>/edit")
@login_required
def edit_user_admin(username):
    if current_user.username=="admin":
        return render_template("edit_user_admin.html", username=username)

@app.route("/user/<username>/edit/result", methods=["GET", "POST"])
@login_required
def edit_user_admin_result(username):
    if current_user.username=="admin":
        user1=User.query.filter_by(username=username).first()
        rating=request.form["rating"]
        maxrating=request.form["maxrating"]
        user1.rating=rating
        user1.maxrating=maxrating
        colour="black"
        new=int(rating)
        if new==0:
            colour="#525252"
        elif new>0 and new<100:
            colour="#99a199"
        elif new<300:
            colour="#95f59d"
        elif new<500:
            colour="#738cde"
        elif new<800:
            colour="#f7c728"
        elif new<1200:
            colour="#fc5347"
        else:
            colour="#800000"
        user1.colour=colour
        db.session.commit()
        return "success"

@app.route("/user/<username>")
def user_profile(username):
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    actual=username
    try:
        user=User.query.filter_by(username=username).first()
        colour="black"
        if user.rating==0:
            username=username+" [unrated]"
            colour="#525252"
        elif user.rating<0:
            username=username+" [cheater]"
            colour="#596b5d"
        elif user.rating>0 and user.rating<100:
            username=username+" [beginner]"
            colour="#99a199"
        elif user.rating<300:
            username=username+" [good]"
            colour="#95f59d"
        elif user.rating<500:
            username=username+" [expert]"
            colour="#738cde"
        elif user.rating<800:
            username=username+" [ruler]"
            colour="#f7c728"
        elif user.rating<1200:
            username=username+" [crazy]"
            colour="#fc5347"
        else:
            username=username+" [god]"
            colour="#800000"
        colour2="black"
        if user.maxrating==0:
            colour2="#525252"
        elif user.maxrating<0:
            colour2="#596b5d"
        elif user.maxrating>0 and user.maxrating<100:
            colour2="#99a199"
        elif user.maxrating<300:
            colour2="#95f59d"
        elif user.maxrating<500:
            colour2="#738cde"
        elif user.maxrating<800:
            colour2="#f7c728"
        elif user.maxrating<1200:
            colour2="#fc5347"
        else:
            colour2="#800000"
        return render_template("user.html", is_ash=(actual in ash), user=user, colour2=colour2, problemcount=problemcount, contestcount=contestcount, totalcontests=0, points=user.totalpoints, username=username, rating=user.rating, max_rating=user.maxrating, contests_authored=user.contestsauthored, colour=colour)
    except:
        return "This username couldn't be found"

@app.route("/rankings")
def rankings():
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    a=0
    users=User.query.order_by(User.totalpoints.desc()).all()
    return render_template("rankings.html", users=users, a=a, problemcount=problemcount, contestcount=contestcount, totalcontests=0)

@app.route("/dark-mode")
@login_required
def dark_mode():
    if current_user.darkmode==0:
        current_user.darkmode=1
        db.session.commit()
    else:
        current_user.darkmode=0
        db.session.commit()
    return redirect(request.referrer)

@app.route("/ash")
def ash_page_info():
    return render_template("ash.html")

@app.route("/contest/<code>")
def contest_page(code):
    if code == "btsbtcp23":
        return """

<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Back to School, Back to CP 2023 | Contest | Volcano Judge</title>
    <link rel="icon" href="/static/favicon.ico">



    <!-- Bootstrap core CSS -->
<link href="/static/bootstrap.min.css" rel="stylesheet">

<meta name="theme-color" content="#7952b3">


    <style>
      .bd-placeholder-img {
        font-size: 1.125rem;
        text-anchor: middle;
        -webkit-user-select: none;
        -moz-user-select: none;
        user-select: none;
      }

      @media (min-width: 768px) {
        .bd-placeholder-img-lg {
          font-size: 3.5rem;
        }
      }
    </style>


    <!-- Custom styles for this template -->
    <link href="/static/offcanvas.css" rel="stylesheet">
  </head>

<main class="container">
  <div class="my-3 p-3 bg-body rounded shadow-sm">
<h3>Back to School, Back to CP 2023 starts soon!</h3>
<p><br>
     Check this page again <b>after September 6, 2023</b> and you will be able to start your personal 150-minute window for the contest.<br>
     Between September 6 and September 15, you may select any day and start your window. Results will be posted after September 15 on the BTSBTCP website.
</p>
    </div>
  </div>
  </div>
</main>


    <script src="/static/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>

      <script src="/static/offcanvas.js"></script>
  </body>
</html>

        """
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    if current_user.is_authenticated:
        time_up=False
        contest=contests.query.filter_by(code=code).first()
        seconds_in_day = 24 * 60 * 60
        difference = datetime.now() - current_user.timestarted
        time=divmod(difference.days * seconds_in_day + difference.seconds, 60)
        endtime_=current_user.timestarted + timedelta(minutes=contest.timelimit) - timedelta(hours=4)
        if current_user.currcontest==code and time[0]>=contest.timelimit:
            time_up=True
        is_rated=""
        if contest.rated==1:
            is_rated="Yes"
        else:
            is_rated="No"
        p1=contest.p1
        p2=contest.p2
        p3=contest.p3
        p4=contest.p4
        p5=contest.p5
        a=str(contest.date)
        for i in range(16):
            a=a[:-1]
        left=300-len(contest.registered.split())
        return render_template("contest.html", endtime_=endtime_, timeup=time_up, registered=contest.registered.split(), problemcount=problemcount, contestcount=contestcount, totalcontests=0, left=left, contest=contest, date=a, code=code, rated=is_rated, title=contest.title, organizers=contest.setter, time_allowed=contest.timelimit)
    else:
        contest=contests.query.filter_by(code=code).first()
        time_up = False
        endtime_ = 0
        registered = []
        left = 300 - len(contest.registered.split())
        a=str(contest.date)
        for i in range(16):
            a=a[:-1]
        is_rated=""
        if contest.rated==1:
            is_rated="Yes"
        else:
            is_rated="No"
        return render_template("contest.html", endtime_=endtime_, timeup=time_up, registered=contest.registered.split(), problemcount=problemcount, contestcount=contestcount, totalcontests=0, left=left, contest=contest, date=a, code=code, rated=is_rated, title=contest.title, organizers=contest.setter, time_allowed=contest.timelimit)

@app.route("/contest/<code>/close")
@login_required
def close_contest(code):
    if current_user.username=="admin":
        contest=contests.query.filter_by(code=code).first()
        db.session.delete(contest)
        prob=problems.query.filter_by(contestfor=code).all()
        user_=User.query.filter_by(currcontest=code).all()
        for p in prob:
            p.contestfor="None"
        if contest.rated==1:
            user=User.query.filter_by(currcontest=code).all()
            username_list=[]
            score_list=[]
            for u in user:
                username_list.append(u.username)
                score_list.append(u.currscore)
            scores, usernames = zip(*sorted(zip(score_list, username_list), reverse=True))
            ratings=[]
            for i in usernames:
                u1=User.query.filter_by(username=i).first()
                ratings.append(u1.rating)
            for i in range(len(usernames)):
                user1=User.query.filter_by(username=usernames[i]).first()
                if user1.rating!=0:
                    user1.rating=(ratings[i]+(2*len(usernames)*(len(usernames)-i+1)))//2
                    new=(ratings[i]+(2*len(usernames)*(len(usernames)-i+1)))//2
                    user1.maxrating=max(user1.maxrating, new)
                    colour="black"
                    if new==0:
                        colour="#525252"
                    elif new>0 and new<100:
                        colour="#99a199"
                    elif new<300:
                        colour="#95f59d"
                    elif new<500:
                        colour="#738cde"
                    elif new<800:
                        colour="#f7c728"
                    elif new<1200:
                        colour="#fc5347"
                    else:
                        colour="#800000"
                    user1.colour=colour
                else:
                    user1.rating=(2*len(usernames)*(len(usernames)-i+1))
                    new=(2*len(usernames)*(len(usernames)-i+1))
                    user1.maxrating=max(user1.maxrating, new)
                    colour="black"
                    if new==0:
                        colour="#525252"
                    elif new>0 and new<100:
                        colour="#99a199"
                    elif new<300:
                        colour="#95f59d"
                    elif new<500:
                        colour="#738cde"
                    elif new<800:
                        colour="#f7c728"
                    elif new<1200:
                        colour="#fc5347"
                    else:
                        colour="#800000"
                    user1.colour=colour
        for u in user_:
            u.currcontest="None"
        db.session.commit()
        return "Contest closed permanently."
    else:
        return "unauthorized"

@app.route("/contest/<code>/register")
@login_required
def contest_register(code):
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    try:
        contest=contests.query.filter_by(code=code).first()
        is_rated=""
        if contest.rated==1:
            is_rated="Yes"
        else:
            is_rated="No"
        p1=contest.p1
        p2=contest.p2
        p3=contest.p3
        p4=contest.p4
        p5=contest.p5
        a=str(contest.date)
        for i in range(16):
            a=a[:-1]
        left=300-len(contest.registered.split())
        return render_template("register_contest.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0, left=left, contest=contest, date=a, code=code, rated=is_rated, title=contest.title, organizers=contest.setter, time_allowed=contest.timelimit)
    except:
        return "This contest couldn't be found"

@app.route("/contest-rules")
def contest_rules():
    return render_template("contest_rules.html")

@app.route("/about")
def about_page():
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    return render_template("about.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0, User=User)

@app.route("/contact")
def contact_page():
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    return render_template("contact.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0, User=User)

@app.route("/contest/<code>/register/submit")
@login_required
def contest_register_submit(code):
    contest=contests.query.filter_by(code=code).first()
    if len(contest.registered.split())<300 and current_user.username not in contest.registered.split():
        contest.registered=contest.registered+" "+current_user.username
        current_user.incontest=1
        current_user.currscore=0
        current_user.currcontest=code
        current_user.timestarted=datetime.now()
        db.session.commit()
        return redirect("/contest/"+code)
    else:
        return "Something happened while trying to register you. Either you have already registered or the max limit has been reached. Stop trying."

@app.route("/contest/change-score")
@login_required
def change_contest_scoreboard():
    if current_user.username=="contestbot" or current_user.username == "admin":
        return render_template("change_scoreboard.html")
    else:
        abort(403)

@app.route("/contest/change-score/submit", methods=['GET', 'POST'])
@login_required
def change_contest_scoreboard_submit():
    if current_user.username=="contestbot" or current_user.username == "admin":
        username=request.form["in1"]
        score=request.form["in2"]
        user1=User.query.filter_by(username=username).first()
        user1.currscore=score
        db.session.commit()
        return "success"
    else:
        abort(403)

@app.route("/contest/<code>/scoreboard")
def contest_scoreboard(code):
    try:
        problemcount=problems.query.count()
        contestcount=contests.query.count()
        contest=contests.query.filter_by(code=code).first()
        user=User.query.filter_by(currcontest=code).all()
        username_list=[]
        score_list=[]
        for u in user:
            username_list.append(u.username)
            score_list.append(u.currscore)
        scores, usernames = zip(*sorted(zip(score_list, username_list), reverse=True))
        ratings=[]
        for i in usernames:
            u1=User.query.filter_by(username=i).first()
            ratings.append(u1.rating)
        return render_template("contest_scoreboard.html", User=User, ratings=ratings, length=len(usernames), rated=contest.rated, title=contest.title, contest=contest, scores=scores, usernames=usernames, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
    except:
        return "Nobody has started yet!"

@app.route("/publish-contest")
@login_required
def publish_contest():
    if current_user.username!="admin":
        abort(403)
    else:
        return render_template("publish.html")

@app.route("/publish-problem")
@login_required
def publish_problem():
    if current_user.username!="admin":
        abort(403)
    else:
        return render_template("publish_prob.html")


@app.route("/publish-news")
@login_required
def publish_news():
    if current_user.username!="admin":
        abort(403)
    else:
        return render_template("publish_news.html")

@app.route("/p-prob",methods=['GET','POST'])
@login_required
def p_prob():
    title = request.form['title']
    code = request.form['code']
    authors = request.form['authors']
    tl = request.form['tl']
    tc = request.form['tc']
    o = request.form['o']
    body = request.form['body']
    samplein = request.form['si']
    sampleout = request.form['so']
    sampleex = request.form['se']
    points = request.form['p']
    contest = request.form['contest']
    if current_user.username=="admin":
        problem=problems(contestfor=contest, title=title, points=points, code=code, authors=authors, timelimit=tl, body=body, testcase=tc, output=o, samplein=samplein, sampleout=sampleout, sampleex=sampleex)
        db.session.add(problem)
        db.session.commit()
        return "Problem Published!"
    else:
        abort(403)

@app.route("/p-cont",methods=['GET','POST'])
@login_required
def p_cont():
    title = request.form['title']
    code = request.form['code']
    organizers = request.form['organizers']
    tl = request.form['tl']
    rated = request.form['rat']
    p1 = request.form['p1l']
    p2 = request.form['p2l']
    p3 = request.form['p3l']
    p4 = request.form['p4l']
    p5 = request.form['p5l']
    end = request.form['end']
    pcount = request.form['pcount']
    about = request.form['body']
    rated1=0
    if rated=="yes":
        rated1=1
    if current_user.username=="admin":
        contest=contests(problemcount=pcount, title=title, about=about, code=code, setter=organizers, timelimit=tl, rated=rated1, p1=p1, p2=p2, p3=p3, p4=p4, p5=p5, end_date=end)
        db.session.add(contest)
        db.session.commit()
        return "Contest Published!"
    else:
        abort(403)

@app.route("/problem/<code>")
def problem_page(code):
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    problem=problems.query.filter_by(code=code).first()
    p=str(problem.body)
    comm=comments.query.filter_by(problem=code).all()
    comm.reverse()
    try:
        if current_user.currcontest==problem.contestfor or current_user.username=="admin":
            return render_template("problem.html", User=User, problem=problem, comm=comm, points=problem.points, problemcount=problemcount, contestcount=contestcount, totalcontests=0, code=code, body=p, testcase=problem.testcase, output=problem.output, authors=problem.authors, timelimit=problem.timelimit, title=problem.title, samplein=problem.samplein, sampleout=problem.sampleout, sampleex=problem.sampleex)
        else:
            return "This problem couldn't be found. You may be writing a contest, this problem may not exist, or you might not be logged in."
    except:
        if problem.contestfor=="None":
            return render_template("problem_no.html", User=User, problem=problem, comm=comm, points=problem.points, problemcount=problemcount, contestcount=contestcount, totalcontests=0, code=code, body=p, testcase=problem.testcase, output=problem.output, authors=problem.authors, timelimit=problem.timelimit, title=problem.title, samplein=problem.samplein, sampleout=problem.sampleout, sampleex=problem.sampleex)
        else:
            return "Problem private. Log in to view."
@app.route("/problem/<code>/edit")
@login_required
def problem_page_edit(code):
    if current_user.username=="admin" or current_user.username=="contestbot":
        problemcount=problems.query.count()
        contestcount=contests.query.count()
        problem=problems.query.filter_by(code=code).first()
        p=str(problem.body)
        comm=comments.query.filter_by(problem=code).all()
        if current_user.currcontest==problem.contestfor  or current_user.username=="admin":
            return render_template("edit_problem.html", User=User, problem=problem, comm=comm, points=problem.points, problemcount=problemcount, contestcount=contestcount, totalcontests=0, code=code, body=p, testcase=problem.testcase, output=problem.output, authors=problem.authors, timelimit=problem.timelimit, title=problem.title, samplein=problem.samplein, sampleout=problem.sampleout, sampleex=problem.sampleex)
        else:
            return "This problem couldn't be found"
    else:
        abort(403)

@app.route("/problem/<code>/edit/result", methods=['GET', 'POST'])
@login_required
def problem_page_edit_result(code):
    if current_user.username=="admin" or current_user.username=="contestbot":
        body=request.form["in1"]
        sampleex=request.form["in2"]
        input=request.form["in3"]
        output=request.form["in4"]
        samplein=request.form["in5"]
        sampleout=request.form["in6"]
        title=request.form["in7"]
        code_=request.form["in8"]
        author=request.form["in9"]
        points=request.form["in10"]
        contestfor=request.form["in11"]
        timel = request.form["in12"]
        problem=problems.query.filter_by(code=code).first()
        problem.code=code_
        problem.title=title
        problem.body=body
        problem.sampleex=sampleex
        problem.testcase=input
        problem.output=output
        problem.samplein=samplein
        problem.sampleout=sampleout
        problem.contestfor=contestfor
        problem.authors=author
        problem.points=points
        problem.timelimit=timel
        db.session.commit()
        return "success"
    else:
        abort(403)

@app.route("/problems")
def redir_problems():
    return redirect("/problems/alpha")

@app.route("/problems/<order>")
def problems_page(order):
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    try:
        if (order=="alpha"):
            p=problems.query.order_by(problems.title.asc()).all()
            return render_template("problems.html", prob=p, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
        elif (order=="high-points"):
            p=problems.query.order_by(problems.points.desc()).all()
            return render_template("problems.html", prob=p, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
        elif (order=="low-points"):
            p=problems.query.order_by(problems.points.asc()).all()
            return render_template("problems.html", prob=p, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
        else:
            return "Format must be 'problems/[order]' Where [order] must be replaced with one of the following:<br>alpha, high-points, low-points"
    except:
        return "There seems to be an issue with loading problems right now"


@app.route("/contests")
def contests_page():
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    try:
        p=contests.query.order_by(contests.date.desc()).all()
        return render_template("contests.html", prob=p, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
    except:
        return "There seems to be an issue with loading contests right now"


@app.route("/announcement/<id>/delete", methods=['GET', 'POST'])
@login_required
def delete_news(id):
    if current_user.username=="admin":
        new=news.query.filter_by(id=id).first()
        db.session.delete(new)
        db.session.commit()
        return "success"

@app.route("/comment/<code>", methods=['GET', 'POST'])
@login_required
def comment_problem(code):
    body=request.form['body']
    username=current_user.username
    user=current_user
    problem=code
    if current_user.currcontest=="None" and "<" not in body and "$" not in body and len(body)>2 and "DROP" not in body:
        comment=comments(body=body, author=username, problem=problem, username=current_user.username)
        db.session.add(comment)
        db.session.commit()
    return redirect(request.referrer)

@app.route("/problem/<code>/submit")
@login_required
def submit_page(code):
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    try:
        problem=problems.query.filter_by(code=code).first()
        return render_template("problem_submit.html", code=code, title=problem.title)
    except:
        return "This problem couldn't be found"

@app.route("/problem/<code>/submit/python3")
@login_required
def submit_page_py3(code):
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    try:
        problem=problems.query.filter_by(code=code).first()
        if current_user.currcontest==problem.contestfor or current_user.username == "admin":
            if current_user.darkmode==0:
                return render_template("problem_submit_py3_light.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0, code=code, title=problem.title, body=problem.body, samplein=problem.samplein, sampleout=problem.sampleout, sampleex=problem.sampleex)
            else:
                return render_template("problem_submit_py3_dark.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0, code=code, title=problem.title, body=problem.body, samplein=problem.samplein, sampleout=problem.sampleout, sampleex=problem.sampleex)
        else:
            return "This problem couldn't be found"
    except:
        return "This problem couldn't be found"

# Python sandbox is based on https://github.com/code-demigod/Building-and-Breaking-a-Python-Sandbox/blob/master/Language%20Level%20Sandboxing%20using%20pysandbox.md
@app.route("/problem/<code>/submit/python3/result",methods=['GET','POST'])
@login_required
def submit_page_py3_send(code):
        problemcount=problems.query.count()
        contestcount=contests.query.count()
        problem1=problems.query.filter_by(code=code).first()
        if current_user.currcontest!=problem1.contestfor and current_user.username != "admin":
            return "Some error occurred."
        prog = request.form['program']
        if "_" in prog:
            pass
        # example custom checking (for contests)
        if code in cgc1:
            # cgc1
            if len(prog)>57:
                return render_template("problem_invalid_return.html", problem=problem1, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
        s=open("try_python.py", "w")
        s.write("from sandbox import Sandbox\n")
        s.write("s=Sandbox()\n")
        s.write("import sys\n")
        s.write("sys.modules['random'] = None\n")
        s.write("sys.modules['os'] = None\n")
        s.write("sys.modules['sys'] = None\n")
        s.write("del sys\n")
        s.write(prog)
        s.close()
        problem=problems.query.filter_by(code=code).first()
        s=open("python_input.txt", "w")
        s.write(problem.testcase)
        s.close()
        c=open("python_input.txt", "r")
        lines=c.readlines()
        with open("python_input.txt", "w") as f:
            for line in lines:
                if line != "\n":
                    f.write(line)
        s=open("python_output.txt", "w")
        s.write(problem.output+"\n")
        s.close()
        c=open("python_output.txt", "r")
        lines=c.readlines()
        with open("python_output.txt", "w") as f:
            for line in lines:
                if line != "\n":
                    f.write(line)
        try:
            r=open("python_input.txt", "r")
            py_output = subprocess.check_output(['python', 'try_python.py'], stderr=PIPE, stdin=r, timeout=problem.timelimit)
        except subprocess.TimeoutExpired as t:
            return render_template("problem_timeout.html", problem=problem1, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
        except subprocess.CalledProcessError as e:
            return render_template("problem_invalid_return.html", problem=problem1, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
            #return str(e)
        output=str(py_output)
        output=output[2:]
        output=output[:-3]
        output=output+"\n"
        f=open("python_output.txt", "r")
        a=bytes(f.read(), 'utf-8')
        output=bytes(output, 'utf-8')
        a=str(a)
        output=str(output)
        output=str(output).replace("\\n", "n")
        output=output[:-2]
        a=a[:-3]
        if a==output:
            if problem.code not in current_user.completedproblems.split():
                current_user.totalpoints+=problem.points
                current_user.completedproblems=current_user.completedproblems+" "+problem.code
                seconds_in_day = 24 * 60 * 60
                difference = datetime.now() - current_user.timestarted
                time=divmod(difference.days * seconds_in_day + difference.seconds, 60)
                if current_user.currcontest!="None":
                    contest=contests.query.filter_by(code=current_user.currcontest).first()
                    if problem.contestfor!="None" and current_user.currcontest==problem.contestfor and time[0]<contest.timelimit:
                        current_user.currscore+=1
            seconds_in_day = 24 * 60 * 60
            difference = datetime.now() - current_user.timestarted
            time=divmod(difference.days * seconds_in_day + difference.seconds, 60)
            if current_user.currcontest!="None":
                contest=contests.query.filter_by(code=current_user.currcontest).first()
                if problem.contestfor!="None" and current_user.currcontest==problem.contestfor and time[0]>=contest.timelimit:
                    current_user.totalpoints+=problem.points
                    current_user.completedproblems=current_user.completedproblems+" "+problem.code
                    contest=contests.query.filter_by(code=problem.contestfor).first()
                    return render_template("problem_correct_time_up.html", problem=problem1, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
            db.session.commit()
            return render_template("problem_correct.html", problem=problem1, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
        else:
            return render_template("problem_wrong.html", problem=problem1, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
        w=open("python_output.txt", "w")
        w.close()

@app.route("/problem/<code>/submit/cpp20")
@login_required
def submit_page_cpp(code):
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    try:
        problem=problems.query.filter_by(code=code).first()
        if current_user.currcontest==problem.contestfor or current_user.username == "admin":
            if current_user.darkmode==0:
                return render_template("problem_submit_cpp20_light.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0, code=code, title=problem.title, body=problem.body, samplein=problem.samplein, sampleout=problem.sampleout, sampleex=problem.sampleex)
            else:
                return render_template("problem_submit_cpp20_dark.html", problemcount=problemcount, contestcount=contestcount, totalcontests=0, code=code, title=problem.title, body=problem.body, samplein=problem.samplein, sampleout=problem.sampleout, sampleex=problem.sampleex)
        else:
            return "This problem couldn't be found"
    except:
        return "This problem couldn't be found"

@app.route("/problem/<code>/submit/cpp20/result",methods=['GET','POST'])
@login_required
def submit_page_cpp_send(code):
    problemcount=problems.query.count()
    contestcount=contests.query.count()
    if current_user.currcontest == "None" and current_user.username != "admin":
        return "C++ is only available for contests - sorry!"
    problem=problems.query.filter_by(code=code).first()
    if problem.contestfor and current_user.currcontest!=problem.contestfor and current_user.username != "admin":
        return "Some error occurred."
    prog = request.form['program']
    s=open("try_cpp.cpp", "w")
    s.write(prog)
    s.close()
    input_data = problem.testcase.replace("\r", "")
    if input_data[-1:] != '\n':
        input_data += '\n'
    expected_out = problem.output.replace("\r", "")
    if expected_out[-1:] != '\n':
        expected_out += '\n'
    # Create a temporary directory for running the code
    temp_dir = '/home/volcanojudge/mysite/code/' # This is for Pythonanywhere. Just change this to /code (or whatever path you wish to isolate the C++ code to)

    # Write the C++ code to a file in the temporary directory
    cpp_file = os.path.join(temp_dir, current_user.username + '.cpp')
    with open(cpp_file, 'w') as f:
        f.write(prog)

    # Compile the C++ code
    executable = os.path.join(temp_dir, current_user.username)
    try:
        subprocess.check_call(['g++', '-o', executable, cpp_file])
    except subprocess.CalledProcessError:
        return render_template("problem_invalid_return.html", problem=problem, problemcount=problemcount, contestcount=contestcount, totalcontests=0)

    # Set up a sandboxed environment for running the code
    sandbox = {
        'stdin': subprocess.PIPE,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'cwd': temp_dir,
    }

    # Run the code with the input
    try:
        time_limit = problem.timelimit

        with subprocess.Popen([executable], **sandbox) as proc:
            try:
                stdout, stderr = proc.communicate(input_data.encode(), timeout=time_limit)
                outputreal = stdout.decode()
                if outputreal[-1:] != '\n':
                    outputreal += '\n'
                if outputreal == expected_out:
                    if problem.code not in current_user.completedproblems.split():
                        current_user.totalpoints+=problem.points
                        current_user.completedproblems=current_user.completedproblems+" "+problem.code
                        seconds_in_day = 24 * 60 * 60
                        difference = datetime.now() - current_user.timestarted
                        time=divmod(difference.days * seconds_in_day + difference.seconds, 60)
                        if current_user.currcontest!="None":
                            contest=contests.query.filter_by(code=current_user.currcontest).first()
                            if problem.contestfor!="None" and current_user.currcontest==problem.contestfor and time[0]<contest.timelimit:
                                current_user.currscore+=1
                    seconds_in_day = 24 * 60 * 60
                    difference = datetime.now() - current_user.timestarted
                    time=divmod(difference.days * seconds_in_day + difference.seconds, 60)
                    if current_user.currcontest!="None":
                        contest=contests.query.filter_by(code=current_user.currcontest).first()
                        if problem.contestfor!="None" and current_user.currcontest==problem.contestfor and time[0]>=contest.timelimit:
                            current_user.totalpoints+=problem.points
                            current_user.completedproblems=current_user.completedproblems+" "+problem.code
                            contest=contests.query.filter_by(code=problem.contestfor).first()
                            return render_template("problem_correct_time_up.html", problem=problem, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
                    db.session.commit()
                    return render_template("problem_correct.html", problem=problem, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
                else:
                    differences = find_string_differences(expected_out, outputreal)
                    return (differences)+"next:"+str(expected_out)
                    #return render_template("problem_wrong.html", problem=problem, problemcount=problemcount, contestcount=contestcount, totalcontests=0)
            except subprocess.TimeoutExpired:
                # Terminate the process with SIGTERM
                proc.terminate()
                try:
                    # Check if the process terminated within a grace period
                    proc.wait(timeout=problem.timelimit)
                except subprocess.TimeoutExpired:
                    # If the process is still running, kill it forcefully with SIGKILL
                    proc.kill()
                return render_template("problem_timeout.html", problem=problem, problemcount=problemcount, contestcount=contestcount, totalcontests=0)

    except subprocess.TimeoutExpired:
        return 'Time Limit Exceeded'
    except subprocess.CalledProcessError:
        return 'Runtime Error'


@app.route("/basalt-license")
def basalt_license():
    return render_template("basalt.html")

@app.route("/p-news",methods=['GET','POST'])
@login_required
def p_news():
    title = request.form['title']
    authors = request.form['authors']
    body = request.form['body']
    if current_user.username=="admin":
        n=news(title=title, body=body, authors=authors)
        db.session.add(n)
        total_news=news.query.order_by(news.date.desc()).all()
        if len(total_news)==9:
            db.session.delete(total_news[-1])
        db.session.commit()
        return "News Published!"
    else:
        abort(403)

@app.route("/contest/<code>/edit")
@login_required
def edit_contest(code):
    if current_user.username == "admin" or current_user.username == "contestbot":
        return render_template("contest_edit.html", code=code)

@app.route("/contest/<code>/edit/submit", methods=['GET', 'POST'])
@login_required
def edit_contest_submit(code):
    if current_user.username == "admin" or current_user.username == "contestbot":
        date = request.form['date']
        cont = contests.query.filter_by(code = code).first()
        cont.end_date = date
        db.session.commit()
        return "Successful"

with app.app_context():
    db.create_all()

# Remove the below section if hosting on Pythonanywhere/similar service. This is for local runs.
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
