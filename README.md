# redis_in_action_demo
demos and exercise of book redis in action


## redis key 说明
    article: 自增序列，用作文章id string(integer)
    voted:(article_id) 用户投票记录 set
    score:  文章列表，以票数排序 sorted set
    time:  文章列表，以发布时间排序 sorted set
    (article_id) 文章详情, hash