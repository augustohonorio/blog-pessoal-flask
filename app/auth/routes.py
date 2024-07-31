from flask import abort, current_app, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.auth.forms import LoginForm, RegistrationForm, UpdatePasswordForm
from app.models import User
from app.auth import bp

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('auth.login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('routes.home'))
    else:
        form = LoginForm()
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes.home'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))
    if not current_app.config.get('REGISTER_ENABLED', True):
        flash('Registration is currently disabled.')
        return redirect(url_for('auth.login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        is_first_user = User.query.count() == 0
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        if is_first_user:
            user.is_admin = True
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        login_user(user)
        return redirect(url_for('routes.home'))
    return render_template('/auth/register.html', form=form)

@bp.route('/user/password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Invalid old password')
            return redirect(url_for('auth.update_password'))
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been updated.')
        return redirect(url_for('routes.home'))
    return render_template('auth/update_password.html', form=form)
    

@bp.route('/user/delete', methods=['POST'])
@login_required
def delete_account():
    user = User.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    flash('Your account has been deleted.')
    return redirect(url_for('routes.home'))

@bp.route('/admin/promote/<int:user_id>', methods=['POST'])
@login_required
def promote_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    flash(f'Usuário {user.username} agora é administrador.')
    return redirect(url_for('routes.admin'))

