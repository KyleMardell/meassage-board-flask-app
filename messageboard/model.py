from messageboard import db

class User(db.Model):
    # schema for the topic model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#User: {0} - {1} Admin: {2}".format(
            self.id, self.username, self.is_admin
            )


class Topic(db.Model):
    # schema for the Topic model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship("Post", backref="topic", cascade="all, delete", lazy=True)
    date = db.Column(db.Date, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    creator_name = db.Column(db.String(25), db.ForeignKey("user.username"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#Topic: {0} - {1} Created by: {2}".format(
            self.id, self.name, self.creator_name
        )


class Post(db.Model):
    # schema for the Task model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey("topic.id", ondelete="CASCADE"), nullable=False)
    topic_name = db.Column(db.String(50), db.ForeignKey("topic.name"), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    creator_name = db.Column(db.String(25), db.ForeignKey("user.username"), nullable=False)
    comments = db.relationship("Comment", backref="post", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Post: {1}".format(
            self.id, self.title
        )

class Comment(db.Model):
    # schema for the Comment model
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    creator_name = db.Column(db.String(25), db.ForeignKey("user.username"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#Post: {0} Created by: {1}".format(
            self.id, self.creator_name
        )