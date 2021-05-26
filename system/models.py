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
    email = models.EmailField(max_length=200, default='example@example.com')
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
        parents = Parent.objects.all()
        for i in parents:
            email_subject = 'hi, ' + str(i.name)
            email_body = f"""There is new vaccine avalible, 
name: {self.name}
This vaccination combats: {self.vaccine_for} disease
child age from: {self.child_age_from}
child age to: {self.child_age_to}
visit our app for more information,
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
    vaccine = models.ManyToManyField(Vaccine)