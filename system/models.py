from django.db import models
from django.core.mail import EmailMessage

# Create your models here.

class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)

class Parent(models.Model):
    name = models.CharField(max_length=50, default='')
    email = models.EmailField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class Vaccine(models.Model):
    name = models.CharField(max_length=50, default='')
    vaccine_for = models.CharField(max_length=100, default='', blank=True)
    child_age_from = IntegerRangeField(min_value=1 ,max_value=12)
    child_age_to = IntegerRangeField(min_value=1 ,max_value=12)
    additional_information = models.CharField(max_length=1000, default='', blank=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        name = self.name
        vaccine_for = self.vaccine_for
        child_age_from = self.child_age_from
        child_age_to = self.child_age_to
        additional_information = self.additional_information
        id = len(Vaccine.objects.all())+1
        parents = Parent.objects.all()
        for i in parents:
            email_subject = 'hi, ' + str(i.name)
            email_body = f"""There is new vaccine avalible, 
name: {name}
This vaccination combats: {vaccine_for} disease
child age from: {child_age_from}
child age to: {child_age_to}
additional information: {additional_information}

• Please click the link below to make us sure that you read this notification:
https://vaccination-system-software.herokuapp.com/api/seen/{i.id}/{id}

• visit our app for more information,
thanks.
"""
            to_account = [str(i.email)]
            email = EmailMessage(email_subject, email_body, to=to_account)
            email.send()
        super(Vaccine, self).save(*args, **kwargs)


class Child(models.Model):
    name = models.CharField(max_length=50, default='')
    date_of_birth = models.DateField()
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class ChildVaccine(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    vaccine = models.ManyToManyField(Vaccine, blank=True)
    done = models.BooleanField(default=False)

class SeenByParent(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)