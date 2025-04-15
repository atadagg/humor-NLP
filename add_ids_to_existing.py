import pandas as pd

# Read the existing CSV
df = pd.read_csv('zaytung_haberler.csv')

# Create IDs for each row
df['ID'] = [f"ZT{i+1:04d}" for i in range(len(df))]

# Reorder columns to put ID first
df = df[['ID', 'Title', 'Link', 'Page']]

# Save back to CSV
df.to_csv('zaytung_haberler_with_ids.csv', index=False, encoding='utf-8-sig')

print(f"✅ Successfully added IDs to {len(df)} articles")
print(f"✅ Saved to zaytung_haberler_with_ids.csv")
print("\nFirst few rows:")
print(df.head()) 