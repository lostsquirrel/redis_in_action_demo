# coding=UTF-8
from datetime import time


def check_token(conn, token):
    """
    根据token 获取用户信息
    :param conn:
    :param token:
    :return:
    """
    return conn.hget('login:', token)


def update_token(conn, token, user, item=None):
    """
    更新token, 添加最近访问记录，并保持不超过25条
    :param conn:
    :param token:
    :param user:
    :param item:
    """
    timestamp = time.time()
    conn.hset('login:', token, user)
    conn.zadd('recent:', token, timestamp)
    if item:
        conn.zadd('viewed:' + token, item, timestamp)
        conn.zremrangebyrank('viewed:' + token, 0, -26)


def clean_sessions(conn):
    """
    保留最近1 000 000 条访问记录， 如果多，每次删除100个
    :param conn:
    """
    while not QUIT:
        size = conn.zcard('recent:')
        if size <= LIMIT:
            time.sleep(1)
            continue
        end_index = min(size - LIMIT, 100)
        tokens = conn.zrange('recent:', 0, end_index-1)
        session_keys = []
        for token in tokens:
            session_keys.append('viewed:' + token)

        conn.delete(*session_keys)
        conn.hdel('login:', *tokens)
        conn.zrem('recent:', *tokens)