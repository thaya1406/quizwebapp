import sqlite3
from random import randint

db_name = 'quiz.sqlite'
conn = None
cursor = None

def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

def close():
    cursor.close()
    conn.close()

def do(query):
    cursor.execute(query)
    conn.commit()

def clear_db():
    ''' deletes all tables '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()

def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    
    do('''CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY, 
            name VARCHAR)''' 
    )
    do('''CREATE TABLE IF NOT EXISTS question (
                id INTEGER PRIMARY KEY, 
                question VARCHAR, 
                answer VARCHAR, 
                wrong1 VARCHAR, 
                wrong2 VARCHAR, 
                wrong3 VARCHAR)'''
    )
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
                id INTEGER PRIMARY KEY,
                quiz_id INTEGER,
                question_id INTEGER,
                FOREIGN KEY (quiz_id) REFERENCES quiz (id),
                FOREIGN KEY (question_id) REFERENCES question (id) )'''
    )
    close()

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def add_questions():
    questions = [
        ('How many months in a year have 28 days?', 'All', 'One', 'None','Two'),
        ('What will the green cliff look like if it falls into the Red Sea?', 'Wet', 'Red', 'Will not change', 'Purple'),
        ('Which hand is better to stir tea with?', 'With a spoon', 'Right', 'Left', 'Any'),
        ('What has no length, depth, width, or height, but can be measured?', 'Time', 'Stupidity', 'The sea','Air'),
        ('When is it possible to draw out water with a net?', 'When the water is frozen', 'When there are no fish', 'When the goldfish swim away', 'When the ne breaks'),
        ('What is bigger than an elephant and weighs nothing?', 'Shadow of elephant','A balloon','A parachute', 'A cloud')
    ]
    open()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close()

def add_quiz():
    quizes = [
        ('Quiz 1', ),
        ('Quiz 2', ),
        ('Strange Quiz', )
    ]
    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()

def add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    answer = input("Add a link (y/n)?")
    while answer != 'n':
        quiz_id = int(input("quiz id: "))
        question_id = int(input("question id: "))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Add a link (y/n)?")
    close()


def get_question_after(last_id=0, vict_id=1):
    ''' returns the next question after the question with the passed ID
    for the first question, the default value is passed'''
    open()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content 
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ? 
    ORDER BY quiz_content.id '''
    cursor.execute(query, [last_id, vict_id] )

    result = cursor.fetchone()
    close()
    return result 

def get_quises():
    '''returns a list of quizzes (id, name)
    you can only take quizzes that have questions, but for now we choose a simple option '''
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result 

def check_answer(q_id, ans_text):
    query = '''
            SELECT question.answer 
            FROM quiz_content, question 
            WHERE quiz_content.id = ? 
            AND quiz_content.question_id = question.id
        '''
    open()
    cursor.execute(query, str(q_id))
    result = cursor.fetchone()
    close()    
    # print(result)
    if result is None:
        return False # cannot find
    else:
        if result[0] == ans_text:
            # print(ans_text)
            return True # the answer matched
        else:
            return False # found but didn't match

def get_quiz_count():
    ''' optional function '''
    query = 'SELECT MAX(quiz_id) FROM quiz_content'
    open()
    cursor.execute(query)
    result = cursor.fetchone()
    close()
    return result 

def get_random_quiz_id():
    query = 'SELECT quiz_id FROM quiz_content'
    open()
    cursor.execute(query)
    ids = cursor.fetchall()
    rand_num = randint(0, len(ids) - 1)
    rand_id = ids[rand_num][0]
    close()
    return rand_id

def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    show_tables()
    add_links()
    show_tables()
    # print(get_question_after(0, 3))
    # print(get_quiz_count())
    # print(get_random_quiz_id())
    pass
    
if __name__ == "__main__":
    main()