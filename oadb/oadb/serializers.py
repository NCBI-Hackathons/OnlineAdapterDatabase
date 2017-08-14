from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class AdaptorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Adaptor
        fields = ('expression',)


class KitSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Kit
		fields = ('vendor', 'name', 'version', 'model', 'user')


class DatabaseSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Database
		fields = ('name', 'template_url', 'url')


class RunSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Run
		fields = ('accession', 'is_public', 'database')
