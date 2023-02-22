##
## Contains the actual HTML generators
##
import config

##
## This function is called at the end of all the other functions below.
## After the page-specific stuff is generated, it is passed here to be
## put into the template. The base template file contains all the stuff
## like the theme, navigation bars, and so on.
##
def generate_template(output, content, nav):
    writer = open(output, "w")
    with open(config.base + "/base.html", "r") as reader:
        for line in reader:
            if line.strip() == "<!--TEMPLATE-->":
                writer.write(content)
            elif line.strip() == "<!--NAVBAR-->":
                for entry in nav:
                    writer.write('\t\t<li class="nav-item">')
                    writer.write('\t\t<a class="nav-link" href="' + entry[1] + '.html">' + entry[0] + '</a>')
                    writer.write('\t\t</li>')
            elif line.strip() == "<!--CUSTOM_NAVBAR-->":
                for item in config.custom_links:
                    writer.write('\t\t<li class="nav-item">')
                    writer.write('\t\t<a class="nav-link" href="' + item[1] + '">' + item[0] + '</a>')
                    writer.write('\t\t</li>')
            elif line.strip() == "<!--NAME-->":
                writer.write('\t\t<title>' + config.name + '</title>\n')
            elif line.strip() == "<!--NAME_NAVBAR-->":
                writer.write('\t\t' + config.name + '\n')
            else:
                writer.write(line)
    writer.close()

##
## This generates a page
##
def generate_page(data, content, nav):
    path = config.output + "/" + data["output"] + ".html"
    final_content = ""
    with open(config.base + "/" + data["template"] + ".html", "r") as reader:
        for line in reader:
            if line.strip() == "<!--PAGE_TITLE-->":
                final_content += "<h1>" + data["title"] + "</h1>\n"
            elif line.strip() == "<!--PAGE_CONTENT-->":
                final_content += "<p>" + content + "</p>\n"
            else:
                final_content += line
    generate_template(path, final_content, nav)
    
##
## This generates a post
##
def generate_post(data, nav):
    path = config.output + "/" + data["output"] + ".html"
    final_content = ""
    with open(config.base + "/post.html", "r") as reader:
        for line in reader:
            if line.strip() == "<!--POST_TITLE-->":
                final_content += "<h2>" + data["title"] + "</h2>\n"
            elif line.strip() == "<!--POST_CONTENT-->":
                final_content += "<p>" + data["content"] + "</p>\n"
            else:
                final_content += line
    generate_template(path, final_content, nav)
    
##
## This generates an individual blog roll item.
## This function is called from the generate_blog_roll function below.
##
def generate_blog_roll_item(data):
    final_content = ""
    with open(config.base + "/blog_roll_item.html", "r") as reader:
        for line in reader:
            if line.strip() == "<!--PREVIEW_TITLE-->":
                final_content += data["title"]
            elif line.strip() == "<!--PREVIEW_DATE-->":
                final_content += data["date"]
            elif line.strip() == "<!--PREVIEW-->":
                final_content += data["content"]
            else:
                final_content += line
    final_content = final_content.replace('href="#"', 'href="/' + data["output"] +'.html"')
    return final_content
   
##
## And finally, this generates the actual blog roll
##            
def generate_blog_roll(data, nav):
    path = config.output + "/blog.html"
    final_content = ""
    with open(config.base + "/blog.html", "r") as reader:
        for line in reader:
            if line.strip() == "<!--PREVIEW_ITEM-->":
                for item in data:
                    final_content += generate_blog_roll_item(item)
            else:
                final_content += line
    generate_template(path, final_content, nav)
    
