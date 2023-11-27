from flask import Blueprint, redirect, render_template, request, url_for, session, flash
from werkzeug.utils import redirect
from Commons import PostId

from Domains.Entities import Post,PostVO, SimplePost
from Applications.Usecases import GetPostList, GetPost, CreatePost, DeletePost
from Applications.Results import Result, Fail
from Infrastructures.IOC import get_user_storage, get_post_storage

from Services.Flask.Models import post_to_dict, posts_to_dicts, dict_to_user
from Services.Flask.Views.forms import PostForm

from icecream import ic
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
        service  = CreatePost(get_post_storage(), get_user_storage())
        if "user" in session:
            ic()
            ic(session["user"])
            user = dict_to_user(session["user"])
        else:
            user = None
        match service.create(form.subject.data, form.content.data,user=user):
            case post if isinstance(post, SimplePost):
                return redirect(url_for('main.index'))
            case Fail(type=type):
                ic()
                ic(type, "NotImplementedError")
            case _:
                ic()
                pass

    return render_template('post/post_form.html', form=form)
    

# @bp.route('/delete/<int:post_id>/', methods=['POST'])
# def delete(post_id):
#     service = DeletePost(get_post_storage(), get_user_storage())
#     if "user" in session:
#         user = dict_to_user(session["user"])
#     else:
#         user = None
#     match service.delete(post_id, user):
#         case id if isinstance(id, PostId):
#             return redirect(url_for('post._list', page=1))
#         case Fail(type=type):
#             ic()
#             ic(type, "NotImplementedError")
#         case _:
#             ic()
#             pass
