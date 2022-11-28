import datetime
import pandas as pd
from datetime import date
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import getpass
import os.path
import wget

ID = str(input("Enter your ID: "))
p = getpass.getpass()
driver = webdriver.Chrome("//Users/piercest/Desktop/kodvs/chromedriver")
driver.get("https://www.instagram.com")
sleep(3)

username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']" )))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']" )))

username.clear()
password.clear()
username.send_keys(ID)
password.send_keys(p)

accept_all = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept All')]"))).click()
sleep(2)
log_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
sleep(2)
Not_now = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not now')]"))).click()
sleep(2)
Not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
sleep(2)

driver.get("https://www.instagram.com/bernakpln")
sleep(3)

following_number = driver.find_element(By.XPATH, "//a[contains(@href, '/following')]").textx
following_number = int(following_number[:following_number.index(" ")])

following = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/following')]"))).click()
sleep(2)

scroll_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[6]/div/div/div[3]")))

last_ht,ht = 0,1

while last_ht != ht:
    last_ht = ht
    ht= driver.execute_script(""" arguments[0].scrollTo(0, arguments[0].scrollHeight);return arguments[0].scrollHeight; """, scroll_box)

sleep(5)
links = scroll_box.find_elements_by_tag_name('a')
sleep(2)
names = [name.text for name in links if name.text != '']
names = names[0:following_number]
sleep(5)

driver.get("https://www.instagram.com/"+names[0]+"/")
posts = driver.find_element(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span").text
posts.replace(",","")

index = 0
usersl = []
dates = []
while index < following_number:
    driver.get("https://www.instagram.com/" + names[index] + "/")
    posts = driver.find_element(By.XPATH,
                                "//*[@id='react-root']/section/main/div/header/section/ul/li[1]/span/span").text
    posts.replace(",", "")
    if posts == "0":

        print("No posts have found")
    else:
        try:

            photo = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                "//*[@id='react-root']/section/main/div/div[3]/article/div/div/div/div[1]/a/div/div[2]"))).click()
            sleep(2)
            time = (driver.find_element_by_xpath("//time[@class='_1o9PC Nzb55']").get_attribute("datetime"))
            year = int(time[0:4])
            month = int(time[5:7])
            day = int(time[8:10])
            photodate = date(year, month, day)
            today = date.today()
            diff = today - photodate
            if diff.days > 180:
                usersl.append(names[index])
                dates.append(diff.days)
            index += 1
            sleep(2)


        except:

            video = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                "//*[@id='react-root']/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]/a/div[1]/div[2]"))).click()
            sleep(2)
            time = (driver.find_element_by_xpath("//time[@class='_1o9PC Nzb55']").get_attribute("datetime"))
            year = int(time[0:4])
            month = int(time[5:7])
            day = int(time[8:10])
            photodate = date(year, month, day)
            today = date.today()
            diff = today - photodate
            if diff.days > 180:
                usersl.append(names[index])
                dates.append(diff.days)
            index += 1
            sleep(2)

dict1 = {"Username":usersl,"Days since last photo":dates}
df = pd.DataFrame(dict1)

i = 0
while i < len(usersl):
    driver.get("https://www.instagram.com/"+usersl[i]+"/")
    unfollow1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button"))).click()
    unfollow = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Unfollow')]"))).click()
    i += 1
    sleep(1)
print(df)






