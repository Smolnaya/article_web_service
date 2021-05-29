from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

import json

from django.views.decorators.csrf import csrf_exempt

from smola.service import *


def index(request):
    if request.method == 'GET':
        xmlList = getXmlList()
        paginator = Paginator(xmlList, 7)
        page = request.GET.get('page')

        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        filterData = getDataForFilter()

        context = {'page_obj': post,
                   'authors': filterData[0],
                   'tags': filterData[1],
                   'sources': filterData[2]}

        return render(request, 'main_page/main_page.html', context)


def getArticle(request, title):
    if title != '-':
        article = getArticleObject(title)
        context = {'article_obj': article}
        return render(request, 'post_page/main_post_page.html', context)
    else:
        return render(request, 'post_page/main_post_page.html')


@csrf_exempt
def updateArticle(request):
    if request.method == 'POST':
        data = request.body.decode('UTF-8')
        jsonData = json.loads(data)
        if checkData(jsonData):
            print(*jsonData)
            result = workXml(jsonData)
            if result[1]:
                return JsonResponse({"resp": 'true'})
            else:
                return JsonResponse({"resp": 'false', "err": result[0]})
        else:
            return JsonResponse({"resp": 'false', "err": 'views.py updateArticle error'})


@csrf_exempt
def deleteArticle(request):
    if request.method == 'POST':
        data = request.body.decode('UTF-8')
        jsonData = json.loads(data)
        if checkData(jsonData):
            result = deleteXml(jsonData['title'])
            if result[1]:
                return JsonResponse({"resp": 'true'})
            else:
                return JsonResponse({"resp": 'false', "err": result[0]})
        else:
            return JsonResponse({"resp": 'false', "err": 'views.py deleteArticle error'})


@csrf_exempt
def sortArticle(request):
    if request.method == 'POST':
        data = request.body.decode('UTF-8')
        jsonData = json.loads(data)
        lst = jsonData['lst']
        param = jsonData['param']  # title / date / author
        sortedLst = sortXml(lst, param)
        paginator = Paginator(sortedLst, 7)
        page = request.GET.get('page')
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        filterData = getDataForFilter()

        context = {'page_obj': post,
                   'authors': filterData[0],
                   'sources': filterData[1],
                   'tags': filterData[2]}
        return render(request, 'main_page/main_page.html', context)


@csrf_exempt
def searchArticle(request):
    if request.method == 'POST':
        data = request.POST.get('param')
        xmlList = searchXmlListByTitle(data)

        sortBy = request.POST.get('radio')

        if sortBy:
            xmlList = sortXml(xmlList, sortBy)

        request.session['data'] = xmlList

        paginator = Paginator(xmlList, 7)
        page = request.GET.get('page')

        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        filterData = getDataForFilter()

        context = {'page_obj': post,
                   'authors': filterData[0],
                   'sources': filterData[1],
                   'tags': filterData[2]}

        return render(request, 'main_page/main_page.html', context)

    if request.method == 'GET':
        paginator = Paginator(request.session['data'], 7)
        page = request.GET.get('page')

        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        filterData = getDataForFilter()

        context = {'page_obj': post,
                   'authors': filterData[0],
                   'sources': filterData[1],
                   'tags': filterData[2]}

        return render(request, 'main_page/main_page.html', context)


@csrf_exempt
def filterArticle(request):
    if request.method == 'POST':
        dateFrom = request.POST.get('filterDateFrom')
        dateTo = request.POST.get('filterDateTo')
        author = request.POST.get('authorSelect')
        source = request.POST.get('sourceSelect')
        tag = request.POST.get('tagSelect')
        data = validateFilterData(dateFrom, dateTo, author, source, tag)
        lst = filterList(*data)
        request.session['data'] = lst

        paginator = Paginator(lst, 7)
        page = request.GET.get('page')
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)
        filterData = getDataForFilter()
        context = {'page_obj': post,
                   'authors': filterData[0],
                   'sources': filterData[1],
                   'tags': filterData[2]}
        return render(request, 'main_page/main_page.html', context)

    if request.method == 'GET':
        paginator = Paginator(request.session['data'], 7)
        page = request.GET.get('page')

        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post = paginator.page(paginator.num_pages)

        filterData = getDataForFilter()

        context = {'page_obj': post,
                   'authors': filterData[0],
                   'sources': filterData[1],
                   'tags': filterData[2]}

        return render(request, 'main_page/main_page.html', context)
