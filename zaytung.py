from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Tarayıcı ayarlarını yap
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

# Tarayıcıyı başlat
driver = webdriver.Chrome(options=options)

# **Kaç sayfa olduğunu bulalım**
driver.get("https://www.zaytung.com/digerleri.asp")
wait = WebDriverWait(driver, 10)

try:
    # Sayfa numaralarını bulalım (En son sayfa numarasını alacağız)
    page_numbers = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'digerleri.asp?pg=')]")))
    
    # Tüm sayfa numaralarını al
    pages = [int(p.text) for p in page_numbers if p.text.isdigit()]
    max_page = max(pages) if pages else 1  # En büyük sayfa numarasını bul
    print(f"📌 Toplam {max_page} sayfa bulundu.")
    
except:
    max_page = 1  # Eğer sayfa sayısını bulamazsak en az 1 olsun


# **Kaç sayfa çekileceğini ayarla (İlk 20 sayfa)**
num_pages = max_page  # En fazla 20 sayfa çek, ancak toplam sayfadan azsa onu kullan

news_data = []

# **Şimdi belirlenen sayıda sayfadan haberleri çekelim**
for page in range(1, num_pages + 1):  
    url = f"https://www.zaytung.com/digerleri.asp?pg={page}"
    driver.get(url)
    print(f"📌 {page}. sayfadaki haberleri çekiyoruz...")

    try:
        # Sayfanın tamamen yüklenmesini bekleyelim
        wait = WebDriverWait(driver, 15)

        # **Tüm haber başlıklarını al**
        news_items = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td/h3/a")))

        for item in news_items:
            try:
                title = item.text.strip()
                link = item.get_attribute("href")  # Link tamamlama

                # Haber verisini sayfa numarasıyla birlikte kaydet (summary kaldırıldı)
                news_data.append([title, link, page])

            except Exception as e:
                print("Hata:", e)

    except Exception as e:
        print(f"{page}. sayfa yüklenirken hata oluştu: {e}")

# **Tekrar eden haberleri temizleyelim**
df = pd.DataFrame(news_data, columns=["Title", "Link", "Page"])

print("Tekrarlar temizlenmeden önceki satır sayısı:", len(df))

df = df.drop_duplicates(subset=["Title"], keep="first")

df.reset_index(drop=True, inplace=True)

print("Tekrarlar temizlendikten sonraki satır sayısı:", len(df))

# DataFrame'i CSV dosyasına aktar
csv_filename = 'zaytung_haberler_retry.csv'
df.to_csv(csv_filename, index=False, encoding='utf-8-sig') # utf-8-sig encoding Türkçe karakterler için önemli
print(f"✅ Haberler başarıyla '{csv_filename}' dosyasına kaydedildi.")

# Tarayıcıyı kapat
driver.quit()