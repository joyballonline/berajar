from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
#from selenium.webdriver.common.by import By

# ブラウザーを起動
options = Options()
#options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
options.add_argument('--headless')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36')
driver = webdriver.Chrome(options=options)

# Google検索画面にアクセス
driver.get('http://www.sukalifeindo.work/')


# htmlを取得・表示
e = driver.find_element_by_xpath("//div[@class='a1']/a")
e.click()

# ブラウザーを終了
driver.quit()
