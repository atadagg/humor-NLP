import pandas as pd

# Read the CSV file
df = pd.read_csv('zaytung_haberler.csv')

# Fix the URLs by removing the duplicate prefix
df['Link'] = df['Link'].str.replace('https://www.zaytung.com/https://www.zaytung.com/', 'https://www.zaytung.com/')

# Save the corrected CSV file
df.to_csv('zaytung_haberler_fixed.csv', index=False)

print("URLs have been fixed and saved to 'zaytung_haberler_fixed.csv'") 