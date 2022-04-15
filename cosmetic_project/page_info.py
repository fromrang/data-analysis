from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import time
import random

import html_info
from keyword_category import peripera_categorylist, clio_categorylist, espoir_categorylist
import crawl

def title_url(url):
    
    time.sleep(random.randrange(0,3))
    
    _html = html_info.Crawl(url)
    html = _html.html_request

    soup = BeautifulSoup(html, "html.parser")
    
    td_tag = soup.find_all('td', {'class': 'title'})
    
    a_tag_list = []
    
    for td_title in td_tag:
        a_tag = td_title.find('a').attrs['href']
        if a_tag.startswith('/index'):
            a_tag_list.append(a_tag)
        else:
            pass
    return a_tag_list

def post_info(url):

    _html = html_info.Crawl(url)
    html = _html.html_selenium

    if html is not None:
        
        soup = BeautifulSoup(html, "html.parser")
        
        result = {'community_id':0, 'brand_id':0, 'post_id': None, 'post_title':None, 'post_time': None, 'post_content' : None, 'comment': []}
                
        title = soup.find('span', {'class':'title'}).get_text(strip=True)
        all_post_content = soup.find('article',{'itemprop':'articleBody'}).get_text('|', strip=True)
        all_comment_content = soup.find('ul',{'class':'fdb_lst_ul'}).get_text(strip=True)

        #게시글 부분
        post_time = soup.find('div', {'class':'side fr'}).get_text(strip=True)
        dateformatter = "%Y.%m.%d %H:%M"
        post_time = datetime.strptime(post_time, dateformatter)

        post_id = url.split("document_srl=")[1]    
        post_content_list = all_post_content.split('|')
        
        post_content = ''
        
        for _post_content in post_content_list:
            if _post_content.startswith('http') == False:
                post_content += _post_content 
        
        result['post_id'] = post_id
        result['post_title'] = title
        result['post_time'] = str(post_time)
        result['post_content'] = post_content
            
        #댓글 부분

        all_comment_tag = soup.find_all('li', {'class':'fdb_itm clear'})
        
        for comment_tag in all_comment_tag:
            
            content_dic = {'comment_id':None, 'comment_content': None, 'comment_date': None}
            
            comment_date  = comment_tag.find('span', {'class':'date'}).get_text(strip=True)
            dateformatter = "%Y-%m-%d %H:%M:%S"
            comment_date = datetime.strptime(comment_date, dateformatter)
            
            comment = comment_tag['id']
            comment_content = soup.find('div', {'class': comment + '_0 xe_content'}).get_text('',strip=True)
            
            if '비회원은 작성한 지 1시간 이내의 댓글은 읽을 수 없습니다.' not in comment_content:
                content_dic['comment_id'] = comment.split('_')[1]
                content_dic['comment_content'] = comment_content
                content_dic['comment_date'] = str(comment_date)
            
                result['comment'].append(content_dic)

        #페리페라
        for peripera_category in peripera_categorylist:
            if peripera_category in (title + all_post_content.replace(' ','')+all_comment_content):
                result['brand_id'] = 1
        #클럽 클리오
        for clio_category in clio_categorylist:
            if clio_category in (title + all_post_content.replace(' ','')+all_comment_content):
                result['brand_id'] = 2
        #에스쁘아
        for espoir_category in espoir_categorylist:
            if espoir_category in (title + all_post_content.replace(' ','')+all_comment_content):
                result['brand_id'] = 3

        if result['post_id'] is not None:
            return result



def run():
    
    for i in range(10, 5000):

        url = "https://theqoo.net/index.php?mid=beauty&filter_mode=normal&page={}".format(i)
        
        outside_url_list = title_url(url)
        
        for _, outside_url in enumerate(outside_url_list):
            
            final_url = 'https://theqoo.net' + outside_url
            
            result = post_info(final_url)
            
            if result != None:
                crawl.insert(result)


if __name__ == "__main__":
    run()




