from django.shortcuts import render
from .models import DataPoint

def index(request):
	data_points = DataPoint.objects.order_by('filed_date')[:10]
	context = {'data_points': data_points}
	return render(request, 'spike/index.html', context)
	
def eric(request):
	context = {'foodd': 'Tacos!', 'sport': 'Football'}
	return render(request, 'spike/eric.html', context)
