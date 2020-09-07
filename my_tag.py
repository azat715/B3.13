class Tag:
    def __init__(self, tag, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self._children = []
        self.indent = ""

        if klass:
            self.attributes["class"] = " ".join(klass)
    
    def child(self, tag, *args, **kwargs):
        child = Tag(tag, *args, **kwargs)
        if self.indent:
            child.indent = "  " + self.indent
        else:
            child.indent = "  "
        self._children.append(child)
        return child
    
    def __str__(self):
        child_line = ""
        if self.attributes:
            attrs = [f"{attribute}={value}" for attribute, value in self.attributes.items()]
            first_line = f'{self.indent}<{self.tag} {" ".join(attrs)}>\n'
        else:
            first_line = f'{self.indent}<{self.tag}>\n'
        if self._children:
            child_line = [f'{item}' for item in self._children]
        last_line = f'{self.indent}/<{self.tag}>\n'                     
        return first_line +f"{self.text}"+ f'{"".join(child_line)}' + last_line

class Html:
    def __init__(self):
        self._child = None

    def child(self, tag):
        self._child = Tag(tag)
        return self._child

    def show(self):
        print(self._child)

test = Html()
test_child = test.child('H1')
test_child2 = test_child.child('H2', klass=("container", "container-fluid"))
test_child3 = test_child2.child('H3')
test_child4 = test_child3.child('H4')
test_child4 = test_child3.child('p')
test_child4.text = 'blavlabab'
test.show()




    



