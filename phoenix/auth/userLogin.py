from .. import db
from .models import Account
from flask_login import UserMixin


class UserLogin(UserMixin):
    def getUser(self, user_id):
        try:
            res = Account.query.filter_by(account_id=user_id).first()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except db.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def fromDB(self, user_id, db):
        self.__user = self.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user.account_id)