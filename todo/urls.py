from django.conf.urls import patterns, url


urlpatterns = patterns('paymentprocessor.views', 
    url(r'^getall/', 'get_all_items'),
    url(r'^create/','create_items'),
)