##
## This is the content processor
## Everything starts here
##
import shutil
import datetime
from os import listdir
from os.path import isfile, join

import config
from generator import *
from markdown import *

##
## This is the first thing that should be called
## Here, we copy raw contents such as images and files to
## the output directory
##
def copy_raw_contents():
    shutil.copytree(config.base + "/css", config.output + "/css", dirs_exist_ok=True)
    shutil.copytree(config.base + "/js", config.output + "/js", dirs_exist_ok=True)
    shutil.copytree("./data/assets", config.output + "/assets", dirs_exist_ok=True)

##
## Despite the name, this is for pages and posts
## Here, we break down the metadata from the actual Markdown post content,
## and return both.
##
## We call the markdown processor from here
##
def parse_page(path, file):
    data = dict()
    content = ""
    
    in_meta = False
    
    with open(path + "/" + file, "r") as reader:
        for line in reader:
            ln = line.strip()
            if ln.startswith("---"):
                in_meta = not in_meta
            
            else:
                # If we're in the meta area, we process as one line
                if in_meta:
                    parts = line.split(":")
                    part2 = ""
                    for i in range(1,len(parts)):
                        part2 += parts[i].strip().strip("\"")
                        if i + 1 < len(parts):
                            part2 += ": "
                    data[parts[0]] = part2
                
                # Otherwise, append to the content
                else:
                    content += line
    
    content = process_content(content)
    return (data, content)

##
## This is the entry point of the processor, while should be called
## after the raw contents are copied.
##
def processor_main():
    # Read the input pages
    all_pages = [f for f in listdir(config.pages) if isfile(join(config.pages, f))]
    all_posts = [f for f in listdir(config.posts) if isfile(join(config.posts, f))]

    all_data = list()
    all_posts_data = list()
    post_previews = list()
    nav_data = [("Home", "index"), ("Blog", "blog")]

    ##
    ## Read in the pages
    ##
    for page in all_pages:
            data = parse_page(config.pages, page)
            all_data.append(data)
            if "menu" not in data[0] or data[0]["menu"] != "false":
                nav_data.append((data[0]["title"], data[0]["output"]))

    ##
    ## Read in the posts
    ##
    for post in all_posts:
        data = parse_page(config.posts, post)
        data_dict = data[0]
        data_dict["content"] = data[1]
        data_dict["output"] = post.rsplit(".", 1)[0]
        
        # Generate post previews
        data_dict2 = data_dict.copy()
        if len(data_dict["content"]) > 100:
            data_dict2["content"] = data[1][:100].replace("<br />", "").replace("<br/>", "")
            stop = 0
            for i in range(0,99):
                if i < len(data_dict2["content"]) and data_dict2["content"][i] == '<':
                    stop = i-2
                    break
            if stop > 0:
                data_dict2["content"] = data[1][:stop].replace("<br />", "").replace("<br/>", "")
            
            data_dict2["content"] += "..."
        all_posts_data.append(data_dict)
        post_previews.append(data_dict2)
        
    # Sort the post previews by date
    all_posts_data.sort(key=lambda x: datetime.datetime.strptime(x["date"], "%Y-%m-%d"))
    post_previews.sort(key=lambda x: datetime.datetime.strptime(x["date"], "%Y-%m-%d"))
    post_previews.reverse()
            
    ##
    ## Generate all the data
    ##
    # The pages...
    for item in all_data:
        data = item[0]
        content = item[1]
        generate_page(data, content, nav_data)
      
    # The posts...  
    for item in all_posts_data:
        generate_post(item, nav_data)
    
    # And the blog roll...   
    generate_blog_roll(post_previews, nav_data)
    
