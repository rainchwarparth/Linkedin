from time import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver  
import time
 
def diver():
    global driver
    driver = webdriver.Chrome(ChromeDriverManager().install())

def gotourl(str):
    url = str
    driver.get(url)

def sleep(tim):
    time.sleep(tim)

def implicitly_wait(tim):
    driver.implicitly_wait(tim)

def execute_script():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

def execute_script_to_top():
    driver.execute_script("window.scrollTo(0,0)")


def find_element_xpath(str_xpath):
    driver.find_element("xpath",str_xpath)

def find_element_xpath_get_attr(str_xpath,attr):
    val = driver.find_element("xpath",str_xpath).get_attribute(attr)
    return val

def find_element_xpath_click(str_xpath_click):
    var = driver.find_element("xpath",str_xpath_click)
    var.click()

def find_element_xpath_click_send_keys(str_xpath_click_send_keys,keys):
    var = driver.find_element("xpath",str_xpath_click_send_keys)
    var.click()
    var.send_keys(keys)

def close():
    driver.close()

def driver_find_text(str_xpath_text):
    val = driver.find_element("xpath",str_xpath_text).text
    return val

def execute_script_runtime(a,b):
    driver.execute_script("window.scrollTo({},{})".format(a,b))

def is_selected(str_xpath_isselected):
    val = driver.find_element("xpath",str_xpath_isselected).is_selected()
    return val

def src_code():
    val = driver.page_source
    return val

def get__url():
    val = driver.current_url
    return val
#removal of the prev fxn