# coding=UTF-8
from demos.config import conn


def test_hash_bulk():
    print conn.hmset('hash-key2', {'short': 'hello', 'long': 1000*'1'})
    print conn.hkeys('hash-key2')
    print conn.hexists('hash-key2', 'num')
    print conn.hincrby('hash-key2', 'num')
    print conn.hexists('hash-key2', 'num')

if __name__ == '__main__':
    test_hash_bulk()
