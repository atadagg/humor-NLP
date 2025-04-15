import pandas as pd

# Read the existing CSV
print("Reading existing CSV file...")
df = pd.read_csv('zaytung_full_content.csv')

# Create IDs
print("Adding IDs to articles...")
df['ID'] = [f"ZT{i+1:04d}" for i in range(len(df))]

# Reorder columns to put ID first
columns = ['ID'] + [col for col in df.columns if col != 'ID']
df = df[columns]

# Save back to CSV
print("Saving updated CSV...")
df.to_csv('zaytung_full_content.csv', index=False, encoding='utf-8-sig')

print(f"✅ Successfully added IDs to {len(df)} articles in zaytung_full_content.csv")
print("First few rows of the updated CSV:")
print(df.head()) 