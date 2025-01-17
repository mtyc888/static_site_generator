import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


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

    def test_split_nodes_delimiter(self):
        # Case 1: Empty text between delimiters
        node1 = TextNode("before``after", TextType.TEXT)
        node1_list = [node1]
        new_nodes = split_nodes_delimiter(node1_list, "`", TextType.CODE)
        
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "before"
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == ""
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == "after"
        assert new_nodes[2].text_type == TextType.TEXT

        # Case 2: Code block with content
        node2 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2_list = [node2]
        new_nodes2 = split_nodes_delimiter(node2_list, "`", TextType.CODE)
        
        assert len(new_nodes2) == 3
        assert new_nodes2[0].text == "This is text with a "
        assert new_nodes2[0].text_type == TextType.TEXT
        assert new_nodes2[1].text == "code block"
        assert new_nodes2[1].text_type == TextType.CODE
        assert new_nodes2[2].text == " word"
        assert new_nodes2[2].text_type == TextType.TEXT


if __name__ == "__main__":
    unittest.main()