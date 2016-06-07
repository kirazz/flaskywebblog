from . import main
from flask import render_template,url_for,session,redirect,abort,flash,\
    request,current_app
from datetime import datetime
from .forms import NameForm,EditProfiledForm,PostForm,CommentForm
from  flask.ext.login import login_required,current_user
from ..models import User,Post,Comment
from app import db

@main.route('/index',methods=['GET','POST'])
@main.route('/',methods=['GET','POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page,per_page=5,error_out=False)
    posts = pagination.items
    return render_template('index.html',form=form,posts=posts,
                           pagination=pagination)

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('user.html',user=user,posts=posts)

@main.route('/edit-profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfiledForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        try:
            db.session.add(current_user)
            flash('你的资料已更新')
            db.session.commit()
        except:
            db.session.rollback()
            raise
        return redirect(url_for('.user',username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',form=form)

@main.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('内容已更新')
        return redirect(url_for('.edit',id=post.id))
    form.body.data= post.body
    return render_template('edit_post.html',form=form)

@main.route('/remove/<int:id>')
@login_required
def post_remove(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author:
        abort(403)
    else:
        db.session.delete(post)
    return redirect(url_for('.index'))

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object())
        db.session.add(comment)
        flash('评论成功.')
        return redirect(url_for('.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) // \
            5 + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=5,error_out=False)
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)