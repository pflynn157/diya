##
## The markdown parser
## TODO: We need to simplify this function a bit
##

def process_content(content):
    new_content = "<br />\n"
    last_c = None
    index = 0
    in_list = False
    
    for _ in content:
        if index >= len(content): break
        c = content[index]
    
        # Markdown newlines
        if c == '\n' and last_c == '\n':
            if in_list:
                in_list = False
                new_content += "</ul>\n"
            new_content += "<br /><br />\n"
        
        # Escape characters
        elif c == '\\':
            if content[index+1] == '_':
                new_content += "_"
                index += 1
            elif content[index+1] == '-':
                new_content += '-'
                index += 1
            elif content[index+1] == '*':
                new_content += '*'
                index += 1
            elif content[index+1] == '[':
                new_content += '['
                index += 1
            elif content[index+1] == ']':
                new_content += ']'
                index += 1
            elif content[index+1] == '\\':
                new_content += "\\"
                index += 1
            elif content[index+1] == '#':
                new_content += "#"
                index += 1
            else:
                new_content += "\\"
        
        # Special characters
        elif c == '<':
            new_content += "&lt;"
        elif c == '>':
            new_content += "&gt;"
        
        # Lists
        elif c == '-' and last_c == '\n':
            if not in_list:
                new_content += "<ul>\n"
                in_list = True
            new_content += "<li>"
        
        elif c == '\n' and in_list:
            new_content += "</li>\n"
        
        # Italics
        elif c == '_':
            new_content += "<i>"
            index += 1
            while index < len(content) and content[index] != '_':
                new_content += content[index]
                index += 1
            new_content += "</i>"
        
        # Headers
        elif c == '#':
            # Figure out the header size
            h = 0
            while c == '#':
                c = content[index]
                h += 1
                index += 1
            h -= 1
            
            # Print the header
            new_content += "<h" + str(h) + ">"
            while content[index] != '\n':
                new_content += content[index]
                index += 1
            new_content += "</h" + str(h) + ">\n"
        
        # Code
        elif c == "`":
            if content[index+1] != "`" or content[index+2] != "`":
                index += 1
                new_content += c
                continue
            new_content += "<code>\n"
            index += 3
            
            #while index < len(content) and content[index] != "`":
            #    if (index+1 < len(content) and content[index+1] == '`') and (index+2 < len(content) and content[index+2] == '`'):
            #        break
            while index < len(content):
                if index + 1 < len(content) and index + 2 < len(content):
                    if content[index] == '`' and content[index+1] == '`' and content[index+2] == '`':
                        break
                   
                if content[index] == '\n':
                    new_content += "<br />"
                elif content[index] == ' ':
                    new_content += "&nbsp;"
                elif content[index] == '\t':
                    for _ in range(0,4):
                        new_content += "&nbsp;"
                elif content[index] == '<':
                    new_content += "&lt;"
                elif content[index] == '>':
                    new_content += "&gt;"
                elif content[index] == '\\':
                    if content[index+1] == '_':
                        new_content += "_"
                        index += 1
                    elif content[index+1] == '-':
                        new_content += '-'
                        index += 1
                    elif content[index+1] == '*':
                        new_content += '*'
                        index += 1
                    elif content[index+1] == '[':
                        new_content += '['
                        index += 1
                    elif content[index+1] == ']':
                        new_content += ']'
                        index += 1
                    elif content[index+1] == '\\':
                        new_content += '\\'
                        index += 1
                    else:
                        new_content += "\\"
                else:
                    new_content += content[index]
                index += 1
            index += 3
            
            new_content += "</code>\n"
        
        # Hyperlinks and images
        # Markdown links follow this syntax: [Text](link)
        # Images follow this syntax: ![Alt](link)
        elif c == '[' or c == '!':
            is_image = False
            
            if c == '!' and content[index+1] == '[':
                index += 1
                is_image = True
            elif c == '!' and content[index+1] != '[':
                new_content += c
                last_c = c
                index += 1
                continue
                
            link_text = ""
            link = ""
            index += 1
            
            while content[index] != "]":
                link_text += content[index]
                index += 1
            
            index += 2
            while content[index] != ")":
                link += content[index]
                index += 1
                
            if is_image:
                new_content += '<img class="img-fluid" src="assets/' + link + '">' + link_text + '</img>'
            else:
                new_content += '<a href="' + link + '">' + link_text + '</a>'
        
        # Otherwise, just plain content...
        else:
            if last_c == '\n' and in_list:
                content += "</ul>\n"
                in_list = False
            new_content += c
            last_c = c
        
        if index < len(content): last_c = content[index]
        index += 1
    
    # Pad the bottom for loops
    new_content += "<br />"
    new_content += "<br />"
    new_content += "<br />"
    
    return new_content
    
    
