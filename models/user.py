from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


class User:
    def __init__(self, name, password):
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)