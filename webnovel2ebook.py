#pylint: disable-all
from selenium import webdriver
import getify
import time
import urllib.request
import sys

driver = webdriver.PhantomJS()

if len(sys.argv) > 1:
  website = sys.argv[1]
else:
    print("Select Category:")
    print("")
    print("01. Popular | Top 30")
    print("02. Magical Realism")
    print("03. Fantasy")
    print("04. Historical Fiction")
    print("05. Horror & Thriller")
    print("06. Romance Fiction")
    print("07. Science Fiction")
    print("08. Competitive Sports")
    print("09. Video Games")
    print("10. Eastern Fantasy")
    print("11. Realistic Fiction")
    print("12. Fan-fiction")
    print("13. Martial Arts")
    print("14. Military Fiction")

    website = None
    x = int(input("Select a category (Enter Number): "))
    if x == 1:
            website = "https://www.webnovel.com/category/list?category=0"
    elif x == 2:
            website = "https://www.webnovel.com/category/list?category=Magical%20Realism"
    elif x == 3:
            website = "https://www.webnovel.com/category/list?category=Fantasy"
    elif x == 4:
            website = "https://www.webnovel.com/category/list?category=Historical%20Fiction"
    elif x == 5:
            website = "https://www.webnovel.com/category/list?category=Horror%20%26%20Thriller"
    elif x == 6:
            website = "https://www.webnovel.com/category/list?category=Romance%20Fiction"
    elif x == 7:
            website = "https://www.webnovel.com/category/list?category=Science%20Fiction"
    elif x == 8:
            website = "https://www.webnovel.com/category/list?category=Competitive%20Sports"
    elif x == 9:
            website = "https://www.webnovel.com/category/list?category=Video%20Games"
    elif x == 10:
            website = "https://www.webnovel.com/category/list?category=Eastern%20Fantasy"
    elif x == 11:
            website = "https://www.webnovel.com/category/list?category=Realistic%20Fiction"
    elif x == 12:
            website = "https://www.webnovel.com/category/list?category=Fan-fiction%20"
    elif x == 13:
            website = "https://www.webnovel.com/category/list?category=Martial%20Arts"	
    elif x == 14:
            website = "https://www.webnovel.com/category/list?category=War%20%26%20Military%20Fiction"

    #Initializes webdriver
    print("Getting Data...")
    driver.maximize_window()
    driver.get(website)
    #print(website)

    # Collects Title and link of the Book
    elem = driver.find_elements_by_css_selector("a.c_strong")
    result = [{"link": category.get_attribute("href"), "text": category.get_attribute("title")}
    for category in elem]
    result = result[::2]
            
    # Sorts and makes the data look kinda pretty
    g = 1
    for i in result:
            if g <= 9:
                    print("0" + str(g) + ". ", end="")
                    print(i["text"])
                    g += 1
            else:
                    print(str(g) + ". ", end="")
                    print(i["text"])
                    g += 1
                    
    #Gets chapter Names and links
    select = int(input("Which Novel do you want to read?: "))
    website = result[select - 1]["link"]
#print(website)
print("Getting Chapter names ,links, cover and metadata...")
driver.get(website)
img = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div[1]/i/img')
src = img.get_attribute("src")
urllib.request.urlretrieve(src, "cover.png")

v = "title"
print("Preparing title page")
getify.download(website, v)
getify.create_title(v)
print("Done!")

print("Counting chapters")

rawMeta = driver.find_elements_by_css_selector("p.ell.dib.vam")
#rawMeta = driver.find_elements_by_xpath("/html/body[@class='footer_auto']/div[@class='page']/div[@class='det-hd mb48']/div[@class='g_wrap']/div[@class='det-info g_row c_strong fs16 pr']/div[@class='_mn g_col_8 pr']/address[@class='lh1d5 mb24 pr']/p[@class='ell dib vam']")
meta = [test.text for test in rawMeta]
for x, y in enumerate(meta):
	if y.startswith("Author: "):
		info = y[len("Author: "):] + ", "
	if y.startswith("Translator: "):
		info += y[len("Translator: "):]
popup = driver.find_element_by_xpath("/html/body[@class='footer_auto']/div[@class='page']/div[@class='g_wrap det-tab-nav mb48 mt-10 _slide']/a[@class='j_show_contents']/span")
popup.click()
time.sleep(1)
chlistRaw = driver.find_elements_by_css_selector("a.c_strong.vam.ell.db.pr" )
chlist = [{"link": category.get_attribute("href"), "text": category.text} for category in chlistRaw]
driver.save_screenshot('screenshot.png')
driver.quit()

print ("There are currently " + str(len(chlist)) + " available")
startingChapter = int(input("What's the starting Chapter?: "))
endingChapter = int(input("What's the ending Chapter?: "))

chlistSelection = chlist[startingChapter - 1 : endingChapter]

file_list = []
# file_list.append("titlem" + ".xhtml")
for q in range(len(chlistSelection)):
	getify.download(chlistSelection[q]["link"], str(q))
	getify.clean(str(q))
	file_list.append(str(q) + "m" + ".xhtml")
	getify.update_progress(q/len(chlistSelection))


getify.generate(file_list, result[select - 1]["text"], info, chlistSelection, str(startingChapter), str(endingChapter))
