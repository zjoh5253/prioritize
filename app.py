#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, redirect, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os

import pyrebase

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
# db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''

#----------------------------------------------------------------------------#
# FB Config.
#----------------------------------------------------------------------------#

# Add your DB information here

config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "storageBucket": ""
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return redirect(url_for('bugs'))

# features


@app.route('/features')
def features():
    features = db.child("features").get().val()
    return render_template('pages/features.html', features=features)


@app.route('/add-feature', methods=['GET', 'POST'])
def add_feature():
    if request.method == 'POST':
        try:
            print("inside try")

            title = request.form['title']
            description = request.form['description']

            data = {
                "title": title,
                "description": description,
                "vote": 1
            }

            print("saving data")
            db.child("features").push(data)
            print("data saved")

            return redirect(url_for('features'))

        except Exception as e:
            print(e)
            return redirect(url_for('features'))

    return redirect(url_for('features'))


@app.route('/remove-feature', methods=['GET', 'POST'])
def remove_feature():
    id = request.args.get("id")

    if request.method == 'POST':
        try:
            print("inside try")

            print("deleting")
            db.child("features").child(id).remove()
            print("successfully deleted")

            return redirect(url_for('features'))

        except Exception as e:
            print(e)
            return redirect(url_for('features'))

    return redirect(url_for('features'))


# Bugs

@app.route('/bugs')
def bugs():
    bugs = db.child("bugs").get().val()
    return render_template('pages/bugs.html', bugs=bugs)


@app.route('/add-bug', methods=['GET', 'POST'])
def add_bug():
    if request.method == 'POST':
        try:
            print("inside try")

            title = request.form['title']
            description = request.form['description']

            data = {
                "title": title,
                "description": description,
                "vote": 1
            }

            print("saving data")
            db.child("bugs").push(data)
            print("data saved")

            return redirect(url_for('bugs'))

        except Exception as e:
            print(e)
            return redirect(url_for('bugs'))

    return redirect(url_for('bugs'))


@app.route('/remove-bug', methods=['GET', 'POST'])
def remove_bug():
    id = request.args.get("id")
    if request.method == 'POST':
        try:
            print("inside try")

            print("deleting")
            db.child("bugs").child(id).remove()
            print("successfully deleted")

            return redirect(url_for('bugs'))

        except Exception as e:
            print(e)
            return redirect(url_for('bugs'))
    return redirect(url_for('bugs'))


@app.route('/upvote', methods=['POST'])
def upvote():
    if request.method == 'POST':
        if request.args.get("type") == 'bug':
            try:
                print("inside try")

                current_vote = db.child("bugs").child(
                    request.args.get("id")).child("vote").get().val()

                new_vote = current_vote + 1

                print("upvoting")
                db.child("bugs").child(
                    request.args.get("id")).update({"vote": new_vote})
                print("success")

                return redirect(url_for('bugs'))

            except Exception as e:
                print(e)
                return redirect(url_for('bugs'))

        else:
            try:
                print("inside try")

                current_vote = db.child("features").child(
                    request.args.get("id")).child("vote").get().val()

                new_vote = current_vote + 1

                print("upvoting")
                db.child("features").child(
                    request.args.get("id")).update({"vote": new_vote})
                print("success")

                return redirect(url_for('bugs'))

            except Exception as e:
                print(e)
                return redirect(url_for('bugs'))
    return redirect(url_for('bugs'))


@app.route('/downvote', methods=['POST'])
def downvote():
    if request.method == 'POST':
        if request.args.get("type") == 'bug':
            try:
                print("inside try")

                current_vote = db.child("bugs").child(
                    request.args.get("id")).child("vote").get().val()

                new_vote = current_vote - 1

                print("downvoting")
                db.child("bugs").child(
                    request.args.get("id")).update({"vote": new_vote})
                print("success")

                return redirect(url_for('bugs'))

            except Exception as e:
                print(e)
                return redirect(url_for('bugs'))

        else:
            try:
                print("inside try")

                current_vote = db.child("features").child(
                    request.args.get("id")).child("vote").get().val()

                new_vote = current_vote - 1

                print("downvoting")
                db.child("features").child(
                    request.args.get("id")).update({"vote": new_vote})
                print("success")

                return redirect(url_for('bugs'))

            except Exception as e:
                print(e)
                return redirect(url_for('bugs'))
    return redirect(url_for('bugs'))


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    id = request.args.get("id")
    print(id)
    
    type = request.args.get("type")
    print(type)

    if type == 'feature':
        content = db.child("features").child(id).get().val()
    else:
        content = db.child("bugs").child(id).get().val()

    if request.method == 'POST':

        try:
            print("inside try")

            title = request.form['title']
            description = request.form['description']
            vote = content['vote']

            data = {
                "title": title,
                "description": description,
                "vote": vote
            }

            if type == 'feature':
                db.child("features").child(id).update(data)
                return redirect(url_for('features'))
            else:
                db.child("bugs").child(id).update(data)
                return redirect(url_for('bugs'))

        except Exception as e:
            print(e)
            error = e
            return render_template('pages/edit.html', type=type, id=id, error=error, content=content)

    return render_template('pages/edit.html', type=type, id=id, content=content)


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
