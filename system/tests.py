from django.test import TestCase,Client
from django.test import SimpleTestCase
from django.urls import reverse,resolve
from .views import *
from .models import *
import json

# Create your tests here.
#URL testing
class TestUrls(SimpleTestCase):

    def test_parent_url_is_resolved(self):

        url = '/api/parent'
        print(resolve(url))
        self.assertEquals(resolve(url).func,parent_view)


    def test_save_url_is_resolved(self):
        url= '/api/save'
        print(resolve(url))
        self.assertEquals(resolve(url).func,save_data)

    def test_child_url_is_resolved(self):
        url= '/api/child'
        print(resolve(url))
        self.assertEquals(resolve(url).func,child_view)


    def test_mail_url_is_resolved(self):
        url= '/api/mail'
        print(resolve(url))
        self.assertEquals(resolve(url).func,child_vaccine_view)

    def test_seen_url_is_resolved(self):
        url= '/api/seen/1/1'
        print(resolve(url))
        self.assertEquals(resolve(url).func,seen_by_parent_view)


#Test views
class TestViews(TestCase):
    def setUp(self):

        self.client=Client()
        self.parent_url ='/api/parent'
        self.child_url  ='/api/child'
        Parent.objects.create(name="ahmad",
                           email="x3@x.com",
                           password="12345",
                           nationalid=12345678912343)






    def test_parent_view_POST_addsnewparent(self):



        response = self.client.post(self.parent_url,
                                    {"id":1
              ,"name":"ahmad","email":"x3@x.com",
          "password":"12345"
         ,"nationalid":"12345678912343",
          "response":"success"})

        self.assertEquals(response.status_code,200)
        self.assertEquals(Parent.objects.first().name,'ahmad')
        self.assertEquals(Parent.objects.first().nationalid,'12345678912343')


    def test_child_view_POST_addsnewchild(self):
        Child.objects.create(name='mohamed',
                         date_of_birth='2000-11-22',
                         parent =Parent.objects.first(),
                         nationalid=12345678912342)
        response = self.client.post(self.child_url,
                                    {"id":1
              ,"name":"mohamed","parent":"ahmad",
          "date_of_birth":"2000/11/22"
         ,"nationalid":"12345678912342",
          "response":"success"})



        self.assertEquals(response.status_code,200)
        self.assertEquals(Child.objects.first().parent.name,'ahmad')
        self.assertEquals(Child.objects.first().name,'mohamed')





    def test_parent_view_POST_nodata(self):

        response = self.client.post(self.parent_url)

        self.assertEquals(response.status_code,200)
        self.assertEquals(Parent.objects.count(),1)

