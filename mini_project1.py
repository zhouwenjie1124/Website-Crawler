import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import *
import time
import os
import ddddocr
import base64


# ---------------------------------------------------------------------------------------
# basic function for reference
def open_driver(url):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # for ignore warning and error (log information)
    driver = webdriver.Chrome(options=options,executable_path='./chromedriver')
    driver.get(url)
    driver.implicitly_wait(7)  # set a waiting time limit for the browser driver
    driver.maximize_window()
    return driver


def search_a_keyword(keyword):
    '''
    find_element(By.name,'q') act equivalant to find_element_by_name('q')
    the method find_element_by_name is deprecated in latest version

    To search a keyword you need to fill in the keyword and press enter.
    We use send_keys() function to simulate keyborad inputs.
    ref:https://selenium-python.readthedocs.io/locating-elements.html#
    '''
    search_bar = driver.find_element(By.NAME, "q")  # the name of search bar is declare as "q"
    search_bar.send_keys(keyword)  # fill the keyword to the bar
    time.sleep(operate_delay)
    search_bar.send_keys(Keys.RETURN)  # press enter to get the search result
    time.sleep(operate_delay)


def save_the_result(produts):
    import json
    with open('first_page_desctiption.json', 'w') as f:
        json.dump(produts, f, indent=4)

    # ---------------------------------------------------------------------------------------


# Task 1: place the order
# implement the following function and run
def t1_place_the_order(product_name: str):
    def login():
        SIGN_IN_button = driver.find_element(By.XPATH, "//*[@id='basic-navbar-nav']/div/a[2]")
        SIGN_IN_button.click()
        time.sleep(operate_delay)
        Email_bar = driver.find_element(By.ID, "email")
        Password_bar = driver.find_element(By.ID, "password")
        Email_bar.send_keys("mc35355@um.edu.mo")
        Password_bar.send_keys("mc35355")
        time.sleep(operate_delay)
        Password_bar.send_keys(Keys.RETURN)
        time.sleep(2)

    def search_a_keyword(product_name: str):
        search_bar = driver.find_element(By.NAME, "q")  # the name of search bar is declare as "q"
        search_bar.clear()
        search_bar.send_keys(product_name)  # fill the keyword to the bar
        time.sleep(operate_delay)
        search_bar.send_keys(Keys.RETURN)  # press enter to get the search result
        time.sleep(operate_delay)
        item_page = driver.find_element(By.CLASS_NAME, "card-img-top")
        item_page.click()
        time.sleep(2)

    def add_to_cart():
        addcart_button = driver.find_element(By.XPATH,"//*[@id='root']/main/div/div[1]/div[3]/div/div/div[4]/button")
        addcart_button.click()
        time.sleep(operate_delay)
        checkout_button = driver.find_element(By.XPATH,"//*[@id='root']/main/div/div/div[2]/div/div/div[2]/button")
        checkout_button.click()

    def place_order():
        address_bar = driver.find_element(By.ID,"address")
        address_bar.send_keys("mc35355@um.edu.mo")
        city_bar = driver.find_element(By.ID,"city")
        city_bar.send_keys("Macau")
        postal_bar = driver.find_element(By.ID,"postalCode")
        postal_bar.send_keys("8533")
        country_bar = driver.find_element(By.ID,"country")
        country_bar.send_keys("China")
        time.sleep(operate_delay)
        continue_button = driver.find_element(By.XPATH,"//*[@id='root']/main/div/div/div/div/form/button")
        continue_button.click()
        time.sleep(operate_delay)
        continue_button2 = driver.find_element(By.XPATH,"/html/body/div/main/div/div/div/div/form/button")
        continue_button2.click()
        time.sleep(operate_delay)
        continue_button3 = driver.find_element(By.XPATH,"/html/body/div/main/div/div[2]/div[2]/div/div/div[7]/button")
        continue_button3.click()
        time.sleep(operate_delay)


    def hack_captcha():
        canvas_element=driver.find_element(By.XPATH,"//*[@id='canv']")
        # 获取 <canvas> 元素的 Base64 图像数据
        canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/jpg').substring(21);",
                                              canvas_element)
        # 将 Base64 数据解码为图像文件
        image_data = base64.b64decode(canvas_base64)

        ocr = ddddocr.DdddOcr()
        res = ocr.classification(image_data)

        captcha_bar = driver.find_element(By.NAME,"user_captcha_input")
        captcha_bar.send_keys(res)
        time.sleep(operate_delay)
        submit_button = driver.find_element(By.XPATH,"/html/body/div/main/div/div/div[2]/div/div/div[6]/div/div/div/div[3]/div/button")
        submit_button.click()

    login()
    search_a_keyword(product_name)
    add_to_cart()
    place_order()
    hack_captcha()

# Task 2: Find the top-x for a given keyword
def t2_find_top_x(x,keyword):
    top_x_result = []
    products = []
    search_a_keyword(keyword)

    # find the page_number element, if no element then skip "def go_to_next_page(i)",else the number of page = table_num
    i = int(1) # index to decide to go to which page
    try:
        parent_element = driver.find_element(By.XPATH, "//*[@id='root']/main/div/ul")
        child_elements = parent_element.find_elements_by_xpath("./*")
        table_num = len(child_elements)
    except NoSuchElementException:
        table_num = 1

    # Please note that the price is a floating number
    def get_all_product_price_in_one_page():
        card_bodys = wait.until(presence_of_all_elements_located((By.CLASS_NAME, "card-body")))
        for card_body in card_bodys:
            # The product link is under tag 'a'
            product_link = card_body.find_element(By.TAG_NAME, 'a')
            if os.name == 'posix':
                # check Operation System, os.name =='posix' indicate the OS is Mac OS or linux
                product_link.send_keys(Keys.COMMAND, Keys.RETURN)
            else:
                product_link.send_keys(Keys.CONTROL, Keys.RETURN)

            windows = driver.window_handles  # driver.window_handles is the list of windows tag
            # windows[0]=the homepage
            # windows[-1]=the latest open page

            # switch to handle the new window tab
            driver.switch_to.window(windows[-1])
            list_items = wait.until(presence_of_all_elements_located((By.CLASS_NAME, "list-group-item")))
            time.sleep(operate_delay)

            # add data into products
            product = {}  # using name as key,description as value
            price = re.findall(r'\d+\.\d+|\d+', list_items[2].text)
            name = list_items[0].text
            description = list_items[3].text
            product['name'] = name
            product['price'] = float(price[0])
            product['description'] = description
            products.append(product)
            print(product, end='\n\n')

            # return to homepage
            driver.close()
            time.sleep(operate_delay)
            driver.switch_to.window(windows[0])

    def go_to_next_page(i):
        page_item = driver.find_elements(By.CLASS_NAME,"page-item")

        page_item[i].click()
        time.sleep(operate_delay)

    def save_dict_to_csv():

        top_x_result = sorted(products,key=lambda x: x["price"],reverse=True)[:x]
        with open('top_%d_result_of_%s.csv' % (x, keyword), 'w') as f:
            writer = csv.writer(f)
            for item in top_x_result :
                writer.writerow([item])
            return (top_x_result)

    while True:
        get_all_product_price_in_one_page()
        if i == table_num:
            break
        else:
            go_to_next_page(i)
            i += 1

        # you should break the loop if next_page does not exist
    top_x_result = save_dict_to_csv()
    return top_x_result


# Task 3: Place the order to the top-5 products you found in task-2
def t3_order_top5(top_x_result: list ):
    def login():
        SIGN_IN_button = driver.find_element(By.XPATH, "//*[@id='basic-navbar-nav']/div/a[2]")
        SIGN_IN_button.click()
        time.sleep(operate_delay)
        Email_bar = driver.find_element(By.ID, "email")
        Password_bar = driver.find_element(By.ID, "password")
        Email_bar.send_keys("mc35355@um.edu.mo")
        Password_bar.send_keys("mc35355")
        time.sleep(operate_delay)
        Password_bar.send_keys(Keys.RETURN)
        time.sleep(2)

    def search_a_keyword(product_name: str):
        search_bar = driver.find_element(By.NAME, "q")  # the name of search bar is declare as "q"
        search_bar.clear()
        search_bar.send_keys(product_name)  # fill the keyword to the bar
        time.sleep(operate_delay)
        search_bar.send_keys(Keys.RETURN)  # press enter to get the search result
        time.sleep(operate_delay)
        item_page = driver.find_element(By.CLASS_NAME, "card-img-top")
        item_page.click()
        time.sleep(2)

    def add_to_cart_return_homepage ():
        addcart_button = driver.find_element(By.XPATH,"//*[@id='root']/main/div/div[1]/div[3]/div/div/div[4]/button")
        addcart_button.click()
        time.sleep(operate_delay)
        homepage_button = driver.find_element(By.XPATH,"/html/body/div/header/nav/div/a")
        homepage_button.click()

    def enter_cart_place_order():
        cart_button = driver.find_element(By.XPATH, "/html/body/div/header/nav/div/div/div/a[1]")
        cart_button.click()
        checkout_button = driver.find_element(By.XPATH, "/html/body/div/main/div/div/div[2]/div/div/div[2]/button")
        checkout_button.click()
        address_bar = driver.find_element(By.ID, "address")
        address_bar.send_keys("mc35355@um.edu.mo")
        city_bar = driver.find_element(By.ID, "city")
        city_bar.send_keys("Macau")
        postal_bar = driver.find_element(By.ID,"postalCode")
        postal_bar.send_keys("8533")
        country_bar = driver.find_element(By.ID,"country")
        country_bar.send_keys("China")
        time.sleep(operate_delay)
        continue_button = driver.find_element(By.XPATH,"//*[@id='root']/main/div/div/div/div/form/button")
        continue_button.click()
        time.sleep(operate_delay)
        continue_button2 = driver.find_element(By.XPATH,"/html/body/div/main/div/div/div/div/form/button")
        continue_button2.click()
        time.sleep(operate_delay)
        continue_button3 = driver.find_element(By.XPATH,"/html/body/div/main/div/div[2]/div[2]/div/div/div[7]/button")
        continue_button3.click()
        time.sleep(operate_delay)

    def hack_captcha():
        canvas_element=driver.find_element(By.XPATH,"//*[@id='canv']")
        # 获取 <canvas> 元素的 Base64 图像数据
        canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/jpg').substring(21);",
                                              canvas_element)
        # 将 Base64 数据解码为图像文件
        image_data = base64.b64decode(canvas_base64)

        ocr = ddddocr.DdddOcr()
        res = ocr.classification(image_data)

        captcha_bar = driver.find_element(By.NAME,"user_captcha_input")
        captcha_bar.send_keys(res)
        time.sleep(operate_delay)
        submit_button = driver.find_element(By.XPATH,"/html/body/div/main/div/div/div[2]/div/div/div[6]/div/div/div/div[3]/div/button")
        submit_button.click()

    login()

    for product in top_x_result:
        search_a_keyword(product['name'])
        add_to_cart_return_homepage()

    enter_cart_place_order()
    hack_captcha()

url = 'http://10.113.178.219'  # the url of shopping cart
operate_delay = 1  # the time gap between each process

# end of parameters declaration
top_result = []
for task in [t1_place_the_order, t2_find_top_x, t3_order_top5]:
    driver = open_driver(url)
    wait = WebDriverWait(driver, 10)  # set a maximum implicit waiting time for the browser driver
    if task == t1_place_the_order:
        task('IPHONE 11 PRO 256GB MEMORY')
    if task == t2_find_top_x:
        top_result = task(3, 'phone')
    if task == t3_order_top5:
        task(top_result)
    driver.close()

# 基本功能已实现，有待优化的问题：1.task2异常处理等待时间过长（只有一页） 2.出现按名字搜索出现第一框是另外的商品 3.readme document里面的小要求