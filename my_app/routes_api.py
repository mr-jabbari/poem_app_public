from flask import request, jsonify, session
from flask_bcrypt import check_password_hash
from flask_login import login_user, login_required, current_user
from my_app import db, app
from my_app.forms import BeytForm, PoemForm, SpeechForm, StoryForm
from my_app.models import Users, Beyts, Stories, Poems, Speechs, BeytLikes, BeytBookmarks, PoemLikes, PoemBookmarks, \
    StoryLikes, StoryBookmarks, SpeechLikes, SpeechBookmarks
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash


# Login & Register
@app.route('/api/register', methods=['POST'])
def app_register():
    data = request.get_json()
    name = data['name']
    phone_email = data['phoneEmail']
    username = data['username']
    password = data['password']
    user = Users.query.filter_by(username=username).first()
    if user:
        return jsonify({'success': False, 'message': 'Username already exists'})
    else:
        new_user = Users(name=name, phone_email=phone_email, username=username)
        new_user.password = password  # Set the password using the property setter
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        return jsonify({'success': True})


@app.route('/api/login', methods=['POST'])
def app_login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = Users.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        login_user(user, remember=True)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'})


# Send Json for main page

@app.route('/api/main_beyts')
@login_required
def json_main_beyt():
    beyts = Beyts.query.order_by(func.rand()).limit(7)
    beyt_list = []
    for beyt in beyts:
        is_liked = BeytLikes.query.filter_by(user_id=current_user.id, beyt_id=beyt.id).first() is not None
        is_bookmarked = BeytBookmarks.query.filter_by(user_id=current_user.id, beyt_id=beyt.id).first() is not None
        user = Users.query.get(beyt.user_id)
        username = user.username
        name = user.name
        beyt_dict = {'id': beyt.id, 'user_id': beyt.user_id, 'mesra1': beyt.mesra1, 'mesra2': beyt.mesra2,
                     'poet': beyt.poet, 'created_at': beyt.created_at, 'is_liked': is_liked,
                     'is_bookmarked': is_bookmarked, 'username': username, 'name': name}
        beyt_list.append(beyt_dict)
    return jsonify(beyt_list)


@app.route('/api/main_poems')
@login_required
def json_main_poem():
    poems = Poems.query.order_by(func.rand()).limit(1)
    poem_list = []
    for poem in poems:
        is_liked = PoemLikes.query.filter_by(user_id=current_user.id, poem_id=poem.id).first() is not None
        is_bookmarked = PoemBookmarks.query.filter_by(user_id=current_user.id, poem_id=poem.id).first() is not None
        user = Users.query.get(poem.user_id)
        username = user.username
        name = user.name
        poem_dict = {'id': poem.id, 'user_id': poem.user_id, 'beyt1_1': poem.beyt1_1, 'beyt1_2': poem.beyt1_2,
                     'beyt2_1': poem.beyt2_1, 'beyt2_2': poem.beyt2_2, 'beyt3_1': poem.beyt3_1, 'beyt3_2': poem.beyt3_2,
                     'beyt4_1': poem.beyt4_1, 'beyt4_2': poem.beyt4_2, 'beyt5_1': poem.beyt5_1, 'beyt5_2': poem.beyt5_2,
                     'beyt6_1': poem.beyt6_1, 'beyt6_2': poem.beyt6_2, 'beyt7_1': poem.beyt7_1, 'beyt7_2': poem.beyt7_2,
                     'beyt8_1': poem.beyt8_1, 'beyt8_2': poem.beyt8_2, 'beyt9_1': poem.beyt9_1, 'beyt9_2': poem.beyt9_2,
                     'beyt10_1': poem.beyt10_1, 'beyt10_2': poem.beyt10_2,
                     'poet': poem.poet, 'created_at': poem.created_at, 'is_liked': is_liked,
                     'is_bookmarked': is_bookmarked, 'username': username, 'name': name}
        poem_list.append(poem_dict)
    return jsonify(poem_list)


@app.route('/api/main_stories')
@login_required
def json_main_story():
    stories = Stories.query.order_by(func.rand()).limit(1)
    story_list = []
    for story in stories:
        is_liked = StoryLikes.query.filter_by(user_id=current_user.id, poem_id=story.id).first() is not None
        is_bookmarked = StoryBookmarks.query.filter_by(user_id=current_user.id, poem_id=story.id).first() is not None
        user = Users.query.get(story.user_id)
        username = user.username
        name = user.name
        story_dict = {'id': story.id, 'user_id': story.user_id, 'title': story.title, 'story': story.story,
                      'writer': story.writer, 'created_at': story.created_at, 'is_liked': is_liked,
                      'is_bookmarked': is_bookmarked, 'username': username, 'name': name}
        story_list.append(story_dict)
    return jsonify(story_list)


@app.route('/api/main_speechs')
@login_required
def json_main_speech():
    speechs = Speechs.query.order_by(func.rand()).limit(1)
    speech_list = []
    for speech in speechs:
        is_liked = SpeechLikes.query.filter_by(user_id=current_user.id, poem_id=speech.id).first() is not None
        is_bookmarked = SpeechBookmarks.query.filter_by(user_id=current_user.id, poem_id=speech.id).first() is not None
        user = Users.query.get(speechs.user_id)
        username = user.username
        name = user.name
        speech_dict = {'id': speech.id, 'user_id': speechs.user_id, 'speech': speech.speech,
                       'wise': speech.wise, 'created_at': speech.created_at, 'is_liked': is_liked,
                       'is_bookmarked': is_bookmarked, 'username': username, 'name': name}
        speech_list.append(speech_dict)
    return jsonify(speech_list)


# GET DATA


@app.route('/api/beyt_data')
@login_required
def get_beyt_data():
    form = BeytForm(request.form)
    if form.validate():
        new_beyt = Beyts(mesra1=form.mesra1.data, mesra2=form.mesra2.data, poet=form.poet.data,
                         opening=form.start.data, ending=form.stop.data, user_id=current_user.id, grade="f")
        db.session.add(new_beyt)
        db.session.commit()
        return {'status': 'success'}
    else:
        return {'status': 'error', 'errors': form.errors}


@app.route('/api/poem_data', methods=['POST'])
@login_required
def get_poem_data():
    form = PoemForm(request.form)
    if form.validate():
        new_poem = Poems(beyt1_1=form.beyt1_1.data, beyt1_2=form.beyt1_2.data, beyt2_1=form.beyt2_1.data,
                         beyt2_2=form.beyt2_2.data, beyt3_1=form.beyt3_1.data, beyt3_2=form.beyt3_2.data,
                         beyt4_1=form.beyt4_1.data, beyt4_2=form.beyt4_2.data, poet=form.poet.data,
                         user_id=current_user.id, grade="f")
        db.session.add(new_poem)
        db.session.commit()
        return {'status': 'success'}
    else:
        return {'status': 'error', 'errors': form.errors}


@app.route('/api/speech_data', methods=['POST'])
@login_required
def get_speech_data():
    form = SpeechForm(request.form)
    if form.validate():
        new_speech = Speechs(speech=form.speech.data, wise=form.wise.data, user_id=current_user.id, grade="f")
        db.session.add(new_speech)
        db.session.commit()
        return {'status': 'success'}
    else:
        return {'status': 'error', 'errors': form.errors}


@app.route('/api/story_data', methods=['POST'])
@login_required
def get_story_data():
    form = StoryForm(request.form)
    if form.validate():
        new_story = Stories(title=form.title.data, story=form.story.data, writer=form.writer.data,
                            user_id=current_user.id, grade="f")
        db.session.add(new_story)
        db.session.commit()
        return {'status': 'success'}
    else:
        return {'status': 'error', 'errors': form.errors}


# SEND JSON
@app.route('/api/beyts')
def json_beyt():
    beyts = Beyts.query.order_by(func.rand()).limit(7)
    beyt_list = []
    for beyt in beyts:
        beyt_dict = {'id': beyt.id, 'grade': beyt.grade, 'user_id': beyt.user_id, 'mesra1': beyt.mesra1,
                     'mesra2': beyt.mesra2, 'poet': beyt.poet, 'opening': beyt.opening, 'ending': beyt.ending,
                     'created_at': beyt.created_at}
        beyt_list.append(beyt_dict)
    return jsonify(beyt_list)


@app.route('/api/stories')
def json_stories():
    stories = Stories.query.order_by(func.rand()).limit(1)
    story_list = []
    for story in stories:
        story_dict = {'id': story.id, 'grade': story.grade, 'user_id': story.user_id, 'title': story.title,
                      'story': story.story, 'writer': story.writer, 'created_at': story.created_at}
        story_list.append(story_dict)
    return jsonify(story_list)


@app.route('/api/poems')
def json_poems():
    poems = Poems.query.order_by(func.rand()).limit(1)
    poem_list = []
    for poem in poems:
        poem_dict = {'id': poem.id, 'grade': poem.grade, 'user_id': poem.user_id,
                     'poet': poem.poet, 'created_at': poem.created_at, 'beyt1_1': poem.beyt1_1,
                     'beyt1_2': poem.beyt1_2, 'beyt2_1': poem.beyt2_1, 'beyt2_2': poem.beyt2_2, 'beyt3_1': poem.beyt3_1,
                     'beyt3_2': poem.beyt3_2, 'beyt4_1': poem.beyt4_1, 'beyt4_2': poem.beyt4_2}
        poem_list.append(poem_dict)
    return jsonify(poem_list)


@app.route('/api/speechs')
def json_speechs():
    speechs = Speechs.query.order_by(func.rand()).limit(1)
    speech_list = []
    for speech in speechs:
        speech_dict = {'id': speech.id, 'grade': speech.grade, 'user_id': speech.user_id, 'speech': speech.speech,
                       'wise': speech.wise, 'created_at': speech.created_at}
        speech_list.append(speech_dict)
    return jsonify(speech_list)


@app.route("/api/my_information")
@login_required
def my_information():
    usre = [{"id": current_user.id, "name": current_user.name, "username": current_user.username, "phone_email":current_user.phone_email}]
    return jsonify(usre)