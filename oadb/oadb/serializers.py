from oadb.models import User, Adapter, Kit, Run, Database
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class AdapterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Adapter
        fields = (
            'id', 'barcode', 'universal_sequence', 'index_sequence',
            'full_sequence', 'index_type'
        )


class KitSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Kit
        fields = ('id', 'vendor', 'kit', 'subkit', 'version', 'status', 'user')


class DatabaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Database
        fields = ('name', 'template_url', 'url')


class RunSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Run
        fields = (
            'accession', 'is_public', 'is_inferred',
            'user', 'database', 'three_seq', 'five_seq'
        )
