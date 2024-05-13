from selenium import webdriver

# Set up webdriver
geckodriver_path = '/snap/bin/geckodriver'
driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)


browser = webdriver.Firefox(service=driver_service)
browser.get('http://localhost:8000')

assert 'successfully' in browser.title
