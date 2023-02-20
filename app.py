from flask import Flask, request, render_template, redirect, flash, session
from surveys import surveys

RESPONSES_KEY = "responses"
CURRENT_SURVEY_KEY = 'current_survey'

app = Flask(__name__)
app.config['SECRET_KEY'] = "MAYISCUTE"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



@app.route("/")
def survey_home():
    """Survey Homepage"""
    
    return render_template("survey_home.html", surveys = surveys)

@app.route("/", methods=["POST"])
def pick_survey():
    """Select a survey."""

    survey_id = request.form['survey_code']

    # don't let them re-take a survey until cookie times out
    if request.cookies.get(f"completed_{survey_id}"):
        return render_template("already-done.html")

    survey = surveys[survey_id]
    session[CURRENT_SURVEY_KEY] = survey_id

    return render_template("survey_start.html",
                           survey=survey)

@app.route("/start", methods=["POST"])
def survey_start():
    """In between POST to start survey"""
    session[RESPONSES_KEY] = [];

    return redirect("/questions/0")

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Displays current question according to route"""
    responses = session.get(RESPONSES_KEY)
    survey = surveys[session.get(CURRENT_SURVEY_KEY)]

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    if(len(responses) != qid):
        flash("Invalid question - Please continue the survey in order")
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[qid]
    return render_template("question.html", qid = qid, question = question)

@app.route("/answer",methods=["POST"])
def question_answered():
    """Handles POST for answering a question"""

    answer = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(answer)
    session[RESPONSES_KEY] = responses
    
    survey = surveys[session.get(CURRENT_SURVEY_KEY)]
    if(len(responses) == len(survey.questions)):
        return redirect("/complete")
    return redirect(f"/questions/{len(responses)}")

@app.route("/complete")
def survey_complete():
    """Shows Completed Page"""
    return render_template("complete.html")


