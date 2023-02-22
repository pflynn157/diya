##
## Utilities and templates for creating a new website
##
import os
import shutil

def new_website():
    print("Creating website in current directory...")
    
    # Create the structure
    os.mkdir("./output")
    os.mkdir("./data")
    os.mkdir("./data/pages")
    os.mkdir("./data/posts")
    os.mkdir("./data/assets")
    shutil.copytree("/usr/share/diya/base", "./base", dirs_exist_ok=True)
    
    # Create the config file
    with open("config.py", "w+") as writer:
        writer.write('name = "My Website!"\n')
        writer.write('output = "./output"\n')
        writer.write('base = "./base"\n')
        writer.write('pages = "./data/pages"\n')
        writer.write('posts = "./data/posts"\n')
        writer.write("\n\n")
    
    # Create the index page file
    with open("./data/pages/index.md", "w+") as writer:
        writer.write(index_template)
        writer.write("\n\n")
    
    # Create the example post file
    with open("./data/posts/hello-world.md", "w+") as writer:
        writer.write(post_template)
        writer.write("\n\n")

##
## The base page templates
##

## Index
index_template = '''
---
title:Home
template:page
output:index
menu: false
---

Hello world! Welcome to the home page.
'''

# Post
post_template = '''
---
title: "New Site"
date: "2021-06-16"
---

Hello world! This is a post.

'''

