import os
from cohost.models.user import User
from cohost.models.block import AttachmentBlock, MarkdownBlock

def main():
    print('logging in... ')
    username = os.getenv('COHOST_USER')
    password = os.getenv("COHOST_PASS")
    handle = 'schlongus'
    if username is None:
        username = input('username: ')
    if password is None:
        password = input('password: ')
    if handle is None:
        handle = input('handle: ')
    user = User.login(username, password)
    project = user.getProject(handle)

    # Begin test!
    blocks=[MarkdownBlock('test')]
    # this is where the exception is raised
    newPost = project.post(headline="test", blocks=blocks) 
    # If we reach this point, no exception was raised.
    print('Check out your post at {}'.format(newPost.url))
    print('test post made successfully')
    return

if __name__ == '__main__':
    main()