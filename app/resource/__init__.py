import inspect
import sys
from .book import AuthorListResource, BookListResource, AuthorDetailResource, BookDetailResource
from flask_restful import Api
from ext import BaseResource, MyAPISpec


def collect_resource():
    resources = []
    for _, resource in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(resource, BaseResource) and resource != BaseResource:
            resources.append(resource)
    return resources


RESOURCE = collect_resource()


class APIDOCSResource(BaseResource):
    uri = '/apidocs.json'

    def get(self, parent_id=None):
        return MyAPISpec().common_docs(RESOURCE)


def resource_register(api: Api):
    for resource in RESOURCE:
        api.add_resource(resource, resource.uri)
    api.add_resource(APIDOCSResource, APIDOCSResource.uri)
