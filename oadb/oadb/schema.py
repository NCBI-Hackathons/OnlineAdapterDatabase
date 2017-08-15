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


class Query(ObjectType):
    user = Node.Field(UserNode)
    all_users = DjangoConnectionField(UserNode)

    kit = Node.Field(KitNode)
    all_kits = DjangoConnectionField(KitNode)

    adaptor = Node.Field(AdaptorNode)
    all_adaptors = DjangoConnectionField(AdaptorNode)


schema = Schema(query=Query)
