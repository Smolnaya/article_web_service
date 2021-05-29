class Article:
    def __init__(self, title, date, author, text, tags, source):
        self.title = title
        self.date = date
        self.author = author
        self.text = text
        self.tags = tags
        self.source = source

    def getAttr(self, attr: str):
        if attr == 'title':
            return self.title
        if attr == 'date':
            return self.date
        if attr == 'author':
            return self.author
        if attr == 'text':
            return self.text
        if attr == 'tags':
            return self.tags
        if attr == 'source':
            return self.source
