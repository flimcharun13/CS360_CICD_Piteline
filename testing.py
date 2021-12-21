import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import json

path_config = "bin/config.json"

options = webdriver.ChromeOptions()
options.headless = True # True - the window is hidden, False - the window is not hidden
options.add_argument("--start-maximized")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driverfile = ChromeDriverManager().install()

def login_function(id,password,ip): #1 #7
    driver = webdriver.Chrome(driverfile,options=options)
    if '8082' in ip:
        driver.get(ip+'/login')
    else:
        driver.get(ip)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(id)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login > button'))).click()
    time.sleep(3)
    login_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'swal2-title'))).text.strip()

    if login_text == 'เข้าสู่ระบบสำเร็จ':
        print('login Successed')
        driver.quit()
        return True
    else:
        print('login Failed')
        driver.quit()
        return False

def logout(id,password,ip): #8 #9
    driver = webdriver.Chrome(driverfile,options=options)
    driver.get(ip+'/login')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username'))).send_keys(id)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login > button'))).click()
    time.sleep(3)
    login_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'swal2-title'))).text.strip()

    if login_text == 'เข้าสู่ระบบสำเร็จ':
        print('login Successed')
        driver.get(ip+'/logout')
        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#navbarSupportedContent > ul > li > a'))).text
        time.sleep(3)
        if logout in 'เข้าสู่ระบบ / สมัครสมาชิก':
            print('logout Successed')
            driver.quit()
            return True
        else:
            print('logout Failed')
            driver.quit()
            return False
    else:
        print('login Failed')
        driver.quit()
        return False

def register_function(id,password,name,ip): #2
    driver = webdriver.Chrome(driverfile,options=options)
    driver.get(ip+'/register')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(id)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'conpassword'))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#register > div:nth-child(5) > input'))).send_keys(name)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#register > div:nth-child(6) > input'))).send_keys('lovely')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#register > div:nth-child(9) > input'))).send_keys('teejirapat@hotmail.com')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#register > button'))).click()
    time.sleep(3)
    register_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'swal2-title'))).text.strip()

    if register_text == 'สมัครสมาชิกสำเร็จ':
        print('register Successed')
        driver.quit()
        result = login_function(id,password,ip)
        if result is True:
            print('login new member Successed')
        else:
            print('login new member Failed')
    else:
        print('register Failed')
        driver.quit()


def __getconnectmongodb() :
	global path_config

	with open(path_config,"r",encoding="utf8") as conf :
		d = json.loads(conf.read())
		if d["mongodb"]["srv"] is True :
			res = "mongodb+srv://%s:%s@%s/%s" % (
				d["mongodb"]["username"],
				d["mongodb"]["password"],
				d["mongodb"]["host"],
				d["mongodb"]["database_auth"]
			)
		else :
			res = "mongodb://%s:%s@%s:%s/%s" % (
				d["mongodb"]["username"],
				d["mongodb"]["password"],
				d["mongodb"]["host"],
				d["mongodb"]["port"],
				d["mongodb"]["database_auth"]
			)

		return res

def __connectdb() :
	e = None 

	try :
		conn = pymongo.MongoClient(__getconnectmongodb(),serverSelectionTimeoutMS=5000)
		conn.server_info()

		return conn
	except Exception as e :
		print("Failed connect to MongoDB retrying connect....")

def check_user_members_database(id): #3

    conn = __connectdb()
    t = conn["hotelsystem"]["user_members"].find({})
    for i in t:
        if i['username'] == id:
            return True

    return False


def check_name_member_display(id,password,name,ip): #4
    driver = webdriver.Chrome(driverfile,options=options)
    driver.get(ip+'/login')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(id)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login > button'))).click()
    time.sleep(3)
    login_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'swal2-title'))).text.strip()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled'))).click()
    if login_text == 'เข้าสู่ระบบสำเร็จ':
        print('login Successed')
        web_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'profile'))).text.strip()
        if name in web_name:
            print('displayed')
            driver.quit()
            return True
        else:
            print('Not displayed')
            driver.quit()
            return False
    else:
        print('login Failed')
        driver.quit()
        return False

def change_name_member(id,password,name,ip): #5
    driver = webdriver.Chrome(driverfile,options=options)
    driver.get(ip+'/login')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(id)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login > button'))).click()
    time.sleep(3)
    login_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'swal2-title'))).text.strip()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled'))).click()
    if login_text == 'เข้าสู่ระบบสำเร็จ':
        print('login Successed')
        driver.get(ip+'/profile')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div > div.overlay > div > div > div > div > div > button.btn.btn-success.font-thai-regular.btn-block.changeprofile'))).click()
        change_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'firstname')))
        change_name.clear()
        change_name.send_keys(name)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#profile-change > button'))).click()
        time.sleep(8)
        change_noti = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'swal2-title'))).text
        if change_noti == 'สำเร็จ':
            print('Change name Successed')
            driver.quit()
            return True
        else:
            print('Change name Failed')
            driver.quit()
            return False

    else:
        print('login Failed')
        print('Change name Failed')
        driver.quit()
        return False

def change_password_member_display(id,password,new_password,ip): #6
    driver = webdriver.Chrome(driverfile,options=options)
    driver.get(ip+'/login')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(id)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password'))).send_keys(password)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login > button'))).click()
    time.sleep(3)
    login_text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'swal2-title'))).text.strip()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.swal2-container.swal2-center.swal2-backdrop-show > div > div.swal2-actions > button.swal2-confirm.swal2-styled'))).click()
    if login_text == 'เข้าสู่ระบบสำเร็จ':
        print('login Successed')
        driver.get(ip+'/profile')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div > div.overlay > div > div > div > div > div > button.btn.btn-primary.font-thai-regular.btn-block.password'))).click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(new_password)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'conpassword'))).send_keys(new_password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#passwordchange > button'))).click()
        time.sleep(8)
        change_noti = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'swal2-title'))).text
        if change_noti == 'สำเร็จ':
            print('Change password Successed')
            driver.quit()
            return True
        else:
            print('Change password Failed')
            driver.quit()
            return False

    else:
        print('login Failed')
        print('Change password Failed')
        driver.quit()
        return False

def check_name_members_database(name): #10

    conn = __connectdb()
    t = conn["hotelsystem"]["user_members"]["details"].find()
    for i in t:
        if i["firstname"] == name:
            return True

    return False

one=login_function('members3','members3','http://ec2-35-173-178-52.compute-1.amazonaws.com:8082')
two=login_function('admin','admin','http://ec2-54-167-192-205.compute-1.amazonaws.com:9000')
three=logout('members3','members3','http://ec2-35-173-178-52.compute-1.amazonaws.com:8082')
#four=logout('admin','admin','http://ec2-54-167-192-205.compute-1.amazonaws.com:9000')
five=register_function('members8','members8','jirapat','http://ec2-35-173-178-52.compute-1.amazonaws.com:8082')
six=check_user_members_database('members8')
seven=check_name_member_display('members8','members8','jirapat','http://ec2-35-173-178-52.compute-1.amazonaws.com:8082')
eight=change_password_member_display('members8','members8','members8test','http://ec2-35-173-178-52.compute-1.amazonaws.com:8082')
nine=change_name_member('members8','members8test','Tom','http://ec2-35-173-178-52.compute-1.amazonaws.com:8082')
ten=check_name_members_database('Tom')
print('user login function test:',one)
print('admin login function test:',two)
print('user logout function test:',three)
#print('admin logout function test:',four)
print('register function test:',five)
print('check_user_members_database test:',six)
print('check_name_member_display test:',seven)
print('change_password_member_display test:',eight)
print('change_name_member test:',nine)
print('check_name_members_database test:',ten)
