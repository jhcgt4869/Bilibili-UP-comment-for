'''
https://api.bilibili.com/x/v1/dm/list.so?oid=837806779弹幕api
https://api.bilibili.com/x/v2/reply?type=1&oid=837806779&&pn=1评论api
弹幕只能够用oid，目前抓包未在到oid集中出现地址
bug:部分网站没有那么严格按照['data']['replies']['content']['message']的顺序来
'''
import requests
from bs4 import BeautifulSoup
import re
import json


# kv = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"}
def Gethtml(url):  # 获取网页
    kv = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"}
    r = requests.get(url, headers=kv)
    # print(r.text)
    r.encoding = r.apparent_encoding
    # print(r.text)
    return r.text


# 获取up的uid
def u_id(uid_html):
    # url = f"https://search.bilibili.com/all?keyword={name}"
    # r = Gethtml(url)
    # print(r)
    # r = requests.get(url, headers=kv)
    html = BeautifulSoup(uid_html, 'lxml')
    # print(html)
    uid = html.find(name='a', attrs={"class": "title"})
    # print(uid)
    # uid = '<a class="title" href="//space.bilibili.com/390461123?from=search" target="_blank" title="徐大sao">徐大sao</a>'
    uid = re.findall(r'<a.*?href="//space.bilibili.com/(.+)f.*', str(uid))
    uid = uid[0][:-1]
    print('以获取up主的id为', uid)
    return uid


def a_id(aid_html):
    videos = json.loads(aid_html)
    # print(videos)
    videos_lists = videos['data']['list']['vlist']
    aid_list = []
    for videos_list in videos_lists:
        aid = videos_list['aid']
        aid_list.append(aid)
    print('已获得视频id长度为：', len(aid_list))
    return aid_list


def comment_save(name, comment_html):
    videos = json.loads(comment_html.text)
    videos_lists = videos['data']['replies']  # ['replies']['content']
    # print(videos_lists)
    bvid_list = []
    if videos_lists:
        for videos_list in videos_lists:
            bvid = videos_list['content']['message']
            bvid_list.append(bvid)
            print(bvid_list)
            with open(f'{name}.txt', 'a+', encoding='utf-8') as f:
                f.write(bvid)

    print('提取完毕！')


def main(name):
    # 获得阿婆主的id
    url_uid = f"https://search.bilibili.com/all?keyword={name}"
    uid_html = Gethtml(url_uid)
    uid = u_id(uid_html)
    # print(uid)

    # 循环获取至少9页的视频（不一定有那么多）
    for i in range(1, 10):
        aid_url = f"https://api.bilibili.com/x/space/arc/search?mid={uid}&ps=30&tid=0&pn={i}&keyword=&order=pubdate&jsonp=jsonp"
        aid_html = Gethtml(aid_url)
        aid_list = a_id(aid_html)
        # print(aid_list)

        # 获取保存评论
        for j in range(len(aid_list)):
            for i in range(1, 15):
                comment_uil = f"https://api.bilibili.com/x/v2/reply?type=1&oid={aid_list[j]}&&pn={i}"
                comment_html = requests.get(comment_uil)
                comment_save(name, comment_html)

            # print(comment_html)


main('共青团中央')
# 贤宝宝baby
# 老师好我叫何同学
# 大祥哥来了
# 女胖胖
# 记录生活的蛋黄派
