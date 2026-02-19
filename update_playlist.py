import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options

def get_toffee_cookie():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    try:
        driver = uc.Chrome(options=options)
        driver.get("https://toffeelive.com/en/live")
        time.sleep(15) # কুকি লোড হওয়ার পর্যাপ্ত সময়
        
        all_cookies = driver.get_cookies()
        edge_cookie = ""
        for cookie in all_cookies:
            if cookie['name'] == 'Edge-Cache-Cookie':
                edge_cookie = f"{cookie['name']}={cookie['value']}"
                break
        driver.quit()
        return edge_cookie
    except Exception as e:
        print(f"Error getting cookie: {e}")
        return None

def generate_m3u(cookie):
    if not cookie:
        print("No cookie found. Skip update.")
        return

    # আপনার দেওয়া চ্যানেল লিস্ট এখানে যোগ করবেন
    base_channels = [
        {
            "category": "LIVE",
            "name": "TOFFEE Sports VIP",
            "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sports_highlights/playlist.m3u8",
            "logo": "https://images.toffeelive.com/images/program/19779/logo/240x240/mobile_logo_975410001725875598.png"
        },
        {
            "category": "News Channel",
            "name": "Somoy TV",
            "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/somoy_tv/playlist.m3u8",
            "logo": "https://assets-prod.services.toffeelive.com//Xi_Ga5oBNnOkwJLWkhKP/posters/ef2899d5-1ae0-4fee-aee5-45f9b0b3ba80.png"
        }
        # ... বাকি সব চ্যানেল এভাবেই যোগ করুন ...
    ]

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in base_channels:
            user_agent = "okhttp/4.11.0"
            f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["category"]}",{ch["name"]}\n')
            f.write(f'{ch["link"]}|User-Agent={user_agent}&Cookie={cookie}\n')
    
    print("Playlist updated with new cookie!")

if __name__ == "__main__":
    new_cookie = get_toffee_cookie()
    generate_m3u(new_cookie)
