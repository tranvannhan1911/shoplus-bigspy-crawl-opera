import time

# from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.opera.options import Options
from seleniumwire import webdriver
import webdriver as myWebdriver
import json
import api
from datetime import datetime
import api_tool
import traceback

max_tries_all = 50
crawled_count = 0
while max_tries_all > 0:
    try:
        ads_ids = api_tool.get_ads_id()
        chrome_options = Options()
        chrome_options.add_extension('./TranNamPhong653.crx')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        capabilities = webdriver.DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+
        driver = myWebdriver.Opera(executable_path=r'./operadriver.exe', desired_capabilities=capabilities, options=chrome_options)
        driver.get('opera://extensions')
        time.sleep(5)

        driver.get('https://trannamphong.top/Vitaminforsale38b5m9')
        input_password = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type=password]")))

        input_password.send_keys('truong193')
        btn_login = driver.find_element_by_css_selector('button.passster-submit')
        btn_login.click()

        tool = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Tool tìm quảng cáo Facebook/Google/TikTok')]")))
        tool.click()

        btn_tool_tiktok = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Click để sử dụng Tool Spy Tiktok Ads')]")))
        btn_tool_tiktok.click()

        time.sleep(5)
        driver.switch_to.window(driver.window_handles[2])
        driver.get('https://www.shoplus.net/discovery/ads')
        time.sleep(10)

        def process_browser_logs_for_network_events(logs):
            """
            Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
            since we're interested in the network events specifically.
            """
            for entry in logs:
                log = json.loads(entry["message"])["message"]
                if (
                        "Network.response" in log["method"]
                        or "Network.request" in log["method"]
                        or "Network.webSocket" in log["method"]
                ):
                    yield log
        logs = driver.get_log("performance")

        events = process_browser_logs_for_network_events(logs)
        token = None
        cookie = None
        for event in events:
            if "headers" in event["params"].keys() and "authorization" in event["params"]["headers"].keys() and event["params"]["headers"]["authorization"].startswith("Bearer") and "cookie" in event["params"]["headers"].keys():
                token = event["params"]["headers"]["authorization"]
                cookie = event["params"]["headers"]["cookie"]

        print("token: "+ token)
        print("cookie: "+ cookie)
        driver.quit()
        max_page = 49
        for page in range(0, max_page+1):
            print("getting page: "+ str(page))
            data = api.get_shoplus_ads_list(page, token, cookie)
            # print(data)
            # print()
            for post in data["data"]["items"]:
                try:
                    if post["id"] in ads_ids:
                        continue
                    last_time_seconds = post["last_time"] // 1000
                    last_time_date = datetime.fromtimestamp(last_time_seconds).strftime('%Y-%m-%d')
                    response = api.get_shoplus_ads_detail(post["id"], post["author_id"], post["video_id"], last_time_date, token, cookie)
                    detail = json.loads(response.text)
                    print("Call api to save data")
                    if "data" not in detail.keys():
                        print(response.text)
                    api_tool.save_opera_shoplus(detail)
                    # video_post = VideoPost.from_shoplus(detail["data"])
                    # if video_post != None:
                    #     crawled_count += 1
                    #     print("[shoplus "+ str(crawled_count) +"] "+ str(video_post))
                    #     print("")
                    time.sleep(2)
                except Exception as e:
                    print(traceback.format_exc())
                    print(post)
            time.sleep(5)
    except Exception as e:
        print(traceback.format_exc())
        max_tries_all-=1

    