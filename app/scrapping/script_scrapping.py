
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from dotenv import load_dotenv, dotenv_values
import os
import time
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta, datetime




import os
import sys
import django

sys.path.append('/app/app')

# set Django param
# doc : Calling django.setup() is required for “standalone” Django usage
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()


from core.models import Alert, Job


def set_up_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-dev-shm-usage')

    chrome_options.binary_location = '/usr/bin/chromium'

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


load_dotenv()
def main_scrapping(alert_title='Django', page='1'):

    global driver

    """SET UP selenium"""
    driver = set_up_selenium()
    driver.get("https://www.free-work.com/fr/tech-it")
    time.sleep(5)


    """LOGIN TO FREEWORK"""
    login()
    time.sleep(5)


    """ALERT DATE TO SCRAP"""
    #date_to_scrapp = get_date_to_scrapp(alert_title)
    date_to_scrapp = "04/07/2024"
    #date_to_scrapp= date_to_scrapp.strftime('%d/%m/%Y')
    print("date = "+date_to_scrapp)


    """ACCESS ALERT"""
    driver.get(f"https://www.free-work.com/fr/tech-it/jobs?query={alert_title}&contracts=contractor&sort=date&page={page}")
    time.sleep(5)


    """Process jobs"""
    continue_search = True
    job_number = 1
    while continue_search:
        continue_search = check_job_date_is_valid(job_number, date_to_scrapp)
        if not continue_search:
            break

        print(continue_search)
        """extract main skills"""
        main_skills = extract_main_skills(job_number)
        print("mains skills = "+ str(main_skills))

        """access job"""
        access_job_details_page(job_number)
        time.sleep(5)

        text_partage = driver.find_element(By.XPATH, "//p[contains(text(), 'Partager cette offre')]")
        print(text_partage.text)
        job_number += 1

    print('fin du while')
    driver.quit()
    return

    """RECOVER DATA"""
    # details_jobs = fetch_data_job()
    # print("detais jobs = "+ str(details_jobs))



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


def check_job_date_is_valid(job_number, date_to_scrapp):
    date_job = driver.find_element(By.XPATH, f"(//div[@class='col-span-3 lg:col-span-2']//time)[{job_number}]")

    # convert str to datetime object
    date_job = datetime.strptime(date_job.text, "%d/%m/%Y").date()
    date_to_scrapp = datetime.strptime(date_to_scrapp, "%d/%m/%Y").date()

    if date_job > date_to_scrapp:
        return True
    else:
        return False


def extract_main_skills(job_number):
    """Main Skills (tag skills in alert title)"""
    tags_skills = driver.find_elements(By.XPATH, f"(//div[@class='mb-4 relative rounded-lg max-full bg-white flex flex-col cursor-pointer shadow hover:shadow-md'])[{job_number}]//div[contains(@class, 'truncate') and contains(@class, 'py-[2px]')]")
    main_skills = []
    for skill in tags_skills:
        main_skills.append(skill.text)

    return main_skills

def access_job_details_page(job_number):
    button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"(//div[@class='mb-4 relative rounded-lg max-full bg-white flex flex-col cursor-pointer shadow hover:shadow-md'])[{job_number}]//button[contains(text(), 'Voir cette offre')]"))
        )
    driver.execute_script("arguments[0].click();", button)


def fetch_data_job():
    res_details_job = driver.find_elements(By.XPATH, "//span[@class='w-full text-sm line-clamp-2']")
    details_job = []
    for detail_job in res_details_job:
        details_job.append(detail_job.text)

    return details_job


if __name__ == "__main__":
    main_scrapping()

