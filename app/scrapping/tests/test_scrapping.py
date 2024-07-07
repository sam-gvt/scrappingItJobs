
from scrapping import script_scrapping
from django.test import TestCase


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time


class ScrappingBaseTest(TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = '/usr/bin/chromium'

        service = Service('/usr/bin/chromedriver')

        self.driver = webdriver.Chrome(service=service, options=chrome_options)


    def test_script_set_up(self):
        self.driver.get("https://google.com/")
        # html_content = self.driver.page_source
        # print(html_content)

        input_element = self.driver.find_element(By.NAME, "q")
        input_element.send_keys("Django documentation" + Keys.ENTER)

        # Attendre que les résultats de la recherche soient visibles
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        self.assertIn("Django documentation", self.driver.title)


    def test_freework_login(self):
        self.driver.get("https://www.free-work.com/fr/tech-it")
        input_element = self.driver.find_element(By.LINK_TEXT, "Connexion")
        input_element.click()

        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        email.send_keys("sam.grandvincent.developer@gmail.com")
        password.send_keys("Ps3123456!" + Keys.ENTER)

        time.sleep(5)

        self.driver.get("https://www.free-work.com/fr/alerts")
        element = self.driver.find_element(By.TAG_NAME, "h1")

        self.assertIn("Mes alertes offres de mission ou d’emploi", element.text)




class ScrappingPrivateTest(TestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-dev-shm-usage')

        chrome_options.binary_location = '/usr/bin/chromium'

        service = Service('/usr/bin/chromedriver')

        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        self.driver.get("https://www.free-work.com/fr/tech-it")
        input_element = self.driver.find_element(By.LINK_TEXT, "Connexion")
        input_element.click()

        email = self.driver.find_element(By.ID, "email")
        password = self.driver.find_element(By.ID, "password")
        email.send_keys("sam.grandvincent.developer@gmail.com")
        password.send_keys("Ps3123456!" + Keys.ENTER)

        time.sleep(5)

    def test_get_date_and_title_job(self):
        self.driver.get("https://www.free-work.com/fr/tech-it/jobs?query=Django&contracts=contractor&sort=date")
        time.sleep(5)
        dates = self.driver.find_elements(By.XPATH, "//div[@class='col-span-3 lg:col-span-2']//time")
        titles = self.driver.find_elements(By.XPATH, "//div[@class='col-span-3 lg:col-span-2']//a")
        time.sleep(5)
        # for title in titles:
        #     print(title.text)
        for date in dates:
            print(date.text)

    def test_get_date_job(self):
        self.driver.get("https://www.free-work.com/fr/tech-it/jobs?query=Django&contracts=contractor&sort=date")
        time.sleep(5)
        dates = self.driver.find_elements(By.XPATH, "//div[@class='col-span-3 lg:col-span-2']//time")
        titles = self.driver.find_elements(By.XPATH, "//div[@class='col-span-3 lg:col-span-2']//a")
        time.sleep(5)
        # for title in titles:
        #     print(title.text)
        for date in dates:
            print(date.text)


    def test_get_tag_skills(self):
        self.driver.get("https://www.free-work.com/fr/tech-it/jobs?query=Django&contracts=contractor&sort=date")
        time.sleep(5)
        tags = self.driver.find_elements(By.XPATH, "(//div[@class='col-span-3 lg:col-span-2'])//div[contains(@class, 'truncate') and contains(@class, 'py-[2px]')]")
        for tag in tags:
            print(tag.text)

    def test_get_tags_skills_for_2nd_job(self):
        self.driver.get("https://www.free-work.com/fr/tech-it/jobs?query=Django&contracts=contractor&sort=date")
        time.sleep(5)
        tags = self.driver.find_elements(By.XPATH, "(//div[@class='mb-4 relative rounded-lg max-full bg-white flex flex-col cursor-pointer shadow hover:shadow-md'])[2]//div[contains(@class, 'truncate') and contains(@class, 'py-[2px]')]")
        for tag in tags:
            print(tag.text)

    def test_access_django_job(self):

        self.driver.get("https://www.free-work.com/fr/tech-it/jobs?query=Django&contracts=contractor&sort=date")


        time.sleep(5)
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Voir cette offre')]"))
        )
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(5)


        text_partage = self.driver.find_element(By.XPATH, "//p[contains(text(), 'Partager cette offre')]")
        self.assertEqual("Partager cette offre", text_partage.text)


    def test_retrieve_data_job(self):
        self.driver.get("https://www.free-work.com/fr/tech-it/jobs?query=Django&contracts=contractor&sort=date")
        time.sleep(5)
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Voir cette offre')]"))
        )
        self.driver.execute_script("arguments[0].click();", button)
        time.sleep(5)

        skills = self.driver.find_elements(By.XPATH, "//span[@class='w-full text-sm line-clamp-2']")

        for skill in skills:
            print(skill.text)

        esn = self.driver.find_element(By.XPATH, "//header//p[@class='font-semibold text-sm']")
        print(esn.text)








