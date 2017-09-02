from oadb.models import User, Adapter, AdapterKit, Kit, Run, Database
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'groups',)



class AdapterSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Adapter
        fields = (
            'id', 'barcode', 'universal_sequence', 'index_sequence',
            'full_sequence', 'index_type', 'user'
        )


class KitSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Kit
        fields = ('id', 'vendor', 'kit', 'subkit', 'version', 'status', 'user')


class KitAdapterSerializer(serializers.ModelSerializer):
    adapters = AdapterSerializer(many=True, required=False)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Kit
        fields = (
            'id', 'vendor', 'kit', 'subkit', 'version', 
            'status', 'user', 'adapters'
        )


class AdapterKitSerializer(serializers.ModelSerializer):
    kit = KitSerializer(many=False, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Adapter
        fields = (
            'id', 'barcode', 'index_type', 'index_sequence',
            'universal_sequence', 'full_sequence',
            'kit', 'user'
        )


class AdapterKitFlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdapterKit
        fields = (
            'id', 'barcode', 'index_type', 'index_sequence',
            'universal_sequence', 'full_sequence',
            'vendor', 'kit', 'subkit', 'version', 'status'
        )



class DatabaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Database
        fields = ('id', 'name', 'template_url', 'url')


class RunSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Run
        fields = (
            'id', 'accession', 'is_public', 'is_inferred', 'user', 'database', 
        )


class RunAdapterSerializer(serializers.ModelSerializer):
    three_prime = AdapterKitSerializer(many=False, read_only=True)
    five_prime = AdapterKitSerializer(many=False, read_only=True)

    class Meta:
        model = Run
        fields = (
            'id', 'accession', 'is_public', 'is_inferred', 'three_prime', 'five_prime', 'user',
        )
