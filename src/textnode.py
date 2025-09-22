from htmlnode import LeafNode
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class TextType(Enum):
	TEXT = "text"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

@dataclass 
class TextNode:
	text: str
	text_type: TextType
	url: Optional[str] = None


	def __post_init__(self):
		if not isinstance(self.text_type, TextType):
			raise TypeError("text_type must be a TextType")

def text_node_to_html_node(text_node):
	if text_node.text_type == TextType.TEXT:
		return LeafNode(None, text_node.text)
	if text_node.text_type == TextType.BOLD:
		return LeafNode("b", text_node.text)
	if text_node.text_type == TextType.ITALIC:
		return LeafNode("i", text_node.text)
	if text_node.text_type == TextType.CODE:
		return LeafNode("code", text_node.text)
	if text_node.text_type == TextType.LINK:
		return LeafNode("a", text_node.text, {"href": text_node.url})
	if text_node.text_type == TextType.IMAGE:
		return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
	raise ValueError(f"invalid text type: {text_node.text_type}")

def text_to_children(text: str):
	tn_list = text_to_textnodes(text)
	return [text_node_to_html_node(tn) for tn in tn_list]

