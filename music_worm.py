import requests
import json


# 爬取网易音乐
class Singlereptile(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control':'no-cache',
            'Pragma':'no-cache',
            'Upgrade-Insecure-Requests':'1',
            # 'Content-Length': '20',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'moresound.tk',
            # 'Origin': 'http://moresound.tk',
            'Proxy-Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'Tip_of_the_day=2; encrypt_data=b977d6c5f602cd5505e3c7b0ae3129f9a986c1708c9a4e31faf9e4caa0130e27eafd302c1a49b5786605086cfad1ed8d54907becd36e9b130672c7ce9798485eac79787de56e727bb45b56dfcae11187fbe8dfd9524e2bcd05e38df9e719a967d231a5c0926d85c5a17a4f925b0c37319e894f729c1fb96358792106494a410c; _omappvp=uQ1fGK1KnDXM9BqBEicAGOzpIz6Px0QDp038GnN1JnACAUB2S1CwWdh0TpaB0QOPhMsI58wlN0nUl6VvSqAORTlu6Q1KVXeb',
        }
        self.url = 'http://moresound.tk/music/'
        self.search = 'api.php?search=wy'
        self.get_song = 'api.php?get_song=wy'


    # 请求模块
    def get_index(self):
        page = 1
        f = open('all_singer.csv', 'r', encoding='utf-8')
        for author_bak in f:
            flag = True
            author = author_bak[:-1]
            # search =
            # get_song =
            # author = '许嵩'
            while flag:
                s = {'w': author, 'p': page, 'n': 20}
                # {"page": 1981, "num": "20", "totalnum": 0, "code": 0}
                page += 1
                resp = requests.post(self.url + self.search, headers = self.headers, data=s)
                print(resp.text)
                if resp.status_code == 200:
                    data = json.loads(resp.text).get('song_list')
                    if not data:
                        page = 1
                        flag = False
                        continue
                    for i in data:
                        number = i.get('songmid')
                        print(number)
                        dic = {'mid': number}
                        self.get_music(dic, author)
        f.close()


    # 得到音乐路径
    def get_music(self,dic,author):
        response = requests.post(self.url + self.get_song, headers=self.headers, data=dic)
        print(response.text)
        if response.status_code == 200:
            music_obj = json.loads(response.text)
            music_name = music_obj.get('album')
            flac = music_obj.get('url').get('FLAC')
            mp3 = music_obj.get('url').get('320MP3')
            # print(flac)
            if flac:
                req = requests.get(self.url + flac, headers=self.headers)
                suf = '.flac'

            else:
                req = requests.get(self.url + mp3, headers=self.headers)
                suf = '.mp3'
            music_url = json.loads(req.text).get('url')
            # print(music_url)
            self.save_music(author, music_url, music_name, suf)


    # 写入模块
    def save_music(self, author, music_url, music_name, suf):
        r = requests.get(music_url, stream=True)
        with open(author + '_' + music_name + suf, "wb") as f:
            for chunk in r.iter_content(chunk_size=10240):
                if chunk:
                    f.write(chunk)


if __name__ == '__main__':
    Singlereptile().get_index()