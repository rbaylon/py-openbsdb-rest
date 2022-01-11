from views import app
from werkzeug.security import check_password_hash, generate_password_hash
from controllers import UserController, InterfaceController
from forms import LoginForm, UsersForm, UsersFormEdit, UsersFormPassword
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from flask import render_template, request, redirect, url_for, abort, session


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    uc = UserController()
    return uc.getuser(uid=int(user_id))


@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route("/users/<int:page_num>")
@login_required
def users(page_num):
    if not current_user.group == 'admin':
        abort(401)

    uc = UserController()
    users = uc.getusers()
    return render_template('users.html', username=current_user.username, users=users)


@app.route("/user/<int:user_id>", methods=["GET", "POST"])
@login_required
def user(user_id):
    if not current_user.is_authenticated:
        abort(401)

    form = UsersFormEdit()
    uc = UserController()
    user = uc.getuser(uid=user_id)
    if not user:
        abort(404)

    if current_user.group != 'admin':
        if current_user.username != user.username:
            abort(401)

    if form.validate_on_submit():
        user_data = {}
        if form.delete.data == 'Y':
            user_data['uid'] = user.id
            uc.deleteuser(user_data)
            return redirect(url_for('users', page_num=1))
        else:
            user_data['username'] = form.username.data
            user_data['uid'] = user.id
            user_data['group'] = form.group.data
            uc.edituser(user_data)
            return redirect(url_for('users', page_num=1))

    form.username.data = user.username
    form.group.data = user.group
    delete = request.args.get('delete', None)
    if delete:
        form.delete.data = 'Y'
    else:
        form.delete.data = 'N'

    return render_template('user.html', username=current_user.username, form=form, uid=user.id)


@app.route("/user/add", methods=["GET", "POST"])
@login_required
def adduser():
    if current_user.group != 'admin':
        abort(401)

    form = UsersForm()
    if form.validate_on_submit():
        uc = UserController()
        hashed_pw = generate_password_hash(form.password.data, method='pbkdf2:sha256:260000',salt_length=16)
        user_data = {'user': form.username.data, 'group': form.group.data, 'password': hashed_pw}
        uc.adduser(user_data)
        return redirect(url_for('users', page_num=1))

    return render_template('register.html', form=form)


@app.route("/resetpw", methods=["GET", "POST"])
@login_required
def reset():
    uid = request.args.get('uid', None)
    if current_user.group != 'admin':
        if current_user.id != int(uid):
            abort(401)

    form = UsersFormPassword()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data, method='pbkdf2:sha256:260000',salt_length=16)
        uc = UserController()
        user_data = {'uid': int(form.uid.data), 'password': hashed_pw}
        uc.edituser(user_data, updatepw=True)

        if current_user.id == int(uid):
            return redirect(url_for('logout'))
        else:
            return redirect(url_for('users', page_num=1))

    form.uid.data = uid
    return render_template('resetpw.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    msg = None
    form = LoginForm()
    remember = False
    nexturl = request.args.get('next', None)
    if form.validate_on_submit():
        uc = UserController()
        user = uc.getuser(username=form.username.data)
        if user:
            if check_password_hash(user.password, form.password.data):
                if form.remember.data:
                    remember = True

                login_user(user, remember=remember)
                if nexturl:
                    return redirect(nexturl)

                return redirect(url_for('home'))
        msg = "Invalid username or password!"

    return render_template('login.html', form=form, msg=msg, nexturl=nexturl)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

