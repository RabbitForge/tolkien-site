from block_types import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode
from split_nodes import extract_markdown_images, extract_markdown_links, text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def text_to_children(text: str):
    return [text_node_to_html_node(n) for n in text_to_textnodes(text)]

def count_leading_hashes(s: str) -> int:
    count = 0
    for ch in s:
        if ch == "#" and count < 6:
            count += 1
        else:
            break
    return count

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children_list = []

    print(f"DEBUG: Total blocks to process: {len(blocks)}")

    for i, block in enumerate(blocks):
        print(f"DEBUG: Processing block {i}: {repr(block[:30])}")
        bt = block_to_block_type(block)
        print(f"DEBUG: Block {i}: '{block[:50]}...' -> {bt}")
        print(f"DEBUG: Block {i} identified as: {bt}")

        if bt == BlockType.HEADING:
            html_node = heading_to_html_node(block)
            children_list.append(html_node)
            print(f"DEBUG: Added heading: {html_node.to_html()[:50]}")
            continue

        if bt == BlockType.CODE:
            print(f"DEBUG: About to process CODE block: {repr(block)}")
            html_node = code_to_html_node(block) 
            children_list.append(html_node)
            print(f"DEBUG: Added code block")
            continue

        if bt == BlockType.QUOTE:
            html_node = quote_to_html_node(block)
            children_list.append(html_node)
            print(f"DEBUG: Added quote block")
            continue

        if bt == BlockType.ULIST:
            html_node = ulist_to_html_node(block)
            children_list.append(html_node)
            print(f"DEBUG: Added unordered list: {html_node.to_html()[:100]}")
            continue

        if bt == BlockType.OLIST:
            html_node = olist_to_html_node(block)
            children_list.append(html_node)
            print(f"DEBUG: Added ordered list: {html_node.to_html()[:100]}")
            continue

        html_node = paragraph_to_html_node(block)
        children_list.append(html_node)
        print(f"DEBUG: Added paragraph: {html_node.to_html()[:50]}")

    print(f"DEBUG: Final children count: {len(children_list)}")
    return ParentNode("div", children_list)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)
