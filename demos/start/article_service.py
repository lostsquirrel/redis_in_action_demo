# coding=UTF-8

# import redis
# from datetime import time
import time

ONE_DAY_IN_SECONDS = 86400
ONE_WEEK_IN_SECONDS = 7 * ONE_DAY_IN_SECONDS
VOTE_LIMIT_PER_DAY = 200  # 前一天有200票，才能与后一个新贴有相同权限
VOTE_SCORE = 86400 / VOTE_LIMIT_PER_DAY
ARTICLES_PER_PAGE = 25


def article_vote(conn, user, article):
    """
     对文章评价, 只能平价一周内发布的文章
    :param conn:
    :param user:
    :param article:
    :return:
    """
    cutoff = time.time() - ONE_WEEK_IN_SECONDS
    if conn.zscore('time:', article) < cutoff:
        return -1

    article_id = article.partition(':')[-1]

    if conn.sadd('voted:' + article_id, user):
        conn.zincrby('score:', article, VOTE_SCORE)
        return conn.hincrby(article, 'votes', 1)
    else:
        return -2


def post_article(conn, user, title, link):
    """
    发布文章
    :param conn:
    :param user:
    :param title:
    :param link:
    :return:
    """
    article_id = str(conn.incr('article:'))

    voted = 'voted:' + article_id
    conn.sadd(voted, user)
    conn.expire(voted, ONE_WEEK_IN_SECONDS)

    now = time.time()
    article = 'article:' + article_id
    link = r'#' + article_id
    conn.hmset(article, {
        'title': title,
        'link': link,
        'poster': user,
        'time': now,
        'votes': 1,
    })
    conn.zadd('score:', article, now + VOTE_SCORE)
    conn.zadd('time:', article, now)

    return article_id


def get_articles(conn, page, order='score:'):
    """
    获取文章列表（分页）
    :param conn:
    :param page:
    :param order:
    :return:
    """
    start = (page - 1) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE - 1

    ids = conn.zrevrange(order, start, end)
    articles = []
    for article_id in ids:
        article_data = conn.hgetall(article_id)
        article_data['id'] = article_id
        articles.append(article_data)

    return articles


def add_groups(conn, article_id, to_add=()):
    """
    添加文章分组
    :param conn:
    :param article_id:
    :param to_add:
    """
    article = 'article:' + article_id
    for group in to_add:
        conn.sadd('group:' + group.strip(), article)


def remove_groups(conn, article_id, to_remove=()):
    """
    从分组中删除文章
    :type to_remove: list
    :param conn:
    :param article_id:
    :param to_remove:
    """
    article = 'article:' + article_id
    for group in to_remove:
        conn.srem('group:' + group.strip(), article)


def get_group_articles(conn, group, page, order='score:'):
    """
    获取指定分组文章
    :param conn:
    :param group:
    :param page:
    :param order:
    :return:
    """
    key = order + group
    if not conn.exists(key):
        conn.zinterstore(key,
                         ['group:' + group, order],
                         aggregate='max',
                         )
        conn.expire(key, 60)
    return get_articles(conn, page, key)


def get_groups(conn):
    return conn.keys('group:*')


'''
Exercise: Down-voting
In our example, we only counted people who voted positively for an article. But on
many sites, negative votes can offer useful feedback to everyone. Can you think of a
way of adding down-voting support to article_vote() and post_article()? If possible,
try to allow users to switch their votes. Hint: if you’re stuck on vote switching,
check out SMOVE, which I introduce briefly in chapter 3.
'''