from app.util.dao import MysqlDao

ACTIVE_GROUP = {}
with MysqlDao() as db:
    res = db.query('SELECT group_id, permission FROM `group` WHERE active=1')
for (gid, permit) in res:
    ACTIVE_GROUP.update({
        int(gid): str(permit).split(',')
    })

ACTIVE_USER = {}
with MysqlDao() as db:
    res = db.query('SELECT qq,permission FROM user WHERE active=1')
for (qid, permit) in res:
    ACTIVE_USER.update({
        int(qid): str(permit).split(',')
    })

ADMIN_USER = []
with MysqlDao() as db:
    res = db.query('SELECT qq FROM user WHERE admin=1')
for (qid,) in res:
    ADMIN_USER.append(int(qid))

LISTEN_MC_SERVER = []
with MysqlDao() as db:
    res = db.query('SELECT ip,port,report,delay FROM mc_server WHERE listen=1')
for (ip, port, report, delay) in res:
    LISTEN_MC_SERVER.append(
        [[ip, int(port)], [i for i in str(report).split(',')], delay]
    )
