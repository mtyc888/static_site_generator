from enum import Enum
from htmlnode import LeafNode
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