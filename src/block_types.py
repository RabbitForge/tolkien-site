from enum import Enum
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    print(f"DEBUG: Raw markdown: {repr(markdown[:100])}")  # Show first 100 chars
    blocks = markdown.split("\n\n")
    print(f"DEBUG: Split into {len(blocks)} blocks")
    filtered_blocks = []
    for i, block in enumerate(blocks):
        if block == "":
            continue
        block = block.strip()
        print(f"DEBUG: Block {i}: {repr(block[:50])}")  # Show first 50 chars of each block
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    print(f"DEBUG: Checking block type for: {repr(block[:30])}")
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        print("DEBUG: Found HEADING")
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        print("DEBUG: Found CODE")
        return BlockType.CODE
    if block.startswith(">"):
        print("DEBUG: Found QUOTE")
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        print("DEBUG: Found OLIST")
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    print("DEBUG: Defaulting to PARAGRAPH")
    return BlockType.PARAGRAPH
