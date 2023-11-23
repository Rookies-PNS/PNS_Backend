from datetime import datetime

from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.utils import redirect

from Domains.Entities import Post,PostVO, SimplePost
from Applications.Usecases import GetPostList, GetPost, CreatePost
from Infrastructures.IOC import get_user_storage, get_post_storage

from Services.Flask.Models import post_to_dict, posts_to_dicts
from Services.Flask.Views.forms import PostForm

bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route('/list/<int:page>')
def _list(page):
    serivce = GetPostList(get_post_storage())
    post_list = posts_to_dicts(serivce.get_list_no_filter(page-1))
    
    if page > 1 and len(post_list)==0:# 넘치는 페이지를 요청할 경우
        return redirect(url_for("post._list", page=1))
    else:# 정상 요청
       return render_template('post/post_list.html', post_list=post_list)


@bp.route('/detail/<int:post_id>/')
def detail(post_id):
    service = GetPost(get_post_storage())
    match  service.get_post_from_post_id(post_id):
        case post if isinstance(post, PostVO):
            post = post_to_dict(post)
            return render_template('post/post_detail.html', post=post)
        case _:
            return redirect(url_for('post._list'), page=1)



@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = PostForm()

    if request.method == 'POST' and form.validate_on_submit():
        service  = CreatePost(get_post_storage(), get_user_storage)
        post = service.create(form.subject.data, form.content.data)
        return redirect(url_for('main.index'))

    return render_template('post/post_form.html', form=form)
