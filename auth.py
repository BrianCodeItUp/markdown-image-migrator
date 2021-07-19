from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from imgurpython import ImgurClient
import configparser

def authenticate():
  config = configparser.ConfigParser()
  config.read('auth.ini')

  client_id = config.get('credentials', 'client_id')
  client_secret = config.get('credentials', 'client_secret')  
  imgur_username = config.get('credentials', 'imgur_username')  
  imgur_password = config.get('credentials', 'imgur_password')

  client = ImgurClient(client_id, client_secret)
  auth_url = client.get_auth_url('pin')
  
  print(auth_url)
  browser = webdriver.Chrome('./chromedriver')
  browser.get(auth_url)

  username = browser.find_element_by_id('username')
  password = browser.find_element_by_id('password')
  username.send_keys(imgur_username)
  password.send_keys(imgur_password)
  browser.find_element_by_id('allow').click()

  timeout = 5
  try:
    element_presnet = EC.presence_of_element_located((By.ID, 'pin'))
    WebDriverWait(browser, timeout).until(element_presnet)
    pin_element = browser.find_element_by_id('pin')
    pin = pin_element.get_attribute('value')
  except TimeoutException:
    print("Timeout out waiting for page to load")

  browser.close()
  credentials = client.authorize(pin, 'pin')
  client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
  print("Authentication Successfully!")
  return client


if __name__ == '__main__':
  authenticate()


