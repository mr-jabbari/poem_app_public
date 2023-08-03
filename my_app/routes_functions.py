from flask import request, redirect
from flask_login import login_required, current_user
from my_app import db, app
from my_app.models import Beyts, Poems, Speechs, Stories


@app.route('/likebeyt_action/<int:beyt_id>/<action>')
@login_required
def likebeyt_action(beyt_id, action):
    beyt = Beyts.query.filter_by(id=beyt_id).first_or_404()
    if action == 'like':
        current_user.beyt_like(beyt)
        db.session.commit()
    if action == 'unlike':
        current_user.beyt_unlike(beyt)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/likepoem_action/<int:poem_id>/<action>')
@login_required
def likepoem_action(poem_id, action):
    poem = Poems.query.filter_by(id=poem_id).first_or_404()
    if action == 'like':
        current_user.poem_like(poem)
        db.session.commit()
    if action == 'unlike':
        current_user.poem_unlike(poem)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/likespeech_action/<int:speech_id>/<action>')
@login_required
def likespeech_action(speech_id, action):
    speech = Speechs.query.filter_by(id=speech_id).first_or_404()
    if action == 'like':
        current_user.speech_like(speech)
        db.session.commit()
    if action == 'unlike':
        current_user.speech_unlike(speech)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/likestory_action/<int:story_id>/<action>')
@login_required
def likestory_action(story_id, action):
    story = Stories.query.filter_by(id=story_id).first_or_404()
    if action == 'like':
        current_user.story_like(story)
        db.session.commit()
    if action == 'unlike':
        current_user.story_unlike(story)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/bookmarkbeyt_action/<int:beyt_id>/<action>')
@login_required
def bookmarkbeyt_action(beyt_id, action):
    beyt = Beyts.query.filter_by(id=beyt_id).first_or_404()
    if action == 'bookmark':
        current_user.beyt_bookmark(beyt)
        db.session.commit()
    if action == 'unbookmark':
        current_user.beyt_unbookmark(beyt)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/bookmarkpoem_action/<int:poem_id>/<action>')
@login_required
def bookmarkpoem_action(poem_id, action):
    poem = Poems.query.filter_by(id=poem_id).first_or_404()
    if action == 'bookmark':
        current_user.poem_bookmark(poem)
        db.session.commit()
    if action == 'unbookmark':
        current_user.poem_unbookmark(poem)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/bookmarkspeech_action/<int:speech_id>/<action>')
@login_required
def bookmarkspeech_action(speech_id, action):
    speech = Speechs.query.filter_by(id=speech_id).first_or_404()
    if action == 'bookmark':
        current_user.speech_bookmark(speech)
        db.session.commit()
    if action == 'unbookmark':
        current_user.speech_unbookmark(speech)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/bookmarkstory_action/<int:story_id>/<action>')
@login_required
def bookmarkstory_action(story_id, action):
    story = Stories.query.filter_by(id=story_id).first_or_404()
    if action == 'bookmark':
        current_user.story_bookmark(story)
        db.session.commit()
    if action == 'unbookmark':
        current_user.story_unbookmark(story)
        db.session.commit()
    return redirect(request.referrer)


@app.route('/delete_beyt_action/<int:beyt_id>/<action>')
@login_required
def delete_beyt_action(beyt_id, action):
    beyt = Beyts.query.filter_by(id=beyt_id).first_or_404()
    if beyt and action == 'delete':
        Beyts.query.filter_by(user_id=current_user.id, id=beyt.id).delete()
        db.session.commit()
    return redirect(request.referrer)


@app.route('/delete_poem_action/<int:poem_id>/<action>')
@login_required
def delete_poem_action(poem_id, action):
    poem = Poems.query.filter_by(id=poem_id).first_or_404()
    if poem and action == 'delete':
        Poems.query.filter_by(user_id=current_user.id, id=poem.id).delete()
        db.session.commit()
    return redirect(request.referrer)


@app.route('/delete_speech_action/<int:speech_id>/<action>')
@login_required
def delete_speech_action(speech_id, action):
    speech = Speechs.query.filter_by(id=speech_id).first_or_404()
    if speech and action == 'delete':
        Speechs.query.filter_by(user_id=current_user.id, id=speech.id).delete()
        db.session.commit()
    return redirect(request.referrer)


@app.route('/delete_story_action/<int:story_id>/<action>')
@login_required
def delete_story_action(story_id, action):
    story = Stories.query.filter_by(id=story_id).first_or_404()
    if story and action == 'delete':
        Stories.query.filter_by(user_id=current_user.id, id=story.id).delete()
        db.session.commit()
    return redirect(request.referrer)