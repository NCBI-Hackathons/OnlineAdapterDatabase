from .models import User, Kit, Adaptor, Database, Run
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


class AdaptorNode(DjangoObjectType):

    class Meta:
        model = Adaptor
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

    adaptor = Node.Field(AdaptorNode)
    all_adaptors = DjangoConnectionField(AdaptorNode)

    run = Node.Field(RunNode)
    all_runs = DjangoConnectionField(RunNode)

    database = Node.Field(DatabaseNode)
    all_databases = DjangoConnectionField(DatabaseNode)


schema = Schema(query=Query)
