 # class UserListResource(ListResource):
#     name = "用户"
#     uri = '/user'
#     docs = docs
#     tag_group = "用户操作"
#
#     Model = User
#     Schema = AliUserSchema
#     PostSchema = AliUserPostSchema
#     ExcelSchema = UserExportSchema
#     Service = UserService
#     like_field = ('name',)
#
#     def post(self, parent_id=None):
#         return self.service.before_post(data=self.data)
#
#
# class UserDetailResource(DetailResource):
#     name = "用户"
#     uri = '/user/<string:resource_id>'
#     docs = docs
#     tag_group = "用户操作"
#
#     Model = User
#     Schema = AliUserSchema
#     PutSchema = AliUserPutSchema
#     Service = UserService
#     method_decorators = [auth]
#
#
# class UserRankView(BaseResource):
#     uri = '/user_rank'
#     name = "身价排名"
#     tag_group = "用户操作"
#
#     docs = docs
#
#     def get(self):
#         user_id = self.param.get('user_id')
#         # user = self.db_session.query(User).filter(User.id == user_id).first()
#         subquery = self.db_session.query(func.sum(ScoreLog.score).label('score'),
#                                          ScoreLog.user_id.label("user_id")).filter(ScoreLog.score > 0).group_by(
#             ScoreLog.user_id).subquery()
#         # rank = self.db_session.query(subquery.c.user_id).filter(subquery.c.score >= int(user.value / 1000)).count()
#         # if rank <= 6:
#         rank_list = self.db_session.query(subquery.c.user_id.label('user_id'),
#                                           subquery.c.score.label("score")
#                                           ).order_by(subquery.c.score.desc(),subquery.c.user_id).all()
#
#         id_list = [i.user_id for i in rank_list]
#         if user_id in id_list:
#             rank = id_list.index(user_id)+1
#         else:
#             rank = '-'
#
#         return {'rank': rank}
#
#     @classmethod
#     def create_docs(cls):
#         cls.docs.parameter('用户ID', _in='query', _type='string', require=True)
#         cls.docs.response(UserRankSchema.__name__)
#         cls.docs.get_opt("自己身价排名", tags=['身价排名'])
#         path = cls.docs.path(cls.uri)
#         cls.docs.create(path=path, tags=cls.name, tag_group=cls.tag_group)
#
