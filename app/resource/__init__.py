from .book import AuthorListResource


def register_resource(app, docs):
    app.add_url_rule('/author', view_func=AuthorListResource.as_view('AuthorListResource'))
    docs.register(AuthorListResource, endpoint='AuthorListResource')
