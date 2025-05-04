from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import os

# --- Configuration ---
input_csv = 'zaytung_haberler_retry.csv'
output_csv = 'zaytung_full_content_retry.csv'

# --- Read Input and Check Existing Output ---
print(f"Reading input file: {input_csv}")
df_input = pd.read_csv(input_csv)

start_index = 0
existing_data = pd.DataFrame(columns=['ID', 'Title', 'Content', 'Link'])

if os.path.exists(output_csv):
    print(f"Found existing output file: {output_csv}. Reading...")
    existing_data = pd.read_csv(output_csv)
    if not existing_data.empty and 'Link' in existing_data.columns:
        last_processed_link = existing_data['Link'].iloc[-1]
        print(f"Last successfully processed link: {last_processed_link}")
        # Find the index in the input df corresponding to the last processed link
        last_processed_index = df_input[df_input['Link'] == last_processed_link].index
        if not last_processed_index.empty:
            start_index = last_processed_index[0] + 1
            print(f"Resuming from index {start_index}...")
        else:
            print("Could not find last processed link in the input file. Starting from the beginning.")
    else:
        print("Existing output file is empty or missing 'Link' column. Starting from the beginning.")
else:
    print(f"Output file {output_csv} not found. Starting from the beginning.")

# --- Browser Setup ---
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument("--headless") # Optional: run in background

print("Initializing browser...")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15) # Increased wait time slightly

# --- Data Storage for New Items ---
new_data_list = []

# --- Process Links ---
print(f"Starting processing from index {start_index}...")
for index, row in df_input.iloc[start_index:].iterrows():
    actual_index = index # Keep track of original index for ID generation
    try:
        url = row['Link']
        # Generate ID based on the overall position in the input file
        article_id = f"ZT{actual_index + 1:04d}" 
        print(f"Processing article {article_id} (Index: {actual_index}): {url}")
        
        driver.get(url)
        time.sleep(1) # Reduced sleep, rely more on WebDriverWait
        
        title_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='manset']//h1")))
        title = title_element.text.strip()
        
        content_div = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@id='manset']//div[@align='left'][contains(@style,'width:635px')]")))
        paragraphs = content_div.find_elements(By.TAG_NAME, "p")
        content = "\n\n".join([p.text.strip() for p in paragraphs if p.text.strip()])
        
        new_data_list.append({
            'ID': article_id,
            'Title': title,
            'Content': content,
            'Link': url
        })
        
        print(f"✅ Successfully extracted content from article {article_id}")
        
        # --- Save Progress Periodically (Optional but Recommended) ---
        if len(new_data_list) % 10 == 0: # Save every 10 articles
            print("Saving intermediate progress...")
            temp_df = pd.DataFrame(new_data_list)
            combined_df = pd.concat([existing_data, temp_df], ignore_index=True)
            combined_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
            print("Intermediate progress saved.")

    except Exception as e:
        print(f"❌ Error processing article {article_id} (Index: {actual_index}): {str(e)}")
        # Optional: Add error details to a separate log or df
        continue # Continue to the next article

# --- Final Save ---
print("\nProcessing finished. Combining and saving final data...")
if new_data_list:
    new_df = pd.DataFrame(new_data_list)
    final_df = pd.concat([existing_data, new_df], ignore_index=True)
    # Ensure no duplicates based on Link if resuming caused overlap
    final_df.drop_duplicates(subset=['Link'], keep='last', inplace=True)
    final_df.sort_values(by='ID', inplace=True) # Keep original order if desired
else:
    print("No new articles were processed.")
    final_df = existing_data

final_df.to_csv(output_csv, index=False, encoding='utf-8-sig')
print(f"✅ Successfully saved {len(final_df)} articles to {output_csv}")

# --- Close Browser ---
print("Closing browser...")
driver.quit()
print("Script finished.") 