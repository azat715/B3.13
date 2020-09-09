from collections import UserList
from pathlib import Path
import textwrap

class TagSingleLine():
    """
    тэг в одну строку, не имеет потомков
    """
    def __init__(self, tag, klass=None, **kwargs):
        self.__tag = tag
        self.text = ""
        # разбор атрибутов
        self._attributes = {}
        if klass:
            self._attributes["class"] = " ".join(klass)
        self._attributes.update(kwargs)
        # атрибут чилдрен тут потому что __init__ тут
        self._children = []

    
    def __iter__(self):
        # можно for собрать отступы но не очень корректно показывает вложенность одного уровня
        return iter(self._children)
      
    @property
    def tag(self):
        # не изменяемый тэг
        if self.attributes:
            return f'<{self.__tag} {self.attributes}>'
        else:
            return f'<{self.__tag}>'

    @property
    def close_tag(self):
        return f'/<{self.__tag}>'
    
    @property
    def attributes(self):
        if self._attributes:
            attr = []
            attr = [f"{attribute}={value}" for attribute, value in self._attributes.items()]
            return " ".join(attr)
         
    def __str__(self):
        return "{}{}{}\n".format(self.tag, self.text, self.close_tag)

class SingleTag(TagSingleLine):
    """
    не парный тэг, не имеет потомков
    """
    @property
    def close_tag(self):
        return f'/>'

class Tag(TagSingleLine):
    """
    парный тэг, с возможностью вложенности
    """

    def __str__(self):
        child = []
        if self._children:
            arr = []
            for item in self._children:
                #вот тут добавляются отступы
                arr.append(textwrap.indent(str(item), '    '))
            child.extend(arr)
        if self.text:
            self.text += "\n"
        child_line = "".join(child)
        return "{0}{1}\n{2}{3}\n".format(self.tag, self.text, child_line, self.close_tag)
    
    def __iadd__ (self, other):
        self._children.append(other)
        return self

class Html(UserList):

    def _render(self):
        # рендеринг текста html
        items = [str(item) for item in self.data] # как бы рекурсивный str
        message = "<html>\n"
        message += "".join(items)
        message += "</html>"
        return message
    
    def show(self):
        print(self._render())

    def write(self, str):
        path = Path(str)      
        path.write_text(self._render())

if __name__ == '__main__':
    doc = Html()
    head = Tag("head")

    title = TagSingleLine("title")
    title.text = "hello"
    head += title
    doc.append(head)

    body = Tag("body")
    h1 = TagSingleLine("h1", klass=("main-text",))
    h1.text = "Test"
    body += h1

    div = Tag("div", klass=("container", "container-fluid"), id="lead")
    paragraph = TagSingleLine("p")
    paragraph.text = "another test"
    div += paragraph

    img = TagSingleLine("img", src="/icon.png", data_image="responsive")
    div += img
    body += div

    doc.append(body)
    doc.show()

    doc.write('index.html')

    test = Html()
    div1 = Tag("div1")
    div2 = Tag("div2")
    div3 = Tag("div3")
    div4 = Tag("div4")
    div1 += div2
    div2 += div3
    div3 += div4
    test.append(div1)
    test.show()
