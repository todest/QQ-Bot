from app.util.dao import MysqlDao


class BotUser:
    def __init__(self, qq, point=0, active=0, admin=0):
        self.qq = qq
        self.point = point
        self.active = active
        self.admin = admin
        self.user_register()

    def user_register(self):
        """注册用户"""
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM user WHERE qq=%s",
                [self.qq]
            )
            if not res[0][0]:
                res = db.update(
                    "INSERT INTO user (qq, points, active, admin) VALUES (%s, %s, %s, %s)",
                    [self.qq, self.point, self.active, self.admin]
                )
                if not res:
                    raise Exception()

    def sign_in(self):
        """签到"""
        with MysqlDao() as db:
            res = db.update(
                "UPDATE user SET points=points+%s, last_login=CURDATE() WHERE qq=%s",
                [self.point, self.qq]
            )
            if not res:
                raise Exception()

    def update_point(self, point):
        """修改积分
        :param point: str, 积分变动值
        """
        with MysqlDao() as db:
            res = db.update(
                "UPDATE user SET points=points+%s WHERE qq=%s",
                [point, self.qq]
            )
            if not res:
                raise Exception()

    def get_sign_in_status(self) -> bool:
        """查询签到状态"""
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM user WHERE qq=%s AND last_login=CURDATE()",
                [self.qq]
            )
            return res[0][0]

    def get_points(self) -> bool:
        """查询积分"""
        with MysqlDao() as db:
            res = db.query(
                "SELECT points FROM user WHERE qq=%s",
                [self.qq]
            )
            return res[0][0]

    def kick(self, src, dst, point, num) -> bool:
        """踢

            :param src: 来源QQ
            :param dst: 目标QQ
            :param point: 掉落积分
            :param num: 每天最多次数
        """
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM kick WHERE src=%s AND dst=%s AND TO_DAYS(time)=TO_DAYS(now())",
                [src, dst]
            )
            if not res[0][0] < num:
                return False
            self.update_point(point)
            res = db.update(
                "INSERT INTO kick (src, dst, time, point) VALUES (%s, %s, NOW(), %s)",
                [src, dst, -point]
            )
            if not res:
                raise Exception()
        return True

    def steal(self, src, dst, point, num) -> bool:
        """偷对方积分

            :param src: 来源QQ
            :param dst: 目标QQ
            :param point: 偷取积分
            :param num: 每天最多次数
        """
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM steal WHERE src=%s AND dst=%s AND TO_DAYS(time)=TO_DAYS(now())",
                [src, dst]
            )
            if not res[0][0] < num:
                return False
            self.update_point(point)
            res = db.update(
                "INSERT INTO steal (src, dst, time, point) VALUES (%s, %s, NOW(), %s)",
                [src, dst, point]
            )
            if not res:
                raise Exception()
        return True

    def bomb(self, src, dst, point, num) -> bool:
        """炸

            :param src: 来源QQ
            :param dst: 目标QQ
            :param point: 掉落积分
            :param num: 每天最多次数
        """
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM bomb WHERE src=%s AND dst=%s AND TO_DAYS(time)=TO_DAYS(now())",
                [src, dst]
            )
            if not res[0][0] < num:
                return False
            self.update_point(point)
            res = db.update(
                "INSERT INTO bomb (src, dst, time, point) VALUES (%s, %s, NOW(), %s)",
                [src, dst, point]
            )
            if not res:
                raise Exception()
        return True

    def get_moving_bricks_status(self) -> bool:
        """查询搬砖状态"""
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM user WHERE qq=%s AND last_moving_bricks=CURDATE()",
                [self.qq]
            )
            return res[0][0]

    def moving_bricks(self):
        """搬砖"""
        with MysqlDao() as db:
            res = db.update(
                "UPDATE user SET points=points+%s, last_moving_bricks=CURDATE() WHERE qq=%s",
                [self.point, self.qq]
            )
            if not res:
                raise Exception()

    def get_work_status(self) -> bool:
        """查询打工状态"""
        with MysqlDao() as db:
            res = db.query(
                "SELECT COUNT(*) FROM user WHERE qq=%s AND last_part_time_job=CURDATE()",
                [self.qq]
            )
            return res[0][0]

    def work(self):
        """打工"""
        with MysqlDao() as db:
            res = db.update(
                "UPDATE user SET points=points+%s, last_part_time_job=CURDATE() WHERE qq=%s",
                [self.point, self.qq]
            )
            if not res:
                raise Exception()
