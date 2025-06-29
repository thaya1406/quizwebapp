import os
from random import shuffle
from flask import Flask, session, request, redirect, render_template, url_for
from db_scripts import get_question_after, get_quises, check_answer

def start_quiz(quiz_id):
    '''creates the desired values ​​in the session dictionary'''
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0

def end_quiz():
    session.clear()

def quiz_form():
    ''' the function receives a list of quizzes from the database and forms a form with a drop-down list '''
    q_list = get_quises()
    return render_template('start.html', q_list=q_list)

def index():
    ''' First page: if you came with a GET request, then select a quiz,
    if POST - then remember the id of the quiz and send questions '''
    if request.method == 'GET':
        # the quiz is not selected, reset the id of the quiz and show the selection form
        start_quiz(-1)
        return quiz_form()
    else:
        # received additional data in the request! We use them:
        quest_id = request.form.get('quiz') #selected quiz number 
        start_quiz(quest_id)
        return redirect(url_for('test'))

def save_answers():
    '''receives data from the form, checks if the answer is correct, writes the results to the session'''
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    # this question has already been asked:
    session['last_question'] = quest_id
    # increase the question counter:
    session['total'] += 1
    # check if the answer matches the correct one for this id
    if check_answer(quest_id, answer):
        session['answers'] += 1

def question_form(question):
    '''gets the row from the database corresponding to the question, returns the html with the form '''
    # question - result of the get_question_after
    # fields: 
            # [0] - quiz question number, 
            # [1] - question text, 
            # [2] - right answer, [3],[4],[5] - false answers

    # shuffle the answers:
    answers_list = [
        question[2], question[3], question[4], question[5]
    ]
    shuffle(answers_list)
    # pass it to the template, return the result:
    return render_template('test.html', question=question[1], quest_id=question[0], answers_list=answers_list)

def test():
    '''returns the question page'''
    # what if the user without choosing a quiz went directly to address '/test'? 
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        # if we received data, then we need to read it and update the information:
        if request.method == 'POST':
            save_answers()
        # in any case, deal with the current question id
        next_question = get_question_after(session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            # the questions are over:
            return redirect(url_for('result'))
        else:            
            return question_form(next_question)

def result():
    html = render_template('result.html', right=session['answers'], total=session['total'])
    end_quiz()
    return html

folder = os.getcwd() # remember the current working folder
# Create a web application object:
app = Flask(__name__, template_folder=folder, static_folder=folder)  
app.add_url_rule('/', 'index', index, methods=['post', 'get'])   # creates rule for URL '/'
app.add_url_rule('/test', 'test', test, methods=['post', 'get']) # creates rule for URL '/test'
app.add_url_rule('/result', 'result', result) # creates rule for URL '/test'
#Setting up the encryption key:
app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'

if __name__ == "__main__":
    #Launching web server:
    app.run()