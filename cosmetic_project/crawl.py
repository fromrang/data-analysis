import db_insert


def insert(result):

    # f = open('test.txt', 'a', encoding='utf8')
    # f.write(str(result)+'\n')
    # f.close()

    #게시글 데이터 인서트
    db_insert.insert_post_info(result['community_id'], result['brand_id'], result['post_id'], result['post_title'], result['post_content'], result['post_time'])

    #댓글 데이터 인서트
    for i in result['comment']:

        db_insert.insert_comment_info(result['community_id'], result['brand_id'], result['post_id'], i['comment_id'], i['comment_content'], i['comment_date'])
