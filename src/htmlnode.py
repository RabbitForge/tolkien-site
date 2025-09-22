import re 
from dataclasses import dataclass
from typing import Optional


@dataclass
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        cls = self.__class__.__name__
        count = len(self.children) if self.children else 0
        return f"{cls}(tag={self.tag!r}, value={self.value!r}, children={count}, props={self.props!r})"

    def to_html(self):
        raise NotImplementedError("Child classes must implement to_html()")

    def props_to_html(self):
        if not self.props:
            return ""
        return " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if not self.children:
            raise ValueError("invalid HTML: no children")
        inner = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{self.props_to_html()}>{inner}</{self.tag}>"
