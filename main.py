import requests
from selenium import webdriver
driver = webdriver.Chrome()
if __name__ == '__main__':
    print("Hello World!")
    driver.get('https://www.charlotte.edu/')
    print(driver.title)




