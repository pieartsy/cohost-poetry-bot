import traceback
traceback.print_stack()
from cohost.models.user import User
from cohost.models.block import AttachmentBlock, MarkdownBlock

import os
user = User.login(os.getenv("COHOST_USER"), os.getenv("COHOST_PASS"))
project = user.getProject('schlongus')

blocks=[MarkdownBlock('test')]

newPost = project.post(headline="test", blocks=blocks) # this is where the exception is raised

print('Check out your post at {}'.format(newPost.url))
traceback.print_stack()