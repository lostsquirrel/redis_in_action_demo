# coding=UTF-8
import tornado
from tornado.escape import json_encode
from demos.start import article_service
from demos.config import conn


class ArticleHandler(tornado.web.RequestHandler):
    def get(self, article_id):
        page = int(self.get_argument('page', '1'))
        order = self.get_argument('order', 'score:')
        articles = article_service.get_articles(conn, page, order)
        self.add_header('content-type', 'application/json')
        self.write(json_encode(articles))

    def post(self, article_id):
        title = self.get_argument('title')
        article_id = article_service.post_article(conn, get_session(), title, '')
        self.add_header('content-type', 'application/json')
        self.write(json_encode({'article_id': article_id, 'msg': '添加成功'}))


class ArticleListHandler(tornado.web.RequestHandler):
    def get(self):
        page = int(self.get_argument('page', '1'))
        order = self.get_argument('order', 'score:')
        tag = self.get_argument('tag', None)
        # articles = list()
        if tag is None:
            articles = article_service.get_articles(conn, page, order)
        else:
            articles = article_service.get_group_articles(conn, tag, page, order)

        self.add_header('content-type', 'application/json')
        self.write(json_encode(articles))


class TagHandler(tornado.web.RequestHandler):
    def get(self):
        tags = article_service.get_groups(conn)
        self.write(json_encode(tags))

    def put(self):
        tags = self.get_argument('tags')
        article_id = self.get_argument('article_id')
        article_service.add_groups(conn, article_id, clean_tags(tags))

    def delete(self):
        tags = self.get_argument('tags')
        article_id = self.get_argument('article_id')
        article_service.remove_groups(conn, article_id, clean_tags(tags))


class VoteHandler(tornado.web.RequestHandler):
    def get(self, article_id):
        self.write("You requested the main page" + article_id)

    def post(self, article_id):
        vote_actions = {'up': 1, 'down': -1}
        vote_action = self.get_argument('vote_action', 'up')
        # vote_actions.index(vote_action)
        article_id = 'article:' + article_id
        result = article_service.article_vote(conn, get_session(), article_id)

        self.write(json_encode(dict(article_id=article_id.split(':')[-1], result=result)))


class UserHandler(tornado.web.RequestHandler):
    def post(self):
        user = self.get_argument('user')
        if len(user) > 0:
            conn.set("current_user:", user)

    def get(self):
        self.write(get_session())


def get_session():
    user = conn.get("current_user:")
    if user is None:
        user = 'admin'
    return user


def clean_tags(tags):
    return [x.strip() for x in tags.split(',')]
