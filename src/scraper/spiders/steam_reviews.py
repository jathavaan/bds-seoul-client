from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
from datetime import datetime

# Setup Edge
options = EdgeOptions()
options.add_argument("start-maximized") #If you want to see whats happening
#options.add_argument("--headless") #It just happends in the background
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.fonts": 2,
    "profile.managed_default_content_settings.stylesheets": 2,
}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)


# Choose Steam game review page
game_id = 730      #CS
#game_id = 413150    #Stardew Valley
#game_id = 2007520  #Rainbow High Runway Rush
url = f'https://steamcommunity.com/app/{game_id}/reviews/?p=1&browsefilter=mostrecent'
driver.get(url)

CUTOFF_DATE = datetime.strptime(f'2022.04.19', "%Y.%m.%d")  # Change to desired date
TARGET_REVIEW_COUNT = 100                                  # Change to desired amount of reviews

start_time = time.time()

#Handle data
def parse_review(user_id: int, container: webdriver ):
        try:
            #content = container.find_element(By.CLASS_NAME, "apphub_CardTextContent").text.strip()
            date = container.find_element(By.CLASS_NAME, "date_posted").text
            hours = container.find_element(By.CLASS_NAME, "hours").text.strip()
            #helpful = container.find_element(By.CLASS_NAME, "found_helpful").text.strip()
            recommended = container.find_element(By.CLASS_NAME, "title").text
            is_last_review = False

            #Content handling
            #content = content.replace(date, "").strip() #Remove the Date from the review

            #Date handling
            date = date.replace("Posted: ", "").strip()
            if "," not in date:
                date = f"{date}, {datetime.now().year}"

            if date[0].isdigit():                   # Format: "31 October, 2024"
                date_obj = datetime.strptime(date, "%d %B, %Y")
            else:                                   # Format: "May 5, 2023"
                date_obj = datetime.strptime(date, "%B %d, %Y")
   
            # Final output in YYYY.MM.DD
            date = date_obj.strftime("%Y.%m.%d")

            #Recommended handling
            recommended = recommended == "Recommended" #Turns into boolean

            #Hours
            hours = float(hours.split()[0].replace(",", "")) if hours else 0.0 #Turn into a number

            #Helpful handling
            # try:
            #     helpful = int(helpful.split()[0])
            # except:
            #     helpful = 0

            #is last review check
            if datetime.strptime(date, "%Y.%m.%d") < CUTOFF_DATE:
                is_last_review = True
                print(f'{CUTOFF_DATE} reached. Ending scroll.')

            if user_id >= TARGET_REVIEW_COUNT:
                is_last_review = True
                print(f'{TARGET_REVIEW_COUNT} reviews loaded. Ending scroll.')

            return {
                "game_id": game_id,
                "date_posted": date,
                "is_recommended": recommended,
                "hours_played": hours,
                #"helpful": helpful,   
                #"content": content,
                "user_id": user_id,
                "is_last_review": is_last_review 
            }

        except Exception as e:
            print(f'❌ Skipped review from {user_id} due to missing info.')
            print(e)
            return None

try:
    old_review_count = 0
    nbreak = False
    while True: 
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, 2).until(
                lambda d: len(d.find_elements(By.CLASS_NAME, "apphub_CardContentMain")) > old_review_count
            )
        except:
            print("No new reviews loaded. Ending scroll.")
            break

        reviews = driver.find_elements(By.CLASS_NAME, "apphub_CardContentMain") 
        current_review_count = len(reviews)


        #Parse and send current loaded reviews
        print(f'Sending reviews {old_review_count} to {current_review_count} to kafka')
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(parse_review, old_review_count + i, container) for i, container in enumerate(reviews[old_review_count:current_review_count], start=1)]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    if result["is_last_review"]:
                        print(result) #Send to Kafka
                        nbreak = True
                        break
        if nbreak:
            break

        old_review_count = current_review_count
 
except Exception as e:
    print("❌ Failed to collect review containers.")
    print(e)

end_time = time.time()
print(f"⏱️ Script finished in {end_time - start_time:.2f} seconds")

# Optional: pause to look at the page
driver.quit()