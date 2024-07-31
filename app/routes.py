from flask import Blueprint, abort, current_app, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app import db
from app.forms import AdminForm, DeleteForm, PostForm
from app.models import Post, User, slugify
import os

bp = Blueprint('routes', __name__)

@bp.route('/')
@bp.route('/home')
def home():
    query = request.args.get('q')
    if query:
        posts = Post.query.filter(Post.title.contains(query) | Post.body.contains(query)).order_by(Post.timestamp.desc()).all()
    else:
        posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('home.html', posts=posts)

@bp.route('/post/<slug>')
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    form = DeleteForm()
    return render_template('post_detail.html', post=post, form=form)

@bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!')
        return redirect(url_for('routes.home'))
    return render_template('post.html', form=form)

@bp.route('/post/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.slug = slugify(post.title)
        db.session.commit()
        flash('Post updated successfully!')
        return redirect(url_for('routes.post', slug=post.slug))
    elif request.method == 'GET':
        form.title.data = post.title
        form.body.data = post.body
    return render_template('post.html', form=form, post=post)

@bp.route('/post/<slug>/delete', methods=['POST'])
@login_required
def delete_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!')
    return redirect(url_for('routes.home'))

@bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if not current_user.is_admin:
        abort(403)
    form = AdminForm()
    if form.validate_on_submit():
        current_app.config['REGISTER_ENABLED'] = form.register_enabled.data
        flash('Settings updated successfully.')
        return redirect(url_for('routes.admin'))
    elif request.method == 'GET':
        form.register_enabled.data = current_app.config['REGISTER_ENABLED']
    users = User.query.all()
    return render_template('admin.html', form=form, users=users)

@bp.route('/promote/<int:user_id>', methods=['POST'])
@login_required
def promote_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    flash(f'Usuário {user.username} agora é administrador.')
    return redirect(url_for('routes.admin'))

@bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'Usuário {user.username} foi deletado.')
    return redirect(url_for('routes.admin'))
