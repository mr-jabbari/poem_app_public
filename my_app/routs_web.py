import time
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from my_app import app, db
from my_app.forms import SearchBeytForm, SearchPoemForm, SearchSpeechForm, SearchStoryForm, BeytForm, PoemForm, \
    SpeechForm, StoryForm, UploadSound, AddCommentForm, RegisterForm, LoginForm
from my_app.functions import add_some
from my_app.models import Beyts, Speechs, Poems, Stories, PoemSounds, BeytBookmarks, PoemBookmarks, SpeechBookmarks, \
    StoryBookmarks, BeytLikes, PoemLikes, SpeechLikes, StoryLikes, BeytComments, PoemComments, Users, StoryComments, \
    SpeechComments
from sqlalchemy.sql import func
from sqlalchemy import or_
from werkzeug.utils import secure_filename
import os

ALPHABET = {1: "الف", 2: "ب", 3: "پ", 4: "ت", 5: "ث", 6: "ج", 7: "چ", 8: "ح", 9: "خ", 10: "د", 11: "ذ", 12: "ر",
            13: "ز", 14: "ژ", 15: "س", 16: "ش", 17: "ص", 18: "ض", 19: "ط", 20: "ظ", 21: "ع", 22: "غ", 23: "ف", 24: "ق",
            25: "ک", 26: "گ", 27: "ل", 28: "م", 29: "ن", 30: "و", 31: "ه", 32: "ی", }


@app.route('/', methods=["POST", "GET"])
def index():
    add_some()
    beyts = Beyts.query.order_by(func.rand()).limit(3)
    speech = Speechs.query.order_by(func.rand()).first()
    poem = Poems.query.order_by(func.rand()).first()
    return render_template("index.html", poem=poem, speech=speech, beyts=beyts)


@app.route('/stories', methods=["POST", "GET"])
def stories():
    story = Stories.query.order_by(func.rand()).first()
    return render_template("stories.html", story=story)


@app.route("/beyts", methods=["POST", "GET"])
def beyts():
    beyts = Beyts.query.order_by(func.rand()).limit(10)
    return render_template("beyts.html", beyts=beyts)


@app.route("/poems", methods=["POST", "GET"])
def poems():
    poems = Poems.query.order_by(func.rand()).limit(1)
    return render_template("poems.html", poems=poems)


@app.route("/speechs", methods=["POST", "GET"])
def speechs():
    speechs = Speechs.query.order_by(func.rand()).limit(1)
    return render_template("speechs.html", speechs=speechs)


@app.route('/sound_poems', methods=["POST", "GET"])
def sound_poems():
    sound_poems = PoemSounds.query.order_by(func.rand()).first()
    print(sound_poems.sound_link)
    return render_template("sound_poems.html", sound_poems=sound_poems)


@app.route('/sound_stories', methods=["POST", "GET"])
def sound_stories():
    sound_stories = PoemSounds.query.order_by(func.rand()).first()
    print(sound_stories.sound_link)
    return render_template("sound_stories.html", sound_stories=sound_stories)


@app.route("/search", methods=["POST", "GET"])
def search():
    form_search_beyt = SearchBeytForm()
    form_search_poem = SearchPoemForm()
    form_search_speech = SearchSpeechForm()
    form_search_story = SearchStoryForm()

    if form_search_beyt.validate_on_submit():
        start = int(form_search_beyt.b_start.data)
        stop = int(form_search_beyt.b_stop.data)
        word = str(form_search_beyt.b_word.data) if len(str(form_search_beyt.b_word.data)) >= 2 else '_'
        poet = str(form_search_beyt.b_poet.data) if len(str(form_search_beyt.b_poet.data)) >= 2 else '_'
        return redirect(url_for("search_beyt", start=start, end=stop, word=word, poet=poet))

    if form_search_poem.validate_on_submit():
        word = str(form_search_poem.p_word.data) if len(str(form_search_poem.p_word.data)) >= 2 else '_'
        poet = str(form_search_poem.p_poet.data) if len(str(form_search_poem.p_poet.data)) >= 2 else '_'
        return redirect(url_for("search_poem", word=word, poet=poet))

    if form_search_speech.validate_on_submit():
        word = str(form_search_speech.sp_word.data)
        wise = str(form_search_speech.sp_wise.data)
        return redirect(url_for("search_speech", word=word, wise=wise))

    if form_search_story.validate_on_submit():
        title = str(form_search_story.st_title.data)
        word = str(form_search_story.st_word.data)
        writer = str(form_search_story.st_writer.data)
        return redirect(url_for("search_story", title=title, word=word, writer=writer))

    return render_template("search.html", form_search_beyt=form_search_beyt, form_search_poem=form_search_poem,
                           form_search_speech=form_search_speech, form_search_story=form_search_story,
                           ALPHABET=ALPHABET)


@app.route('/search_beyt/<string:word>/<string:poet>/<int:start>/<int:end>/', methods=['POST', 'GET'])
def search_beyt(start, end, word, poet):
    sbeyts = Beyts.query
    if start > 0:
        sbeyts = sbeyts.filter(Beyts.opening == start)
    if end > 0:
        sbeyts = sbeyts.filter(Beyts.ending == end)
    if len(word) > 1:
        sbeyts = sbeyts.filter(or_(Beyts.mesra1.like("%" + word + "%"), Beyts.mesra2.like("%" + word + "%")))
    if len(poet) > 1:
        sbeyts = sbeyts.filter(Beyts.poet.like("%" + poet + "%"))
    if not sbeyts:
        flash("چیزی پیدا نشد", category='info')
        return redirect(url_for('search'))

    return render_template('searched_beyts.html', beyts=sbeyts)


@app.route('/search_poem/<string:word>/<string:poet>/', methods=['POST', 'GET'])
def search_poem(word, poet):
    spoems = Poems.query
    if len(word) > 0:
        spoems = spoems.filter(or_(Poems.beyt1_1.like("%" + word + "%"), Poems.beyt1_2.like("%" + word + "%"),
                                   Poems.beyt2_1.like("%" + word + "%"), Poems.beyt2_2.like("%" + word + "%"),
                                   Poems.beyt3_1.like("%" + word + "%"), Poems.beyt3_2.like("%" + word + "%"),
                                   Poems.beyt4_1.like("%" + word + "%"), Poems.beyt4_2.like("%" + word + "%"),
                                   Poems.beyt5_1.like("%" + word + "%"), Poems.beyt5_2.like("%" + word + "%"),
                                   Poems.beyt6_1.like("%" + word + "%"), Poems.beyt6_2.like("%" + word + "%"),
                                   Poems.beyt7_1.like("%" + word + "%"), Poems.beyt7_2.like("%" + word + "%"),
                                   Poems.beyt8_1.like("%" + word + "%"), Poems.beyt8_2.like("%" + word + "%"),
                                   Poems.beyt9_1.like("%" + word + "%"), Poems.beyt9_2.like("%" + word + "%"),
                                   Poems.beyt10_1.like("%" + word + "%"), Poems.beyt10_2.like("%" + word + "%")))
    if len(poet) > 0:
        spoems = spoems.filter(Poems.poet.like("%" + poet + "%"))
    if not spoems:
        flash("چیزی پیدا نشد", category='info')
        return redirect(url_for('search'))

    return render_template("searched_poems.html", poems=spoems)


@app.route('/search_speech/<string:word>/<string:wise>/', methods=['POST', 'GET'])
def search_speech(word, wise):
    sspeech = Speechs.query
    if len(word) > 0:
        sspeech.filter(Speechs.speech.like("%" + word + "%"))
    if len(wise) > 0:
        sspeech.filter(Speechs.wise.like("%" + wise + "%"))
    if not sspeech:
        flash("چیزی پیدا نشد", category='info')
        return redirect(url_for('index'))

    return render_template("searched_speechs.html", speechs=sspeech)


@app.route('/search_story/<string:title>/<string:word>/<string:writer>/', methods=['POST', 'GET'])
def search_story(title, word, writer):
    sstory = Stories.query
    if len(title) > 0:
        sstory.filter(Stories.title.like("%" + title + "%"))
    if len(word) > 0:
        sstory.filter(Stories.story.like("%" + word + "%"))
    if len(writer) > 0:
        sstory.filter(Stories.writer.like("%" + writer + "%"))
    if not sstory:
        flash("چیزی پیدا نشد", category='info')
        return redirect(url_for('index'))

    return render_template(url_for("searched_stories.html", stories=sstory))


@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/edit_me')
def edit_me():
    return render_template("edit_me.html")


@app.route('/me')
def my_beyts():
    user_beytes = Beyts.query.filter(Beyts.user_id == current_user.id)
    user_stories = Stories.query.filter(Stories.user_id == current_user.id)
    user_speechs = Speechs.query.filter(Speechs.user_id == current_user.id)
    user_poems = Poems.query.filter(Poems.user_id == current_user.id)
    return render_template("me.html", poems=user_poems, stories=user_stories, speechs=user_speechs,
                           beyts=user_beytes)


@app.route('/bookmarks', methods=["POST", "GET"])
def bookmarks():
    bookmarked_beytes = Beyts.query.join(BeytBookmarks, BeytBookmarks.beyt_id == Beyts.id).filter(
        BeytBookmarks.user_id == current_user.id)
    bookmarked_poems = Poems.query.join(PoemBookmarks, PoemBookmarks.poem_id == Poems.id).filter(
        PoemBookmarks.user_id == current_user.id)
    bookmarked_speechs = Speechs.query.join(SpeechBookmarks, SpeechBookmarks.speech_id == Speechs.id).filter(
        SpeechBookmarks.user_id == current_user.id)
    bookmarked_stories = Stories.query.join(StoryBookmarks, StoryBookmarks.story_id == Stories.id).filter(
        StoryBookmarks.user_id == current_user.id)
    return render_template("bookmarks.html", beyts=bookmarked_beytes, poems=bookmarked_poems,
                           speechs=bookmarked_speechs, stories=bookmarked_stories)


@app.route('/likes', methods=["POST", "GET"])
def likes():
    liked_beytes = Beyts.query.join(BeytLikes, BeytLikes.beyt_id == Beyts.id).filter(
        BeytLikes.user_id == current_user.id)
    liked_poems = Poems.query.join(PoemLikes, PoemLikes.poem_id == Poems.id).filter(
        PoemLikes.user_id == current_user.id)
    liked_speechs = Speechs.query.join(SpeechLikes, SpeechLikes.speech_id == Speechs.id).filter(
        SpeechLikes.user_id == current_user.id)
    liked_stories = Stories.query.join(StoryLikes, StoryLikes.story_id == Stories.id).filter(
        StoryLikes.user_id == current_user.id)
    return render_template("likes.html", beyts=liked_beytes, poems=liked_poems, speechs=liked_speechs,
                           stories=liked_stories)


@app.route('/notes', methods=["POST", "GET"])
@login_required
def notes():
    form_beyt = BeytForm()
    form_poem = PoemForm()
    form_speech = SpeechForm()
    form_story = StoryForm()
    if form_beyt.validate_on_submit():
        new_beyt = Beyts(mesra1=form_beyt.mesra1.data, mesra2=form_beyt.mesra2.data, poet=form_beyt.poet.data,
                         opening=form_beyt.start.data, ending=form_beyt.stop.data, user_id=current_user.id, grade="f")
        db.session.add(new_beyt)
        db.session.commit()
        return redirect(url_for('notes'))

    if form_poem.validate_on_submit():
        new_poem = Poems(beyt1_1=form_poem.beyt1_1.data, beyt1_2=form_poem.beyt1_2.data, beyt2_1=form_poem.beyt2_1.data,
                         beyt2_2=form_poem.beyt2_2.data, beyt3_1=form_poem.beyt3_1.data, beyt3_2=form_poem.beyt3_2.data,
                         beyt4_1=form_poem.beyt4_1.data, beyt4_2=form_poem.beyt4_2.data, poet=form_poem.poet.data,
                         user_id=current_user.id, grade="g")
        db.session.add(new_poem)
        db.session.commit()
        return redirect(url_for('notes'))

    if form_speech.validate_on_submit():
        new_speech = Speechs(speech=form_speech.speech.data, wise=form_speech.wise.data, user_id=current_user.id,
                             grade="f")
        db.session.add(new_speech)
        db.session.commit()
        return redirect(url_for('notes'))

    if form_story.validate_on_submit():
        new_story = Stories(title=form_story.title.data, story=form_story.story.data, writer=form_story.writer.data,
                            user_id=current_user.id, grade="f")
        db.session.add(new_story)
        db.session.commit()
        return redirect(url_for('notes'))

    return render_template("notes.html", form_beyt=form_beyt, form_poem=form_poem, form_speech=form_speech,
                           form_story=form_story, ALPHABET=ALPHABET)


@app.route('/profile/<int:user_id>')
def users_profile(user_id):
    user_beytes = Beyts.query.filter(Beyts.user_id == user_id)
    user_stories = Stories.query.filter(Stories.user_id == user_id)
    user_speechs = Speechs.query.filter(Speechs.user_id == user_id)
    user_poems = Poems.query.filter(Poems.user_id == user_id)
    return render_template("user_profile.html", poems=user_poems, stories=user_stories, speechs=user_speechs,
                           beyts=user_beytes)


@app.route('/beyt/<int:beyt_id>', methods=["POST", "GET"])
def t_beyt(beyt_id):
    form_add_sound = UploadSound()
    form_comment_beyt = AddCommentForm()
    tak_beyt = Beyts.query.filter(Beyts.id == beyt_id).first()
    beyt_comments = BeytComments.query.join(Users, Users.id == BeytComments.user_id).filter(
        BeytComments.beyt_id == beyt_id)
    if form_comment_beyt.validate_on_submit():
        new_beyt_comment = BeytComments(comment=form_comment_beyt.comment.data, user_id=current_user.id,
                                        beyt_id=beyt_id)
        db.session.add(new_beyt_comment)
        db.session.commit()
    return render_template('beyt.html', form_add_sound=form_add_sound, beyt=tak_beyt, ALPHABET=ALPHABET,
                           comments=beyt_comments, form_comment_beyt=form_comment_beyt)


@app.route('/poem/<int:poem_id>', methods=["POST", "GET"])
def t_poem(poem_id):
    form_add_sound = UploadSound()
    form_comment_poem = AddCommentForm()
    tak_poem = Poems.query.filter(Poems.id == poem_id).first()
    poem_comments = PoemComments.query.join(Users, Users.id == PoemComments.user_id).filter(
        PoemComments.poem_id == poem_id)
    if form_comment_poem.validate_on_submit():
        new_poem_comment = PoemComments(comment=form_comment_poem.comment.data, user_id=current_user.id,
                                        poem_id=poem_id)
        db.session.add(new_poem_comment)
        db.session.commit()
    if form_add_sound.validate_on_submit():
        try:
            file = form_add_sound.file.data
            secure_filenam = secure_filename(file.filename)
            now = time.time()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                                   f"poem-{str(poem_id)}_time-{now}_user-{str(current_user.id)}--{file.filename}"))
            sound = PoemSounds(user_id=current_user.id, poem_id=poem_id,
                               sound_link=f"sounds/poem-{str(poem_id)}_time-{now}_user-{str(current_user.id)}--{file.filename}")
            db.session.add(sound)
            db.session.commit()
        except:
            flash("Error!  Looks like there was a problem...try again!")
            return redirect(request.referrer)
    return render_template('poem.html', form_add_sound=form_add_sound, comments=poem_comments, poem=tak_poem,
                           ALPHABET=ALPHABET, form_comment_poem=form_comment_poem)


@app.route('/speech/<int:speech_id>', methods=["POST", "GET"])
def t_speech(speech_id):
    form_comment_speech = AddCommentForm()
    tak_speech = Speechs.query.filter(Speechs.id == speech_id).first()
    speech_comments = SpeechComments.query.join(Users, Users.id == SpeechComments.user_id).filter(
        SpeechComments.speech_id == speech_id)
    if form_comment_speech.validate_on_submit():
        new_speech_comment = SpeechComments(comment=form_comment_speech.comment.data, user_id=current_user.id,
                                            speech_id=speech_id)
        db.session.add(new_speech_comment)
        db.session.commit()
    return render_template('speech.html', speech=tak_speech, comments=speech_comments, ALPHABET=ALPHABET,
                           form_comment_speech=form_comment_speech)


@app.route('/story/<int:story_id>', methods=["POST", "GET"])
def t_story(story_id):
    form_comment_story = AddCommentForm()
    tak_story = Stories.query.filter(Stories.id == story_id).first()
    story_comments = StoryComments.query.join(Users, Users.id == StoryComments.user_id).filter(
        StoryComments.story_id == story_id)
    if form_comment_story.validate_on_submit():
        new_comment_story = StoryComments(comment=form_comment_story.comment.data, user_id=current_user.id,
                                          story_id=story_id)
        db.session.add(new_comment_story)
        db.session.commit()
    return render_template('story.html', story=tak_story, ALPHABET=ALPHABET, comments=story_comments,
                           form_comment_story=form_comment_story)


@app.route('/login_register', methods=["POST", "GET"])
def login_register_page():
    form_register = RegisterForm()
    form_login = LoginForm()
    if form_register.validate_on_submit():
        user_to_create = Users(username=form_register.username.data,
                               name=form_register.name.data,
                               phone_email=form_register.phone_email.data,
                               password=form_register.password_hash.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        return redirect(url_for('index'))

    if form_login.validate_on_submit():
        attempted_user = Users.query.filter_by(username=form_login.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form_login.password.data):
            login_user(attempted_user)
            return redirect(url_for('index'))
        else:
            flash("Username or Password are not match! please try again!!!", category="danger")
    return render_template('login.html', ALPHABET=ALPHABET, form_login=form_login, form_register=form_register)


@app.route('/logout', methods=["POST", "GET"])
@login_required
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("index"))
