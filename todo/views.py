from django.shortcuts import render

import uuid
from django.http import HttpResponse
import traceback
import simplejson
from todo.models import SysUser
from todo.models import Item
import logging

logger = logging.getLogger('todo')
# Create your views here.


def create_user(request):
    try:
        if request.method == 'POST':
            request_params = request.POST
            email_id = request_params.get('email_id')
            id = uuid.uuid4().hex
            user = SysUser(id = id, email_id = email_id)
            user.save()
            logger.error("error in creating user %s" %str(traceback.format_exc()))
            responseString = {'meta': { 'message': { 'title': 'Ok' , 'subtitle': 'ok' },'code': 200 },'response' : {}}
            return HttpResponse(simplejson.dumps(responseString))
        else:
            responseString = {'meta': { 'message': { 'title': 'Error in creating user.' , 'subtitle': 'Please try later' },'code': 400 },'response' : {}}
            return HttpResponse(simplejson.dumps({}))
    except:
            logger.error("error in creating user %s" %str(traceback.format_exc()))
            responseString = {'meta': { 'message': { 'title': 'Error in creating user.' , 'subtitle': 'Please try later' },'code': 400 },'response' : {}}
            return HttpResponse(simplejson.dumps(responseString))
                    



def get_all_items(request):
    if request.method == 'GET':
        request_params = request.POST
        email_id = request.GET.get('email_id')
        creator = SysUser.objects.get(email_id = email_id)
        response = Item.objects.get_all_active_items(creator)
        responseString = {'meta': { 'message': { 'title': 'Ok' , 'subtitle': 'ok' },'code': 200 },'response' : response}
        return HttpResponse(simplejson.dumps(responseString))
                

    
def create_items(request):
    try:
        if request.method == 'POST':
            request_params = request.POST
            email_id = request_params.get('email_id')
            title = request_params.get('title')
            creator = SysUser.objects.get(email_id = email_id)
            obj  = Item.objects.create_item(creator,title,'H',3)
            if obj:
                responseString = {'meta': { 'message': { 'title': 'Ok' , 'subtitle': 'ok' },'code': 200 },'response' : {}}
                return HttpResponse(simplejson.dumps(responseString))
            responseString = {'meta': { 'message': { 'title': 'Error in creating user.' , 'subtitle': 'Please try later' },'code': 400 },'response' : {}}
            return HttpResponse(simplejson.dumps(responseString))
    except:
            logger.error("error in creating user %s" %str(traceback.format_exc()))
            responseString = {'meta': { 'message': { 'title': 'Error in creating user.' , 'subtitle': 'Please try later' },'code': 400 },'response' : {}}
            return HttpResponse(simplejson.dumps(responseString))
                    

