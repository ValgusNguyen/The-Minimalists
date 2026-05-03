
from textnode import TextType,TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node.append(node)
            continue
        new_string = node.text.split(delimiter)
        if len(new_string) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i, part in enumerate(new_string):
            if new_string[i] == "":
                continue
            if i % 2 == 0:
                new_node.append(TextNode(part,TextType.TEXT))
            else:
                new_node.append(TextNode(part,text_type))
    return new_node

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    match = re.findall(pattern,text)
    return match

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    match = re.findall(pattern,text)
    return match

def split_nodes_image(old_nodes):
    new_node = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node.append(node)
            continue
        origin = node.text
        images = extract_markdown_images(origin)
        if len(images) == 0:
            new_node.append(node)
            continue
        for image in images:
            part = origin.split(f"![{image[0]}]({image[1]})",1)
            if part[0] != "":
                new_node.append(TextNode(part[0],TextType.TEXT))
            if len(part) != 2:
                raise ValueError("invalid markdown, formatted section not closed")
            new_node.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            origin = part[1]
        if origin != "":
            new_node.append(TextNode(origin,TextType.TEXT))
    return new_node
            
def split_nodes_link(old_nodes):
    new_node = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node.append(node)
            continue
        origin = node.text
        links = extract_markdown_links(origin)
        if len(links) == 0:
            new_node.append(node)
            continue
        for link in links:
            part = origin.split(f"[{link[0]}]({link[1]})",1)
            if part[0] != "":
                new_node.append(TextNode(part[0],TextType.TEXT))
            if len(part) != 2:
                raise ValueError("invalid markdown, formatted section not closed")
            new_node.append(
                TextNode(
                    link[0],
                    TextType.LINK,
                    link[1],
                )
            )
            origin = part[1]
        if origin != "":
            new_node.append(TextNode(origin,TextType.TEXT))
    return new_node

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes