from flaskr import app,conn,db,forms,mail
from flaskr.forms import RegisterForm, LoginForm, AddSavingsForm, TransferForm,AcceptForm,RecoverForm,PasswordChangeForm
from flask import render_template,abort,redirect,url_for,flash
from sqlalchemy.orm import aliased
from sqlalchemy import desc
from sqlalchemy.sql import func
from flaskr.models import User, Transactions
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
import datetime


session={}

def send_mail(user):
	token=user.get_token()
	msg=Message('Resetowanie hasła',recipients=[user.email],sender="raggioconivalli@gmail.com")
	msg.body=f'''
		Aby zresetować hasło naciśnij poniższy link:
		{url_for('reset_page',token=token,_external=True)}

		W przeciwnym razie zignoruj wiadomość

	'''
	mail.send(msg)
	print("Wyslalem wiadomosc")

@app.route('/index')
@app.route('/')
def home_page():
	return render_template('base.html')

@app.route('/login',methods=['GET','POST'])
def login_page():
	if current_user.is_authenticated:
		return redirect(url_for('home_page'))
	form=LoginForm()
	if form.validate_on_submit():
		requested_user=User.query.filter_by(login=form.login.data).first()
		if requested_user and requested_user.check_passw_correction(form.password.data):
			login_user(requested_user)
			flash('Udało Ci się zalogować na konto o nazwie: {}'.format(requested_user.login), category='success')
			return redirect(url_for('home_page'))
		else:
			flash('Logowanie nie powiodło się. Spróbuj ponownie',category='danger')
	if form.errors != {}:
		for err_msg in form.errors.values():
			flash('Logowanie nie powiodło się, powód: {}'.format(err_msg),category='danger')
	return render_template('login.html',form=form)

@app.route('/signUp',methods=['GET','POST'])
def signup_page():
	if current_user.is_authenticated:
		return redirect(url_for('home_page'))
	form=RegisterForm()
	if form.validate_on_submit():
		query=db.session.query(User.id).all()
		print(query)
		if query == []:
			max_id=0
		else:
			max_id=int(query[-1][0])
		new_acc_number=max_id+1
		acc_number=str(new_acc_number).zfill(8)
		user_to_create=User(account_number=acc_number,login=form.login.data,email=form.email.data,passw=form.password1.data,savings=0)
		db.session.add(user_to_create)
		db.session.commit()
		login_user(user_to_create)
		flash('Zakładanie konta ukończone powodzeniem, jesteś zalogowany jako:{}'.format(user_to_create.login), category='success')
		return redirect(url_for('home_page'))
	if form.errors != {}:
		for err_msg in form.errors.values():
			flash('Utworzenie użytkownika nie powiodło się, powód: {}'.format(err_msg),category='danger')
	return render_template('signup.html',form=form)

@app.route('/restore',methods=["GET", "POST"])
def restore_page():
	if current_user.is_authenticated:
		return redirect(url_for('home_page'))
	form = RecoverForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			send_mail(user)
		flash('Informacje o resetowaniu hasła zostały przesłane na wprowadzony adres e-mail',category='success')
		return redirect(url_for('home_page'))
	if form.errors != {}:
		for err_msg in form.errors.values():
			flash('Wysłanie wiadomości z odzyskaniem hasła nie powiodła się, powód: {}'.format(err_msg),category='danger')

	return render_template('restore.html',form=form)

@app.route('/logout')
@login_required
def logout_page():
	logout_user()
	flash("Pomyślnie wylogowano!",category="info")
	return redirect(url_for('home_page'))

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard_page():
	add=AddSavingsForm()
	transfer=TransferForm()
	transferHistoryTO=Transactions.query.filter_by(receiver_account_number=current_user.account_number).all()
	transferHistory=Transactions.query.filter_by(sender_account_number=current_user.account_number).all()
	transferHistoryFROM=[]
	for item in transferHistory:
		if item.receiver_account_number!=current_user.account_number:
			transferHistoryFROM.append(item)
	if add.validate_on_submit():
		if add.id.data == "add":
			user=User.query.filter_by(login=current_user.login).first()
			user.savings=user.savings+add.amount.data
			transaction=Transactions(sender_account_number=current_user.account_number,
				receiver_account_number=current_user.account_number,
				amount=add.amount.data,
				date=datetime.date.today(),
				title="Testowa funkcjonalność przelewu wewnętrznego")
			db.session.add(transaction)
			db.session.commit()
			return redirect(url_for('dashboard_page'))
		elif transfer.id.data == "transfer":
			session['receiver']=User.query.filter_by(account_number=transfer.account.data).first()
			session['amount']=transfer.amount.data
			session['date']=transfer.date.data
			session['title']=transfer.title.data
			if(session['receiver']==None):
				flash('Nie znaleziono podanego numeru konta',category='danger')
			elif(session['amount'] > current_user.savings or session['amount']<0):
				flash('Niewystarczające środki',category='danger')
			elif(session['date'] < datetime.date.today()):
				flash('Podano niepoprawną datę', category='danger')
			else:
				return redirect(url_for('accept_page'))
	return render_template('dashboard.html',addForm=add,transferForm=transfer,transactionsTO=transferHistoryTO,transactionsFROM=transferHistoryFROM)
	if transfer.errors != {}:
		for err_msg in trasnfer.errors.values():
			flash('Dokonanie przelewu nie powiodło się, powód: {}'.format(err_msg),category='danger')

@app.route('/accept',methods=['GET','POST'])
@login_required
def accept_page():
	accept=AcceptForm()
	if accept.validate_on_submit():
		sender=User.query.filter_by(account_number=current_user.account_number).first()
		receiver=User.query.filter_by(account_number=session['receiver'].account_number).first()
		sender.savings=sender.savings-int(session['amount'])
		receiver.savings=receiver.savings+int(session['amount'])
		transaction=Transactions(sender_account_number=current_user.account_number,
				receiver_account_number=receiver.account_number,
				amount=session['amount'],
				date=session['date'],
				title=session['title'])
		db.session.add(transaction)
		db.session.commit()
		return redirect(url_for('summary_page'))

	return render_template('accept.html',sender_account_number=current_user.account_number,
				receiver_account_number=session['receiver'].account_number,
				amount=session['amount'],
				date=session['date'],
				title=session['title'],
				acceptForm=accept)

@app.route('/summary')
@login_required
def summary_page():
	flash('Przelew przyjęty do realizacji',category='success')
	return render_template('summary.html',sender_account_number=current_user.account_number,
				receiver_account_number=session['receiver'].account_number,
				amount=session['amount'],
				date=session['date'],
				title=session['title'])

@app.route('/reset/<token>',methods=['GET','POST'])
def reset_page(token):
	if current_user.is_authenticated:
		return redirect(url_for('home_page'))
	user=User.verify_token(token)
	if user is None:
		flash('Niepoprawny link aktywujacy',category='danger')
		return redirect(url_for('home_page'))
	form=PasswordChangeForm()
	if form.validate_on_submit():
		user.passw=form.password1.data
		db.session.commit()
		flash('Hasło zostało zmienione, zaloguj się przy pomocy nowych danych: ',category='success')
		return redirect(url_for('login_page'))
	return render_template('reset.html',form=form)




