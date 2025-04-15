from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Read the existing CSV with links
df = pd.read_csv('zaytung_haberler.csv')

# Browser settings
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

# Initialize browser
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# Lists to store the content
ids = []
titles = []
contents = []
links = []

# Process each link
for index, row in df.iterrows():
    try:
        url = row['Link']
        article_id = f"ZT{index+1:04d}"  # Creates IDs like ZT0001, ZT0002, etc.
        print(f"Processing article {article_id}: {url}")
        
        # Visit the page
        driver.get(url)
        time.sleep(2)  # Small delay to ensure page loads
        
        # Get the title
        title = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='manset']//h1"))).text.strip()
        
        # Get the content
        content_div = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='manset']//div[@align='left'][@style='width:635px; float:left;text-align:left; padding-right:0px; margin-top:14px; font-size:13px; word-spacing:1px; line-height:1.5;']")))
        paragraphs = content_div.find_elements(By.TAG_NAME, "p")
        content = "\n\n".join([p.text.strip() for p in paragraphs if p.text.strip()])
        
        # Store the data
        ids.append(article_id)
        titles.append(title)
        contents.append(content)
        links.append(url)
        
        print(f"✅ Successfully extracted content from article {article_id}")
        
    except Exception as e:
        print(f"❌ Error processing article {index + 1}: {str(e)}")
        continue

# Create new DataFrame with full content
content_df = pd.DataFrame({
    'ID': ids,
    'Title': titles,
    'Content': contents,
    'Link': links
})

# Save to CSV
content_df.to_csv('zaytung_full_content.csv', index=False, encoding='utf-8-sig')
print(f"\n✅ Successfully saved {len(content_df)} articles to zaytung_full_content.csv")

# Close the browser
driver.quit() 