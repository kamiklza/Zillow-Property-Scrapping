from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
desktop_driver_path = "C:/Users/user/PycharmProjects/chromedriver.exe"

header = {
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"

}

zillow_website = "https://www.zillow.com/san-francisco-ca/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.5645923614502%2C%22east%22%3A-122.39842414855957%2C%22south%22%3A37.653858877365266%2C%22north%22%3A37.81025862543724%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D"
response = requests.get(url=zillow_website, headers=header)
web_content = response.text


soup = BeautifulSoup(web_content, "html.parser")
all_listings = soup.find(id="grid-search-results").find(name="ul").find_all(name="li")

price_list = []
address_list = []
url_list = []
for listing in all_listings:
    try:
        url_list.append(listing.find(name="a").get("href"))
        address_list.append(listing.find(name="address").getText())
        price_list.append(listing.find(class_="list-card-price").getText().split("$")[1].split("+")[0].split("/")[0].replace(",", ""))
    except AttributeError:
        pass

print(url_list)
print(address_list)
print(price_list)

form_address = "https://docs.google.com/forms/d/e/1FAIpQLSfpmCbN5YRuLFFKY7eqVgqmWehszkexeP6QY1_3ZCDPZMFrKw/viewform"

driver = webdriver.Chrome(executable_path=desktop_driver_path)
driver.get(url=form_address)

for n in range(len(url_list)):
    question_1 = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    question_1.send_keys(address_list[n])
    question_2 = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    question_2.send_keys(price_list[n])
    question_3 = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    question_3.send_keys(url_list[n])
    time.sleep(2)
    submit = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    submit.click()
    time.sleep(2)
    back_to_form = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    back_to_form.click()
    time.sleep(2)


