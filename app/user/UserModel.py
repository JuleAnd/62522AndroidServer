from passlib.handlers.sha2_crypt import sha256_crypt
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired
from app import db_client
from config import __CONFIGURATIONS__

__author__ = 'jacobgilsaa'

__TOKEN_TTL__ = 86400


class User(db_client.Document):
    userid = db_client.StringField(required=True)
    email = db_client.EmailField(required=True)
    firstname = db_client.StringField(max_length=64, required=True)
    lastname = db_client.StringField(max_length=64, required=True)
    password = db_client.StringField(max_length=256, required=True)

    def set_password(self, password):
        hashed_password = sha256_crypt.encrypt(password)
        self.password = hashed_password

    def verify_password(self, password):
        return sha256_crypt.verify(password, self.password)

    def generate_token(self, exp= __TOKEN_TTL__):
        serializer = Serializer(__CONFIGURATIONS__['SECRET_KEY'], expires_in=exp)
        return serializer.dumps({'userid': self.userid})

    @staticmethod
    def verify_token(token):
        serializer = Serializer(__CONFIGURATIONS__['SECRET_KEY'])
        try:
            decoded_token = serializer.loads(token)
        except SignatureExpired:
            print("Expired?")
            return 401
        except BadSignature:
            print("Bad sig")
            return 401
        return decoded_token['userid']

    def get_profile(self):
        return {'userid': self.userid, 'email': self.email, 'firstname': self.firstname, 'lastname': self.lastname}

