from selenium import webdriver
import os
import requests
from hashlib import md5
import time

browser = webdriver.Chrome()

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
}

#获取每个图片的具体url


def get_image_url(url):
    browser.get(url)
    urls = []
    lis = []
    for li in browser.find_elements_by_css_selector('.commentlist li'):
        comment = li.get_attribute('id')
        if comment==None:
            continue
        else:
            lis.append(comment)
    lis.pop(3)
    for s in lis:
        try:
            img_url = browser.find_element_by_css_selector('#'+s+' > div > div > div.text > p > a').get_attribute('href')
            urls.append(img_url)
        except:
            print('出错', '#' + s + ' > div > div > div.text > p > a')
            return None
    i = 0
    for URL in urls:
        if URL == 'javascript:;':
            urls.pop(i)
            lis.pop(i)
        else:
            None
        i += 1
    data = {
        'title': lis,
        'urls': urls
    }
    return data

#保存每张图片


def save_to_file(item):
    for url in item['urls']:
        try:
            response = requests.get(url, headers=headers)
            time.sleep(0.5)
            if response.status_code == 200:
                file_path = '{0}/{1}.{2}'.format('pic', md5(response.content).hexdigest(), 'jpg')
                if not os.path.exists(file_path):
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                else:
                    print('Already Downloaded', file_path)
        except:
            return None


def main(offset):
    url = 'http://jandan.net/ooxx/page-'+str(offset)+'#comments'
    item = get_image_url(url)
    save_to_file(item)


if __name__ == '__main__':
    for i in range(1, 11):
        main(i)
