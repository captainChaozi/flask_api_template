from app import Author
from app.schema.schema import AuthorSchema
from ext import ListResource

class AuthorListResource(ListResource):
    Model = Author
    Schema = AuthorSchema

    def get(self, parent_id=None):
        from task import delay_task
        delay_task.delay('你好')

        return None,204
