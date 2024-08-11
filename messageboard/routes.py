from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from messageboard import app, db, bcrypt
from messageboard.model import User, Topic, Post, Comment
from datetime import datetime


# Index Page 
@app.route('/')
def index():
    return render_template('index.html')


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            session['username'] = username
            session['user_id'] = user.id
            session['user_is_admin'] = user.is_admin
            return redirect(url_for('home'))
        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template("login.html")

# Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_repeat = request.form.get('password-repeat')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists')
            return redirect(url_for('signup'))
        if password == password_repeat:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_password, date=datetime.utcnow())
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Passwords do not match')
            return redirect(url_for('signup'))
    return render_template('login.html')


# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# Home
@app.route('/home')
@login_required
def home():
    username = session.get('username', None)
    posts = list(Post.query.order_by(Post.date).all())
    return render_template('home.html', username=username, posts=posts)


# Topics
@app.route('/topics')
@login_required
def topics():
    username = session.get('username', None)
    topics = list(Topic.query.order_by(Topic.name).all())
    return render_template('topics.html', topics=topics, username=username)


@app.route('/create_topic', methods=['GET', 'POST'])
@login_required
def create_topic():
    username = session.get('username', None)
    user_id = session.get('user_id', None)

    if request.method == 'POST':
        current_time = datetime.now().strftime('%Y=%m-%d %H:%M:%S')
        topic = Topic(
            name=request.form.get('topic-title'),
            date=current_time,
            creator_id=user_id,
            creator_name=username
            )
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('topics'))
    return render_template('create_topic.html', username=username)


@app.route('/delete_topic/<int:topic_id>')
@login_required
def delete_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    db.session.delete(topic)
    db.session.commit()
    return redirect(url_for('topics'))


# Posts
@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    username = session.get('username', None)
    user_id = session.get('user_id', None)
    topics = list(Topic.query.order_by(Topic.name).all())
    
    if request.method == 'POST':
        current_time = datetime.now().strftime('%Y=%m-%d %H:%M:%S')
        form_topic_value = request.form.get('topic_name')
        form_topic_id, form_topic_name = form_topic_value.split('|')

        post = Post(
            title=request.form.get('post-title'),
            content=request.form.get('post-content'),
            date=current_time,
            creator_name=username,
            creator_id=user_id,
            topic_id=form_topic_id,
            topic_name=form_topic_name
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_post.html', username=username, topics=topics)


@app.route('/my_posts')
@login_required
def my_posts():
    username = session.get('username', None)
    user_id = session.get('user_id', None)
    posts = list(Post.query.filter_by(creator_id=user_id).order_by(Post.date).all())
    return render_template('my_posts.html', username=username, posts=posts)


@app.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('my_posts'))


# Users page - Admin Only
@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    username = session.get('username', None)

    if request.method == 'POST':
        for user in User.query.all():
            user_id = user.id
            checkbox_name = f'is-admin-{user_id}'
            is_admin = checkbox_name in request.form

            user.is_admin = is_admin
            db.session.commit()
        
        flash('User roles updated successfully.')
        return redirect(url_for('users'))

    users = list(User.query.order_by(User.id).all())

    return render_template('users.html', users=users, username=username)