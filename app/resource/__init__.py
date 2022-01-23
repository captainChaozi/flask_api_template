from .book import AuthorListResource


def register_api(api):
    api.add_resource(AuthorListResource, '/author')
