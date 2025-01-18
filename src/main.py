from textnode import *
import os
import shutil
def main():
    print("calling copy_content_src_to_des function")
    copy_content_src_to_des("static", "public")
    generate_pages_recursive("content", "template.html", "public")


"""
 This function serves as a static site file copier, it:
 1) Takes content from a source directory (static/) and copies to a destination directory (public/).
 2) Maintains the exact same directory structure when copying.
 3) Recursively go though nested directories (/static/images/).
 4) Cleans/Delete the destination directory first before copying, to ensure fresh copy each iteration.

 The objective of this function is to make sure all HTML/CSS and images files are in 1 place (public directory) so we can generate our static website
"""
def copy_content_src_to_des(src_path, des_path):
    if os.path.exists(des_path):
        shutil.rmtree(des_path)
        print(f"The destination {des_path} has been deleted")

    os.makedirs(des_path)
    print(f"The destination {des_path} has been created")

    #recursive copying
    #list all items from src_path
    dirs = os.listdir(src_path)
    for dir in dirs:
        #for each items, determine if it's a file or directory
        #if it's a file copy it
        #if it's a directory, create it in the destination and recursively copy it's contents
        #full path
        source_item = os.path.join(src_path, dir)
        dest_item = os.path.join(des_path, dir)
        if os.path.isdir(source_item):
            print(f"{dir} directory reached")
            # 1. create a directory in the destination
            # 2. make a recursive call to copy it's contents
            copy_content_src_to_des(source_item, dest_item)
        elif os.path.isfile(source_item):
            shutil.copy(source_item, dest_item)
            print(f"{dir} file reached")
        else:
            print(f"{dir} does not exists")

"""
    Converts a markdown file to HTML using a template.

    Args:
        from_path (str): Path to source markdown file
        template_path (str): Path to HTML template file
        dest_path (str): Path where generated HTML should be written

    Process:
        1. Reads markdown content from from_path
        2. Reads HTML template from template_path
        3. Converts markdown to HTML using markdown_to_html_node()
        4. Extracts title from markdown and HTML content from nodes
        5. Formats template by replacing:
            - {{ Title }} with extracted title
            - {{ Content }} with generated HTML
        6. Creates destination directory if needed
        7. Writes complete HTML to dest_path
"""
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #read the markdown files from from_path to dest_path using template_path
    markdown_content = ""
    template_content = ""
    with open(from_path, "r") as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()
    #convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()

    #extract title 
    title = extract_title(markdown_content)

    #replace template placeholders
    html_doc = template_content.replace("{{ Title }}", title)
    html_doc = html_doc.replace("{{ Content }}", html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # write the output file
    with open(dest_path, 'w') as f:
        f.write(html_doc)

"""
Generate html file using template.html for each markdown file in the content directory, and write them in the public directory. 
"""
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Checking directory: {dir_path_content}")
    dir_items = os.listdir(dir_path_content)
    print(f"Found items: {dir_items}")
    
    for item in dir_items:
        item_full_path = os.path.join(dir_path_content, item)
        print(f"Processing: {item_full_path}")
        relative_path = os.path.relpath(item_full_path, dir_path_content)
        item_dest_path = os.path.join(dest_dir_path, relative_path)
        
        if os.path.isfile(item_full_path) and item_full_path.endswith(".md"):
            print(f"Found markdown file: {item_full_path}")
            html_dest_path = item_dest_path.replace(".md", ".html")
            print(f"Will generate HTML at: {html_dest_path}")
            os.makedirs(os.path.dirname(html_dest_path), exist_ok=True)
            generate_page(item_full_path, template_path, html_dest_path)
        elif os.path.isdir(item_full_path):
            print(f"Found directory: {item_full_path}")
            generate_pages_recursive(item_full_path, template_path, os.path.join(dest_dir_path, item))


main()