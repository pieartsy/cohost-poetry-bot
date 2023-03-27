# access sqlite3 db where the poems are
import sqlite3
from formatpost import format_post

con = sqlite3.connect('poems.db')

cur = con.cursor()
    
def make_post(poemRow):
    #get column names from the row
    columnNames = [desc[0] for desc in poemRow.description]
    poemDict = format_post(poemRow, columnNames)

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
    import os
    user = User.login(os.getenv("COHOST_USER"), os.getenv("COHOST_PASS"))
    print("logged in")
    project = user.getProject('dailypoem') # will retrieve the page I have edit writes for with handle @dailypoem
    print("pulled up project")

    if poemDict['title']:
        newPost = project.post(poemDict['title'], blocks, tags=poemDict['tags'])
    else:
        newPost = project.post(headline="", blocks=blocks, tags=poemDict['tags'])

    try:
        print('Check out your post at {}'.format(newPost.url))
    except AttributeError:
        print("the draft posted, just trust me")

#find the poem row after the row we left off at
lastPoemRow = cur.execute("SELECT * FROM poems WHERE rowid = (SELECT max(poem_id) FROM pointer)")
    #remove tuple
lastPoemRow = [item for tup in lastPoemRow for item in tup]


# if the row exists, make the post
if lastPoemRow != []:
    print(lastPoemRow)
    make_post(lastPoemRow)
    #increase pointer so we go to the next poem next run
    cur.execute("UPDATE pointer SET poem_id = (SELECT max(poem_id) FROM pointer) + 1")
    con.commit()
else:
    import datetime
    now = datetime.datetime.now()
    filename = f"C:\\Users\\maddi\\Desktop\\NO-POEMS-LEFT_{now.strftime('%b')}_{now.strftime('%d')}_{now.strftime('%y')}.txt"

    with open(filename, "x") as f:
        f.write(f"It's {now.strftime('%x')} and I need to add more poems!")
    
