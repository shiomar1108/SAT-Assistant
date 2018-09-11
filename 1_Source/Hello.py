from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
import requests

#Global variables
months = ['01','02','03','04','05','06','07','08','09','10','11','12']

#Read Credentials
file = open("/home/shiomar/Desktop/SAT/1_Source/1_Keys/credenciales.txt", "r")
rfc = file.readline()
clave = file.readline()
year = file.readline()
file.close()

#Initialize Firefox explorer
browser = webdriver.Firefox()

# Reach CDFI Portal
browser.get('https://portalcfdi.facturaelectronica.sat.gob.mx/')

#Write RFC
element = browser.find_element_by_id('rfc')
element = element.send_keys(rfc)

#Write Password
element = browser.find_element_by_id('password')
element = element.send_keys(clave)

#TODO: Save captcha image
#Captcha part
text = raw_input("Write the Captcha...  ")
element = browser.find_element_by_id('jcaptcha')
element = element.send_keys(text)

#Submit form
element = browser.find_element_by_id('submit').click()

#Delay for resource optimization
sleep(1)

#Click round button and submit
element = browser.find_element_by_id('ctl00_MainContent_RdoTipoBusquedaReceptor').click() 
element = browser.find_element_by_id('ctl00_MainContent_BtnBusqueda').click()

#Select date conditions
element = browser.find_element_by_id('ctl00_MainContent_RdoFechas').click()

#Stablish year of calculation
s1 = Select(browser.find_element_by_id('DdlAnio'))
s1.select_by_visible_text(str(year))

#Stablish "vigente" as a parameter
s1 = Select(browser.find_element_by_id('ctl00_MainContent_DdlEstadoComprobante'))
s1.select_by_visible_text('Vigente')

for x in months: 
	#Stablish month of calculation and submit
	s1 = Select(browser.find_element_by_id('ctl00_MainContent_CldFecha_DdlMes')) 
	s1.select_by_visible_text(x)
	element = browser.find_element_by_id('ctl00_MainContent_BtnBusqueda').click()

	#Delay for resource optimization
	sleep(10)

browser.close()