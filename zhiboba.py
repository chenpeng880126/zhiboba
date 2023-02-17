import time

import requests
import json
import datetime
from bs4 import BeautifulSoup


# 获取页面
def get_page(link):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    r = requests.get(link, headers=headers)
    html = r.content
    html = html.decode('UTF-8')
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_pl_count(link):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    r = requests.get(link, headers=headers)
    if r.status_code == 404:
        return 0
    return int(r.json()['all_num'])


def get_page_data(soup):
    t_controller = soup.find('div', class_='title')
    print(t_controller.text)


def analysis_zhiboba(json_obj, end_time):
    all_post = []
    for i in json_obj['news']:
        if i['type'] == 'nba':
            c_t = i['createtime']
            create_time = datetime.datetime.strptime(c_t, "%Y-%m-%d %H:%M:%S")
            if create_time > end_time:
                all_post.append(i)
                #print("%s,%s,%s" % (i['createtime'],i['title'],"https://news.zhibo8.cc"+i['url']))
    all_post.sort(key=lambda s: s['createtime'], reverse=True)

    pl_url_temp = 'https://cache.zhibo8.cc/json/[page]_count.htm'
    for p in all_post:
        #print("https://news.zhibo8.cc"+p['url'])
        pl_url = pl_url_temp.replace('[page]', p['pinglun'].replace('-', '/'))
        #print(pl_url)
        p['pl_count'] = get_pl_count(pl_url)
        time.sleep(3)
        print("%s,%s,%d,%s" % (p['createtime'], p['title'], p['pl_count'], "https://news.zhibo8.cc" + p['url']))

    #all_post.sort(key=lambda s: s['createtime'], reverse=True)
    #for j in all_post:
    #    print("%s,%s,%d,%s" % (j['createtime'], j['title'], j['pl_count'], "https://news.zhibo8.cc"+j['url']))


if __name__ == '__main__':
    t1 = "2023-02-16 15:58:29"
    t1_datetime = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S")
    url = 'https://m.zhibo8.cc/json/hot/24hours.htm'
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
    r = requests.get(url, headers=headers)
    analysis_zhiboba(r.json(), t1_datetime)

    #test
    '''
    with open('data/zhiboba1', "w+", encoding="utf-8") as f:
        f.write(str(r.json()))
    with open('data/zhiboba1', "r+", encoding="utf-8") as f:
        news24_json = json.loads(f.read(), encoding="utf-8")
        #for k in news24_json:
        #    print(k)
        analysis_zhiboba(news24_json, t1_datetime)
    '''