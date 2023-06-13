from .. import db
from ..registration.models import Account
from flask_login import UserMixin


class UserLogin(Account, UserMixin):

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

    def fromDB(self, user_id):
        self.__user = self.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        return str(self.__user.account_id)

    def get_roles(self):
        try:
            return {'is_manager': self.__user.account_manager_id,
                    'is_student': self.__user.account_student_id,
                    'is_parent': self.__user.account_parent_id,
                    'is_trainer': self.__user.account_trainer_id}
        except:
            return {'is_manager': None,
                    'is_student': None,
                    'is_parent': None,
                    'is_trainer': None}