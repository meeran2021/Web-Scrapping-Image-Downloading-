import os
import time
import bs4
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager



def download_image(url, dirName, num):

    # write image to file
    reponse = requests.get(url)
    if reponse.status_code==200:
        with open(os.path.join(dirName, str(num)+".jpg"), 'wb') as file:
            file.write(reponse.content)




search_URL = "https://www.ecosia.org/images?q="         # ULR where you want to search for the element
querry = input('Object name: ')
url = search_URL + querry
chromePath=r'C:\Users\mohta\chromedriver.exe'

# Creating a directory for saving images
dirName = querry+'Image'
if not os.path.isdir(dirName):
    os.makedirs(dirName)


# driver=webdriver.Chrome(chromePath)
s=Service(ChromeDriverManager().install())      # Installing chrome driver
options = webdriver.ChromeOptions()
options.add_argument('headless')                        
driver = webdriver.Chrome(service=s)            # Launching chrome driver
driver.maximize_window()                        # Maximizing chrome window


driver.get(url)                                 # Searching foe the object

driver.execute_script("window.scrollTo(0, 0);") # Executing JavaScript passed as string argument
page_html = driver.page_source                  # Getting the source of the current page
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')      # Pulling data out of HTML and XML files

# container = pageSoup.findAll('article', {'class':"image-feed__item image-result"} ) # Finding all the matches
# containerLen = len(container)
# print(containerLen)


for i in range(1, 330):
    # if i>220:             #for setting max image to be downloaded
    #     break
    
    xPath = """//*[@id="__layout"]/div/main/div/section/div/article[%s]"""%(i)

    previewImageXPath = """//*[@id="__layout"]/div/main/div/section/div/article[%s]/div[1]/a/img"""%(i)
    previewImageElement = driver.find_element(By.XPATH,previewImageXPath)
    previewImageURL = previewImageElement.get_attribute("src")

    # Clicking on each emage one by one
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xPath))).click()
    
    timeStarted = time.time()
    while True:
        
        imgxPath = """/html/body/div/div/div/main/div/section/div/article[%s]/figure/div/a/img"""%(i)
        imageElement = driver.find_element(By.XPATH,imgxPath)
        # print(imageElement)
        imageURL= imageElement.get_attribute('src')
        # print(imageURL)

        if imageURL != previewImageURL:
            break
        else:
            currentTime = time.time()
            if currentTime - timeStarted > 10:
                # Moving onto the next image if loading of image takes too much time
                print("Timeout! Will download a lower resolution image and move onto the next one")
                break
    try:
        download_image(imageURL, dirName, i)                    # Calling func to download image
        print("Downloaded element %s \nURL: %s" % (i, imageURL))
    except:
        print("Couldn't download an image %s, continuing downloading the next one"%(i))
