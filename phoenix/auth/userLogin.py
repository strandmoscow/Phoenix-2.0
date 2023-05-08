from .. import db
from .models import account

class UserLogin():
    def getUser(self, user_id):
        try:
            res = account.query.filter_by(account_id=user_id).first()
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

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.account_id)