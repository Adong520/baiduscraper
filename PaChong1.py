import requests
import time
from bs4 import BeautifulSoup
import logging
logging.basicConfig(level=logging.INFO)

def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        #r.encoding = r.apparent_encoding
        r.encoding = 'utf-8'
        return r.text
    except:
        return "ERROR"

def get_content(url):
    '''
    anaylize tieba and format content，
    :param url:
    :return:
    '''
    comments = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    liTags = soup.find_all('li', attrs={'class': ' j_thread_list clearfix'})

    for li in liTags:
        comment = {}
        try:
            # 【高淸】大爆炸1-11季。中英字。aa取
            comment['title']=li.find('a', attrs={'class':'j_th_tit'}).text.strip()

            #use [] for tag attribute
            comment['link']= "http://tieba.baidu.com" + li.find('a', attrs={'class':'j_th_tit'})['href']


            comment['name']=li.find('span', attrs={'class': 'tb_icon_author'}).text.strip()

            comment['time'] = li.find('span', attrs={'class': 'pull-right is_show_create_time'}).text.strip()

            comment['replyNum'] = li.find('span', attrs={'class': 'threadlist_rep_num center_text'}).text.strip()


            comments.append(comment)
        except:
            print('something wrong')
    return comments


def out2File(dict):
    '''
    write to file and save TTBT.txt
    :param dict:
    :return:
    '''
    with open('TTBT.txt', 'a+', encoding='gbk') as f:
        for comment in dict:
            '''
            print('comment[title]=', comment['title'])
            print('comment[link]=', comment['link'])
            print('comment[name]=', comment['name'])
            print('comment[time]=', comment['time'])
            print('comment[replyNum]=', comment['replyNum'])
            '''
            #logging.info('comment[title]= %s' % comment['title'])
            f.write('标题： {} \t 链接：{} \t 发帖人：{} \t 发帖时间：{} \t 回帖数量： {} \n'.format(
                comment['title'], comment['link'], comment['name'], comment['time'], comment['replyNum']))
        print('finish')

def main(base_url, deep):
    url_list=[]

    #store all url in list
    for i in range(0, deep):
        url_list.append(base_url + '&pn=' + str(50*i))
    print('all web pages are downloaded to local, begin to picking information....')

    for url in url_list:
        content = get_content(url)
        out2File(content)
    print("all content saved")

base_url = 'http://tieba.baidu.com/f?kw=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&ie=utf-8'

deep = 3

if __name__ == '__main__':
    main(base_url,deep)








