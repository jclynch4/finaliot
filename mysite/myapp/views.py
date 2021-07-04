from django.shortcuts import render
from myapp.models import Mode, State
from rest_framework import viewsets
from myapp.serial import ModeSerializer, StateSerializer
import requests
import json
import time
from subprocess import call

# Create your views here.


class ModeViewSet(viewsets.ModelViewSet):
    queryset = Mode.objects.all()
    serializer_class = ModeSerializer


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer


def home(request):
    out = ''
    currentmode = 'auto'
    currentstate = 'on'

    if 'on' in request.POST:
        values = {'name': 'on'}
        print("yo yo yo yo yo yo yo")
        r = requests.put('http://127.0.0.1:8000/state/6/', data=values, auth=('admin', 'admin'))
        result = r.text
        print("here is the result it's right here" + result)
        output = json.loads(result)
        out = output['name']

    if 'off' in request.POST:
        values = {'name': 'off'}
        r = requests.put('http://127.0.0.1:8000/state/6/', data=values, auth=('admin', 'admin'))
        result = r.text
        output = json.loads(result)
        out = output['name']

    if 'auto' in request.POST:
        values = {'name': 'auto'}
        r = requests.put('http://127.0.0.1:8000/mode/1/', data=values, auth=('admin', 'admin'))
        result = r.text
        output = json.loads(result)
        out = output['name']

    if 'manual' in request.POST:
        values = {'name': 'manual'}
        r = requests.put('http://127.0.0.1:8000/mode/1/', data=values, auth=('admin', 'admin'))
        result = r.text
        output = json.loads(result)
        out = output['name']

    r = requests.get('http://127.0.0.1:8000/mode/1/', auth=('admin', 'admin'))
    result = r.text
    output = json.loads(result)
    currentmode = output['name']

    r = requests.get('http://127.0.0.1:8000/state/6/', auth=('admin', 'admin'))
    result = r.text
    output = json.loads(result)
    currentstate = output['name']
    
    
    return render(request, 'home.html', {'r':out, 'currentmode':currentmode, 'currentstate':currentstate})

call(['python', 'myapp/controller.py'])
