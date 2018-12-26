import os
import requests
import json
from lxml import etree
from urllib.request import urlretrieve


class Singlereptile(object):
    def __init__(self):
        self.header = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Host': 'music.163.com',
            'Origin': 'https://music.163.com',
            'Referer': 'https://music.163.com/',
            'Cookie': 'nts_mail_user=wpcaxys@163.com:-1:1; mail_psc_fingerprint=4b7038f128128ecf935ec3a22433605c; _iuqxldmzr_=32; _ntes_nnid=9832612155e58ac50c272f7548ebed37,1537959851522; _ntes_nuid=9832612155e58ac50c272f7548ebed37; WM_TID=6KsVpW6xlGpFAVRQEENoPAYikeS6YJxL; __f_=1538297168225; usertrack=CrHualvRxeIb1YF/Aw6eAg==; vjuids=-23d877345.166d98bdbd7.0.55306e71680ce; vjlast=1541248114.1541248114.30; vinfo_n_f_l_n3=27ed687cd065ab3a.1.0.1541248113751.0.1541248528316; _ga=GA1.2.1034785504.1542942163; P_INFO=wpcaxys@163.com|1543398872|0|other|11&11|gud&1543308788&mail163#gud&440300#10#0#0|134311&0|mail163|wpcaxys@163.com; WM_NI=jONmDTRgwOxqfwle2yogDW%2BcC8t1kscaHZrL656kFQdDDOrsICe5BMsLUmuMRZQuZkZSI6Q6KPXSa6WfkvXWeSWqsn4Gn5yd0FFX9VSqM7WenrN3eROnxcEWBlO4dKhCZEk%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee8bd861a89bfb8df26a82eb8bb6d85b939b9faeb75cf290bfbbd25a8dbbbbb8ef2af0fea7c3b92aaa91828ec76092b9b9b0fb7ba6a9a486b173adb98cb8aa6981e8bcd2ea79a1bf88bbf148f6ebfa8cc55ba89c8cb0f1798b9dabd6c147b1949b8ef84792869f96d9619a8d87d7d43e899098b4e43e95baa597db5da78d9992f266f899a2d6fc70f49a8ab9bc5e91af83d8d66faeae82d4e85a8db2b884c85d82b481d5e741ac9d96a6ea37e2a3; __utmc=94650624; __utmz=94650624.1543542181.6.4.utmcsr=sogou.com|utmccn=(referral)|utmcmd=referral|utmcct=/link; playerid=96316702; JSESSIONID-WYYY=UcRv68UIW2245SRP3g%2FI851%5Cibqp2jPIvF2xC%2BGbykdsZPCh%2Fs2zXEUa6bF%2BxTDopOI5kMsII7YYdMxGYzDQGFmXy0%2BOTs1caWn0sRTdXjIPjw%5CbdOmuXRj0ofVMKGNd3H6GAD3FSdz2QO%2FiA9F2NJQU5Fx%2B%2BzgObysz%2B%2B%2FGbaJS4ahP%3A1543575812397; __utma=94650624.65444533.1542182698.1543545871.1543574688.8; __utmb=94650624.1.10.1543574688',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        self.data = {
            'params': 'hCr9zr95pzaMvgDz2vMAikxrtK0r4ufl6/KcqpdMk/XSbgb+pafgqd9f/JVcAWEqW/JpNRtZPlrG3Yg4OXvgFH0Q/LthEHBny/30obsnw1obfXSNJ2j8qOLsEEUKS6ks',
            'encSecKey': '42c68650c6ef601a8a162c326196c035856a654ec93350fa04f8b5e9f354153e7e6bf37cd4e3fac0eedd6d19a6b170d8d7ba94e5dce48071b601e0b5079a35a5469928ada551067ef5c5bc93d7e02a87300b5d6bbf7f83a2360fbb943d45de5a0aac7ffb26f173326d1712a56441abe947695438e4673f66cfcb7ec0caa0b4c2',
        }
        self.url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token='

    def get_music(self):
        res = requests.session()
        f = open('all_singer.csv', 'r', encoding='utf-8')
        for id_bak in f:
            id = id_bak[:-1]
            get_music_list = res.get('https://music.163.com/artist?id={}'.format(id), headers=self.header)
            if get_music_list.status_code == 200:
                get_music_list.encoding = 'utf8'
                html = etree.HTML(get_music_list.text)
                a_list = html.xpath('//ul[@class="f-hide"]/li')
                count = 0
                for i in a_list:
                    count += 1
                    name = i.xpath('a/text()')[0]
                    # id = i.xpath('a/@href')[0]
                    # id = id.split('=')[-1]
                    req = res.post(self.url, headers=self.header, data=self.data)
                    if req.status_code == 200:
                        req.encoding = 'utf8'
                        json_dict = json.loads(req.content)
                        song_url = json_dict['data'][0]['url']
                        song_dir = os.path.exists('songs')
                        if not song_dir:
                            os.makedirs("songs")
                        if '//' in name:
                            name = ''.join(name.split('//'))
                            # print(name)
                        print("正在下载{}歌曲, 这是第{}首歌曲".format(name, count))
                        path = os.path.join('songs', name + ".mp3")
                        urlretrieve(song_url, path)
                        print("{}下载结束".format(name))
                print('一共{}首歌曲下载完毕！'.format(count))
        f.close()

if __name__ == '__main__':
    Singlereptile().get_music()