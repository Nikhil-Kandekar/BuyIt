import unittest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
import xlwt

workbook = xlwt.Workbook() 
sheet = workbook.add_sheet("Test Case",cell_overwrite_ok=True)
bold = xlwt.easyxf('font: bold 1')
fail = xlwt.easyxf('font: bold 1,color red;')
success = xlwt.easyxf('font: bold 1,color green;')
sheet.write(0, 0, 'Sr. No.', bold)
sheet.write(0, 1, 'Test Case', bold)
sheet.write(0, 2, 'Status', bold)

test_cases=['Check if admin can login',
            'Check if admin can logout',
            'Check if user can login',
            'Check if user can logout',
            'Check if logo takes user to homescreen',
            'Check if searched item is available',
            'Check add to cart functionality',
            'Check pricing',
            'Check checkout functionality',
            'Check if cart is empty',
            'Check user orders',
            'Check if order is placed',
            'Check if user can comment',
            'Check if user comment is saved'
            ]

for i in range(1,15):
    sheet.write(i, 0, i)
    sheet.write(i, 1,   test_cases[i-1]) 
    sheet.write(i, 2, 'Fail', fail)

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
driver.maximize_window()

def elementWaitClick(delay,xpath):
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
    myElem.click()

def elementWaitGetText(delay,xpath):
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
    return myElem.text

def enterDataInElement(xpath,keys):
    driver.find_element(By.XPATH,xpath).send_keys(keys)


driver.get('http://localhost:3000')
assert "Welcome To Buy It" == driver.title ,"Website Title error"

def adminLogin():
    assert elementWaitGetText(4,'//*[@id="basic-navbar-nav"]/div/a[2]') == "SIGN IN" ,"User already signed in"
    elementWaitClick(4,'//*[@id="basic-navbar-nav"]/div/a[2]')
    enterDataInElement('//*[@id="email"]',"admin@example.com")
    enterDataInElement('//*[@id="password"]',"123456")
    elementWaitClick(2,'//*[@id="root"]/main/div/div/div/div/form/button')
    assert elementWaitGetText(4,'//*[@id="username"]') ==  "ADMIN USER" ," User is not Admin user"

def userLogin():
    assert elementWaitGetText(4,'//*[@id="basic-navbar-nav"]/div/a[2]') == "SIGN IN" ,"User already logged in"
    elementWaitClick(4,'//*[@id="basic-navbar-nav"]/div/a[2]')
    enterDataInElement('//*[@id="email"]',"john@example.com")
    enterDataInElement('//*[@id="password"]',"123456")
    elementWaitClick(2,'//*[@id="root"]/main/div/div/div/div/form/button')
    assert elementWaitGetText(4,'//*[@id="username"]') ==  "JOHN DOE" ,"User name incorrect"

def logoutUser():
    elementWaitClick(4,'//*[@id="username"]')
    elementWaitClick(4,'//*[@id="basic-navbar-nav"]/div/div/div/a[2]')

def homeScreen():
    elementWaitClick(4,'//*[@id="root"]/header/nav/div/a/img')

def searchProduct(item):
    enterDataInElement('//*[@id="basic-navbar-nav"]/form/input',item)
    elementWaitClick(4,'//*[@id="basic-navbar-nav"]/form/button')
    if elementWaitGetText(4,'//*[@id="root"]/main/div/div/div/div/div/a/div/strong'):
        assert item in elementWaitGetText(4,'//*[@id="root"]/main/div/div/div/div/div/a/div/strong'),"Item not found"

def addToCart():
    elementWaitClick(4,'//*[@id="root"]/main/div/div[2]/div[2]/div/div/a/div/strong')
    elementWaitClick(4,'//*[@id="root"]/main/div/div[1]/div[3]/div/div/div[3]/div/div[2]/select')
    elementWaitClick(4,'//*[@id="root"]/main/div/div[1]/div[3]/div/div/div[3]/div/div[2]/select/option[3]')
    elementWaitClick(4,'//*[@id="root"]/main/div/div[1]/div[3]/div/div/div[4]/button')

    elementWaitClick(4,'//*[@id="root"]/main/div/div/div[2]/div/div/div[2]/button')
    if elementWaitGetText(4,'//*[@id="basic-navbar-nav"]/div/a[2]') == "SIGN IN":
        userLogin()
        elementWaitClick(4,'//*[@id="basic-navbar-nav"]/div/a')

def checkCart():
    mrp=elementWaitGetText(4,'//*[@id="root"]/main/div/div/div[1]/div/div/div/div[3]')
    assert mrp == "₹6000", "Price incorrect"
    assert "(3)" in elementWaitGetText(4,'//*[@id="root"]/main/div/div/div[2]/div/div/div[1]/h2') , "Quantity incorrect"
    assert "₹18000.00" in elementWaitGetText(4,'//*[@id="root"]/main/div/div/div[2]/div/div/div[1]') , "SubTotal error"

def checkOutCart():
    elementWaitClick(4,'//*[@id="root"]/main/div/div/div[2]/div/div/div[2]/button')
    shippingAddress()
    assert "₹2700.00" in elementWaitGetText(4,'//*[@id="root"]/main/div/div[2]/div[2]/div/div/div[4]/div/div[2]') , "Incorrect taxation amount "
    assert "₹20700.00" in elementWaitGetText(4,'//*[@id="root"]/main/div/div[2]/div[2]/div/div/div[5]/div/div[2]') , "Incorrect Total Amount"
    elementWaitClick(4,'//*[@id="root"]/main/div/div[2]/div[2]/div/div/div[7]/button')

def payment():
    myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="credit-card-number"]')))
    enterDataInElement('//*[@id="credit-card-number"]',"4032036478270935")
    enterDataInElement('//*[@id="expiry-date"]',"1225")
    enterDataInElement('//*[@id="credit-card-security"]',"123")
    enterDataInElement('//*[@id="root"]/div/div/form/div/div[4]/div[2]/div[1]/div[1]/input',"John")
    enterDataInElement('//*[@id="root"]/div/div/form/div/div[4]/div[2]/div[3]/div/input',"Doe")
    enterDataInElement('//*[@id="root"]/div/div/form/div/div[4]/div[3]/div[1]/div/div[1]/input',"abcd")
    enterDataInElement('//*[@id="root"]/div/div/form/div/div[4]/div[3]/div[2]/div/div/input',"lmno")
    enterDataInElement('//*[@id="root"]/div/div/form/div/div[4]/div[3]/div[3]/div/div[1]/input',"pqr")
    elementWaitClick(4,'//*[@id="root"]/div/div/form/div/div[4]/div[3]/div[4]/div/div[1]/div/select')
    elementWaitClick(4,'//*[@id="root"]/div/div/form/div/div[4]/div[3]/div[4]/div/div[1]/div/select/option[2]')
    enterDataInElement('//*[@id="root"]/div/div/form/div/div[4]/div[3]/div[5]/div/div/input',"35007")
    enterDataInElement('//*[@id="phone"]',"4082310194")
    enterDataInElement('//*[@id="email"]',"sb-wazjx3792005@personal.example.com")
    elementWaitClick(4,'//*[@id="submit-button"]')

def shippingAddress():
    enterDataInElement('//*[@id="address"]',"Pimpri")
    enterDataInElement('//*[@id="city"]',"Pune")
    enterDataInElement('//*[@id="postalCode"]',"411018")
    enterDataInElement('//*[@id="country"]',"India")
    elementWaitClick(4,'//*[@id="root"]/main/div/div/div/div/form/button')
    elementWaitClick(4,'//*[@id="root"]/main/div/div/div/div/form/button')

def ordersInProfile():
    elementWaitClick(4,'//*[@id="username"]')
    elementWaitClick(4,'//*[@id="basic-navbar-nav"]/div/div/div/a[1]')
    elementWaitClick(4,'//*[@id="root"]/main/div/div/div[2]/div/table/tbody/tr[2]/td[6]/a')

def orderPlaced():
    assert "Paid" in elementWaitGetText(4,'//*[@id="root"]/main/div/div/div[1]/div/div[2]/div'), "Payment not done"
    assert "Not Delivered" in elementWaitGetText(4,'//*[@id="root"]/main/div/div/div[1]/div/div[1]/div'), "Delivered"

def emptycart():
    elementWaitClick(4,'//*[@id="basic-navbar-nav"]/div/a')
    assert elementWaitGetText(4,'//*[@id="root"]/main/div/div/div[1]/div') , "Cart not empty"

def comment():
    elementWaitClick(4,'//*[@id="root"]/main/div/div[2]/div[1]/div/a/img')
    elementWaitClick(4,'//*[@id="rating"]')
    elementWaitClick(4,'//*[@id="rating"]/option[5]')
    enterDataInElement('//*[@id="comment"]',"Best Product")
    elementWaitClick(4,'//*[@id="root"]/main/div/div[2]/div/div/div[4]/form/button')

def clearSearch():
    driver.find_element(By.XPATH,'//*[@id="basic-navbar-nav"]/form/input').clear()

def checkComment():
    driver.get("http://localhost:3000/product/5fb50ad94ac05c1ee077fbd9")
    driver.refresh()
    assert "Nikhil Kandekar" in elementWaitGetText(4,'//*[@id="root"]/main/div/div[2]/div/div/div[1]/strong'),"Comment not by John Doe"
    assert "Very nice product" == elementWaitGetText(4,'//*[@id="root"]/main/div/div[2]/div/div/div[1]/p[2]')

try:
    # TEST CASE 1 check if admin can login
    adminLogin()
    sheet.write(1, 2, 'Success', success)
    # TEST CASE 2 check if admin can logout
    logoutUser()
    sheet.write(2, 2, 'Success', success)
    # TEST CASE 3 check if user can login
    userLogin()
    sheet.write(3, 2, 'Success', success)
    # TEST CASE 4 check if user can logout
    logoutUser()
    sheet.write(4, 2, 'Success', success)
    # TEST CASE 5 check if logo takes user to homescreen
    homeScreen()
    sheet.write(5, 2, 'Success', success)
    # TEST CASE 6 check if searched item is available
    searchProduct("Camera")
    homeScreen()
    sheet.write(6, 2, 'Success', success)
    # TEST CASE 7 check add to cart functionality
    addToCart()
    sheet.write(7, 2, 'Success', success)
    # TEST CASE 8 check pricing
    checkCart()
    sheet.write(8, 2, 'Success', success)
    # TEST CASE 9 check checkout functionality
    checkOutCart()
    sheet.write(9, 2, 'Success', success)
    # TEST CASE 10 check if cart is empty
    emptycart()
    sheet.write(10, 2, 'Success', success)
    # TEST CASE 11 check user orders
    ordersInProfile()
    sheet.write(11, 2, 'Success', success)
    # TEST CASE 12 check if order is placed
    orderPlaced()
    homeScreen()
    clearSearch()
    sheet.write(12, 2, 'Success', success)
    # TEST CASE 13 check if user can comment
    comment()
    homeScreen()
    sheet.write(13, 2, 'Success', success)
    # TEST CASE 14 check if user comment is saved
    checkComment()
    sheet.write(14, 2, 'Success', success)
except TimeoutException:
    print("Loading took too much time!")

time.sleep(10)
driver.quit()
workbook.save("LP2.xls")
