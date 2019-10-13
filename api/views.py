from django.shortcuts import render
from django.http import JsonResponse
from threading import Thread
from glob import glob
import os, importlib, time, requests, sys, json


def test(request):
    searchID = request.GET.get('id', '')
    searchTerm = request.GET.get('q', '')
    if not searchID or not searchTerm:
        return JsonResponse({'error': True}, status=400)
    t = Thread(target=process_data, args=(searchID, searchTerm))
    t.start()
    return JsonResponse({'accepted': True}, status=200)

def process_data(searchID, searchTerm):
    dir_path = "%s/%s" % (os.path.dirname(os.path.abspath(__file__)), 'inteal')
    sys.path.insert(0, dir_path)
    domain_file = "%s/inteal.py" % (dir_path)
    module_name = os.path.basename(os.path.splitext(domain_file)[0])
    inteal = importlib.import_module(module_name)
    output = inteal.main(searchTerm)
    output['id'] = searchID

    headers = {'content-type': 'application/json'}
    url = 'https://crawlr-api.herokuapp.com/search/result'

    requests.post(url, data=json.dumps(output), headers=headers)
