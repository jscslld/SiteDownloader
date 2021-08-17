import json
import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urljoin
from urllib.parse import urlparse



"""
设置下载页面
"""
downloadurl="http://netgon.ru/themeforest/arion_html/index.html"


"""
算法部分，请勿随意修改
"""
finishurl=[]
def download(url):
    if not os.path.exists(os.path.dirname(os.path.abspath('.'+urlparse(url).path))):
        os.makedirs(os.path.dirname(os.path.abspath('.'+urlparse(url).path)))
    try:
        urllib.request.urlretrieve(url, os.path.abspath('.'+urlparse(url).path))
        print(url)
    except:
        print(url,"下载失败")
        return False
def getRousource(url):
    try:
        if url[0:4] != "http":
            return False
        if url in finishurl:
            return True
        download(url)
        finishurl.append(url)
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = { 'performance':'ALL' }
        chrome_options = Options()
        # 使用无头浏览器
        chrome_options.add_argument('--headless')
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73')
        # 浏览器启动默认最大化
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option('w3c', False)
        # 该处替换自己的chrome驱动地址
        browser = webdriver.Chrome("E://chromedriver.exe", chrome_options=chrome_options, desired_capabilities=d)
        browser.set_page_load_timeout(150)
        browser.get(url)
        # 静态资源链接存储集合
        rurls = []
        urls = []
        # 获取静态资源有效链接
        for log in browser.get_log('performance'):
            if 'message' not in log:
                continue
            log_entry = json.loads(log['message'])
            try:
                # 该处过滤了data:开头的base64编码引用和document页面链接
                if "data:" not in log_entry['message']['params']['request']['url'] and 'Document' not in \
                        log_entry['message']['params']['type']:
                    rurls.append(log_entry['message']['params']['request']['url'])
                    if log_entry['message']['params']['request']['url'] not in finishurl:
                        download(log_entry['message']['params']['request']['url'])
                        finishurl.append(log_entry['message']['params']['request']['url'])
            except Exception as e:
                pass
        _urls = browser.find_elements_by_xpath("//a")
        pending=[]
        for _url in _urls:
            if _url.get_attribute("href") != None and _url.get_attribute("href") != "#" and _url.get_attribute("href") not in finishurl:
                if urljoin(url,_url.get_attribute("href")) not in finishurl:
                    pending.append(urljoin(url,_url.get_attribute("href")))
        _urls = browser.find_elements_by_xpath("//link")
        for _url in _urls:
            if _url.get_attribute("href") not in finishurl:
                if urljoin(url, _url.get_attribute("href")) not in finishurl:
                    download(urljoin(url, _url.get_attribute("href")))
                    finishurl.append(urljoin(url, _url.get_attribute("href")))
        _urls = browser.find_elements_by_xpath("//script")
        for _url in _urls:
            if _url.get_attribute("src") not in finishurl:
                if urljoin(url, _url.get_attribute("src")) not in finishurl:
                    download(urljoin(url, _url.get_attribute("src")))
                    finishurl.append(urljoin(url, _url.get_attribute("src")))
        browser.quit()
        for u in pending:
            getRousource(u)
    except:
        print(url,"解析失败")
        return False

getRousource(downloadurl)