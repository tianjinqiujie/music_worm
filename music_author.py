import requests
import re


# 爬取网易歌手名单
class SingerSpider(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.181 Safari/537.36'
        }


    # 请求模块
    def get_index(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                self.parse_re(resp.text)
            else:
                print('error')
        except ConnectionError:
            self.get_index(url)


    #  解析模块
    def parse_re(self, resp):
        tags = re.findall(r'<a href=".*?/artist\?id=\d+" class="nm nm-icn f-thide s-fc0" title=".*?的音乐">(.*?)</a>',resp, re.S)
        for tag in tags:
            self.save_csv(tag)


    #  存储模块
    def save_csv(self, tag):
        with open('all_singer.csv', 'a+' , encoding='utf-8') as f:
            f.write(tag+'\n')


if __name__ == '__main__':
    # 歌手分类id
    id = [1001, 1002, 1003, 2001, 2002, 2003, 6001, 6002, 6003, 7001, 7002, 7003, 4001, 4002, 4003]
    # initial的值
    initial_list = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 0]
    for i in id:
        for j in initial_list:
            url = 'http://music.163.com/discover/artist/cat?id=' + str(i) + '&initial=' + str(j)
            print('start spider {}'.format(url))
            SingerSpider().get_index(url)