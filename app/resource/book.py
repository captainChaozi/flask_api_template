from app.model import Author
from app.schema.schema import AuthorSchema
from ext import ListResource

class AuthorListResource(ListResource):
    Model = Author
    Schema = AuthorSchema

    def get(self, parent_id=None):

        self.logger.info('这是日志')

        return None