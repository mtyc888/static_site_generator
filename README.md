Static Site Generator
Objective: Takes raw content files (like Markdown and images) and turn them into a static website (HTML and CSS files).

![image](https://github.com/user-attachments/assets/c67d8d9b-3347-48ae-a6da-872ae78e5bd6)


High-level architecture 

![image](https://github.com/user-attachments/assets/02799f3a-a28b-43af-93f9-fa0359006416)

Flow of data through the full system:

1) Markdown files are in the /content directory. A template.html file is in the root of the project.
2) The static site generator (the Python code in src/) reads the Markdown files and the template file.
3) The generator converts the Markdown files to a final HTML file for each page and writes them to the /public directory.
4) We start the built-in Python HTTP server (a separate program, unrelated to the generator) to serve the contents of the /public directory on http://localhost:8888 (our local machine).
5) We open a browser and navigate to http://localhost:8888 to view the rendered site.

How it works:

1) Delete everything in the /public directory.
2) Copy any static assets (HTML template, images, CSS, etc.) to the /public directory.
3) Generate an HTML file for each Markdown file in the /content directory. For each Markdown file:
   1) Open the file and read its contents.
   2) Split the markdown into "blocks" (e.g. paragraphs, headings, lists, etc.).
   3) Convert each block into a tree of HTMLNode objects. For inline elements (like bold text, links, etc.) we will convert:
      -Raw markdown -> TextNode -> HTMLNode
   4) Join all the HTMLNode blocks under one large parent HTMLNode for the pages.
   5) Use a recursive to_html() method to convert the HTMLNode and all its nested nodes to a giant HTML string and inject it in the HTML template.
   6) Write the full HTML string to a file for that page in the /public directory.
