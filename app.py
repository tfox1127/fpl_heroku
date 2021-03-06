from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
#from flask_session import Session
from send_mail import send_mail
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime as datetime

app = Flask(__name__)

ENV = 'dev'

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://kbhpppsbtsabyk:6f9f47eb4721c77c17f1fccefeb2693a629e1f6e571bad88143561ba10e422be@ec2-52-20-248-222.compute-1.amazonaws.com:5432/d22l4qure274m')
                                                  # DATABASE_URL is an environment variable that indicates where the database lives
db = scoped_session(sessionmaker(bind=engine))    # create a 'scoped session' that ensures different users' interactions with the
                                                  # database are kept separate


#engine = create_engine('postgres://kbhpppsbtsabyk:6f9f47eb4721c77c17f1fccefeb2693a629e1f6e571bad88143561ba10e422be@ec2-52-20-248-222.compute-1.amazonaws.com:5432/d22l4qure274m')
#app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
#Session(app)
#db = scoped_session(sessionmaker(bind=engine))
#ter system set idle_in_transaction_session_timeout='1min';
#SET SESSION idle_in_transaction_session_timeout = '1min';
#SQLALCHEMY_POOL_RECYCLE = 60
#alter database dbnamehere set statement_timeout = 600;

@app.route('/')
def index():
    elements = db.execute('SELECT * FROM blog ORDER BY post_number DESC LIMIT 10')
    db.commit()
    return render_template('index.html', elements=elements)

@app.route('/live')
def live():
    time = db.execute("SELECT updated FROM live2;").fetchone()
    elements = db.execute("SELECT * FROM live2 ORDER BY points_lg DESC LIMIT 50")
    bottoms =  db.execute("SELECT * FROM live2 where player_name not in (SELECT name FROM \"LMS\") ORDER BY score LIMIT 5")
    epls =  db.execute("SELECT * FROM score_board")
    sss =  db.execute("SELECT * FROM score_sheet")

    db.commit()
    #time = times.item() #.datetime.strftime("%m/%d/%Y, %H:%M:%S")
    return render_template('live.html', elements=elements, time=time, bottoms=bottoms, epls=epls, sss=sss)

@app.route("/teams/<int:team_id>")
def teams(team_id):
  """List details about a single flight."""
  pname    = db.execute("SELECT * FROM live2 WHERE entry = :team_id", {"team_id": team_id})
  #elements = db.execute("SELECT * FROM teams2 WHERE entry = :team_id", {"team_id": team_id})
  elements = db.execute("SELECT * FROM \":team_id\"", {"team_id": team_id})
  db.commit()
  return render_template("teams.html", elements=elements, pname=pname)

@app.route('/lms')
def lms():
    acti = db.execute("SELECT * FROM lms_ac")
    elim = db.execute("SELECT * FROM lms_el")
    db.commit()
    return render_template('lms.html', acti=acti, elim=elim)

@app.route('/lcs')
def lcs():
    return render_template('lcs.html')

@app.route('/cups')
def cups():
    return render_template('cups.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('fpl_list.html')

@app.route('/hof')
def hof():
    elements = db.execute('SELECT * FROM hof_rk ORDER BY "Overall" DESC LIMIT 50').fetchall()
    champs   = db.execute('SELECT * FROM hof_ch').fetchall()
    db.commit()
    return render_template('hof.html', elements=elements, champs = champs)


if __name__ == '__main__':
    app.run()
