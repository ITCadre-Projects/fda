import datetime
import json
import urllib.error
import urllib.request
from urllib.parse import urlparse

from .classes import DataPoint
from .models import DataRecord


def get_json(url, username=None, password=None):
    try:
        if username and password:
            url_parts = urlparse(url)
            url_base = "{}://{}/".format(url_parts.scheme, url_parts.netloc)
            password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            password_manager.add_password(None, url_base, username, password)
            auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
            opener = urllib.request.build_opener(auth_handler)
            urllib.request.install_opener(opener)
        with urllib.request.urlopen(url) as response:
            raw = response.read().decode('utf-8')
            data = json.loads(raw)
        return data
    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.msg)


def baseline_10_years(search_type=None):
    print(search_type)
    base = "https://api.fda.gov/drug/event.json"

    if not search_type or search_type == 'All':
        search = "receivedate:[20050101+TO+20150101]"
    else:
        search = 'patient.drug.openfda.pharm_class_epc:"' + search_type + '"'

    print(search)
    count = "receivedate"
    url = "{}?search={}&count={}".format(base, search, count)
    data = get_json(url)
    points = []
    for result in data["results"]:
        # print(result)
        point = DataPoint(filed_date=result["time"], drug_name="All", count=result["count"])
        points.append(point)
    return points


def search_by_product(products, start_date, end_date):
    my_products = products.split(',')

    base = "https://api.fda.gov/drug/event.json"

    my_data_dict = {'final': []}
    for product in my_products:
        my_drug_dict = {'name': product, 'data': {}}
        search = 'patient.drug.medicinalproduct:{}+AND+receivedate:[{}+TO+{}]+AND+primarysourcecountry:ca'.format(
                product,
                start_date,
                end_date)
        count = "receivedate"
        url = "{}?search={}&count={}".format(base, search, count)
        data = get_json(url)
        if data:
            my_drug_dict["data"] = data
            my_data_dict['final'].append(my_drug_dict)
    return my_data_dict


def retreive_drug_names(count=None):
    if count:
        my_count = count
    else:
        my_count = 20

    base = "https://api.fda.gov/drug/event.json"
    search = ""
    pcount = "medicinalproduct"

    url = "{}?search={}&count={}&limit={}".format(base, search, pcount, my_count)

    print(url)
    data = get_json(url)
    return data


def retrieve_mentioned_event_twitter(drug_name, start_date=None, end_date=None, limit=None):
    points = []
    events = DataRecord.objects.filter(data_src__iexact="twitter")
    if limit:
        mylimit = int(limit)
    else:
        mylimit = 10

    if events and len(events) > 0:
        if drug_name:
            events = events.filter(raw_data__icontains=drug_name)
        if start_date:
            sdate = datetime.datetime.strptime(start_date, '%Y%m%d')
            events = events.filter(submitted_date__gte=sdate)
        if end_date:
            edate = datetime.datetime.strptime(end_date, '%Y%m%d')
            events = events.filter(submitted_date__lte=edate)

        if len(events) > 0:
            pre_date = events[0].submitted_date
            mycount = 0
            index = 0
            for event in events:
                if index >= 1 and event.submitted_date > pre_date:
                    point = DataPoint(filed_date=pre_date, drug_name=drug_name, count=mycount)
                    points.append(point)
                    mycount = 1
                    pre_date = event.submitted_date
                elif index == (len(events) - 1):
                    point = DataPoint(filed_date=event.submitted_date, drug_name=drug_name, count=mycount + 1)
                    points.append(point)
                else:
                    mycount = mycount + 1
                index = index + 1

        if len(points) > mylimit:
            points = points[:mylimit]
    return points

def retrieve_latest_tweets(limit=None):
     events = DataRecord.objects.filter(data_src__iexact="twitter")
     if limit:
         events = events[:limit]
     return events

