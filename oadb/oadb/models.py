from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    un = models.CharField(max_length=150)
    login_type = models.CharField(max_length=25)
    affiliation = models.CharField(max_length=150)
    website = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)

    class Meta:
        ordering = ('username',)


class Kit(models.Model):
    # aka manufacturer
    vendor = models.CharField(max_length=100)
    kit = models.CharField(max_length=100)
    subkit = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    status = models.IntegerField(default=0)
    # user 1 (system) used for built-in kits
    user = models.ForeignKey('User')

    @property
    def name(self):
        return '%s %s %s %s' % (self.vendor, self.kit, self.subkit, self.version)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('kit', 'subkit', 'version',)
        ordering = ('vendor', 'kit', 'subkit',)


IDX_CHOICES = (
    ('i5', 'i5'),
    ('i7', 'i7'))


class Adapter(models.Model):
    universal_sequence = models.CharField(max_length=100)
    index_sequence = models.CharField(max_length=100)
    full_sequence = models.CharField(max_length=100)
    index_type = models.CharField(max_length=5, choices=IDX_CHOICES)
    barcode = models.CharField(max_length=100, default='')
    user = models.ForeignKey('User')
    kit = models.ForeignKey('Kit', related_name='adapters')

    def __str__(self):
        return self.barcode

    class Meta:
        db_table = 'oadb_adaptor'
        ordering = ('kit', 'barcode',)


class AdapterKit(models.Model):
    """
    Model for a view joining Adapter to Kit
    """
    universal_sequence = models.CharField(max_length=100)
    index_sequence = models.CharField(max_length=100)
    full_sequence = models.CharField(max_length=100)
    index_type = models.CharField(max_length=5, choices=IDX_CHOICES)
    barcode = models.CharField(max_length=100, default='')
    vendor = models.CharField(max_length=100)
    kit = models.CharField(max_length=100)
    subkit = models.CharField(max_length=100)
    version = models.CharField(max_length=100)
    status = models.IntegerField(default=0)

    @property
    def name(self):
        return '%s %s %s %s (%s)' % (self.vendor, self.kit, self.subkit, self.version, self.barcode)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'oadb_adapterkit'
        ordering = ('kit', 'subkit', 'version','barcode',)


class DatabaseManager(models.Manager):
    """
    Allow use of natural keys in fixture data
    """
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Database(models.Model):
    objects = DatabaseManager()
    name = models.CharField(max_length=100, unique=True)
    template_url = models.CharField(max_length=250)
    url = models.CharField(max_length=250)

    def natural_key(self):
        return (self.name,)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Run(models.Model):
    accession = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)
    is_inferred = models.BooleanField(default=True)
    database = models.ForeignKey(Database, null=True)
    user = models.ForeignKey(User, null=False)
    three_prime = models.ForeignKey('Adapter', null=True, related_name='three')
    five_prime = models.ForeignKey('Adapter', null=True, related_name='five')
    sequencing_instrument = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.accession

    class Meta:
        ordering = ('accession', 'user',)

