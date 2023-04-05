def format_post(poem_row, columns):
    '''
    Formats and returns the information from the databse to be suitable as a cohost post block.

        Parameters:
                poem_row (list): a list of contents 
                columns (list): a list of names
            
        Returns:
                poem_dict (dict): the names as keys with contents as (formatted) values
    '''
    poem_dict = {}
    for i, data in enumerate(poem_row):
        column = columns[i]
        poem_dict[column] = data

    #making the content block
    poem_dict['content'] = f"*by {poem_dict['author']}*"
    if poem_dict['lines']:
        poem_dict['content'] += "<br><br>" + poem_dict['lines'].replace("\n", "<br>")
    
    #making the tag block
    if poem_dict['tags']:
        poem_dict['tags'] = poem_dict['tags'].split(', ') + ['poem', 'poetry', 'poem a day', 'daily poem', poem_dict['author']]
    else:
        poem_dict['tags'] = ['poem', 'poetry', 'poem a day', 'daily poem', poem_dict['author']]
    
    if poem_dict['title']:
        poem_dict['tags'].append(poem_dict['title'])

    #CWs list
    if poem_dict['cws']:
        poem_dict['cws'] = poem_dict['cws'].split(', ')
    else:
        poem_dict['cws'] = []

    #attachment
    if poem_dict['attachment']:
        poem_dict['attachment'] = "attachments/" + poem_dict['attachment']
    
    return poem_dict