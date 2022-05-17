import inspect
import sys

from flask_restful import Api

from app.ext_init import docs
from ext import BaseResource


def collect_resource():
    resources = []
    for _, resource in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(resource, BaseResource) and resource != BaseResource:
            resources.append(resource)
    sort = {'ListResource': 1,
            'DetailResource': 2,
            'BaseResource': 3
            }
    resources.sort(key=lambda obj: sort[obj.__base__.__name__])
    return resources


RESOURCE = collect_resource()


class APIDOCSResource(BaseResource):
    uri = '/apidocs.json'

    @staticmethod
    def get():
        return docs.to_dict()


def api_register(api: Api):
    for resource in RESOURCE:
        if resource.docs:
            resource.create_docs()
        api.add_resource(resource, resource.uri)
    api.add_resource(APIDOCSResource, APIDOCSResource.uri)
