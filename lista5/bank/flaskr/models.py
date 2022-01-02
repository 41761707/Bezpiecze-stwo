from flaskr import db, bcrypt,login_manager,app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model,UserMixin):
	__tablename__="User"
	id=db.Column(db.Integer(),primary_key=True)
	account_number=db.Column(db.String(8),nullable=False,unique=True)
	login=db.Column(db.String(20),nullable=False,unique=True)
	password=db.Column(db.String(80),nullable=False)
	email=db.Column(db.String(40),nullable=False,unique=True)
	savings=db.Column(db.Integer(),nullable=False)

	@property
	def pretty_savings(self):
		if(len(str(self.savings))) >3:
			pass 
			return "str({}[:-3]),str({}[-3:])".format(self.savings)
		else:
			return self.savings


	@property
	def passw(self):
		return self.passw

	@passw.setter
	def passw(self,plain_text_password):
		self.password=bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

	def check_passw_correction(self,attempted_password):
		return bcrypt.check_password_hash(self.password,attempted_password)

	def get_token(self):
		serial=Serializer(app.config['SECRET_KEY'],expires_in=360)
		return serial.dumps({'user_id':self.id}).decode('utf-8')

	@staticmethod
	def verify_token(token):
		serial=Serializer(app.config['SECRET_KEY'])
		try:
			user_id=serial.loads(token)['user_id']
		except:
			return None
		return User.query.get(int(user_id))


class Transactions(db.Model):
	__tablename__="Transactions"
	id=db.Column(db.Integer(),primary_key=True)
	sender_account_number=db.Column(db.String(8),nullable=False)
	receiver_account_number=db.Column(db.String(8),nullable=False)
	amount=db.Column(db.Integer(),nullable=False)
	date=db.Column(db.DateTime, default=datetime.datetime.utcnow,nullable=False)
	title=db.Column(db.String(100))