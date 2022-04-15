#-*- coding:utf-8 -*-
from flask import Flask, request
import pymysql


db = pymysql.connect(host='127.0.0.1', port =3306, user = 'root', passwd = password, db = db_name, charset = 'utf8mb4')

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/insert_post_info', methods=['post'])
def insert_post_info():
    
    ret_msg = {
        'result': 'fail',
        'status': 0
    }
    community_id = request.form.get('community_id')
    brand_id = request.form.get('brand_id')
    post_id = request.form.get('post_id')
    post_title = request.form.get('title')
    post_content = request.form.get('content')
    post_dtime = request.form.get('d_time')
    
    cursor = db.cursor()

    sp = 'sp_insert_post'
    sp_args = (community_id, brand_id, post_id, post_title, post_content, post_dtime)
    
    is_suc = True

    try:
        sp_res = cursor.callproc(sp, sp_args)
        db.commit()
    except Exception as ex:
        is_suc = False
        msg = "apiserver, Exception {} call {}({})".format(ex, sp, sp_args)

    if is_suc:
        ret_msg["result"] = "success"
        ret_msg["status"] = 200
        ret_msg["detail"] = sp_res
    else:
        ret_msg["result"] = "fail"
        ret_msg["status"] = 500
        ret_msg["detail"] = msg
    
    return ret_msg

@app.route('/insert_comment_info', methods=['post'])
def insert_comment_info():
    
    ret_msg = {
        'result': 'fail',
        'status': 0
    }
    community_id = request.form.get('community_id')
    brand_id = request.form.get('brand_id')
    post_id = request.form.get('post_id')
    comment_id = request.form.get('comment_id')
    comment_content = request.form.get('comment_content')
    comment_dtime = request.form.get('d_time')
    
    cursor = db.cursor()

    sp = 'sp_insert_comment'
    sp_args = (community_id, brand_id, post_id, comment_id, comment_content, comment_dtime)
    
    is_suc = True

    try:
        sp_res = cursor.callproc(sp, sp_args)

        db.commit()
    except Exception as ex:
        is_suc = False
        msg = "apiserver, Exception {} call {}({})".format(ex, sp, sp_args)

    if is_suc:
        ret_msg["result"] = "success"
        ret_msg["status"] = 200
        ret_msg["detail"] = sp_res
    else:
        ret_msg["result"] = "fail"
        ret_msg["status"] = 500
        ret_msg["detail"] = msg
    
    return ret_msg

if __name__ == "__main__":
    app.run()
