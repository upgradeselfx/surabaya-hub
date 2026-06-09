import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def run():
    target_url = "https://www.loker.id/lokasi-pekerjaan/surabaya"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    print("Mencoba mengakses situs...") # Cek apakah ini muncul di log
    response = requests.get(target_url, headers=headers)
    print(f"Status Code: {response.status_code}") # Jika muncul 403 atau 404, ini masalahnya
    
    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = soup.find_all('article', class_='post-item')
    print(f"Jumlah lowongan ditemukan: {len(jobs)}") # Cek apakah ada data yang diambil
    
    
    for job in jobs:
        try:
            title_tag = job.find('h2', class_='entry-title')
            link_tag = title_tag.find('a')
            
            data = {
                "title": title_tag.text.strip(),
                "url": link_tag['href']
            }
            
            # Cek apakah sudah ada di DB
            existing = supabase.table("listings").select("id").eq("url", data['url']).execute()
            if not existing.data:
                supabase.table("listings").insert(data).execute()
                print(f"Berhasil ambil: {data['title']}")
        except:
            continue

if __name__ == "__main__":
    run_scraper()
