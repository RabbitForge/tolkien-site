import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("not a valid url", TextType.BOLD, url = "not a valid url")
        node4 = TextNode("this is a valid url", TextType.BOLD, url = "https://example.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node3, node4)

    def test_why(self):
        test = TextNode("not the same type", TextType.ITALIC)
        test2 = TextNode("not the same type", TextType.BOLD)
        test3 = TextNode("not the same type", TextType.BOLD)
        self.assertEqual(test2, test3)
        self.assertNotEqual(test, test2)

    def test_url(self):
        test = TextNode("text", TextType.BOLD, url = "")
        test2 = TextNode("text", TextType.BOLD, url = "https://example.com")
        test3 = TextNode("text", TextType.BOLD, url = "https://example.com")
        self.assertEqual(test2, test3)
        self.assertNotEqual(test, test2)

    def test_text(self):
        test = TextNode("text", TextType.TEXT)
        test2 = TextNode("text", TextType.BOLD)
        test3 = TextNode("text", TextType.TEXT)
        self.assertEqual(test, test3)
        self.assertNotEqual(test2, test3)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )


if __name__ == "__main__":
    unittest.main()
