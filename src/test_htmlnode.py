import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        #Test for none prop
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        #Test for multiple prop
        node2 = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank"
        })
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node2.props_to_html(), expected)
        #Test for single prop
        node3 = HTMLNode(props={"class":"primary-btn"})
        expected3 = ' class="primary-btn"'
        self.assertEqual(node3.props_to_html(), expected3)