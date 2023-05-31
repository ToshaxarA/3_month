import sqlite3
import re

async def add_tsk(task):
    connect = sqlite3.connect('todo_list.db')
    cursor = connect.cursor()
    spisok_del = []
    spisok_del.append(task)
    cursor.execute('INSERT INTO todo_list (task) VALUES(?)', (spisok_del))
    connect.commit()
    cursor.close()


async def add_time(time):
    connect = sqlite3.connect('todo_list.db')
    cursor = connect.cursor()
    spisok_vremeni = []
    spisok_vremeni.append(time)
    cursor.execute('INSERT INTO todo_list (time) VALUES(?)', (spisok_vremeni))
    connect.commit()
    cursor.close()

async def show_all_tasks():
    connect = sqlite3.connect('todo_list.db')
    cursor = connect.cursor()
    query = 'SELECT * FROM todo_list'
    cursor.execute(query)
    data = cursor.fetchall()
    spisok_del = []

    for i in data:
        spisok_del.append(i)
    l=len(spisok_del)
    g = []

    for i in range(l):
        a = re.sub('|\(|\'|\,|\)', '', str(spisok_del[i]))
        g.append(a)
    c = []
    for i in g:
        q = i + '\n'
        c.append(q)

    v = '\n'.join(c)
    return v
