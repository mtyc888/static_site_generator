import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", None)
        node2 = TextNode("This is a text node", None)
        self.assertIsNone(node.text_type)
        self.assertIsNone(node2.text_type)
    
    def test_text_node_to_html_node(self):
        node = TextNode("this is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        #we expect an HTMLNode with no tag
        #the text content should match the input
        self.assertEqual(html_node.tag, "")
        self.assertEqual(html_node.value, "this is a text node")

        node2 = TextNode("this is a text node", TextType.BOLD) 
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node2.value, "this is a text node")

        with self.assertRaises(Exception):
            node3 = TextNode("this is a text node", None) 
            html_node3 = text_node_to_html_node(node3)

if __name__ == "__main__":
    unittest.main()