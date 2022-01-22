from .book import AuthorListResource


def register_api(app):
    app.add_url_rule('/author', view_func=AuthorListResource.as_view('author'))

