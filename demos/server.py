# coding=UTF-8
import tornado.web
import tornado.ioloop
from demos.views import *


application = tornado.web.Application([
    (r"/blog", ArticleListHandler),
    (r"/blog/([0-9]+)", ArticleHandler),
    (r"/blog/vote/([0-9]+)", VoteHandler),
    (r"/blog/tag", TagHandler),
    (r"/blog/user", UserHandler),
])


if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()