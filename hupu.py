import requests
from bs4 import BeautifulSoup
import time
import datetime
import json
import re


# 获取页面
def get_page(link):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    r = requests.get(link, headers=headers)
    html = r.content
    html = html.decode('UTF-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_hot_data(soup, end_time):
    # 回复数r_quantity 浏览量v_quantity 作者p_auth 发布时间p_time 标题p_title 链接p_href
    lis = soup.find_all('li', class_='bbs-sl-web-post-body')
    all_post = []
    for li in lis:
        p_time = li.find('div', class_='post-time').text
        #print(p_time)
        p_datetime = datetime.datetime.strptime(p_time, "%m-%d %H:%M")
        if p_datetime < end_time:
            continue
        r_v = li.find('div', class_='post-datum').text
        r_quantity = int(r_v.split('/')[0].strip())
        v_quantity = int(r_v.split('/')[1].strip())
        r_v_rate = round((r_quantity/v_quantity)*1000, 2)
        p_auth = li.find('div', class_='post-auth').text
        p_title = li.find('a', class_='p-title').text
        p_href = li.find('a', class_='p-title')['href']
        post = {
            'p_time': p_time,
            'p_title': p_title,
            'r_v_rate': r_v_rate,
            'r_quantity': r_quantity,
            'p_href': 'https://bbs.hupu.com' + p_href,
            'v_quantity': v_quantity,
            'p_auth': p_auth,
        }
        all_post.append(post)
    return all_post


def get_article_data(soup):
    post_detail = {}
    main_post = soup.find('div', class_='main-post-info')
    main_post_text = main_post.find('div', class_='thread-content-detail').text
    # print(main_post_text)
    main_post_summary = main_post.find('div', class_='post-operate-comp-main').text
    tjs = re.findall(r'推荐.*\((\d+)\).*评论', main_post_summary)
    tj = int(tjs[0])
    # print(tj)
    post_detail['text'] = main_post_text
    post_detail['tj'] = tj
    # main-post-info
    # thread-content-detail

    reply_details = []
    reply_lists = soup.find_all('div', class_='post-reply-list-content')
    r_limited = len(reply_lists) if len(reply_lists) < 15 else 15
    for i in range(0, r_limited):
        rl = reply_lists[i]
        t_c_d = rl.find('div', class_='thread-content-detail').text
        # print(t_c_d)
        lls = re.findall(r'亮了\((\d+)\)回复', rl.text)
        ll = int(lls[0])
        # print(ll)
        rp_content = {'reply': t_c_d, 'll': ll}
        # print(rp_content)
        reply_details.append(rp_content)
    post_detail['reply'] = reply_details
    return post_detail


def get_hot_data_test(link,end_time):
    #回复数r_quantity 浏览量v_quantity 作者p_auth发布时间p_time 标题p_title 链接p_href
    with open(link, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')
    return get_hot_data(soup, end_time)


def get_article_data_test(link):
    with open(link, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')
    return get_article_data(soup)


def analysis_data(all_post):
    print(all_post)
    #all_post.sort(key=lambda s: s['r_v_rate'], reverse=True)
    all_post.sort(key=lambda s: s['p_time'])
    print(all_post)


if __name__ == '__main__':

    t1 = "02-16 13:27"
    t1_datetime = datetime.datetime.strptime(t1, "%m-%d %H:%M")
    url1 = "https://bbs.hupu.com/502-hot"
    all_post = get_hot_data(get_page(url1), t1_datetime)
    all_post.sort(key=lambda s: s['p_time'], reverse=True)
    for p in all_post:
        p_href = p['p_href']
        post_detail = get_article_data(get_page(p_href))
        p.update(post_detail)
        time.sleep(2)
        print("%s,%s,%s,%s,%s" % (p['p_time'],p['p_title'],p['r_v_rate'],p['tj'],p['p_href']))

    #print(all_post)


    #url2 = "D:/Python_Study/zhiboba/data/test4_2.html"
    #print(get_article_data_test(url2))

    #url1 = "D:/Python_Study/zhiboba/data/test3.html"
    #all_post = get_page_data_test(url1, t1_datetime)


   #analysis_data(all_post)
    #compare_time()

    #s1 = get_page(url1)
    #with open("data/test2.html", "w", encoding="utf-8") as f:
    #    f.write(s1.text)
    '''
    response = requests.get(url1)
    with open("data/test1.html", "w", encoding="utf-8") as f:
        f.write(response.text)
        
    '''
    #print("ok")
    #hupu_url = "https://bbs.hupu.com/57932440.html"
    #print(get_page(hupu_url))
