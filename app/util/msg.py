from app.util.dao import MysqlDao


def save(gid, mid, msg):
    with MysqlDao() as db:
        res = db.update(
            'INSERT INTO msg (group_id, member_id, content, time) VALUES (%s, %s, %s, NOW())',
            [gid, mid, msg]
        )
        if not res:
            raise Exception()


def repeated(qid, bid, num):
    with MysqlDao() as db:
        res = db.query(
            'SELECT content FROM msg WHERE group_id=%s ORDER BY id DESC LIMIT %s',
            [qid, num]
        )
        if len(res) != num:
            raise Exception()
        if res[0][0].startswith('[图片]'):
            return False
        for i in range(len(res) - 1):
            if res[i] != res[i + 1]:
                return False
        bot = db.query(
            'SELECT content FROM msg WHERE group_id=%s AND member_id=%s ORDER BY id DESC LIMIT %s',
            [qid, bid, 1]
        )
        if bot:
            if bot[0][0] == res[0][0]:
                return False
        return True
