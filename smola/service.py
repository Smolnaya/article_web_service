import os
from os import listdir, getcwd
from os.path import splitext
from smola.article import Article
import re
import xml.etree.ElementTree as et
from datetime import date


def splitList(fullList, wantedParts):
    length = len(fullList)
    return [fullList[i * length // wantedParts: (i + 1) * length // wantedParts]
            for i in range(wantedParts)]


def getXmlList():
    xmlPath = f'{getcwd()}/static/xml'
    lst = [splitext(f)[0] for f in listdir(xmlPath)]
    return lst


def getArticleObject(title):
    if title != '':
        xmlPath = f'{getcwd()}/static/xml/{title}.xml'
        xml = et.ElementTree(file=xmlPath)
        date = xml.find('date').text
        author = xml.find('author').text
        text = xml.find('text').text[8:-2]
        tags = xml.find('tags').text
        source = xml.find('source').text
        return Article(title, date, author, text, tags, source)

    else:
        path = f'{getcwd()}/static/xml'
        lst = list()
        for filename in os.listdir(path):
            if not filename.endswith('.xml'):
                continue
            fullname = os.path.join(path, filename)
            xml = et.ElementTree(file=fullname)
            date = xml.find('date').text
            author = xml.find('author').text
            text = xml.find('text').text[8:-2]
            tags = xml.find('tags').text
            source = xml.find('source').text
            lst.append(Article(title, date, author, text, tags, source))
        return lst


def checkData(jsonData):
    lst = ['title', 'date', 'author', 'text']
    for elem in lst:
        if jsonData[elem] == '':
            return False
    return True


def workXml(jsonData):
    try:
        article = Article(*jsonData.values())
        root = et.Element('doc')

        sourceElem = et.SubElement(root, 'source')
        sourceElem.text = article.source

        authorElem = et.SubElement(root, 'author')
        authorElem.text = article.author

        titleElem = et.SubElement(root, 'title')
        titleElem.text = article.title

        dateElem = et.SubElement(root, 'date')
        dateElem.text = article.date

        tagsElem = et.SubElement(root, 'tags')
        tagsElem.text = article.tags

        textElem = et.SubElement(root, 'text')
        textElem.text = f"![CDATA[{article.text}]]"

        tree = et.ElementTree(root)

        title = re.sub(r'[^а-яА-Яa-zA-Z0-9_\s]', '', article.title)

        with open(f"{getcwd()}/static/xml/{title}.xml", "wb") as files:
            tree.write(files, encoding='UTF-8', xml_declaration=True)
        return '', True

    except Exception as err:
        return err, False


def deleteXml(title):
    try:
        xmlPath = f'{getcwd()}/static/xml/{title}.xml'
        os.remove(xmlPath)
        return '', True
    except Exception as err:
        return err, False


def searchXmlListByTitle(title):
    if title != '':
        out = list(filter(lambda s: s.lower().find(title.lower()) != -1, getXmlList()))
        return out
    else:
        return getXmlList()


def sortXml(lst: list, param: str):
    rawDict = dict()
    for title in lst:
        article = getArticleObject(title)
        rawDict.update({article.title: article.getAttr(param)})
    sortedDict = dict(sorted(rawDict.items(), key=lambda item: item[1]))
    return list(sortedDict.keys())


def getDataForFilter():
    articleList = getArticleObject('')
    author = list()
    tags = list()
    source = list()
    for article in articleList:
        author.append(article.author)
        tags.append(article.tags)
        source.append(article.source)
    return list(set(author)), list(set(source)), list(set(tags))


def validateFilterData(dateFrom, dateTo, author, source, tag):
    if dateFrom:
        dateFrom = date(*map(int, (dateFrom.split('-'))))
    else:
        dateFrom = None

    if dateTo:
        dateTo = date(*map(int, (dateTo.split('-'))))
    else:
        dateTo = None

    if (dateFrom and dateTo) and (dateFrom > dateTo):  # если есть обе даты, но С больше ПО
        dateFrom = None
        dateTo = None

    if author == '-':
        author = None

    if source == '-':
        source = None

    if tag == '-':
        tag = None

    return dateFrom, dateTo, author, source, tag


def filterList(dateFrom, dateTo, author, source, tag):
    lst = getXmlList()
    filteredLst = list()
    for title in lst:
        article = getArticleObject(title)
        suitable = True

        # Дата
        articleDate = date(*map(int, (article.date.split('-'))))
        if dateFrom and dateTo:
            if not (dateFrom <= articleDate <= dateTo):  # если есть обе даты, то статья между С ПО
                suitable = False
        elif dateFrom and not dateTo:
            if not (dateFrom <= articleDate):  # если есть С, то статья больше С
                suitable = False
        elif dateTo and not dateFrom:
            if not (articleDate <= dateTo):  # если есть ПО, то статья меньше ПО
                suitable = False

        # Автор
        articleAuthor = article.author
        if author and (author != articleAuthor):
            suitable = False

        # Источник
        articleSource = article.source
        if source and (source != articleSource):
            suitable = False

        # Теги
        articleTags = article.tags
        if tag and (tag != articleTags):
            suitable = False

        if suitable:
            filteredLst.append(title)

    return filteredLst
