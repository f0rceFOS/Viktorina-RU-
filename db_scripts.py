import sqlite3
db_name = 'db.sqlite'
conn = None

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
    ''' удаляет все таблицы '''
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
    cursor.execute(''' PRAGMA foreign_keys=on ''')
    quiz_request = '''CREATE TABLE IF NOT EXISTS quiz (
        id INTEGER PRIMARY KEY,
        name VARCHAR )'''
    do(quiz_request)

    question_request = ''' CREATE TABLE IF NOT EXISTS question (
        id INTEGER PRIMARY KEY,
        question VARCHAR, answer VARCHAR, wrong1 VARCHAR, wrong2 VARCHAR )'''
    do(question_request)

    quiz_connect = ''' CREATE TABLE IF NOT EXISTS quiz_content(
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER,
        question_id INTEGER,
        FOREIGN KEY (quiz_id) REFERENCES quiz (id),
        FOREIGN KEY (question_id) REFERENCES question (id)
    )'''
    do(quiz_connect)

def addQuestion():
    vopros = [
        ("Сколько будет 285 + 115?", "400", "315", "425"),
        ("В каком году открыли Америку?", "1492", "1512", "1309"),
        ("Самая высокая гора?", "Эверест", "Эльбрус", "Маллака"),
        ("Какая формула площади прямоугольника правильная?", "2 * (a + b)", "4 * ab", "2 * a + b"),
        ("Когда родился Пушкин?", "1799", "1862", "1926")
    ]
    open()
    cursor.executemany(''' INSERT INTO question(question, answer, wrong1, wrong2)
                    VALUES (?,?,?,?)''', vopros)
    conn.commit()

def addQuiz():
    victorina = [
    ("Школьная работа",),
    ("Проверка знаний",)
    ]
    open()
    cursor.executemany('''INSERT INTO quiz(name) VALUES (?)''', victorina)
    conn.commit()
    close()

def check_answer(id, user_answer):
    open()
    request = ''' SELECT question.answer FROM question, quiz_content
    WHERE question.id == quiz_content.question_id
    AND quiz_content.id == ?'''
    cursor.execute(request, str(id))
    data = cursor.fetchall()
    right_answer = data[0][0]
    if right_answer == user_answer:
        return True
    else:
        return False

def get_quizes():
    open()
    cursor.execute(''' SELECT * FROM quiz ORDER BY id''')
    data = cursor.fetchall()
    print(data)
    return data

def get_quiz_name(id):
    open()
    cursor.execute(''' SELECT quiz.name FROM quiz WHERE quiz.id == ? ''', [id])
    data = cursor.fetchone()
    close()
    return data

def get_question_after(question_id=0, quiz_id=1):
    open()
    query = '''
    SELECT *
    FROM question, quiz_content
    WHERE quiz_content.question_id == question.id
    AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id ''' 
    cursor.execute(query, [quiz_id] )
    result = cursor.fetchall()
    close()
    if len(result) > question_id:
        return result[question_id]
    else:
        return None


def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def add_link():
    open()
    otvet = int(input("Хотите добавить вопрос в базу? 0 - стоп"))
    while otvet:
        quiz_id = int(input("в какую викторину добавить вопрос?"))
        quest_id = int(input("вопрос с каким id использовать?"))

        cursor.execute('''INSERT INTO quiz_content(
            quiz_id, question_id) VALUES (?,?) ''', [quiz_id, quest_id] )
        otvet = int(input("Хотите добавить вопрос в базу? 0 - стоп"))
    conn.commit()

    close()


def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def main():
    clear_db()
    create()
    addQuestion()
    addQuiz()
    add_link()
    show_tables()
    get_question_after(1,1)


if __name__ == "__main__":
    main()
    
    
    """
    for quiz in [1,2]:
        print("проверяем викторину с id", quiz)
        for question in range(0,5):
            print(get_question_after(question,quiz))
"""