# access sqlite3 db where the poems are
import sqlite3
from dotenv import load_dotenv
import os
from formatpost import format_post

con = sqlite3.connect('poems.db')

cur = con.cursor()

def writeFile(filename, content):
    '''writes to a file on the desktop with the date of trying to run the script and a message'''
    import datetime
    now = datetime.datetime.now()
    filename = f"C:\\Users\\maddi\\Desktop\\{filename}_{now.strftime('%b')}_{now.strftime('%d')}_{now.strftime('%y')}.txt"

    with open(filename, "a+") as f:
        f.write(f"\nIt's {now.strftime('%x')} and {content}!")


def make_post(poemRow, columns):
    '''makes a cohost post based off the formatted poem data from the database'''

    poemDict = format_post(poemRow, columns)

    # importing the cohost posting bot
    from cohost.models.user import User
    from cohost.models.block import AttachmentBlock, MarkdownBlock


    #Creates a block to add to the cohost post
    if poemDict['attachment'] and not poemDict['alt']:
        blocks = [AttachmentBlock(poemDict['attachment']),
                MarkdownBlock(poemDict['content'])]
    elif poemDict['attachment'] and poemDict['alt']:
        blocks = [AttachmentBlock(poemDict['attachment'], alt_text=poemDict['alt']),
                MarkdownBlock(poemDict['content'])]
    else:
        blocks = [MarkdownBlock(poemDict['content'])]

    #get login from .env
    load_dotenv()
    user = User.login(os.getenv("COHOST_USER"), os.getenv("COHOST_PASS"))
    print("logged in")
    project = user.getProject('dailypoem') # will retrieve the page I have edit writes for with handle @dailypoem
    print("pulled up project")

    if poemDict['title']:
        newPost = project.post(poemDict['title'], blocks, tags=poemDict['tags'])
    else:
        newPost = project.post(headline="", blocks=blocks, tags=poemDict['tags'])

    try:
        writeFile("Success", f"my poem is at {format(newPost.url)}")
    except AttributeError:
        writeFile("SuccessDraft", "the draft posted, just trust me")

#find the poem row after the row we left off at
lastPoemRow = cur.execute("SELECT * FROM poems WHERE rowid = (SELECT max(poem_id) FROM pointer)")

columnNames = [desc[0] for desc in lastPoemRow.description]
    #remove tuple
lastPoemRow = [item for tup in lastPoemRow for item in tup]

# if the row exists, make the post
if lastPoemRow != []:
    make_post(lastPoemRow, columnNames)
    #increase pointer so we go to the next poem next run
    cur.execute("UPDATE pointer SET poem_id = (SELECT max(poem_id) FROM pointer) + 1")
    con.commit()
elif lastPoemRow == []:
    writeFile("NO_POEM_TODAY_", "I need to add more poems!")
    
