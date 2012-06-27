from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from csvdialer import forms
from django.conf import settings
import StringIO
import csv
import random
import hashlib
import time
import telapi
import base64
import logging
# Create your views here.
ACCOUNT_SID = settings.ACCOUNT_SID
ACCOUNT_TOKEN = settings.ACCOUNT_TOKEN
# Create your views here.
from telapi import rest
import threading
import Queue


call_queue = Queue.Queue()


class CallerThread(threading.Thread):
    def __init__(self, queue):
        super(CallerThread, self).__init__()
        self.queue = queue
        self.daemon = True
        self.finished = threading.Event()
        self.client = rest.Client(ACCOUNT_SID, ACCOUNT_TOKEN)
        self.account = self.client.accounts[self.client.account_sid]

    def run(self):
        while not self.finished.is_set():
            work = self.queue.get()
            from_number, to_number, url = work
            list(self.account.calls)
            self.account.calls.create(from_number=from_number,
                                      to_number=to_number,
                                      url=url)
            logging.error("Called %s, from %s, url: %s", to_number, from_number, url)
            time.sleep(1)

ct = CallerThread(call_queue)
ct.start()

def robocall(request):
    if request.method == 'POST':
        form = forms.RobocallerForm(request.POST, request.FILES)
        print form.is_valid()
        print form.errors
        if form.is_valid():
            sio = StringIO.StringIO(request.FILES['numbers_to_call'].read())
            url = form.cleaned_data['message']
            encoded_url = settings.CALLBACK_BASE_URL + '/csvdialer/telml/%s/'
            encoded_url = encoded_url % base64.encodestring(url).strip()
            for row in csv.reader(sio, delimiter=',', quotechar='"'):
                from_number, to_number = row[:2]
                print from_number, to_number, row[:2]
                call_queue.put((from_number, to_number, encoded_url))
            return HttpResponse('Ok')
    form = forms.RobocallerForm()
    return render_to_response('csvdialer/robocall.html',
                              {'form': form},
                              context_instance=RequestContext(request))


@csrf_exempt
def telml_call(request, encoded_url):
    url = base64.decodestring(encoded_url)
    msg = '<Response><Play>%s</Play></Response>' % url
    return HttpResponse(msg, 'application/xml')

