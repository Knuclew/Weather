import requests
import sys

class HavaDurumuUygulamasi:
    def __init__(self):
        self.api_key = "API_KEY"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        
        # Renkler (ANSI kodları)
        self.CYAN = '\033[96m'
        self.GREEN = '\033[92m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[91m'
        self.BLUE = '\033[94m'
        self.MAGENTA = '\033[95m'
        self.RESET = '\033[0m'
        self.BOLD = '\033[1m'
    
    def sehir_bul(self, sehir_adi):
        """Şehir adını coğrafi koordinatlara çevirir"""
        try:
            params = {
                'q': sehir_adi,
                'limit': 1,
                'appid': self.api_key
            }
            
            response = requests.get(self.geo_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data:
                return data[0]
            return None
            
        except Exception:
            return None
    
    def hava_durumu_al(self, lat, lon):
        """Koordinatlara göre hava durumu bilgilerini alır"""
        try:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'tr'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except Exception:
            return None
    
    def hava_durumu_goster(self, veri, sehir_bilgi):
        """Hava durumu bilgilerini minimalist şekilde gösterir"""
        sehir = sehir_bilgi['name']
        ulke = sehir_bilgi.get('country', '')
        
        sicaklik = veri['main']['temp']
        hissedilen = veri['main']['feels_like']
        nem = veri['main']['humidity']
        durum = veri['weather'][0]['description'].title()
        ruzgar = veri['wind']['speed']
        
        print(f"\n{self.BOLD}{self.CYAN}{sehir}, {ulke}{self.RESET}")
        print(f"{self.YELLOW}{durum}{self.RESET}")
        print(f"{self.GREEN}Sıcaklık: {sicaklik}°C{self.RESET}")
        print(f"{self.BLUE}Hissedilen: {hissedilen}°C{self.RESET}")
        print(f"{self.MAGENTA}Nem: %{nem}{self.RESET}")
        print(f"{self.CYAN}Rüzgar: {ruzgar} m/s{self.RESET}\n")
    
    def calistir(self):
        """Ana uygulama döngüsü"""
        print(f"\n{self.BOLD}{self.CYAN}Hava Durumu{self.RESET}\n")
        
        while True:
            sehir = input(f"{self.BOLD}Şehir: {self.RESET}").strip()
            
            if not sehir:
                print(f"{self.RED}Lütfen bir şehir adı girin.{self.RESET}\n")
                continue
            
            # Şehri bul
            sehir_bilgi = self.sehir_bul(sehir)
            
            if not sehir_bilgi:
                print(f"{self.RED}Şehir bulunamadı.{self.RESET}\n")
                continue
            
            # Hava durumunu al
            hava_veri = self.hava_durumu_al(
                sehir_bilgi['lat'], 
                sehir_bilgi['lon']
            )
            
            if not hava_veri:
                print(f"{self.RED}Hava durumu bilgileri alınamadı.{self.RESET}\n")
                continue
            
            # Sonuçları göster
            self.hava_durumu_goster(hava_veri, sehir_bilgi)

# Uygulamayı başlat
if __name__ == "__main__":
    try:
        app = HavaDurumuUygulamasi()
        app.calistir()
    except KeyboardInterrupt:
        print(f"\n\nKnuclew\n")
        sys.exit(0)