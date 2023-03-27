def format_post(poemRow, columns):
    poemDict = {}
    for i, data in enumerate(poemRow):
        column = columns[i]
        poemDict[column] = data

    #making the content block
    poemDict['content'] = f"*by {poemDict['author']}*"
    if poemDict['lines']:
        poemDict['content'] += "<br><br>" + poemDict['lines'].replace("\n", "<br>")
    
    #making the tag block
    if poemDict['tags']:
        poemDict['tags'] = poemDict['tags'].split(', ') + ['poem', 'poetry', 'poem a day', 'daily poem', poemDict['author']]
    else:
        poemDict['tags'] = ['poem', 'poetry', 'poem a day', 'daily poem', poemDict['author']]
    
    if poemDict['title']:
        poemDict['tags'].append(poemDict['title'])

    if poemDict['attachment']:
        poemDict['attachment'] = "attachments/" + poemDict['attachment']
    
    return poemDict