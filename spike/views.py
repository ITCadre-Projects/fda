from django.http import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from .forms import PostForm
from .models import DataPoint
from .services import baseline_10_years
from .services import retreive_drug_names
from .services import search_by_product
from .services import retrieve_mentioned_event_twitter
from .services import retrieve_latest_tweets
import json
import datetime


def index(request):
    data_points = DataPoint.objects.order_by('filed_date')
    context = {'data_points': data_points}
    return render(request, 'spike/index.html', context)


def fda(request):
    data_points = baseline_10_years()
    context = {'data_points': data_points}
    return render(request, 'spike/index.html', context)


def search_form(request):
    return render(request, 'spike/search.html')


@api_view(['GET', 'POST'])
def search(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            drug_name = request.POST.get('drug_name')
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            by_date = request.POST.get('by_date')
            three_d = request.POST.get('3d')
            interval = request.POST.get('interval')

    else:
        drug_name = request.query_params.get('drug_name')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        by_date = request.query_params.get('by_date')
        three_d = request.query_params.get('3d')
        interval = request.query_params.get('interval')

    data_points = search_by_product(drug_name, start_date, end_date)

    if data_points:
        if by_date and by_date == "true":
            result = {"hello": "waipang"}

            return JsonResponse(result)
        elif three_d and three_d == "true" and interval:

            my_data_dict = {'final': []}

            for drug in data_points['final']:
                print(drug['data']['results'])
                my_drug_dict = {'name':'', 'data':''}
                my_drug_dict['name'] = drug['name']

                my_result_dict ={'result':[]}


                my_date = start_date
                while my_date <= end_date:
                     my_record ={'date':'', 'count':''}
                     my_count = 0
                     old_my_date = my_date
                     my_date2 = datetime.datetime.strptime(my_date, '%Y%m%d')
                     my_date2 = my_date2 + datetime.timedelta(days=int(interval))
                     my_date = datetime.datetime.strftime(my_date2,'%Y%m%d')
                     for d in drug['data']['results']:
                         if d['time'] <= my_date and d['time'] > old_my_date:
                            my_count = my_count + d['count']
                     my_record['date']=my_date
                     my_record['count'] = my_count
                     my_result_dict['result'].append(my_record)



                my_drug_dict['data'] = my_result_dict
                my_data_dict['final'].append(my_drug_dict)
            return JsonResponse(my_data_dict)
        else:
            return JsonResponse(data_points)
    else:
        return render(request, 'spike/search.html', {'error': True})


@api_view(['GET', 'POST'])
def get_drug_names(request):
    return JsonResponse(retreive_drug_names(request.query_params.get('count')))


@api_view(['GET', 'POST'])
def search_mentioned_events_twitter(request):
    drug_name = request.query_params.get('drug_name')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    limit = request.query_params.get('limit')


    return JsonResponse(retrieve_mentioned_event_twitter(drug_name, start_date, end_date, limit), safe=False)

@api_view(['GET'])
def get_latest_tweets(request):
    limit = request.query_params.get('limit')
    if limit:
        my_limit = limit
    else:
        my_limit = 10
    tweets = retrieve_latest_tweets(my_limit)
    my_data_dict = {'final': []}

    for event in tweets:
        my_drug_dict = {'date': datetime.datetime.strftime(event.submitted_date, '%Y%m%d'), 'tweet': event.raw_data}
        my_data_dict['final'].append(my_drug_dict)
    return JsonResponse(my_data_dict)
