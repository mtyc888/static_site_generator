from enum import Enum
from htmlnode import LeafNode
import re
class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

"""
    This function is to convert TextNode objects into HTMLNode objects based on their text type.
"""
def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case(TextType.TEXT):
            return LeafNode(text_node.text,"")
        case(TextType.BOLD):
            return LeafNode(text_node.text,"b")
        case(TextType.ITALIC):
            return LeafNode(text_node.text,"i")
        case(TextType.CODE):
            return LeafNode(text_node.text,"code")
        case(TextType.LINK):
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        case(TextType.IMAGE):
            return LeafNode("", "img", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception()

"""
    This function takes a list of old nodes, a delimeter and a text type. It returns a new list of nodes,
    where any "text" type nodes in the input list are split into multiple nodes based on the syntax.

    eg.

    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

    returns:

    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
    ]
"""
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

"""
    This function takes raw markdown text and returns a list of tuples. Each tuple should contain the alt text and the URL of any markdown images.
    For example:

    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
"""
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)
"""
    This function takes raw markdown text and returns a list of tuples. Each tuple should contain the alt text and the URL of any markdown links.
    For example:

    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))
    # [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
""" 
def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

"""
    Function to split TextNode objects, works similarly to split_nodes_delimiter(); We want to split 1 text nodes into multiple,
    text nodes objects and store them into a list.

    example for images:

    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )

    result: A list of TextNode objects

    new_nodes = split_nodes_link([node])
    # [
    #     TextNode("This is text with a link ", TextType.TEXT),
    #     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
    #     TextNode(" and ", TextType.TEXT),
    #     TextNode(
    #         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
    #     ),
    # ]
"""
def split_nodes_image(old_nodes):
    # list to keep the list of TextNodes
    return_list = []
    # loop through the current text node(s)
    for node in old_nodes:
        # we get the text of the current text node object for splitting
        remaining_text = node.text
        # we extract the images from the text
        # example: This is text with a link [to boot dev](https://www.boot.dev) -> [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        images = extract_markdown_images(node.text)
        # we check if images (list) is empty
        if not images:
            # if empty we will append it into the list
            return_list.append(node)
        else:
            # we will then split it into image_alt and image_url
            # image_alt -> "rick roll" 
            # image_url -> "https://i.imgur.com/aKaOqIh.gif"
            # [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
            # (example) remaining_text -> This is text with a link [to boot dev](https://www.boot.dev) test test
            for image_alt, image_url in images:
                # we split it into sections list, 
                # where sections[0] will be the part of the string before the delimiter -> "This is text with a link"
                # and sections[1] will be the part of the string after the delimiter -> "test test"
                # and image_alt will be -> "to boot dev"
                # and image_url will be -> "https://www.boot.dev"
                sections = remaining_text.split(f"![{image_alt}]({image_url})", 1)
                # only if section[0] exists, we create a node and append it into the list
                if sections[0]:
                    node_1 = TextNode(sections[0], TextType.TEXT)
                    return_list.append(node_1)
                # create a node with the image alt and image url
                return_list.append(TextNode(image_alt, TextType.IMAGE, image_url))
                # we shift the remaining_text to the second half of the string (after alt and url)
                # so following the previous example, remaining_text -> "test test"
                # this is done so we can further process the remaining portion of the text
                remaining_text = sections[1]
            # if remaining_text exists, we create the node
            if remaining_text:
                node_3 = TextNode(remaining_text, TextType.TEXT)
                return_list.append(node_3)
    return return_list


def split_nodes_link(old_nodes):
    return_list = []
    for node in old_nodes:
        remaining_text = node.text
        links = extract_markdown_links(node.text)
        if not links:
            return_list.append(node)
        else:
            for link_text, link_url in links:
                sections = remaining_text.split(f"[{link_text}]({link_url})", 1)
                if sections[0]:
                    node_1 = TextNode(sections[0], TextType.TEXT)
                    return_list.append(node_1)

                return_list.append(TextNode(link_text, TextType.LINK, link_url))
                remaining_text = sections[1]

            if remaining_text:
                node_2 = TextNode(remaining_text, TextType.TEXT)
                return_list.append(node_2)
                
    return return_list

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
    
