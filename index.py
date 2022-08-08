from bottle import route, run, request, template, post, redirect
from lxml import html
import xml.etree.ElementTree as ET
import requests
import re


# Задаём параметры доступа в сервисе xmlstock.com
XMLSTOCK_USER = 'USER_ID'
XMLSTOCK_KEY = 'API_KEY'


HOST_ADRESS = 'IP_ADDRESS'  # указываем адрес сервера, или localhost если запускается на своём компьютере
PORT = 'PORT'  # указываем порт, на котором запускается сервис, например 8080


# Отображение ip адреса при обращении по адресу
@route('/ip')
def check_ip():
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    return ['Your IP is: {}\n'.format(client_ip)]


# Отображение первого сниппета для запроса в google по определённому сайту, полезно для сравнения сниппета и title страницы.
@route('/parse')
def mypars():
    # Для получения сниппета необходимо сформировать запрос вида http://host:port/parse?keyword=запрос&domain=site.ru
    # Где "запрос" - ключевая фраза, "site.ru" - домен
    keyword = request.query.keyword
    domain = request.query.domain
    print(keyword)
    print(domain)
    url = f'https://www.google.ru/search?q={keyword}+site%3A{domain}&oq={keyword}+site%3A{domain}'
    user_agent = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
    responses = requests.get(url, headers=user_agent)
    responses.encoding = 'utf-8'
    tree = html.fromstring(responses.text)

    try:
        names = tree.xpath("(//h3)[1]")[0].text
    except:
        names = "Запрос названия не распознан"
    if 'Картинки по запросу' not in str(names):
        try:
            names = tree.xpath("(//h3)[1]")[0].text
        except:
            names = "Запрос названия не распознан"
        try:
            url_result = tree.xpath("(//h3)[1]/parent::a/@href")[0]
        except:
            url_result = "Запрос адреса не распознан"
    else:
        try:
            names = tree.xpath("(//h3)[3]")[0].text
        except:
            names = "Запрос названия не распознан"
        try:
            url_result = tree.xpath("(//h3)[3]/parent::a/@href")[0]
        except:
            url_result = "Запрос адреса не распознан"
    return template('<h2>{{names}}</h2><br><h3>{{url_result}}</h3', names=str(names), url_result=str(url_result))
    print([i.text for i in names])
    print(url_result)


# Отображает количество страниц в индексе google для выборанного сайта
# Для получения результата необходимо сформировать запрос вида http://host:port/google?url=site.ru
@route('/google')
def googl():
    site = request.query.get('url')
    url = 'https://www.google.com/search?q=site:' + str(site) + '&hl=en&newwindow=1'
    print(url)
    user_agent = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}
    responses = requests.get(url, headers=user_agent)
    tree = html.fromstring(responses.text)
    dss = tree.xpath('//div[@id="result-stats"]/text()[normalize-space()]')
    dscln = re.sub(r'\\x..', '', str(dss))
    dscln = re.sub('[^0-9]', '', dscln)

    return template('<p class="pages"> {{pages}} страниц</p>', pages=dscln)


# Отображает количество страниц в индексе yandex для выбранного сайта. Сначала попытка через выдачу, если нет, то через xmlstock.com
# Для получения результата необходимо сформировать запрос вида http://host:port/yandex?url=site.ru
@route('/yandex')
def yand():
    site = request.query.get('url')
    url = 'https://yandex.ru/search/?text=host%3A' + str(site) + '%20%7C%20host%3Awww.' + str(site)
    print(url)
    user_agent = {
        'User-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0'}
    responses = requests.get(url, headers=user_agent)
    tree = html.fromstring(responses.text)
    if 'yandex.ru/captcha' not in str(tree.xpath("//body/descendant::img/@src")):
        print(''.join(tree.xpath("//body/descendant::img/@src")))
        dss = tree.xpath("//div[@class='serp-adv__found']/text()")[0]
        dscln = re.sub(r'\\x..', '', str(dss))
        print(dscln)
    else:
        print('Есть капча')
        url = f'https://xmlstock.com/yandex/xml/?user={XMLSTOCK_USER}&key={XMLSTOCK_KEY}&lr=213&query=host%3A{str(site)}%20%7C%20host%3Awww.{str(site)}'
        print(url)
        xmlfile = requests.get(url).content
        root = ET.fromstring(xmlfile)
        print(root.find("./response/found-human").text)
        dscln = root.find("./response/found-human").text

    return template('<p class="pages"> {{pages}}</p>', pages=dscln)


# Это код из проверки запросов для яндекса и гугла
def verification_keyword(keyword):
    url = f'https://xmlstock.com/yandex/xml/?user={XMLSTOCK_USER}&key={XMLSTOCK_KEY}&lr=213&query={keyword}'
    with open('bad_domains.txt', 'r') as f:  # В файле bad_domains.txt список нежелательных сайтов
        bad_domains = f.read().splitlines()
    domains = []
    xmlfile = requests.get(url).content
    root = ET.fromstring(xmlfile)
    for child in root.findall("./response/results/grouping/group"):  # ищем группы результатов выдачи
        try:
            domain = child[3][3].text.lower().replace('www.', '')  # ищем названия доменов в результатах выдачи
            domains.append(domain)    
        except:
            continue
    
    result = list(set(bad_domains) & set(domains))
    return result


@route('/bad_domains')
def form_bad_domains():
    return template('form.tpl')


@post('/bad_domains')
def bad_domains():
    keyword = request.forms.getunicode('keyword')
    if ',' in keyword:
        keyword = keyword.split(',')
        keyword_len_dict = {keyw: verification_keyword(keyw) for keyw in keyword}
        return template('bad_dom_many.tpl', keywdict=keyword_len_dict, keyword=keyword)
    elif '\r\n' in keyword:
        keyword = keyword.split('\r\n')
        keyword_len_dict = {keyw: verification_keyword(keyw) for keyw in keyword}
        return template('bad_dom_many.tpl', keywdict=keyword_len_dict, keyword=keyword)
    else:
        return template('bad_dom.tpl', result=verification_keyword(keyword), keyword=keyword,
                        lenres=len(verification_keyword(keyword)), ranglen=range(len(verification_keyword(keyword))))


@route('/')
def wrong():
    redirect("/bad_domains")	


run(host=HOST_ADRESS, port=PORT, debug=True)