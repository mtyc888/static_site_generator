import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_node(self):
        #test base case
        nodeLeaf = LeafNode("Click me!","a", {"href": "https://www.google.com"})
        expected_leaf = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(nodeLeaf.to_html(), expected_leaf)