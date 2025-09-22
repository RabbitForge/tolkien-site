import re
from textnode import TextNode, TextType, text_node_to_html_node

IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')

LINK_RE = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def extract_markdown_images(text: str):
    return IMAGE_RE.findall(text)

def extract_markdown_links(text: str):
    return LINK_RE.findall(text)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = node.text
        matches = extract_markdown_images(current_text)
        if not matches:
            new_nodes.append(node)
            continue
        for image_alt, image_link in matches:
            token = f"![{image_alt}]({image_link})"
            left, right = current_text.split(token, 1)
            if left:
                new_nodes.append(TextNode(left, TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            current_text = right
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = node.text
        matches = extract_markdown_links(current_text)
        if not matches:
            new_nodes.append(node)
            continue
        for link_text, link_url in matches:
            token = f"[{link_text}]({link_url})"
            left, right = current_text.split(token, 1)
            if left:
                new_nodes.append(TextNode(left, TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            current_text = right
        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    return nodes


def text_to_children(text: str):
    return [text_node_to_html_node(n) for n in text_to_textnodes(text)]
