from .models import User, Kit, Adapter, Database, Run
from graphene import ObjectType, Node, Schema
from graphene_django.fields import DjangoConnectionField
from graphene_django.types import DjangoObjectType


class UserNode(DjangoObjectType):

    class Meta:
        model = User
        interfaces = (Node,)


class KitNode(DjangoObjectType):

    class Meta:
        model = Kit
        interfaces = (Node,)


class AdapterNode(DjangoObjectType):

    class Meta:
        model = Adapter
        interfaces = (Node,)


class RunNode(DjangoObjectType):

    class Meta:
        model = Run
        interfaces = (Node,)


class DatabaseNode(DjangoObjectType):

    class Meta:
        model = Database
        interfaces = (Node,)


class Query(ObjectType):
    user = Node.Field(UserNode)
    all_users = DjangoConnectionField(UserNode)

    kit = Node.Field(KitNode)
    all_kits = DjangoConnectionField(KitNode)

    adapter = Node.Field(AdapterNode)
    all_adapters = DjangoConnectionField(AdapterNode)

    run = Node.Field(RunNode)
    all_runs = DjangoConnectionField(RunNode)

    database = Node.Field(DatabaseNode)
    all_databases = DjangoConnectionField(DatabaseNode)


schema = Schema(query=Query)
