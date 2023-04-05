# access sqlite3 db where the poems are
import sqlite3
from dotenv import load_dotenv
import os
from formatpost import format_post

con = sqlite3.connect('poems.db')

cur = con.cursor()

def write_file(filename, content):
    '''
    Writes to a file on the desktop. The filename is appended with the date of trying to run the script and contains a message.
        
        Parameters:
                filename (str): what the file will be named
                content (str): what message will be written in the file
        
        Returns:
                None
    '''
    # imports datetime module and gets the time now
    import datetime
    now = datetime.datetime.now()
    # names file after filename parameter + date formatted as April_23 with a markdown extension (so that links are clickable if present)
    name_of_file = f"C:\\Users\\maddi\\Desktop\\{filename}_{now.strftime('%b')}_{now.strftime('%d')}.md"

    # writes to file mentioning the date and the content.
    with open(name_of_file, "a+") as f:
        f.write(f"It's {now.strftime('%x')} and {content}\n")


def make_post(poemRow, columns):
    '''
    Logs in with the cohost API and makes a cohost post based off the formatted poem data from the database
            
        Parameters:
                poem_row (list): a list of contents 
                columns (list): a list of names
            
        Returns:
                None
    '''

    poem_dict = format_post(poemRow, columns)

    # making more readable variables
    headline = poem_dict.get('title', '')
    content = poem_dict.get('content', None)
    tags = poem_dict['tags'] # I guess tags is always set?
    cws = poem_dict.get('cws')
    
    attachment = poem_dict.get('attachment', None)
    alt = poem_dict.get('alt', None)


    # importing the cohost posting bot
    from cohost.models.user import User
    from cohost.models.block import AttachmentBlock, MarkdownBlock

    #Creates a block to add to the cohost post
    if attachment:
        blocks = [AttachmentBlock(filepath=attachment, alt_text=alt),
                MarkdownBlock(content)]
    else:
        blocks = [MarkdownBlock(content)]

    #get login from .env
    load_dotenv()
    user = User.login(os.getenv("COHOST_USER"), os.getenv("COHOST_PASS"))
    print("logged in")
    project = user.getProject('dailypoem') # will retrieve the page I have edit writes for with handle @dailypoem
    print("pulled up project")

    # make the actual post. the page returns a 403 if it's private (i think??) so it's an exception
    try:
        newPost = project.post(headline=headline, blocks=blocks, tags=tags, cws=cws)
    except PermissionError:
        write_file("Private", "the page is private. Unprivate it and try again.")

    # calls write_file to write the URL to a file. there's an attribute error when it's a draft (because it can't reach the URL)
    try:
        write_file("Success", f"my poem is [here]({format(newPost.url)})!")
    except AttributeError:
        write_file("Draft", "the draft posted, just trust me.")


#find the poem row after the row we left off at
last_poem_row = cur.execute("SELECT * FROM poems WHERE rowid = (SELECT max(poem_id) FROM pointer)")

column_names = [desc[0] for desc in last_poem_row.description]
    #remove tuple
last_poem_row = [item for tup in last_poem_row for item in tup]

# if the row exists, make the post
if last_poem_row != []:
    make_post(last_poem_row, column_names)
    #increase pointer so we go to the next poem next run
    cur.execute("UPDATE pointer SET poem_id = (SELECT max(poem_id) FROM pointer) + 1")
    con.commit()
# if the last row matching the pointer doesn't exist (i.e. the pointer is past the amount of poems I have in the db) then make a file that alerts me
elif last_poem_row == []:
    write_file("NO_POEMS", "I need to add more poems!")
    
