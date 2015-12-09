from django.http import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from .forms import PostForm
from .models import DataPoint
from .services import baseline_10_years
from .services import retreive_drug_names
from .services import search_by_product
from .services import retrieve_mentioned_event_twitter

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
    else:
        drug_name = request.query_params.get('drug_name')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

    data_points = search_by_product(drug_name, start_date, end_date)

    if data_points:
        return JsonResponse(data_points)
        # return HttpResponse(data_points, content_type="application/json")
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
    count = request.query_params.get('count')

    events = retrieve_mentioned_event_twitter(drug_name, start_date, end_date, count)

    my_data_dict = {'final': []}
    for event in events:
        mye = {"raw_data": event.raw_data, "captured_date": event.captured_date}
        my_data_dict["final"].append(mye)

    return JsonResponse(my_data_dict, safe=False)
