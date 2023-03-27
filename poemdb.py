import sqlite3

con = sqlite3.connect('poems.db')

cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS pointer(poem_id INT)")
cur.execute("CREATE TABLE IF NOT EXISTS poems(title TEXT, author TEXT, lines TEXT, tags TEXT, attachment TEXT, alt TEXT, UNIQUE(lines))")

import os
poemList = os.listdir("poems")
attachmentList = os.listdir("attachments")
    
def insert_data(filename):
    filePath = 'poems/' + filename
    with open(filePath, 'r', encoding='utf-8') as f:
        fileData = f.read()
    
    poemData = fileData.split('\n-\n')

    #Adds 'None' for everything that isn't filled out or is blank
    for i in range(0, 6):
        try:
            poemData[i]
            if poemData[i] == '':
                poemData[i] = None
        except IndexError:
            poemData.append(None)

    #Attachment replaced with 'None' if it isn't valid.
    if poemData[4] and not (poemData[4] in attachmentList and poemData[4].endswith(('.png', '.jpg'))):
        print("non-valid attachment:", poemData[4])
        poemData[4] = None

        
    cur.execute("INSERT OR IGNORE INTO poems(title, author, lines, tags, attachment, alt) VALUES(?, ?, ?, ?, ?, ?)", (poemData))
    con.commit()

for poem in poemList:
    insert_data(poem)