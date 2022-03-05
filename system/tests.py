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
     #Create fake data and client and add app urls to vars
    def setUp(self):

        self.client=Client()
        self.parent_url ='/api/parent'
        self.child_url  ='/api/child'
        self.check_url  ='/api/mail'
        self.save_url   ='api/save'


        self.parent_object = Parent.objects.create(name="ahmad",
                           email="ahmad@gmail.com",
                           password="12345",
                           nationalid=12345678912343)

        Child.objects.create(name= "ehab",
                    parent= self.parent_object, nationalid="12345678912222", date_of_birth= "2019-02-02")


        Vaccine.objects.create(
            name="vaccine 1",
            vaccine_for="corona",
            child_age_from = 4,
            child_age_to = 9)


        print(" View Test passed")





    # check if data is correct and response is correct
    def test_parent_view_POST_addsnewparent(self):

        response = self.client.post(self.parent_url,
                                    {"name":"tarek","email":"tarek@gmail.com",
          "password":"12345"
         ,"nationalid":"12345678912345"})

        self.assertEquals(response.status_code,200)
        self.assertEquals(response.data.get("name"),'tarek')
        self.assertEquals(response.data.get("nationalid"),'12345678912345')
        self.assertEquals(response.data.get('response'), 'success')


    def test_child_view_POST_addsnewchild(self):

        response = self.client.post(self.child_url,
                                    {"name":"mohamed","parent":"ahmad@gmail.com",
                                    "password": "12345","date_of_birth":"2016-11-22"
         ,"nationalid":"12345678912342",
          })



        self.assertEquals(response.status_code,200)
        self.assertEquals(response.data.get('response'),'success')
        self.assertEquals(response.data.get('parent'),self.parent_object.id)
        self.assertEquals(response.data.get('name'),'mohamed')

    def test_child_vaccine_view_check(self):

        response = self.client.post(self.check_url,
                                    {"parent":"ahmad@gmail.com"})

        self.assertEqual(response.status_code,200)
        self.assertEquals(response.data.get('response'), 'succeeded')



    def test_parent_view_POST_nodata(self):

        response = self.client.post(self.parent_url)
        self.assertEquals(response.status_code,400)
        self.assertEquals(Parent.objects.count(),1)
        self.assertEquals(response.data.get('response'), 'error')


    def test_parent_seen_view_POST(self):

        response = self.client.get('/api/seen/1/1', {},parent=1,vaccine=1)


        self.assertEquals(response.status_code,200)
        self.assertEquals(response.data, {'Done!'})
