import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def run():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    url = "https://www.loker.id/lokasi-pekerjaan/surabaya"
    
    print(f"--- Memulai Scraping: {url} ---")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print("Gagal akses situs!")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        
        jobs = soup.select('article.post-item') 
        print(f"Ditemukan {len(jobs)} lowongan.")
        
        for job in jobs:
            title = job.select_one('h2.entry-title a').text.strip()
            link = job.select_one('h2.entry-title a')['href']
            
            exist = supabase.table("listings").select("id").eq("url", link).execute()
            if not exist.data:
                supabase.table("listings").insert({"title": title, "url": link}).execute()
                print(f"Berhasil simpan: {title}")
                
    except Exception as e:
        print(f"Error fatal: {e}")

if __name__ == "__main__":
    run()
