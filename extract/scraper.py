import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os

def scrape_avito(pages=1):
    chrome_options = Options()
    chrome_options.add_argument("--headless") 

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    listings = driver.find_elements(By.CSS_SELECTOR, "[data-testid='ad-card']")
    all_ads = []

    
    for page in range(1, pages + 1):
        url = f"https://www.avito.ma/fr/maroc/appartements-%C3%A0_vendre?o={page}"
        print(f"جاري فحص الصفحة: {page}...")
        driver.get(url)
        time.sleep(7) 

        
        links = driver.find_elements(By.TAG_NAME, "a")
        
        for link_element in links:
            try:
                href = link_element.get_attribute("href")
                
                if href and "/vi/" in href:
                    title = link_element.text
                    if not title: continue 
                    
                    all_ads.append({
                        "title": title,
                        "price": "Check Site", 
                        "city_district": "Maroc",
                        "link": href
                    })
            except:
                continue

    driver.quit()

    os.makedirs("../staging", exist_ok=True)
    df = pd.DataFrame(all_ads)
    output_path = "../staging/raw_avito_data.csv"
    df.to_csv(output_path, index=False)
    print(f"تم بنجاح جلب {len(df)} إعلان وحفظهم في {output_path}")


if __name__ == "__main__":
    scrape_avito(pages=2)