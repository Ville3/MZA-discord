#from selenium import webdriver
#BROWSER_DRIVER = "bot/webdriver/geckodriver.exe"

#firefoxOptions = webdriver.FirefoxOptions()
#firefoxOptions.add_argument("--width=800"), firefoxOptions.add_argument("--height=800")
# firefoxOptions.headless = True
#firefoxOptions.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0")
#firefoxOptions.set_preference("intl.accept_languages", 'en-us')
#firefoxOptions.set_preference("layers.acceleration.disabled", True)
#firefoxOptions.set_preference("browser.privatebrowsing.autostart", True)
#firefoxOptions.set_preference("permissions.default.microphone", 2)
#firefoxOptions.set_preference("permissions.default.camera", 2)
#browser = webdriver.Firefox(executable_path=BROWSER_DRIVER, options=firefoxOptions)


#options = webdriver.ChromeOptions()
# options.add_argument("--headless")
#options.add_argument("--disable-infobars")
#options.add_argument("--window-size=1200,800")
#options.add_argument("user-agent='User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'")
#options.add_experimental_option("prefs", { \
#    "profile.default_content_setting_values.media_stream_mic": 2,     # 1:allow, 2:block
#    "profile.default_content_setting_values.media_stream_camera": 2,
#     "profile.default_content_setting_values.notifications": 2
#  })
#browser = webdriver.Chrome(options=options)