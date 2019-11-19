# # # # #   MADE BY:    @rTUNAboss | rtuna#4321           # # # # #

print(r'''
 ____    ____   _   _  ______       __     __ _        
|  _ \  / __ \ | \ | ||___  /    /\ \ \   / /(_)       
| |_) || |  | ||  \| |   / /    /  \ \ \_/ /  _   ___  
|  _ < | |  | || . ` |  / /    / /\ \ \   /  | | / _ \ 
| |_) || |__| || |\  | / /__  / ____ \ | | _ | || (_) |
|____/  \____/ |_| \_|/_____|/_/    \_\|_|(_)|_| \___/ 
''')
print(" • made by: rtuna#4321 | @rTunaboss")
print(" • for personal use only")

import requests
from bs4 import BeautifulSoup as bs
import json
import re
from jsoncomment import JsonComment
import random
import datetime
import threading
from threading import Thread
import time
from colorama import Fore, Back, Style, init
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dhooks import Webhook, Embed
init(autoreset=True)

with open('config.json') as f:
    config_json = json.loads(f.read())

product_link = config_json['product_link']
webhook_url = config_json['webhook_url']
delay = int(config_json['delay'])

keywords=[] #not used right now
get_headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding" : "gzip, deflate, br",
    "Accept-Language" : "en-GB,en-US;q=0.9,en;q=0.8,cs;q=0.7,de;q=0.6",
    "Connection" : "keep-alive",
    "Host": "store.sacai.jp",
    "Origin" : "https://store.sacai.jp",
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36",
}

proxyList = []

def loadProxy1(nomeFile):
    global proxyList
    f = open('' + nomeFile + '.txt')
    dividiStiProxy = f.read()
    # tmp = f.readlines()
    tmp = dividiStiProxy.split('\n')
    for n in range(0, len(tmp)):
        if ':' in tmp[n]:
            temp = tmp[n]
            temp = temp.split(':')
            proxies = {'http':'http://' + temp[2] + ':' + temp[3] + '@' + temp[0] + ':' + temp[1] + '/', 
             'https':'http://' + temp[2] + ':' + temp[3] + '@' + temp[0] + ':' + temp[1] + '/'}
            # print(proxies)
            proxyList.append(proxies)

def loadProxy2(nomeFile):
    f = open('' + nomeFile + '.txt')
    dividiStiProxy = f.read()
    # tmp = f.readlines()
    tmp = dividiStiProxy.split('\n')
    for n in range(0, len(tmp)):
        if ':' in tmp[n]:
            temp = tmp[n]
            proxies = {'http':'http://' + temp,  'https':'http://' + temp}
            proxyList.append(proxies)

try:
    loadProxy1('proxies')
except: 
    loadProxy2('proxies')

totalproxies = len(proxyList)
if int(totalproxies) == 0:
    print(Fore.YELLOW + Style.DIM + '[INFO] Running localhost!')
else:
    print(Fore.YELLOW + Style.DIM + f'[INFO] Loaded {totalproxies} proxies!')

def send_webhook(title, inputsize, image, url, paymentype, checkout_time):
    try:
        hook = Webhook(url=webhook_url)
        embed = Embed(title='SACAI Checkout', color=15957463, url=url, thumbnail_url=str(image))
    
        embed.add_field(name='Product', value=str(title))
        embed.add_field(name='Product Size', value=str(inputsize))
        embed.add_field(name='Payment Type', value=str(paymentype))
        embed.add_field(name='Checkout Speed', value=str(checkout_time) + ' sec')
        embed.set_footer(text=f'BONZAY SACAI • {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',icon_url='https://cdn.discordapp.com/icons/594125608003305492/7f5110cf3bb22f6d622cd03ba1586f59.webp?size=512')

        hook.send(embed=embed)
        print(gettime() + Fore.GREEN + Style.BRIGHT +' [SUCCESS] -> Successfully sent success webhook!')
    except:
        print(gettime() + Fore.RED + ' [ERROR] -> Failed sending success webhook!')

def gettime():
    now = str(datetime.datetime.now())
    now = now.split(' ')[1]
    threadname = threading.currentThread().getName()
    threadname = str(threadname).replace('Thread', 'Task')
    now = '[' + str(now) + ']' + ' ' + '[' + str(threadname) + ']'
    return now

def login(s, email, passw):
    login_url = 'https://store.sacai.jp/login'
    r = s.get(login_url, headers=get_headers)
    soup = bs(r.text,'lxml')
    fuel_csrf_token = soup.find('input', {'name':"fuel_csrf_token"})['value']

    login_headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding" : "gzip, deflate, br",
    "Accept-Language" : "en-GB,en-US;q=0.9,en;q=0.8,cs;q=0.7,de;q=0.6",
    "Connection" : "keep-alive",
    "Content-Length" : "229",
    "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
    "Host" : "store.sacai.jp",
    "Origin" : "https://store.sacai.jp",
    "Referer" : 'https://store.sacai.jp/login',
    "Sec-Fetch-Site" : "same-origin",
    "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36",
    "X-Requested-With" : "XMLHttpRequest",
    }
    
    login_payload = {
        "fuel_csrf_token":fuel_csrf_token,
        "login_id":email,
        "password":passw,
        "check_preserve_login":"1",
        "preserve_login_flag":"1",
    }
    print(gettime() + ' [STATUS] -> Trying to log in...')
    
    r = s.post(url=login_url, headers=login_headers, data=login_payload)
    if 'Mail addressとPasswordを確認して下さい。' in r.text:
        print(gettime() + Fore.RED + ' [ERROR] -> Failed to log in, retrying...')
        time.sleep(delay)
        login(s, email, passw)
    print(gettime() + Fore.GREEN + Style.BRIGHT +' [SUCCESS] -> Successfully logged in!')

def get_avail_sizes(colors_data_dict):
    avail_sizes = {}
    try:
        for color_data in colors_data_dict:
            color_code = color_data["color_code"]
            sizes_data = color_data['sizes']
            for size in sizes_data:
                if size['stock'] is not 0:
                    avail_sizes[size['size_code']] = color_code
    except Exception as e:
        print(gettime() + Fore.RED + ' [ERROR] -> Exception: ' + str(e))
    finally:
        return avail_sizes

def check_sold_out(s, product_url):
    r = s.get(product_url, headers=get_headers)
    soup = bs(r.text, 'lxml')
    # print(soup)
    data_size = soup.find_all('script', {'type': 'text/javascript'})
    text_data = data_size[10].text
    data = re.findall(r"var item_stock =(.+?);\n", text_data, re.S)
    text_data = data[0]
    parser = JsonComment(json)
    j = parser.loads(text_data) #json with all the data we need
    colors_data_dict = j['colors']
    available_sizes = get_avail_sizes(colors_data_dict)
    if available_sizes == {}:
        print(gettime() + Fore.YELLOW + ' [WARN.] -> Product is soldout, retrying...')
        time.sleep(delay)
        check_sold_out(s, product_url)
    else:
        return available_sizes, soup

def pick_random_instock_combination(colors_data_dict):
    '''('L', '212')'''
    avail_sizes = get_avail_sizes(colors_data_dict)
    random_combination = random.choice(list(avail_sizes.items()))
    if random_combination == None:
        pick_random_instock_combination(colors_data_dict)
    else:
        return random_combination

def atc(s, random_combination, product_url, fuel_csrf_token):
    print(Fore.YELLOW + f'[INFO] Trying to ATC {random_combination}')
    atc_headers = {
        "Accept" : "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding" : "gzip, deflate, br",
        "Accept-Language" : "en-GB,en-US;q=0.9,en;q=0.8,cs;q=0.7,de;q=0.6",
        "Connection" : "keep-alive",
        "Content-Type" : "application/x-www-form-urlencoded; charset=UTF-8",
        "Host" : "store.sacai.jp",
        "Origin" : "https://store.sacai.jp",
        "Referer" : product_url,
        "Sec-Fetch-Mode" : "cors",
        "Sec-Fetch-Site" : "same-origin",
        "User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36",
        "X-Requested-With" : "XMLHttpRequest",
    }
    get_atc_headers = get_headers
    get_atc_headers["Referer"] = product_url

    atc_url = 'https://store.sacai.jp/apis/cart/add.json'
    cart_url = 'https://store.sacai.jp/'
    code_from_url = re.findall(r"((?<=https:\/\/store\.sacai\.jp\/product\/).*|(?<=https:\/\/store\.sacai\.jp\/item\/)).*", product_url, re.S)[0]
    atc_payload = {
            "fuel_csrf_token" : fuel_csrf_token,
            "detail_disp_manage_code" : code_from_url.split('/')[0],
            "color_code" : code_from_url.split('/')[1],
            "size_code" : random_combination[0],
            "pod" : "1",
            "currency" : "JPY",
        }
    print(gettime() + ' [STATUS] -> Trying to ATC...')
    p = s.post(url=atc_url, headers=atc_headers, data=atc_payload)
    r = s.get(cart_url, headers=get_headers)
    if p.status_code != 200:
        print(gettime() + Fore.RED + ' [ERROR] -> ATC failed, retrying...')
        atc(s, random_combination, product_url, fuel_csrf_token)
    else:
        print(gettime() + Fore.GREEN + Style.BRIGHT +' [SUCCESS] -> ATC was successfull!')

def get_shoe_links():
    category_url = 'https://store.sacai.jp/product-list/shoes'
    r = requests.get(category_url, headers=get_headers)
    soup = bs(r.text, 'lxml')
    item_archive_list = soup.find_all('div', {'class':'item_archive__list'})
    links = []
    for item in item_archive_list:
        a = item.find('a')
        product_name = a.find('dt').text
        for keyword in keywords:
            if keyword in product_name:
                links.append('https://store.sacai.jp' + a['href'])
                print(gettime() + Fore.GREEN + Style.BRIGHT + f' [SUCCESS] -> Product "{product_name}" found!')
                print(Fore.GREEN + 'https://store.sacai.jp' + a['href'])
    if links:
        return links
    else:
        print(gettime() + Fore.RED + ' [ERROR] -> Failed getting product urls...')
        links=list(input(gettime() + Fore.CYAN + ' [INPUT NEEDED] -> Enter URL you want to run for...'))
        return links

def run(product_url, data_json, profile_name):
    print(gettime() + Fore.YELLOW + Style.DIM + ' [STATUS] -> Starting...')
    profile_data = data_json[profile_name]
    paymentype = profile_data['payment']
    email = profile_data['email']
    password = profile_data['password']
    cc_num = profile_data['cc_num']
    cc_expiry = profile_data['cc_expiry']
    cvv = profile_data['cvv']
    s = requests.Session()
    s.proxies = proxyList

    #login
    login(s, email, password)

    available_sizes, soup = check_sold_out(s, product_url)

    # go to productpage and get needed data
    # s = requests.Session()
    # r = s.get(product_url, headers=get_headers)
    # soup = bs(r.text, 'lxml')
    # # print(soup)
    # data_size = soup.find_all('script', {'type': 'text/javascript'})
    # text_data = data_size[10].text
    # data = re.findall(r"var item_stock =(.+?);\n", text_data, re.S)
    # text_data = data[0]
    # parser = JsonComment(json)
    # j = parser.loads(text_data) #json with all the data we need
    # colors_data_dict = j['colors']
    # available_sizes = get_avail_sizes(colors_data_dict)

    #dict_keys(['color_code', 'color_name', 'color_swatch', 'color_proper', 'color_proper_usd', 'color_proper_eur', 'color_sale', 'color_sale_usd', 'color_sale_eur', 'color_percent', 'html_color', 'image_url', 'stock', 'sizes', 'images'])

    # for color in colors_data_dict:
    #     avail_sizes = get_avail_sizes(color)
    #     print(avail_sizes)
    fuel_csrf_token = soup.find('input', {'name':"fuel_csrf_token"})['value']
    now = datetime.datetime.now()
    random_combination = random.choice(list(available_sizes.items()))

    atc(s, random_combination, product_url, fuel_csrf_token)
    #checkout

    print(gettime() + ' [STATUS] -> Opening Chrome...')
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.set_window_size(400,600)
    driver.get('https://store.sacai.jp/legal?lang=en')
    print(gettime() + ' [STATUS] -> Adding cookies...')
    for c in s.cookies :
        driver.add_cookie({'name': c.name, 'value': c.value, 'path': c.path, 'expiry': c.expires})

    driver.get('https://store.sacai.jp/cart/step02')
    print(gettime() + ' [STATUS] -> Going to cart...')
    try:
        if paymentype.lower() == 'paypal':
            print(gettime() + ' [STATUS] -> Checking out with PayPal...')
            driver.find_element_by_xpath('//*[@id="action_form"]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/label').click()
            print(gettime() + ' [STATUS] -> Going to step 3...')
            driver.find_element_by_xpath('//*[@id="form_next_step03"]').click()
            driver.set_window_size(600,600)
        else:
            # driver.execute_script("window.open()")
            print(gettime() + ' [STATUS] -> Checking out with CC...')
            driver.find_element_by_xpath('//*[@id="action_form"]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/label').click()
            print(gettime() + ' [STATUS] -> Going to step 3...')
            driver.find_element_by_xpath('//*[@id="form_next_step03"]').click() 
            checkout_button = driver.find_element_by_xpath('//*[@id="customButton"]')
            checkout_button.click()
            driver.switch_to.frame(driver.find_element_by_xpath('/html/body/iframe'))
            driver.set_window_size(400,600)
            email_form = driver.find_element_by_xpath('//input[@type="email"]')
            email_form.send_keys(email)

            cc_form = driver.find_element_by_xpath('//input[@placeholder="Card number"]')
            cc_form.send_keys(cc_num)

            expiry_form = driver.find_element_by_xpath('//input[@placeholder="MM / YY"]')
            expiry_form.send_keys(cc_expiry)

            cvv_form = driver.find_element_by_xpath('//input[@placeholder="CVC"]')
            cvv_form.send_keys(cvv)
            print(gettime() + Fore.GREEN + Style.BRIGHT +' [SUCCESS] -> Successfully checked out!')
            r = s.get(product_url, headers=get_headers)
            soup = bs(r.text, 'lxml')
            title = soup.find('h2', {'class':'entry__title'}).text
            img_span = soup.find('span', {'class':'thumb__img'})
            img_url = 'https://store.sacai.jp' + img_span.find('img')['src']
            paymentype = 'Stripe'
        
        send_webhook(title, random_combination[0], img_url, product_url, paymentype, checkout_time=(datetime.datetime.now() - now).total_seconds())
    except:
        send_webhook(title, random_combination[0], img_url, product_url, paymentype='Manual Checkout', checkout_time=(datetime.datetime.now() - now).total_seconds())
    finally:
        input()
        driver.close()


with open('data.json') as f:
    data_json = json.loads(f.read())
for profile_name in list(data_json.keys()):
    t = Thread(target=run, args=(product_link, data_json, profile_name))
    t.start()
