#!/usr/bin/python3
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests
from io import BytesIO
from PIL import Image
class InvalidCode(Exception):
    pass
class nhentaiObject:
    def __init__(self, json) -> None:
        self.json     = json
        self.id       = json["id"]
        self.title    = json["title"][:-38]
        self.images   = json["image"]
        self.url      = json["url"]
        self.bytes    = BytesIO()
    def download(self, workers=5):
        assert isinstance(workers, int)
        if self.bytes.getbuffer().tobytes():
            return self.bytes
        else:
            with ThreadPoolExecutor(max_workers=workers) as thread:
                result = []
                for i in self.images:
                    result.append(Image.open(BytesIO(thread.submit(requests.get, i).result().content)).convert("RGB"))
            result[0].save(fp=self.bytes,format='pdf', save_all=True, append_images=result[1:])
            return self.bytes
    def save_to_file(self, fn):
        assert isinstance(fn, str)
        if not self.bytes.getbuffer().tobytes():
            self.download()
        open(f"{fn}{'' if fn[-4:].lower() == '.pdf' else '.pdf'}", 'wb').write(self.bytes.getbuffer().tobytes())
    def __repr__(self):
        return f"<[{self.title}]>"
    def __str__(self) -> str:
        return self.__repr__()

class nsearch:
    def __init__(self, query) -> None:
        self.query = query
        self.req = requests.get("https://nhentai.net/search", params={"q":self.query}).text
        self.all_fetch = []
    @property
    def fetch(self):
        if self.all_fetch:
            return self.all_fetch
        title=re.findall("\<\/noscript\>\<div class\=\"caption\"\>(.*?)\</div\>",self.req)
        nuklir=re.findall("href\=\"/g/([0-9]{5,6})/\"",self.req)
        thumb=re.findall("data\-src\=\"(https://t.nhentai.net/galleries/[0-9]{6,8}/thumb.jpg)\"",self.req)
        for i in enumerate(thumb):
            self.all_fetch.append(nhentai(nuklir[i[0]], i[1], title[i[0]]))
        return self.all_fetch
    def __str__(self) -> str:
        return f"<[count {self.fetch.__len__()}]>"
    def __repr__(self) -> str:
        return self.__str__()


class nhentai:
    def __init__(self, nuklir, thumb=None, title=None) -> None:
        self.nuklir = nuklir
        self.thumb  = thumb
        self.title  = title
    def __str__(self) -> str:
        return self.title.__str__()
    def __repr__(self) -> str:
        return self.__str__()
    @property
    def doujin(self):
        try:
            self.html   = requests.get('https://nhentai.net/g/%s'%(self.nuklir))
            parsing=BeautifulSoup(self.html.text, 'html.parser')
            komik = []
            for i in parsing.find_all('a',class_='gallerythumb'):
                if i('img'):
                    komik.append('https://i'+i('img')[0]['data-src'][9:-5]+'.jpg')
            id_=komik[0].split('/')[-2]
            komik.insert(+0,'https://t.nhentai.net/galleries/%s/cover.jpg'%(id_))
            return nhentaiObject({'id':id_, 'title':parsing.title.text, 'image':komik, 'url':self.html.url})
        except IndexError:
            raise InvalidCode("Error")