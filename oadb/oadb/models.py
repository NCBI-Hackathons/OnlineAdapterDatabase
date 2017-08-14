from django.db import models
from django.contrib.auth.models import AbstractUser


class Test(models.Model):
	field1 = models.CharField(max_length=100)
	field2 = models.CharField(max_length=100)
	field3 = models.CharField(max_length=100)

class User(AbstractUser):
	un = models.CharField(max_length=150)
	login_type = models.CharField(max_length=25)
	affiliation = models.CharField(max_length=150)
	website = models.CharField(max_length=150)
	is_staff = models.BooleanField(default=False)
	
class Kit(models.Model):
	vendor = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	version = models.CharField(max_length=100)
	model = models.CharField(max_length=100)
	user = models.ForeignKey('User')

class Adaptor(models.Model):
	expression = models.CharField(max_length=100)
	kit = models.ForeignKey('Kit')

class Database(models.Model):
	name = models.CharField(max_length=100)
	template_url = models.CharField(max_length=250)
	url = models.CharField(max_length=250)

class Run(models.Model):
	accession = models.ForeignKey('Adaptor')
	is_public = models.BooleanField(default=True)
	database = models.ForeignKey(Database)
	sequencing_instrument = models.CharField(max_length=50)


