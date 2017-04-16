# -*- coding:utf-8 -*-
#多线程 爬取斗图网

import requests
import threading #多线程处理
from lxml import etree #解析网页 比html.praser快
from bs4 import BeautifulSoup

#打开源码
def get_html(url):
    # url="https://www.doutula.com/article/list/?page=1"
    headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    request=requests.get(url=url,headers=headers)
    response=request.content
    return response  #源码

#从主页获取内页的url
def get_img_html(html):
    soup = BeautifulSoup(html,'lxml') #创建一个对象
    all_a=soup.find_all('a',class_='list-group-item')
    for i in all_a:
        img_html=get_html(i['href'])#找到超链接
        get_img(img_html)
#获取每个图片
def get_img(html):
    soup=etree.HTML(html) #初始化打印源码
    items=soup.xpath('//div[@class="artile_des"]')#解析网页方式 选定盒子方式
    for item in items:
        imgurl_list=item.xpath('table/tbody/tr/td/a/img/@onerror')
        start_save_image(imgurl_list)
#下载图片
# x=1
def save_img(img_url):
    # global x
    # x+=1
    img_url= img_url.split('=')[-1][1:-2].replace('jp','jpg')
    print u'正在下载'+'http:'+img_url
    img_content=requests.get('http:'+img_url).content
    with open('doutu/%s' % img_url.split('/')[-1],'wb') as f:
        f.write(img_content)

#多线程
def start_save_image(imgurl_list):
    for i in imgurl_list:
        th=threading.Thread(target=save_img,args=(i,))
        th.start()

#多页
def main():
    start_url="https://www.doutula.com/article/list/?page="
    for i in range(1,2):
        start_html=get_html(start_url.format(i))#获取外页的url
        get_img_html(start_html)# 获取内页url里面的源码

if __name__ == '__main__': #判断文件入口
    main()


