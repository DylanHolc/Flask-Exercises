from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Chizzle'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

@app.route('/')
def start_page():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('start.html', title = title, instructions = instructions)

@app.route('/survey')
def start_survey():
    session['responses'] = []
    return redirect('/questions/0')

@app.route('/questions/<int:qnum>')
def show_questuons(qnum):
    responses = session['responses']
    if responses is None:
        return redirect('/')
    
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')
    
    if (len(responses) != qnum):
        flash('Invalid Question Number! Please Complete the Survey in the Intended Order')
        return redirect(f'/questions/{len(responses)}')
    
    question = satisfaction_survey.questions[qnum]
    return render_template('questions.html', question = question, question_num = qnum)

@app.route('/answer', methods = ['post'])
def record_answer():
    choice = request.form['answer']
    responses = session['responses']
    responses.append(choice)
    session['responses'] = responses
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/complete')
def complete_survey():
    return render_template('completed.html')