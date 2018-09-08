from flask import render_template,request,flash,redirect,url_for
from . import main
from flask_login import login_required,current_user
from app.models import User,Pitch
from datetime import datetime
from app import db
from .forms import PostForm

@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@main.route('/')
# @login_required
def index():

    title = 'Welcome to woo'
    posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }
    ]

    return render_template('index.html', title= title,posts=posts)



@main.route('/index', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Pitch(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('main.index'))

    posts = current_user.followed_posts().all()

    return render_template("posts.html", title='Home Page', form=form,
                           posts=posts)



@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))
# @login_required
# def post():
#     form = PostForm()
#     if form.validate_on_submit():
#         pitches = Pitch(body=form.post.data, author=current_user)
#         db.session.add(post)
#         db.session.commit()
#         flash(_('Your post is now live!'))
#         return redirect(url_for('index'))
#     page = request.args.get('page', 1, type=int)
#     pitches = current_user.followed_pitches().paginate(
#         page, app.config['POSTS_PER_PAGE'], False)
#     next_url = url_for('index', page=pitches.next_num) \
#         if pitches.has_next else None
#     prev_url = url_for('index', page=pitches.prev_num) \
#         if pitches.has_prev else None
#     return render_template('index.html', title=_('Home'), form=form,
#                            pitches=pitches.items, next_url=next_url,
#                            prev_url=prev_url)

# @main.route('/user/<username>')
# @login_required
# def user_profile(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     posts = [
#         {
#             'author':user, 'body':'test Post#1'
#         }
#     ]
#     return render_template('profile/user_profile.html',posts=posts, user=user)
#     '''
#     i have used a variant of first() called fist_or_404()
#     which works exactly like first() when there are results, and in case there 
#     are no results it auto sends a 404 error back
#     '''




