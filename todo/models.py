from django.db import models
import uuid

import pytz
from datetime import datetime, timedelta

import traceback

from task import settings
import logging

logger = logging.getLogger('todo')

CATEGORY_REVERSE = dict((x, y) for x, y in settings.CATEGORY)

STATUS_CHOICES_REVERSE_DICT = dict((x, y) for x, y in settings.STATUS)

class SysUserManager(models.Manager):
    pass

class SysUser(models.Model):

    id = models.CharField(max_length=50,null=False,primary_key=True, verbose_name="primary key") 

    email_id = models.CharField(max_length = 150)
    
    is_active = models.BooleanField(default=True)

    objects = SysUserManager()


class ItemManager(models.Manager):

    def create_item(self,user,title, category,priority):
        try:
            itemObj = Item(id = uuid.uuid4().hex ,\
                title = title ,\
                start_time = datetime.now(pytz.utc) ,\
                due_time = datetime.now(pytz.utc) + timedelta(days = 5) ,\
                creator = user ,\
                category = category ,\
                priority = priority ,\
                    )
            itemObj.save()
            return itemObj
        except:
            logger.error("error %s " %str(traceback.format_exc()))
            return None


    
    def get_all_active_items(self,user):

        try:
            item_list = Item.objects.filter(creator = user)
            items = []
            for item in item_list:
                item_dict = {}
                item_dict['title'] = item.title
                item_dict['date_created'] = item.date_created.strftime("%Y-%m-%dT%H:%M:%SZ")
                item_dict['start_time'] = item.start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                item_dict['due_time'] = item.due_time.strftime("%Y-%m-%dT%H:%M:%SZ")
                item_dict['status'] = STATUS_CHOICES_REVERSE_DICT.get(item.status)
                item_dict['category'] = CATEGORY_REVERSE.get(item.category)
                item_dict['priority'] = item.priority
                items.append(item_dict)




            return items
        except:
            logger.error("error in getting active items %s" %str(traceback.format_exc()))
            return None

    def set_item_as_done(self,item_id):
        try:
            item = Item.object.filter(id  = item_id).update(status = 'C', complete_time = datetime.now(pytz.utc))
            return True
        except:
            logger.error(" error item_id %s" %str(item_id))
            return False

    def get_all_completed_itmes(self,user):

        try:
            item_list = Item.objects.filter(creator = user, status = 'C')
            return item_list
        except:
            logger.error("error in getting active items %s" %str(traceback.format_exc()))
            return None




class Item(models.Model):

    id = models.CharField(max_length=50,null=False,primary_key=True, verbose_name="primary key") 

    title = models.CharField(max_length = 150)
    
    date_created = models.DateTimeField(auto_now_add = True , null=False)
    
    start_time = models.DateTimeField()
    
    due_time = models.DateTimeField(null=False)
    
    complete_time = models.DateTimeField(blank=True,null=True)
    
    creator = models.ForeignKey(SysUser, related_name='creator')
    
    STATUS = (   ('W','NOT YET STARTED'),\
                 ('A', 'ACTIVE'),\
                 ('C', 'COMPLETED'),\
                 ('R','ARCHIEVED'),\
                );
    status = models.CharField(max_length = 1,default = 'A',choices = STATUS)


    CATEGORY = ( ('H', 'Home'),\
                 ('F', 'Office'),\
                 ('O','Others'),\
                );
    category = models.CharField(max_length = 1, default = 'H',choices = CATEGORY)
    
    PRIORITY = ( (1, 'Low'),\
                 (2, 'Normal'),\
                 (3, 'High'),\
                );

    priority = models.IntegerField(max_length=1,choices = PRIORITY)


    objects = ItemManager()

    def __unicode__(self):
        return self.title 





   

    