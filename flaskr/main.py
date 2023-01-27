from os import access
from threading import currentThread

from flask import render_template, request, redirect, abort
from flask_login import login_user, logout_user, login_required, current_user
import traceback

# from werkzeug.security import generate_password_hash, check_password_hash

from flaskr import app, APP_NAME
from . import User
from . import db
from . import login_manager

from flaskr import controller_helper as helper
from .oauth import oauth_twitter_oauth1session as oauth_twitter

@app.route('/')
def home():
    try:
        return render_template('views/index.html', title=helper.title('トップページ | '))
    except:
        abort(500)


# Twitter認証

# 「Twitterでログイン」ボタンから遷移
# Twitter認証画面へリダイレクト
@app.route('/twitter-login', methods=['GET'])
def twitter_login():
    oauth_url = oauth_twitter.create_authorization_url()
    return redirect(oauth_url)

# Twitter認証画面からコールバック
@app.route('/twitter-callback')
def twitter_callback():
    oauth_denied = request.args.get('denied')
    if oauth_denied:
        # 認証失敗
        return redirect('/?login-failed=1')
    # 認証成功
    access_token_content = oauth_twitter.fetch_access_token_content(request.url)
    
    # 認証したユーザーでログイン
    # 未登録なら登録
    user_profile = oauth_twitter.fetch_profile_by_id(access_token_content['user_id']).json()
    user = User.query.filter_by(tw_id=user_profile['data']['id']).first()
    bigger_image = user_profile['data']['profile_image_url'].replace('_normal', '_bigger')
    if user == None:
        # ユーザー登録
        user = User(
            tw_id=user_profile['data']['id'],
            tw_screen_id=user_profile['data']['username'],
            tw_name=user_profile['data']['name'],
            tw_description=user_profile['data']['description'],
            tw_protected=user_profile['data']['protected'],
            tw_profile_image_url=bigger_image,
            tw_access_token=access_token_content['oauth_token'],
            tw_access_token_secret=access_token_content['oauth_token_secret']
        )
        db.session.add(user)
        db.session.commit()
    else:
        # ユーザー情報更新
        user.tw_screen_id = user_profile['data']['username']
        user.tw_name = user_profile['data']['name']
        user.tw_description = user_profile['data']['description']
        user.tw_protected = user_profile['data']['protected']
        user.tw_profile_image_url = bigger_image
        user.tw_access_token = access_token_content['oauth_token']
        user.tw_access_token_secret = access_token_content['oauth_token_secret']
        db.session.add(user)
        db.session.commit()
    login_user(user)
    # プロフィール作成ページにリダイレクト
    return redirect('/edit-profile')
    
@app.route('/user-logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/-/about')
def about():
    return render_template('views/about.html', title=helper.title('使い方 | '))

@app.route('/<tw_screen_id>', methods=['GET'])
def show_profile(tw_screen_id):
    """
    ユーザープロフィールを表示
    """
    print('@update')
    user: User = User.search_by_tw_screen_id(tw_screen_id=tw_screen_id)
    if user == None:
        return render_template(
            'views/profile_not_found.html',
            title=helper.title('ユーザーが見つかりません | '),
            target_id=tw_screen_id
        )
    else:
        return render_template(
            'views/show.html',
            title=helper.title(user.tw_name + 'のプロフィール | '),
            user=user
        )

@app.route('/edit-profile', methods=['GET'])
# @login_required
def edit_get():
    return render_template('views/edit.html', title=helper.title('プロフィール作成 | '))

@app.route('/edit-profile', methods=['POST'])
@login_required
def edit_post():
    profile_text = request.form.get('profile_text')
    if profile_text == None:
        profile_text = ''
    user = User.search_by_id(id=current_user.id)
    user.profile_text = profile_text
    db.session.add(user)
    db.session.commit()
    return redirect('/' + current_user.tw_screen_id)

# @app.route('/<id>/delete', methods=['GET'])
# @login_required
# def delete(id):
#     post = Post.query.get(id)
    
#     db.session.delete(post)
#     db.session.commit()
#     return redirect('/')

# load_user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('views/error/internal_server_error.html')