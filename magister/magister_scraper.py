import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
from seleniumwire import webdriver
import os
import platform
# Importing libraries

class Scraper:

    def __init__(self, username, password, school) -> bool:

        # Adding chrome driver, and launching it in headless mode:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        if platform.system() == "Windows":
            chrome_driver = os.getcwd() + "\\app\\chromedriver.exe"
        if platform.system() == "Linux":
            chrome_driver = os.getcwd() + "/chromedriver"
            # chrome_options.add_argument("--remote-debugging-port=9222")
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

        # Uncomment for Firefox GUI webdriver:
        # driver = webdriver.Firefox()
        self.driver = webdriver.Chrome(
            chrome_options=chrome_options)
        # Navigating to Magister and loging in,
        # Grabbing the accestoken for the private API:
        self.driver.get("https://" + school + ".magister.net")
        self.driver.implicitly_wait(3)
        elem = self.driver.find_element_by_id("username")
        elem.clear()
        elem.send_keys(username)
        elem.send_keys(Keys.RETURN)
        sleep(0.5)
        elem = self.driver.find_element_by_id("i0118")
        elem.clear()
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        elem = self.driver.find_element_by_id("idSIButton9")
        elem.click()
        sleep(2)
    


    def rooster(self):

        elem = self.driver.find_element_by_id("menu-agenda")
        elem.click()
        time.sleep(2)

        elem = self.driver.find_element_by_xpath('//*[@id="afsprakenLijst"]/div[2]/table/tbody')
        #get subelements from elem
        elems = elem.find_elements_by_tag_name('tr')

        daynum = 0

        rooster_items = []

        # get text from subelements
        for i in range(1, len(elems)+1):

            rooster_item = {
                "lesuur": -1,
                "vak": "",
                "docent": "",
                "lokaal": "",
            }
            # get elem class
            xpath = f'//*[@id="afsprakenLijst"]/div[2]/table/tbody/tr[{i}]'
            elem = self.driver.find_element_by_xpath(xpath)
            class_name = elem.get_attribute('class')
            if class_name == "k-grouping-row ng-scope":
                daynum += 1
                if daynum == 2:
                    break
            else:
                xpath2 = xpath + "/td[3]/span/span[1]"
                elem2 = self.driver.find_element_by_xpath(xpath2)
                lesuur = int(elem2.text)
                rooster_item["lesuur"] = lesuur

                xpath3 = xpath + "/td[3]/span/span[2]"
                elem3 = self.driver.find_element_by_xpath(xpath3)
                txt = elem3.text

                vak, _, docent, _,_ = txt.split(" ")

                xpath4 = xpath + "/td[3]/span/span[3]"
                elem4 = self.driver.find_element_by_xpath(xpath4)
                lokaal = elem4.text

                rooster_item["vak"] = vak
                rooster_item["docent"] = docent
                # remove the first and last chr
                rooster_item["lokaal"] = lokaal[1:-1]

                rooster_items.append(rooster_item)


        return rooster_items


    def cijfers(self):
        
        menu_item_xpath = '//*[@id="menu-cijfers"]'

        elem = self.driver.find_element_by_xpath(menu_item_xpath)
        elem.click()

        time.sleep(2)

        cijverlijst_xpath = '//*[@id="cijfers-laatst-behaalde-resultaten-container"]/section/div/div[2]/div/div/table/tbody'
        elem = self.driver.find_element_by_xpath(cijverlijst_xpath)
        elems = elem.find_elements_by_tag_name('tr')

        cijvers = []

        for cijver_elem in elems:
            cijver = {
                "vak": "",
                "datum_invoer":"",
                "omschrijving":"",
                "cijver":-1,
                "weging":0
                    }
            
            # get td elems from cijver_elem
            td_elems = cijver_elem.find_elements_by_tag_name('td')
            # get text from td elems
            txt = [td_elem.text for td_elem in td_elems]
            
            cijver["vak"] = txt[0]
            cijver["datum_invoer"] = txt[1]
            cijver["omschrijving"] = txt[2]
            cijver["omschrijving"] = txt[2]
            cijver["cijfer"] = txt[3]
            cijver["weging"] = int(txt[4][:-1])

            cijvers.append(cijver)
        
        return cijvers