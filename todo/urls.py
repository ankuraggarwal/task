from django.conf.urls import patterns, url


urlpatterns = patterns('todo.views', 
    url(r'^getall/', 'get_all_items'),
    url(r'^create/','create_items'),
    url(r'^cuser/','create_user'),
    
    
)