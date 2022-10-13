from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .forms import *
from pusher import Pusher
import json
#instantiate pusher
pusher = Pusher(app_id=u'1486009', key=u'fcfbccb5f3c92f233684', secret=u'f81a015eeb00988429e6', cluster=u'ap2')
# Create your views here.
# function that serves the welcome page
def index(request):
    # get all current photos ordered by the latest
    channel_subscriber = pusher.channel_info(u'presence-chatroom', [u"subscription_count"])["subscription_count"]
    channel_user = pusher.channel_info(u'presence-chatroom', [u"user_count"])['user_count']
    print(channel_subscriber, channel_user)
    all_documents = Feed.objects.all().order_by('-id')
    # return the index.html template, passing in all the feeds
    return render(request, 'feed/index.html', {'all_documents': all_documents, 'users' : channel_user + 1, 'subscriber': channel_subscriber + 1})
#function that authenticates the private channel 
def pusher_authentication(request):
    channel = request.GET.get('channel_name', None)
    socket_id = request.GET.get('socket_id', None)
    auth = pusher.authenticate(
      channel = channel,
      socket_id = socket_id
    )
    return JsonResponse(json.dumps(auth), safe=False)
#function that triggers the pusher request
def push_feed(request):
    # check if the method is post
    if request.method == 'POST':
        # try form validation
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save()
            # trigger a pusher request after saving the new feed element 
            pusher.trigger(u'a_channel', u'an_event', {u'description': f.description, u'document': f.document.url})
            return HttpResponse('ok')
        else:
            # return a form not valid error
            return HttpResponse('form not valid')
    else:
       # return error, type isnt post
       return HttpResponse('error, please try again')