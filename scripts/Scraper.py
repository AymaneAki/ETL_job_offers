from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from selenium.webdriver.common.action_chains import ActionChains

driver_path = r"C:\Users\Aymane\Downloads\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
service = Service(driver_path)
Chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=Chrome_options)

driver.get("https://www.jobzyn.com/fr/jobs/maroc")
time.sleep(3)  
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)


def scroll_and_click_load_more():
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  
            
            load_more_buttons = driver.find_elements(By.XPATH, '//button[@class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 text-primary underline-offset-4 hover:underline h-10 px-4 py-2"]')

            if not load_more_buttons:
                print("No more 'Load More' buttons found.")
                break  
            
            for button in load_more_buttons:
                try:
                    actions.move_to_element(button).perform()  
                    wait.until(EC.element_to_be_clickable(button)).click()
                    time.sleep(2) 
                except:
                    print("Failed to click a 'Load More' button. Moving to the next.")

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("No more content is loading.")
                break  
            last_height = new_height

        except Exception as e:
            print(f"Error while scrolling and clicking 'Load More': {e}")
            break  

scroll_and_click_load_more()

try:
    anchor_divs = driver.find_elements(By.XPATH, '//a[@class="h-full w-full max-w-[350px]"]')
    all_h_links = [anchor_div.get_attribute('href') for anchor_div in anchor_divs]
finally:
    driver.quit()


def extract_data(driver_object):
    time.sleep(1)
    data = {}

    try:
        try:
            data['Poste'] = driver_object.find_element(
                By.XPATH, '//h2[@class="sm:text-[20px] xs:text-[20px] lg:text-[28px] text-greenish-black-500 font-semibold"]').text
        except:
            data['Poste'] = "-"

        try:
            data['Entreprise'] = driver_object.find_element(By.XPATH, '//span[@class="text-greenish-black-500 text-[18px] sm:text-[23px] sm:ml-[-6px] sm:mt-[10px] xs:ml-[-6px] xs:mt-[10px] "]').text
        except:
            data['Entreprise'] = "-"

        try:
            data['Ville'] = driver_object.find_element(By.XPATH, '//span[@class="text-[#04151f81] text-[12px] block "]').text
        except:
            data['Ville'] = "-"
        try:
            elmts = driver_object.find_elements(By.XPATH, '//span[@class="text-[11px]"]')
            parts1 = elmts[0].text.split()
            parts2 = elmts[2].text.split()
            data['Type de contrat'] = parts1[-1] 
            data['Expérience'] = parts2[1] + "-" + parts2[3]
        except:
            data['Type de contrat'] = "-"
            data['Expérience'] = "-"

        try:
            lien = driver_object.find_element(By.XPATH, '//a[@class="w-full "]')
            data['Lien'] = lien.get_attribute('href')
        except:
            data['Lien'] = "-"
            
    except Exception as e:
        print(f"Error extracting data: {e}")

    return data


list_data = []

with webdriver.Chrome(service=service, options=Chrome_options) as driver2:
    for hlink in all_h_links:
        try:
            driver2.get(hlink)
            info = extract_data(driver2)
            list_data.append(info)
        except Exception as e:
            print(f"Error processing link {hlink}: {e}")

csv_filename = "data.csv"

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    fieldnames = ["Poste", "Entreprise", "Ville", "Type de contrat", "Expérience", "Lien"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()  
    writer.writerows(list_data) 

print(f"Data saved successfully in {csv_filename}")