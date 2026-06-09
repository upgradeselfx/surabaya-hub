import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def run_scraper():
    # URL target dari loker.id untuk area Surabaya
    target_url = "https://www.loker.id/lokasi-pekerjaan/surabaya"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    response = requests.get(target_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Berdasarkan struktur loker.id, data biasanya ada di dalam tag artikel
    # Kamu mungkin perlu menyesuaikan class-nya melalui Inspect Element
    jobs = soup.find_all('article', class_='post-item') 
    
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
