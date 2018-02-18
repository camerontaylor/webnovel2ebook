#pylint: disable-all
from selenium import webdriver
import getify
import time
import urllib.request

print("Select Category:")
print("")
print("1. Popular | Top 30")
print("2. Xianxia")
print("3. Xuanhuan")
print("4. Fantasy")
print("5. Sci-Fi")
print("6. Modern")
print("7. Romance")
print("8. Gaming")
print("9. Other")

website = None
x = int(input("Select a category (Enter Number): "))
if x == 1:
	website = "https://www.webnovel.com/category/list?category=0"
elif x == 2:
	website = "https://www.webnovel.com/category/list?category=20014"
elif x == 3:
	website = "https://www.webnovel.com/category/list?category=20001"
elif x == 4:
	website = "https://www.webnovel.com/category/list?category=20005"
elif x == 5:
	website = "https://www.webnovel.com/category/list?category=20042"
elif x == 6:
	website = "https://www.webnovel.com/category/list?category=20019"
elif x == 7:
	website = "https://www.webnovel.com/category/list?category=30031"
elif x == 8:
	website = "https://www.webnovel.com/category/list?category=20050"
elif x == 9:
	website = "https://www.webnovel.com/category/list?category=-1"
	
#Initializes webdriver
print("Getting Data...")
driver = webdriver.PhantomJS("phantomjs.exe")
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

# Delete empty lines from files
for n in file_list:
	getify.remove_empty_lines(n)

getify.generate(file_list, result[select - 1]["text"], info, chlistSelection, str(startingChapter), str(endingChapter))
