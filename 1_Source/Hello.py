from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
import requests
import os, sys
from PIL import Image

# Function to save the Captcha image
def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    location = element.location
    size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    # uses PIL library to open image in memory
    image = Image.open(path)

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']

    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save(path, 'png')  # saves new cropped image


# Global variables
months = ['01','02','03','04','05','06','07','08','09','10','11','12']

# Read Credentials from file and year for calculations.
file = open("/home/shiomar/Desktop/SAT/1_Source/1_Keys/credenciales.txt", "r")
rfc = file.readline()
clave = file.readline()
year = file.readline()
file.close()

#Configure Firefox Web Driver to set the absolute path for the XML files.
downloadPath = os.getcwd() + '/2_XMLS'
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", downloadPath)
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

# Initialize Firefox explorer.
browser = webdriver.Firefox(firefox_profile=profile)

# Reach CDFI Portal
browser.get('https://portalcfdi.facturaelectronica.sat.gob.mx/')

# Write RFC.
element = browser.find_element_by_id('rfc')
element = element.send_keys(rfc)

# Write Password.
element = browser.find_element_by_id('password')
element = element.send_keys(clave)

# Saving Captcha image.
imgPath = os.getcwd() + '/3_Captcha/captcha.png'
pic = browser.find_element_by_xpath( "//label[@for='jcaptcha']")
get_captcha(browser, pic, imgPath)



# Captcha part.
text = raw_input("Write the Captcha...  ")
element = browser.find_element_by_id('jcaptcha')
element = element.send_keys(text)

# Submit form.
element = browser.find_element_by_id('submit').click()

# Delay for resource optimization.
sleep(5)

# Click round button and submit.
element = browser.find_element_by_id('ctl00_MainContent_RdoTipoBusquedaReceptor').click() 
element = browser.find_element_by_id('ctl00_MainContent_BtnBusqueda').click()
sleep(5)

# Select date conditions.
element = browser.find_element_by_id('ctl00_MainContent_RdoFechas').click()

# Set year of calculation.
s1 = Select(browser.find_element_by_id('DdlAnio'))
s1.select_by_visible_text(str(year))

# Set "vigente" as a parameter.
s1 = Select(browser.find_element_by_id('ctl00_MainContent_DdlEstadoComprobante'))
s1.select_by_visible_text('Vigente')

for x in months:
	# Set the Window context in the proper range to avoid errors.
	browser.execute_script("scrollBy(0,100);")
	#Delay for resource optimization.
	sleep(5)
	# Set month of calculation and submit
	s1 = Select(browser.find_element_by_name('ctl00$MainContent$CldFecha$DdlMes'))
	s1.select_by_visible_text(x)
	element = browser.find_element_by_id('ctl00_MainContent_BtnBusqueda').click()
	# Delay for resource optimization.
	sleep(15)

	# XML Download Cycle, this cycle will downloadd all the xmls of the current month.
	xml = browser.find_elements_by_class_name("BtnDescarga")
	for e in xml:
		e.click()
		sleep(3)

	# Message of completation a month.
	print('Full month done...')

# Close browser after whole download process.
browser.close()