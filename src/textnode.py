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
    return_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_list.append(node)
        else:
            node_value = node.text
            try:
                #first back tick
                start = node_value.index(delimiter)
                #second backtick after start
                end = node_value.index(delimiter, start + 1)
                # What would you do with the text start, during, and after?

                #start
                #if start is 0 it means that the code block happens at the beginning of the text 
                if start > 0:
                    string_before = node_value[0:start]
                    node = TextNode(string_before, TextType.TEXT)
                    return_list.append(node)
                #during
                string_during = node_value[start+1:end]
                node2 = TextNode(string_during, text_type)
                return_list.append(node2)
                #after
                if end < len(node_value) - 1:
                    string_after = node_value[end+1:]
                    node3 = TextNode(string_after, TextType.TEXT)
                    return_list.append(node3)
            except ValueError:
                return_list.append(node)
    return return_list

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

