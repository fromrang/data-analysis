import requests

base_url = 'http://127.0.0.1:5000'

def insert_post_info(community_id, brand_id, post_id, title, post_content, date_time):
    
    url = base_url + '/insert_post_info'
    data = {
        'community_id': community_id,
        'brand_id': brand_id,
        'post_id': post_id,
        'title': title,
        'content': post_content,
        'd_time': date_time
        }
    try:
        res = requests.post(url, data = data, verify=False, timeout= 300)
        if res.json()['status'] == 200:
            print('[SUCCESS] api insert complete')
    except Exception as ex: 
        print('[FAIL] {} api insert fail'.format(url), ex)
    
def insert_comment_info(community_id, brand_id, post_id, comment_id, comment_content, date_time):
    
    url = base_url + '/insert_comment_info'
    data = {
        'community_id': community_id,
        'brand_id': brand_id,
        'post_id': post_id,
        'comment_id': comment_id,
        'comment_content': comment_content,
        'd_time': date_time
        }
    try:
        res = requests.post(url, data = data, verify=False, timeout= 300)
        if res.json()['status'] == 200:
            print('[SUCCESS] api insert complete')
    except Exception as ex:
        print('[FAIL] {} api insert fail'.format(url), ex)