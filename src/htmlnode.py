class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        # Handle case where tag is None
        if self.tag is None:
            return ""
            
        # Get HTML properties string
        props = self.props_to_html()
        
        # Handle self-closing tags (img, br, hr)
        if self.tag == "img":
            return f"<{self.tag}{props}/>"
            
        # Handle regular tags
        if self.children is None:
            # Return tag with value for tags without children
            inner_content = self.value if self.value is not None else ""
            return f"<{self.tag}{props}>{inner_content}</{self.tag}>"
        
        # Handle tags with children
        children_html = ""
        for child in self.children:
            if child is None:
                continue
            child_html = child.to_html()
            if child_html is None:
                continue
            children_html += child_html
        
        return f"<{self.tag}{props}>{children_html}</{self.tag}>"
    
    def props_to_html(self):
        string = ""
        if self.props:
            for key, value in self.props.items():
                string += f' {key}="{value}"'
        return string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is None")
        if self.children is None:
            raise ValueError("children is None")
        
        result = f"<{self.tag}"
        if self.props:
            result += f"{self.props_to_html()}"
        result += ">"
        for child in self.children:
            result +=child.to_html()     
        result +=f"</{self.tag}>"
        return result

class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)
        self.tag = tag
        self.value = value
    
    def to_html(self):
        if self.value is None:
            raise ValueError()
        if self.tag is None:
            return self.value
        if self.value:
            #self.props_to_html() to check if there is any href's in the tag
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

