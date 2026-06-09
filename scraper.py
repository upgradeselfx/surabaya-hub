import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client

# Ambil kunci dari GitHub Secrets (nanti kita buat)
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# Target web contoh (Ganti dengan target asli nanti)
def run_scraper():
    response = requests.get("URL_TARGET_DI_SINI")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Cari elemen iklan (Contoh struktur)
    items = soup.find_all('div', class_='item') 
    
    for item in items:
        data = {
            "title": item.find('h2').text,
            "url": item.find('a')['href']
        }
        # Masukkan ke Supabase
        supabase.table("listings").insert(data).execute()

if __name__ == "__main__":
    run_scraper()
