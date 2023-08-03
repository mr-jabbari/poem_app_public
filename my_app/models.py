from my_app import db, app, login_manager
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin
from sqlalchemy.dialects.mysql import CHAR, VARCHAR, INTEGER, TINYINT, LONGTEXT
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    followers = db.relationship('Followers', foreign_keys='Followers.followed_id', backref='followed', lazy='dynamic')
    following = db.relationship('Followers', foreign_keys='Followers.follower_id', backref='follower', lazy='dynamic')
    def follow(self, user):
        if not self.is_following(user):
            follow = Followers(follower_id=self.id, followed_id=user.id)
            db.session.add(follow)
    def unfollow(self, user):
        if self.is_following(user):
            Followers.query.filter_by(follower_id=self.id, followed_id=user.id).delete()
    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id).count() > 0
    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).count() > 0

    beyt_liked = db.relationship('BeytLikes', foreign_keys='BeytLikes.user_id', backref='users', lazy='dynamic')
    beyt_bookmarked = db.relationship('BeytBookmarks', foreign_keys='BeytBookmarks.user_id', backref='users',
                                      lazy='dynamic')
    def beyt_like(self, beyt):
        if not self.has_liked_beyt(beyt):
            like = BeytLikes(user_id=self.id, beyt_id=beyt.id)
            db.session.add(like)
    def beyt_unlike(self, beyt):
        if self.has_liked_beyt(beyt):
            BeytLikes.query.filter_by(user_id=self.id, beyt_id=beyt.id).delete()
    def has_liked_beyt(self, beyt):
        return BeytLikes.query.filter(BeytLikes.user_id == self.id, BeytLikes.beyt_id == beyt.id).count() > 0
    def beyt_bookmark(self, beyt):
        if not self.has_bookmarked_beyt(beyt):
            bookmark = BeytBookmarks(user_id=self.id, beyt_id=beyt.id)
            db.session.add(bookmark)
    def beyt_unbookmark(self, beyt):
        if self.has_bookmarked_beyt(beyt):
            BeytBookmarks.query.filter_by(user_id=self.id, beyt_id=beyt.id).delete()
    def has_bookmarked_beyt(self, beyt):
        return BeytBookmarks.query.filter(BeytBookmarks.user_id == self.id,
                                          BeytBookmarks.beyt_id == beyt.id).count() > 0

    poem_liked = db.relationship('PoemLikes', foreign_keys='PoemLikes.user_id', backref='users', lazy='dynamic')
    poem_bookmarked = db.relationship('PoemBookmarks', foreign_keys='PoemBookmarks.user_id', backref='users',
                                      lazy='dynamic')
    def poem_like(self, poem):
        if not self.has_liked_poem(poem):
            like = PoemLikes(user_id=self.id, poem_id=poem.id)
            db.session.add(like)
    def poem_unlike(self, poem):
        if self.has_liked_poem(poem):
            PoemLikes.query.filter_by(user_id=self.id, poem_id=poem.id).delete()
    def has_liked_poem(self, poem):
        return PoemLikes.query.filter(PoemLikes.user_id == self.id, PoemLikes.poem_id == poem.id).count() > 0
    def poem_bookmark(self, poem):
        if not self.has_bookmarked_poem(poem):
            bookmark = PoemBookmarks(user_id=self.id, poem_id=poem.id)
            db.session.add(bookmark)
    def poem_unbookmark(self, poem):
        if self.has_bookmarked_poem(poem):
            PoemBookmarks.query.filter_by(user_id=self.id, poem_id=poem.id).delete()
    def has_bookmarked_poem(self, poem):
        return PoemBookmarks.query.filter(PoemBookmarks.user_id == self.id,
                                          PoemBookmarks.poem_id == poem.id).count() > 0
    speech_liked = db.relationship('SpeechLikes', foreign_keys='SpeechLikes.user_id', backref='users', lazy='dynamic')
    speech_bookmarked = db.relationship('SpeechBookmarks', foreign_keys='SpeechBookmarks.user_id', backref='users',
                                        lazy='dynamic')

    def speech_like(self, speech):
        if not self.has_liked_speech(speech):
            like = SpeechLikes(user_id=self.id, speech_id=speech.id)
            db.session.add(like)
    def speech_unlike(self, speech):
        if self.has_liked_speech(speech):
            SpeechLikes.query.filter_by(user_id=self.id, speech_id=speech.id).delete()
    def has_liked_speech(self, speech):
        return SpeechLikes.query.filter(SpeechLikes.user_id == self.id, SpeechLikes.speech_id == speech.id).count() > 0
    def speech_bookmark(self, speech):
        if not self.has_bookmarked_speech(speech):
            bookmark = SpeechBookmarks(user_id=self.id, speech_id=speech.id)
            db.session.add(bookmark)
    def speech_unbookmark(self, speech):
        if self.has_bookmarked_speech(speech):
            SpeechBookmarks.query.filter_by(user_id=self.id, speech_id=speech.id).delete()
    def has_bookmarked_speech(self, speech):
        return SpeechBookmarks.query.filter(SpeechBookmarks.user_id == self.id,
                                            SpeechBookmarks.speech_id == speech.id).count() > 0

    story_liked = db.relationship('StoryLikes', foreign_keys='StoryLikes.user_id', backref='users', lazy='dynamic')
    story_bookmarked = db.relationship('StoryBookmarks', foreign_keys='StoryBookmarks.user_id', backref='users',
                                       lazy='dynamic')
    def story_like(self, story):
        if not self.has_liked_story(story):
            like = StoryLikes(user_id=self.id, story_id=story.id)
            db.session.add(like)
    def story_unlike(self, story):
        if self.has_liked_story(story):
            StoryLikes.query.filter_by(user_id=self.id, story_id=story.id).delete()
    def has_liked_story(self, story):
        return StoryLikes.query.filter(StoryLikes.user_id == self.id, StoryLikes.story_id == story.id).count() > 0
    def story_bookmark(self, story):
        if not self.has_bookmarked_story(story):
            bookmark = StoryBookmarks(user_id=self.id, story_id=story.id)
            db.session.add(bookmark)
    def story_unbookmark(self, story):
        if self.has_bookmarked_story(story):
            StoryBookmarks.query.filter_by(user_id=self.id, story_id=story.id).delete()
    def has_bookmarked_story(self, story):
        return StoryBookmarks.query.filter(StoryBookmarks.user_id == self.id,
                                           StoryBookmarks.story_id == story.id).count() > 0

    @property
    def password(self):
        return self.password
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = generate_password_hash(plain_text_password).decode('utf-8')
    def check_password_correction(self, attempted_password):
        return check_password_hash(self.password_hash, attempted_password)

    id = db.Column(INTEGER, primary_key=True)
    name = db.Column(db.String(length=50), nullable=False)
    username = db.Column(db.String(length=50), nullable=False, unique=True)
    bio = db.Column(VARCHAR(length=500))
    phone_email = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    profile_pic_url = db.Column(VARCHAR(length=255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


class Followers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, follower_id, followed_id):
        self.follower_id = follower_id
        self.followed_id = followed_id


class Beyts(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    grade = db.Column(CHAR(1), nullable=False)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    mesra1 = db.Column(VARCHAR(100), nullable=False)
    mesra2 = db.Column(VARCHAR(100), nullable=False)
    poet = db.Column(VARCHAR(50), nullable=False)
    opening = db.Column(TINYINT)
    ending = db.Column(TINYINT)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


class Poems(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    grade = db.Column(CHAR(1), nullable=False)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    beyt1_1 = db.Column(VARCHAR(100), nullable=False)
    beyt1_2 = db.Column(VARCHAR(100), nullable=False)
    beyt2_1 = db.Column(VARCHAR(100), nullable=False)
    beyt2_2 = db.Column(VARCHAR(100), nullable=False)
    beyt3_1 = db.Column(VARCHAR(100))
    beyt3_2 = db.Column(VARCHAR(100))
    beyt4_1 = db.Column(VARCHAR(100))
    beyt4_2 = db.Column(VARCHAR(100))
    beyt5_1 = db.Column(VARCHAR(100))
    beyt5_2 = db.Column(VARCHAR(100))
    beyt6_1 = db.Column(VARCHAR(100))
    beyt6_2 = db.Column(VARCHAR(100))
    beyt7_1 = db.Column(VARCHAR(100))
    beyt7_2 = db.Column(VARCHAR(100))
    beyt8_1 = db.Column(VARCHAR(100))
    beyt8_2 = db.Column(VARCHAR(100))
    beyt9_1 = db.Column(VARCHAR(100))
    beyt9_2 = db.Column(VARCHAR(100))
    beyt10_1 = db.Column(VARCHAR(100))
    beyt10_2 = db.Column(VARCHAR(100))
    poet = db.Column(VARCHAR(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


class PoemSounds(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    sound_link = db.Column(VARCHAR(100), nullable=False)
    poem_id = db.Column(INTEGER, db.ForeignKey(Poems.id))


class Speechs(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    grade = db.Column(CHAR(1), nullable=False)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    speech = db.Column(VARCHAR(250), nullable=False)
    wise = db.Column(VARCHAR(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


class Stories(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    grade = db.Column(CHAR(1), nullable=False)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    title = db.Column(VARCHAR(100), nullable=False)
    story = db.Column(LONGTEXT, nullable=False)
    writer = db.Column(VARCHAR(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


class StorySounds(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    sound_link = db.Column(VARCHAR(100), nullable=False)
    story_id = db.Column(INTEGER, db.ForeignKey(Stories.id))
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))


class BeytLikes(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    beyt_id = db.Column(INTEGER, db.ForeignKey(Beyts.id))


class BeytBookmarks(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    beyt_id = db.Column(INTEGER, db.ForeignKey(Beyts.id))


class BeytComments(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    beyt_id = db.Column(INTEGER, db.ForeignKey(Beyts.id))
    comment = db.Column(VARCHAR(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


class PoemLikes(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    poem_id = db.Column(INTEGER, db.ForeignKey(Poems.id))


class PoemBookmarks(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    poem_id = db.Column(INTEGER, db.ForeignKey(Poems.id))


class PoemComments(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    poem_id = db.Column(INTEGER, db.ForeignKey(Poems.id))
    comment = db.Column(VARCHAR(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


class SpeechLikes(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    speech_id = db.Column(INTEGER, db.ForeignKey(Speechs.id))


class SpeechBookmarks(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    speech_id = db.Column(INTEGER, db.ForeignKey(Speechs.id))


class SpeechComments(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    speech_id = db.Column(INTEGER, db.ForeignKey(Speechs.id))
    comment = db.Column(VARCHAR(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


class StoryLikes(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    story_id = db.Column(INTEGER, db.ForeignKey(Stories.id))


class StoryBookmarks(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    story_id = db.Column(INTEGER, db.ForeignKey(Stories.id))


class StoryComments(db.Model):
    id = db.Column(INTEGER, primary_key=True)
    user_id = db.Column(INTEGER, db.ForeignKey(Users.id))
    story_id = db.Column(INTEGER, db.ForeignKey(Stories.id))
    comment = db.Column(VARCHAR(500), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())






with app.app_context():
    db.create_all()
