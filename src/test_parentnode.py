import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_parent_node(self):

        #test base case
        node_child = LeafNode("Bold text","b")
        node = ParentNode("p",[node_child])
        expected = "<p><b>Bold text</b></p>"
        self.assertEqual(node.to_html(), expected)

        #test parent with multiple children
        node_child_2 = LeafNode("Bold text","b")
        node_child_3 = LeafNode("Bold text second","b")
        node2 = ParentNode("p",[node_child_2,node_child_3])
        expected_2 = "<p><b>Bold text</b><b>Bold text second</b></p>"
        self.assertEqual(node2.to_html(), expected_2)

        #test parent with no tag(should raise value error)
        node_child_4 = LeafNode("Bold text","b")
        with self.assertRaises(ValueError):
            node3 = ParentNode(None,[node_child_4])
            node3.to_html()
        