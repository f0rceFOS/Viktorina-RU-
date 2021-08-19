from flask import Flask, url_for, redirect, session, request, render_template
from db_scripts import get_question_after, get_quizes, check_answer, get_quiz_name
import os
from random import *

folder = os.getcwd()

def start_value():
    session["quest_counter"] = 0
    session["quiz_number"] = -1
    session["total_right_answer"] = 0

def index():
    if request.method == "GET":
        start_value()
        quiz_names = get_quizes()
        return render_template('start.html', list =quiz_names)


    if request.method == "POST":
        session["quiz_number"] = int(request.form.get("quiz_select"))
        return redirect(url_for("test"))




def test():
    next_quest = get_question_after(session["quest_counter"], session["quiz_number"])
    session["quest_counter"] += 1

    if request.method == "POST":
        _id = request.form.get("id")
        ans = request.form.get("ans")
        if check_answer(_id, ans):
            session["total_right_answer"] += 1

    if next_quest == None:
        return redirect(url_for("finish"))

    q_id = next_quest[0]
    quest_text = next_quest[1]
    answers = [next_quest[2], next_quest[3], next_quest[4]]

    shuffle(answers)

    return render_template("test.html", quest_text=quest_text, answers=answers, q_id = q_id)

def finish():
   return render_template("result.html",
   quiz_name = get_quiz_name(session["quiz_number"]),
   user_point = session["total_right_answer"],
   quest_amount = session["quest_counter"]-1)


app = Flask(__name__, template_folder=folder, static_folder=folder)
app.config['SECRET_KEY'] = "ggwp1337"


app.add_url_rule('/', 'index', index, methods=["POST", "GET"])
app.add_url_rule('/test', 'test', test, methods=["POST", "GET"])
app.add_url_rule('/finish', 'finish', finish)

if __name__ == "__main__":
    #app.run()
    app.run()
    #app.run(host = '0.0.0.0', port=5000, debug=False)

