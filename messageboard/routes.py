from flask import render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from messageboard import app, db, bcrypt
from messageboard.model import User, Topic, Post, Comment
from datetime import datetime


@app.route('/')
def index():
    return render_template('index.html')


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
            return redirect(url_for('home'))
        flash('Invalid username or password')
        return redirect(url_for('login'))
    return render_template("login.html")


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/home')
def home():
    username = session.get('username', None)
    return render_template('home.html', username=username)


@app.route('/topics')
def topics():
    username = session.get('username', None)
    topics = list(Topic.query.order_by(Topic.name).all())
    return render_template('topics.html', topics=topics, username=username)


@app.route('/create_topic', methods=['GET', 'POST'])
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


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    username = session.get('username', None)

    return render_template('create_post.html', username=username)