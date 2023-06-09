import sqlite3

con = sqlite3.connect('poems.db')

cur = con.cursor()

#cur.execute("CREATE TABLE IF NOT EXISTS pointer(poem_id INT)")
#cur.execute("CREATE TABLE IF NOT EXISTS poems(title TEXT, author TEXT, lines TEXT, tags TEXT, cws TEXT, attachment TEXT, alt TEXT,  PRIMARY KEY(title, author))")

import os
poem_list = os.listdir("poems")
attachment_list = os.listdir("attachments")

def insert_data(filename):
    '''
    Reads data from the /poems directory then inserts the data into a database
    
        Parameters:
                filename (str): the name of the poem file being read

        Returns:
                None
    '''
    file_path = 'poems/' + filename
    with open(file_path, 'r', encoding='utf-8') as f:
        fileData = f.read()
    
    poem_data = fileData.split('\n-\n')

    #Adds 'None' for everything that isn't filled out or is blank
    for i in range(0, 7):
        try:
            poem_data[i]
            if poem_data[i] == '':
                poem_data[i] = None
        except IndexError:
            poem_data.append(None)

    #Attachment replaced with 'None' if it isn't valid.
    if poem_data[5] and not (poem_data[5] in attachment_list and poem_data[5].endswith(('.png', '.jpg'))):
        print("non-valid attachment:", poem_data[4])
        poem_data[4] = None

    # inserts the stuff into the poems table or updates it if there's already the same author and title in the table.
    cur.execute("INSERT INTO poems (title, author, lines, tags, cws, attachment, alt) VALUES(?, ?, ?, ?, ?, ?, ?) ON CONFLICT(title, author) DO UPDATE SET lines=excluded.lines, tags=excluded.tags, cws=excluded.cws, attachment=excluded.attachment, alt=excluded.alt", (poem_data))
    con.commit()

for poem in poem_list:
    insert_data(poem)