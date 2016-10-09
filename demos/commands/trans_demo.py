# coding=UTF-8
import threading
import time
from demos.config import conn

TEST_ROUND = 3


def notrans():
    print conn.incr('notrans:')
    time.sleep(.1)
    conn.incr('notrans:', -1)


def test(key, callback):
    for x in range(TEST_ROUND):
        for i in xrange(3):
            threading.Thread(target=callback).start()
        time.sleep(.5)

    print conn.get(key)


def trans():
    pipeline = conn.pipeline()
    pipeline.incr('trans:')
    time.sleep(.1)
    pipeline.incr('trans:', -1)
    print pipeline.execute()[0]


if __name__ == '__main__':
    # test('notrans:', notrans)
    test('trans:', trans)