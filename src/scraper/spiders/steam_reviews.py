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

# 1. Open a Steam game review page
game_id = 730
#game_id = 2007520
url = f'https://steamcommunity.com/app/{game_id}/reviews/?p=1&browsefilter=mostrecent'
driver.get(url)

start_time = time.time()

try:
    TARGET_REVIEW_COUNT = 100
    REVIEW_COUNT = 0

    # If it has scrolled more times than reviews to count, assume that there are no more reviews
    while True: 
        reviews = driver.find_elements(By.CLASS_NAME, "apphub_CardContentMain")
        CURRENT_COUNT = len(reviews)
        
        if CURRENT_COUNT >= TARGET_REVIEW_COUNT:
            print("It breaks")
            break  
        
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, 2).until(
                lambda d: len(d.find_elements(By.CLASS_NAME, "apphub_CardContentMain")) > REVIEW_COUNT
            )
        except:
            print("❌ No new reviews loaded. Ending scroll.")
            break

        REVIEW_COUNT = CURRENT_COUNT
    scroll_time = time.time()
    print(f"⏱️ Script stopped scrolling in {scroll_time - start_time:.2f} seconds")

    #Handle data
    def parse_review(i: int, container: webdriver):
        try:

            content = container.find_element(By.CLASS_NAME, "apphub_CardTextContent").text.strip()
            date = container.find_element(By.CLASS_NAME, "date_posted").text
            hours = container.find_element(By.CLASS_NAME, "hours").text.strip()
            helpful = container.find_element(By.CLASS_NAME, "found_helpful").text.strip()
            recommended = container.find_element(By.CLASS_NAME, "title").text

            #Content handling
            # content = content.replace(date, "").strip() #Remove the Date from the review

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

            return {
                "game_id": game_id,
                "date_posted": date,
                "is_recommended": recommended,
                "hours_played": hours,
                #"helpful": helpful,   
                #"content": content,
                "user_id": i
            }

        except Exception as e:
            print("❌ Skipped ", i, " review due to missing info.")
            print(e)
            return None


    review_data = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(parse_review, i, container) for i, container in enumerate(reviews[:TARGET_REVIEW_COUNT], start=1)]
        for future in as_completed(futures):
            result = future.result()
            if result:
                review_data.append(result)

    # Save to JSON
    with open("reviews.json", "w", encoding="utf-8") as f:
        json.dump(review_data, f, ensure_ascii=False, indent=4)

    

except Exception as e:
    print("❌ Failed to collect review containers.")
    print(e)

end_time = time.time()
print(f"⏱️ Script finished in {end_time - start_time:.2f} seconds")

# Optional: pause to look at the page
driver.quit()