from django.views import View
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
import json
from django.conf import settings
from operator import itemgetter  # sort news by date
from datetime import datetime  # sort news by date
from .forms import NewsForm, SearchForm
import random


def simple_date(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect('/news/')


class News(View):

    def get(self, request, link, *args, **kwargs):
        data_list = settings.DEFAULT_NEWS
        data = dict()
        try:
            with open(settings.NEWS_JSON_PATH) as f:
                data_list = json.load(f)
        except FileNotFoundError:
            with open(settings.NEWS_JSON_PATH, 'w') as f:
                json.dump(data_list, f)
        for d in data_list:
            if d['link'] == link:
                data['title'] = d['title']
                data['created'] = d['created']
                data['text'] = d['text']
                break
        return render(request, 'news/news.html',
                      context={'title': data['title'],
                               'created': data['created'],
                               'text': data['text']})


class Main(View):

    def get(self, request, *args, **kwargs):
        data_list = settings.DEFAULT_NEWS
        result_list = list()
        new_dict = dict()
        q = request.GET.get('q')
        try:
            with open(settings.NEWS_JSON_PATH) as f:
                data_list = json.load(f)
        except FileNotFoundError:
            with open(settings.NEWS_JSON_PATH, 'w') as f:
                json.dump(data_list, f)
        data_list = sorted(data_list, key=itemgetter('created'), reverse=True)
        if q is None:
            result_list = data_list
        else:
            for d in data_list:
                if q in d['title']:
                    result_list.append(d)
        for d in result_list:
            if simple_date(d['created']) in new_dict:
                new_dict[simple_date(d['created'])].append(d)
            else:
                s_d = simple_date(d['created'])
                new_dict[s_d] = [d]

        return render(request, 'news/main.html',
                      context={'sorted_news': new_dict})

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        clean_form = dict()
        if form.is_valid():
            clean_form = form.cleaned_data
        q = clean_form['q']

        data_list = settings.DEFAULT_NEWS
        result_list = list()
        new_dict = dict()
        try:
            with open(settings.NEWS_JSON_PATH) as f:
                data_list = json.load(f)
        except FileNotFoundError:
            with open(settings.NEWS_JSON_PATH, 'w') as f:
                json.dump(data_list, f)
        data_list = sorted(data_list, key=itemgetter('created'), reverse=True)

        for d in data_list:
            if q in d['title']:
                result_list.append(d)

        for d in result_list:
            if simple_date(d['created']) in new_dict:
                new_dict[simple_date(d['created'])].append(d)
            else:
                s_d = simple_date(d['created'])
                new_dict[s_d] = [d]
        return render(request, 'news/main.html',
                      context={'sorted_news': new_dict})


class Create(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        form = NewsForm(request.POST)
        clean_form = dict()
        if form.is_valid():
            clean_form = form.cleaned_data
        title = clean_form['title']
        text = clean_form['text']
        created = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        link = random.randint(1, 1000000)
        data_list = settings.DEFAULT_NEWS
        link_ids = list()
        new_news_dict = dict()
        try:
            with open(settings.NEWS_JSON_PATH) as f:
                data_list = json.load(f)
        except FileNotFoundError:
            with open(settings.NEWS_JSON_PATH, 'w') as f:
                json.dump(data_list, f)
        for d in data_list:
            link_ids.append(d['link'])
        while link in link_ids:
            link = random.randint(1, 1000000)
        new_news_dict['created'] = created
        new_news_dict['text'] = text
        new_news_dict['title'] = title
        new_news_dict['link'] = link
        data_list.append(new_news_dict)

        with open(settings.NEWS_JSON_PATH, 'w') as f:
            json.dump(data_list, f)
        return HttpResponseRedirect('/news/')
