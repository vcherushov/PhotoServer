from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *
from django.db.models import Q

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

import csv
import xlwt


menu = [ {'title': "Обратная связь", 'url_name': 'contact'},

]

class AvtobusHome(ListView):
    model = TrackCar
    template_name = 'main/index.html'
    context_object_name = 'post'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        return context

#def index(request):
    #post = Avtobus.objects.all()
    #context = {
        #'post': post,
        #'menu': menu,
        #'title': 'Главная страница',
        #'cat_selected': 0,
    #}
    #return render(request, 'main/index.html', context=context)



def about(request):
    return render(request, 'main/about.html', {'menu': menu, 'title': 'О сайте'})


def addpage(request):
    form = AddPostForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            form.save()
            return redirect('home')
        except:
            form.add_error(None, 'Ошибка добавления')
    else:
        form = AddPostForm()
    return render(request, 'main/addpage.html', {'form': form,'menu': menu, 'title': 'Добавление видео'})



def contact(request):
    return HttpResponse("Обратная связь")




def show_post(request, post_slug):
    post = TrackCar.objects.filter(slug=post_slug)

    context = {
        'post': post,
        'menu': menu,
        'title': 'Видео',
        'cat_selected': 0,
    }
    return render(request, 'main/post.html', context=context)



def show_category(request):
    post = TrackCar.objects.all()
    form = AddPostForm(request.GET)
    if form.is_valid():

        if form.cleaned_data["time_create"]:
            post = post.filter(time_create=form.cleaned_data["time_create"])

        if form.cleaned_data["time_time"]:
            post = post.filter(time_time__gt=form.cleaned_data["time_time"]) #выборка >= time_time



    context = {
        'post': post,
        'menu': menu,
        'form': form,
        'title': 'Все фото',
        'cat_selected': 0,
    }

    return render(request, 'main/category.html', context=context)



def download(request):
    post = TrackCar.objects.all()
    form = DownloadForm(request.GET)

    if form.is_valid():

        if form.cleaned_data["day_start"]:
            post = post.filter(time_create__gte=form.cleaned_data["day_start"])

        if form.cleaned_data["day_end"]:
            post = post.filter(time_create__lte=form.cleaned_data["day_end"])

        if form.cleaned_data["time_start"]:
            post = post.filter(time_time__gt=form.cleaned_data["time_start"])  # выборка >= time_time


        all = len(post)
        if form.cleaned_data["day_start"] == None:
            day = "все время"
            str_date = str("все время")
        else:
            day = form.cleaned_data["day_start"]
            str_date = str(form.cleaned_data["day_start"])

        if form.cleaned_data["day_end"] == None:
            day_end = "-"
            str_date_end = str("-")
        else:
            day_end = form.cleaned_data["day_end"]
            str_date_end = str(form.cleaned_data["day_end"])



        truck = len(post.filter(cat="emptytrack"))
        car = len(post.filter(cat="car"))
        full_truck = len(post.filter(cat="fulltrack"))



    context = {
        'post': post,
        'menu': menu,
        'form': form,
        'day': day,
        'day_end': day_end,
        'str_date': str_date,
        'str_date_end': str_date_end,
        'car': car,
        'truck': truck,
        'full_truck': full_truck,
        'all': all,
        'title': 'Скачать',
        'cat_selected': 0,
    }

    return render(request, 'main/download.html', context=context)



def save(request, date, date_end):
    template_path = 'main/pdf.html'
    post = TrackCar.objects.all()
    if date != "все время":
        post = post.filter(time_create__gte=date)
    if date_end != "-":
        post = post.filter(time_create__lte=date_end)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('report')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    ws.write(row_num, 0, 'Отчет с ', font_style)
    ws.write(row_num, 1, str(date), font_style)
    ws.write(row_num, 2, 'по', font_style)
    ws.write(row_num, 3, str(date_end), font_style)
    row_num += 1
    ws.write(row_num, 0, 'Всего', font_style)
    ws.write(row_num, 1, len(post), font_style)
    row_num += 1
    ws.write(row_num, 0, 'Легковые', font_style)
    ws.write(row_num, 1, len(post.filter(cat="car")), font_style)
    row_num += 1
    ws.write(row_num, 0, 'Грузовые без песка', font_style)
    ws.write(row_num, 1, len(post.filter(cat="emptytrack")), font_style)
    row_num += 1
    ws.write(row_num, 0, 'Грузовые с песком', font_style)
    ws.write(row_num, 1, len(post.filter(cat="fulltrack")), font_style)
    row_num += 2
    columns = ['Дата', 'Время', 'Категория', 'Номер', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = post.values_list('time_create', 'time_time', 'cat', 'number')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if col_num == 0:
                ws.write(row_num, col_num, str(row[col_num]), font_style)
            elif col_num == 1:
                ws.write(row_num, col_num, str(row[col_num]), font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response







def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Не найдена</h1>')
