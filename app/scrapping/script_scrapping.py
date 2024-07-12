
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException

import script_openai
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from datetime import timedelta, datetime
import time
import os
import sys
import django
import re
from dotenv import load_dotenv, dotenv_values


sys.path.append('/app/app')

# set Django param
# doc : Calling django.setup() is required for “standalone” Django usage
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()
from django.contrib.auth import get_user_model

from core.models import Alert,Job
from alert.serializers import JobSerializer


def set_up_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome_options.binary_location = '/usr/bin/chromium'

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver



"""
a user creates an alert
the script will be executed at midnight
    it collects each alert, it executes the main_scrapping function for each alert

"""
def script():

    global driver

    """SET UP selenium"""
    driver = set_up_selenium()
    driver.get("https://www.free-work.com/fr/tech-it")
    time.sleep(5)

    """LOGIN TO FREEWORK"""
    login()
    time.sleep(5)

    alerts = Alert.objects.all()
    for alert in alerts:
        title = alert.title
        user_id = alert.id_user
        print("title = "+str(title))
        main_scrapping(alert_title=title, id_alert=alert.id)

    driver.quit()
    return



load_dotenv()
def main_scrapping(alert_title, id_alert, page='1', openai=False):

    """ACCESS ALERT"""
    driver.get(f"https://www.free-work.com/fr/tech-it/jobs?query={alert_title}&contracts=contractor&freshness=less_than_24_hours&page={page}")
    time.sleep(5)


    """Process jobs"""
    number_of_elements = total_jobs_to_analyse()
    print(f"Nombre d'éléments div présents : {number_of_elements}")

    for job_number in range(1,number_of_elements+1):
        print("Process for job number : "+str(job_number))
        """extract main skills"""
        main_skills = extract_main_skills(job_number)

        """access job"""
        access_job_details_page(job_number)
        time.sleep(5)

        """RECOVER DATA"""
        details_jobs = fetch_data_job()
        """add technos"""
        if openai:
            res = get_technos_with_openai()
            details_jobs['technos'] = res
        else:
            details_jobs['technos'] = main_skills

        """add id_alert """
        details_jobs['id_alert'] = id_alert

        """Save the data"""
        res = save_data(details_jobs)
        return

        # exit detail_job_page
        driver.get(f"https://www.free-work.com/fr/tech-it/jobs?query={alert_title}&contracts=contractor&freshness=less_than_24_hours&page={page}")
        time.sleep(5)








def login():
    input_element = driver.find_element(By.LINK_TEXT, "Connexion")
    input_element.click()

    email = driver.find_element(By.ID, "email")
    password = driver.find_element(By.ID, "password")
    email.send_keys(os.getenv("EMAIL_FREEWORK"))
    password.send_keys(os.getenv("PASSWORD_FREEWORK") + Keys.ENTER)



def get_date_to_scrapp(alert_title):
    """retrieve the last date processed in database or today's date"""
    try:
        alert = Alert.objects.get(title=alert_title)
        last_job_processed = Job.objects.filter(id_alert=alert.id_alert).order_by('-date').first()
        return last_job_processed.date

    except ObjectDoesNotExist:
        # return yesterday date
        return timezone.now().date() - timedelta(days=1)


def total_jobs_to_analyse():
    try:
        div_job_elements = driver.find_elements(By.XPATH, f"(//div[@class='mb-4 relative rounded-lg max-full bg-white flex flex-col cursor-pointer shadow hover:shadow-md'])")
        number_of_elements = len(div_job_elements)
        return number_of_elements
    except NoSuchElementException:
        return 0





def extract_main_skills(job_number):
    """Main Skills (tag skills in alert title)"""
    tags_skills = driver.find_elements(By.XPATH, f"(//div[@class='mb-4 relative rounded-lg max-full bg-white flex flex-col cursor-pointer shadow hover:shadow-md'])[{job_number}]//div[contains(@class, 'truncate') and contains(@class, 'py-[2px]')]")
    main_skills = []
    for skill in tags_skills:
        main_skills.append({'name':skill.text})
    print(str(main_skills))
    return main_skills


def access_job_details_page(job_number):
    try:
        button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"(//div[@class='mb-4 relative rounded-lg max-full bg-white flex flex-col cursor-pointer shadow hover:shadow-md'])[{job_number}]//button[contains(text(), 'Voir cette offre')]"))
            )
        driver.execute_script("arguments[0].click();", button)
    except TimeoutException:
        return None


def fetch_data_job():
    esn = driver.find_element(By.XPATH, "//header//p[@class='font-semibold text-sm']")
    title = driver.find_element(By.TAG_NAME, "h1")
    date = driver.find_element(By.XPATH, "//span[contains(text(), 'Publiée le')]")

    match = re.search(r'\d{2}/\d{2}/\d{4}', date.text)
    date_str = match.group() if match else ""


    details_job = {
        "tjm": "",
        "localization": "",
        "experience": "",
        "mission_duration": "",
        "contract_type": "",
        "esn": esn.text,
        "title": title.text,
        "date": date_str,

    }
    # contains text elements like "Paris, France"
    res_details_job = driver.find_elements(By.XPATH, "//span[@class='w-full text-sm line-clamp-2']")
    # contains svg elements
    div_element_svg = driver.find_elements(By.XPATH, "//div[@class='flex items-center py-1']")

    for index, div_svg_element in enumerate(div_element_svg):
        svg_element = div_svg_element.find_element(By.TAG_NAME, "path")
        svg_path_attribute = svg_element.get_attribute("d")
        name = match_svg_to_name(str(svg_path_attribute))

        if name is not None:
            value = res_details_job[index].text
            details_job[name] = value

    return details_job


def match_svg_to_name(svg):
    switcher = {
        'tjm': 'M88 32C39.4 32 0 71.4 0 120V392c0 48.6 39.4 88 88 88H424c48.6 0 88-39.4 88-88V216c0-48.6-39.4-88-88-88H120c-13.3 0-24 10.7-24 24s10.7 24 24 24H424c22.1 0 40 17.9 40 40V392c0 22.1-17.9 40-40 40H88c-22.1 0-40-17.9-40-40V120c0-22.1 17.9-40 40-40H456c13.3 0 24-10.7 24-24s-10.7-24-24-24H88zM384 336a32 32 0 1 0 0-64 32 32 0 1 0 0 64z',
        'localization': 'M320.7 249.2c-10.5 24.8-25.4 52.2-42.5 79.9C249.8 375.3 216.8 420 192 451.7c-24.8-31.8-57.8-76.4-86.2-122.6c-17.1-27.7-32-55.1-42.5-79.9C52.5 223.6 48 204.4 48 192c0-79.5 64.5-144 144-144s144 64.5 144 144c0 12.4-4.5 31.6-15.3 57.2zm-105 250C267 435 384 279.4 384 192C384 86 298 0 192 0S0 86 0 192c0 87.4 117 243 168.3 307.2c12.3 15.3 35.1 15.3 47.4 0z',
        'experience': 'M176 56V96H336V56c0-4.4-3.6-8-8-8H184c-4.4 0-8 3.6-8 8zM128 96V56c0-30.9 25.1-56 56-56H328c30.9 0 56 25.1 56 56V96h64c35.3 0 64 28.7 64 64V416c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V160c0-35.3 28.7-64 64-64h64zm232 48H152 64c-8.8 0-16 7.2-16 16V416c0 8.8 7.2 16 16 16H448c8.8 0 16-7.2 16-16V160c0-8.8-7.2-16-16-16H360z',
        'mission_duration': 'M464 256A208 208 0 1 1 48 256a208 208 0 1 1 416 0zM0 256a256 256 0 1 0 512 0A256 256 0 1 0 0 256zM232 120V256c0 8 4 15.5 10.7 20l96 64c11 7.4 25.9 4.4 33.3-6.7s4.4-25.9-6.7-33.3L280 243.2V120c0-13.3-10.7-24-24-24s-24 10.7-24 24z',
        'contract_type': 'M224.8 5.4c8.8-7.2 21.5-7.2 30.3 0l216 176c10.3 8.4 11.8 23.5 3.4 33.8s-23.5 11.8-33.8 3.4L416 198.4V240H368V159.3L240 55 112 159.3V360c0 4.4 3.6 8 8 8H272v48H120c-30.9 0-56-25.1-56-56V198.4L39.2 218.6c-10.3 8.4-25.4 6.8-33.8-3.4s-6.8-25.4 3.4-33.8l216-176zM288 216v45.7c-6 6.8-10.6 14.9-13.3 23.8c-3.2 1.6-6.9 2.5-10.7 2.5H216c-13.3 0-24-10.7-24-24V216c0-13.3 10.7-24 24-24h48c13.3 0 24 10.7 24 24zm64 104V464H544V320H352zm-48-16c0-17.7 14.3-32 32-32H560c17.7 0 32 14.3 32 32V464h36c6.6 0 12 5.4 12 12c0 19.9-16.1 36-36 36H592 544 352 304 292c-19.9 0-36-16.1-36-36c0-6.6 5.4-12 12-12h36V304z',
    }
    for key, val in switcher.items():
        if val == svg:
            return key
    return None

def get_technos_with_openai():
    parent_div = driver.find_element(By.XPATH, "//div[@class='shadow bg-white rounded-lg'][.//h2[contains(text(), 'Profil recherché')]]")
    description_div = parent_div.find_element(By.XPATH, ".//div[@class='html-renderer prose-content']")

    skills_array = script_openai.get_all_skills_with_openai(description_div.text)
    # format array to fit with serializer
    skills_list = [{'name': skill.lower()} for skill in skills_array]

    return skills_list

def  save_data(details_jobs):
    serializer = JobSerializer(data=details_jobs)

    if serializer.is_valid():
        job_instance = serializer.save()
        return job_instance
    else:
        print(serializer.errors)


if __name__ == "__main__":
    script()





