import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_toffee_cookie():
    options = uc.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    try:
        driver = uc.Chrome(options=options)
        
        # IP চেক করার জন্য (লগ-এ দেখার জন্য)
        driver.get("https://api.ipify.org")
        current_ip = driver.find_element(By.TAG_NAME, 'body').text
        print(f"Current Runner IP: {current_ip}")
        
        # Toffee সাইটে ভিজিট
        print("Toffee ভিজিট করা হচ্ছে...")
        driver.get("https://toffeelive.com/en/live")
        time.sleep(20) # কুকি জেনারেট হওয়ার পর্যাপ্ত সময়
        
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
        print("Failed: No Edge-Cache-Cookie found! IP restricted হতে পারে।")
        return

    # আপনার দেওয়া চ্যানেলের সম্পূর্ণ লিস্ট
    base_channels = [
        {"category": "LIVE", "name": "TOFFEE Sports VIP", "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sports_highlights/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/19779/logo/240x240/mobile_logo_975410001725875598.png"},
        {"category": "LIVE", "name": "TOFFEE Movies VIP", "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/toffee_movie/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/2708/logo/240x240/mobile_logo_724353001725875591.png"},
        {"category": "LIVE", "name": "TOFFEE Dramas VIP", "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/toffee_drama/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/44878/logo/240x240/mobile_logo_764950001725875605.png"},
        {"category": "News Channel", "name": "CNN VIP", "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/cnn/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/333/logo/240x240/mobile_logo_146607001735536058.png"},
        {"category": "News Channel", "name": "Somoy TV", "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/somoy_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com//Xi_Ga5oBNnOkwJLWkhKP/posters/ef2899d5-1ae0-4fee-aee5-45f9b0b3ba80.png"},
        {"category": "News Channel", "name": "Independent TV", "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/independent_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_480,q_75,f_webp/ES_cZZsBNnOkwJLW1Oz1/posters/b872b8f5-cb6b-45a1-a1cd-7609df51d614.png"},
        {"category": "News Channel", "name": "Jamuna TV", "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/jamuna_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/w_640,q_75,f_webp/PiL635oBEef-9-uV2uCe/posters/36f380e0-6c71-4b27-a73b-2afb3ce7e982.png"},
        {"category": "Sports Channels", "name": "SONY SPORTS TEN 1 HD", "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_sports_1_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/603/logo/240x240/mobile_logo_237244001666780563.png"},
        {"category": "Sports Channels", "name": "SONY SPORTS TEN 5 HD", "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sony_sports_5_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/606/logo/240x240/mobile_logo_689539001672145843.png"},
        {"category": "Entertainment Channels", "name": "Zee Bangla VIP", "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/zee_bangla/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/340/logo/240x240/mobile_logo_094417001655891123.png"},
        {"category": "Entertainment Channels", "name": "Sony Aat VIP", "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/sonyaath/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/343/logo/240x240/mobile_logo_496322001666780228.png"},
        {"category": "Kids", "name": "Cartoon Network HD", "link": "https://bldcmprod-cdn.toffeelive.com/cdn/live/cartoon_network_hd/playlist.m3u8", "logo": "https://images.toffeelive.com/images/program/26942/logo/240x240/mobile_logo_443429001678950505.png"}
    ]

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        user_agent = "okhttp/4.11.0"
        for ch in base_channels:
            f.write(f'#EXTINF:-1 tvg-logo="{ch["logo"]}" group-title="{ch["category"]}",{ch["name"]}\n')
            f.write(f'{ch["link"]}|User-Agent={user_agent}&Cookie={cookie}\n')
    
    print(f"Success: Playlist updated with {len(base_channels)} channels!")

if __name__ == "__main__":
    new_cookie = get_toffee_cookie()
    generate_m3u(new_cookie)
