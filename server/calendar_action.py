from seleniumbase import SB
import time
from selenium.webdriver.common.by import By

# date is YYYY/MM/DD
def calendar_add(date, startTime, endTime):
    with SB(uc=True, headed=True) as driver:
        driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAmgQ&hl=en&ifkv=AVQVeyynx9vTWrORetNTDJstyP9KRREywFTztGbPzXPZOA0CLrrBLZexaIuorYLmTqCW3xH2qcyPmg&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-653967197%3A1698546704446367&theme=glif")
        driver.type("#identifierId", 'calhacks224')
        driver.click("#identifierNext > div > button")
        driver.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", 'Dortnite@1233')
        driver.click("#passwordNext > div > button")
        time.sleep(3)
        driver.get(f'https://calendar.google.com/calendar/u/0/r/day/{date}')
        element = driver.find_element(By.CSS_SELECTOR, ".WJVfWe.A3o4Oe")
        element.click()
        startTime = driver.find_element(By.XPATH, '//*[@data-key="startTime"]')
        endTime = driver.find_element(By.XPATH, '//*[@data-key="endTime"]')
        driver.execute_script("arguments[0].textContent = arguments[1];", startTime, "5:00pm")
        driver.execute_script("arguments[0].textContent = arguments[1];", endTime, "6:00pm")
        time.sleep(10)
       
       

if __name__ == '__main__':
    calendar_add(date='2023/10/29', startTime='5:00pm', endTime='6:00pm')