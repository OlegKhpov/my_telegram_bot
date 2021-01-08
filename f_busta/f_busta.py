'''
http://flibusta.is/makebooklist
?ab=ab1 - ???
?sort=st1 - sort_title 1
?sort=st2 - sort_title 2
?sort=ss1 - sort-size 1
?sort=ss2 - sort-size 2
?sort=sd1 - sort-date 1
?sort=sd2 - sort-date 2
?t - title
?ln - last_name
?fn - first_name
?mn - middle_name
?g - genre
?s1 = max_size[int]
?s2 = max_size[int]
?issueYearMin - year[int]
?issueYearMax - year[int]
?e - format Форматы: (fb2, pdf, djvu, doc, html, epub, chm, rtf, txt, exe,
    docx, pdb, rgo, lrf, mht, jpg, mhtm, dic, mobi, xml, htm, azw, png, odt, tex, azw3, dat, 
    mp3, cbr, 7zip, djv, word, prc, pdg, wri, wps, xps, sxw, gdoc, phf, НТМl, epab, zip, 
    docs, dock, bqt, fb, md5, ebup), можно указать несколько через запятую. 
?lng - language Языки: (be, kk, ru, RU, uk, ru~ru-petr1708), можно указать несколько через запятую.
-GET-ASK-
?chb=on - books on
?chs=on - series on
?cha=on - authors on
?chg=on - genres on
'''
import requests
import re
from bs4 import BeautifulSoup


class Booksearch:
    BASE_URL = 'http://flibusta.is'
    def __init__(self):
        self.last_params = {
            "chb": "on",
            "chs": "on",
            "cha": "on",
            "chg": "on",
        }
        self.url = '/booksearch'


    def __str__(self):
        return str(self.soup)

    def _get_response(self, init=True):
        last_params = self.last_params
        if init:
            last_params['ask'] = self.search_words
            response = requests.get(self.BASE_URL + self.url, last_params)
        else:
            response = requests.get(self.BASE_URL + self.url)
        return response

    def _get_response_page(self, page):
        last_params = self.last_params
        last_params['ask'] = self.search_words
        if int(page) > 0:
            last_params['page'] = page
        else:
            last_params['page'] = ''
        response = requests.get(self.BASE_URL + self.url, last_params)
        return response

    def _get_soup(self):
        soup = BeautifulSoup(self.response.text, 'html.parser')
        soup = soup.find(attrs={'id': 'main'})
        return soup

    def get_links(self):
        end = ('fb2', 'pdf', 'djvu', 'doc', 'html',
        'epub', 'chm', 'rtf', 'txt', 'exe', 'docx',
        'pdb', 'rgo', 'lrf', 'mht', 'jpg', 'mhtm',
        'dic', 'mobi', 'xml', 'htm', 'azw', 'png',
        'odt', 'tex', 'azw3', 'dat', 'mp3', 'cbr',
        '7zip', 'djv', 'word', 'prc', 'pdg', 'wri',
        'wps', 'xps', 'sxw', 'gdoc', 'phf', 'НТМl',
        'epab', 'zip', 'docs', 'dock', 'bqt', 'fb',
        'md5', 'ebup', 'download')
        links = self.soup.find_all('a')
        list_of_links = []
        for link in links:
            if link['href'].endswith(end):
                file_type = re.findall('/b/\d+/(.+)', link['href'])[0]
                if file_type == 'download':
                    file_type = re.findall('\(\w+ (.+)\)', link.text)[0]
                list_of_links.append([file_type, link['href']])
        return list_of_links

    def _prepare_data(self):
        self.data = []
        seq = self.soup.find_all('a', {'href': re.compile('/sequence/+')})
        aut = []
        for author in self.soup.find_all('a', {'href': re.compile('/a/+')}):
            if self.search_words.capitalize() in author.text.split(' '):
                aut.append(author)
        boo = self.soup.find_all('a', {'href': re.compile('/b/+')})
        for s in seq:
            s_split = s['href'].split('/')
            if s_split[-1].isnumeric():
                self.data.append([s.text, s['href'], s_split[-2], s_split[-1]])
        for a in aut:
            s_split = a['href'].split('/')
            if s_split[-1].isnumeric():
                self.data.append([a.text, a['href'], s_split[-2], s_split[-1]])
        for b in boo:
            s_split = b['href'].split('/')
            if s_split[-1].isnumeric():
                self.data.append([b.text, b['href'], s_split[-2], s_split[-1]])

    def _prepare_book_data(self):
        self.data = []
        url = self.BASE_URL + self.url
        name = self.soup.find('a', {'href': re.compile('/a/\d+')}).text
        title = self.soup.find('h1').text
        annotation = self.soup.find_all('p')[1]
        message = ''
        lst = [title, name, url, annotation]
        for i in lst:
            message += f'{i}\n'
        return message

    def find_search_words_in_msg(self, message):
        words = re.findall('(?<=search=).+', message)
        return words[0]

    def _find_pages(self):
        soup = BeautifulSoup(self.response.text, 'html.parser')
        page_prev = soup.find(attrs={'class': 'pager-previous'})
        if page_prev is not None:
            page_prev = page_prev.find('a')
            page_prev = page_prev['href']
            page_prev = re.findall('page=\d+', page_prev)
            if page_prev != []:
                page_prev = page_prev[0].split('=')[-1]
            else:
                page_prev = '0'
            self.page_prev = page_prev
        else:
            self.page_prev = None
        page_next = soup.find(attrs={'class': 'pager-next'})
        if page_next is not None:
            page_next = page_next.find('a')
            page_next = page_next['href']
            page_next = re.findall('page=\d+', page_next)[0].split('=')[-1]
            self.page_next = page_next
        else:
            self.page_next = None

    def get_pages(self):
        self._find_pages()
        pages = []
        if self.page_prev is not None:
            pages.append(self.page_prev)
        else:
            pages.append(None)
        if self.page_next is not None:
            pages.append(self.page_next)
        else:
            pages.append(None)
        return pages

    def search(self, search, page=None):
        message = f'search={search}\n'
        self.search_words = search
        if any((
            self.search_words.startswith('/a/'),
            self.search_words.startswith('/b/'),
            self.search_words.startswith('/sequence/'),
            self.search_words.startswith('/g/'),
        )):
            self.url = self.search_words
            self.response = self._get_response(False)
        else:
            if page is not None:
                self.response = self._get_response_page(page)
            else:
                self.response = self._get_response()
        self.soup = self._get_soup()
        if self.search_words.startswith('/b/'):
            return self._prepare_book_data()
        self._prepare_data()
        for item in self.data:
            if item[-2] == "sequence":
                link = "/" + "s" + item[-1]
            else:
                link = "/" + item[-2] + item[-1]
            message += f'{item[0]} - {link}\n'
        return message


if __name__ == "__main__":
    b = Booksearch()
    print(b.search('/b/67618'))
    print(b.get_links())
