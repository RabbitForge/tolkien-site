import unittest
from htmlnode import *
from textnode import *
from block_types import *
from mark_down import *
from split_nodes import *

def text_to_children(text: str):
    return [text_node_to_html_node(n) for n in text_to_textnodes(text)]


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        s = node.props_to_html()
        self.assertIn(' href="https://example.com"', s)
        self.assertIn(' target="_blank"', s)
        self.assertTrue(s.startswith(" "))

    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_repr_has_class_and_counts(self):
        parent = HTMLNode(tag="div", children=[HTMLNode(tag="p"), HTMLNode(tag="a")])
        r = repr(parent)
        self.assertIn("HTMLNode(", r)
        self.assertIn("children=2", r)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_html_fail(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",)

    def test_mixed_content(self):
        text = "Here's an ![image](img.jpg) and a [link](site.com)"
        print("Images:", extract_markdown_images(text))
        print("Links:", extract_markdown_links(text))

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_triple_blank_lines(self):
        md = """
        First block



        Second block
        """.replace(" \n", "\n")
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_single_lines(self):
        md = """This is just a single line"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is just a single line"])

    def test_trailing(self):
        md = "\nThis is just a single line\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(markdown_to_blocks(md), ["This is just a single line"])

    def test_paragraph(self):
        md = "Line one\nLine two"
        blocks = markdown_to_blocks(md)
        self.assertEqual(markdown_to_blocks(md), ["Line one\nLine two"])


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )





if __name__ == "__main__":
    unittest.main()
