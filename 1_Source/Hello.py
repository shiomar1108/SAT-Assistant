# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests
import os, sys
from PIL import Image
from selenium.common.exceptions import *
import shutil
import xml.etree.ElementTree as ET

# Function to list all XML's files
def GetXMLs(path):
	dirs = os.listdir(path)
	for file in dirs:
		if file.endswith('.xml'):
			XMLFiles.append(os.path.join(path, file));

# Function to get a sub-tree from a XML file
def GetXMLTree(fileName, treeToFind):
	tree = [];
	with open(fileName, 'r') as xml_file:
		for root in ET.parse(xml_file).getroot().iter(treeToFind):
			for child in root:
				tree.append(child);
	return tree;

# Function to get an elemento from a XML file
def GetXMLElement(fileName, nodeToFind, description, attrib):
	if(nodeToFind != None):
		namespaces = {'cfdi': 'http://www.sat.gob.mx/cfd/3'};
		for element in ET.parse(fileName).getroot().iter():
			ele = element.find(nodeToFind, namespaces)
			if(ele != None):
				if(ele.get("Descripcion") == description):
					return float(ele.get(attrib));
	return 0;

# Function to get incomesConcepts
def GetIncomesConcepts():
	incomesTotal = 0;
	incomesConcepts = GetXMLTree(TDFFile, 'Ingresos');
	for file in XMLFiles:
		for element in incomesConcepts:
			# income = GetXMLElement(file, element.get("Node"), element.get("Descripcion"), element.get("Atributo"));
			income = GetXMLElement(file, element.get("Node"), "Pago de nómina", element.get("Atributo"));
			if(income > 0):
				incomesTotal += income;
				myElementList = [];
				myElementList.append(element.get("Descripcion"))
				myElementList.append(element.get("Atributo"))
				myElementList.append(income);
				print(myElementList);
	print(str(incomesTotal));

# Function to get deductionConcepts
def GetDeductionsConcepts():
	deductionsTotal = 0;
	deductionsConcepts = GetXMLTree(TDFFile, 'Deducciones');
	for file in XMLFiles:
		for element in deductionsConcepts:
			deduction = GetXMLElement(file, element.get("Node"), element.get("Descripcion"), element.get("Atributo"));
			if(deduction > 0):
				deductionsTotal += deduction;
				myElementList = [];
				myElementList.extend(element.get("Descripcion"))
				myElementList.extend(element.get("Atributo"))
				myElementList.extend(deduction);
				print(myElementList);
	print(str(deductionsTotal));

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

def init ():
	#Configure Firefox Web Driver to set the absolute path for the XML files.
	downloadPath = os.path.join(os.getcwd(), "2_XMLS")
	# shutil.rmtree(downloadPath)
	sleep(1)
	# os.makedirs(downloadPath)
	profile = webdriver.FirefoxProfile()
	profile.set_preference("browser.download.folderList", 2)
	profile.set_preference("browser.download.manager.showWhenStarting", False)
	profile.set_preference("browser.download.dir", downloadPath)
	profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

	# Initialize Firefox explorer.
	browser = webdriver.Firefox(firefox_profile=profile)

	# Resize the window to the screen width/height
	browser.set_window_size(1000, 500)
	return browser

def login (browser):
	# Read Credentials from file and year for calculations.
	file = open(os.path.join(os.getcwd(), "1_Keys/credenciales.txt"), "r")
	rfc = file.readline()
	clave = file.readline()
	year = file.readline()
	file.close()
	# Reach CDFI Portal
	browser.get('https://portalcfdi.facturaelectronica.sat.gob.mx/')

	current = browser.current_url
	url_captcha = current == 'https://portalcfdi.facturaelectronica.sat.gob.mx/'
	
	while not url_captcha:
		# Write RFC.
		element = browser.find_element_by_id('rfc')
		element = element.send_keys(rfc)

		# Write Password.
		element = browser.find_element_by_id('password')
		element = element.send_keys(clave)

		# Saving Captcha image.
		imgPath = os.path.join(os.getcwd(), '3_Captcha')
		shutil.rmtree(imgPath)
		sleep(1)
		os.makedirs(imgPath)
		pic = browser.find_element_by_xpath( "//label[@for='jcaptcha']")
		get_captcha(browser, pic, os.path.join(imgPath,'captcha.png'))

		# Captcha part.
		text = raw_input("Write the Captcha...  ")
		element = browser.find_element_by_id('jcaptcha')
		element = element.send_keys(text)

		# Submit form.
		element = browser.find_element_by_id('submit').click()

		current = browser.current_url
		url_captcha = current == 'https://portalcfdi.facturaelectronica.sat.gob.mx/'
		# Delay for resource optimization.
		sleep(5)

	return year
		
def download (browser,year):
	# Click round button and submit.
	element = browser.find_element_by_xpath('//*[@title="Facturas Recibidas"]').click()
	#element = browser.find_element_by_id('ctl00_MainContent_BtnBusqueda').click()
	sleep(5)

	# Select date conditions.
	element = browser.find_element_by_id('ctl00_MainContent_RdoFechas')
	element.send_keys(Keys.SPACE)
	sleep(2)

	# Set the Window context in the proper range to avoid errors.
	browser.execute_script("scrollBy(50,0);")

	# Set year of calculation.
	s1 = Select(browser.find_element_by_name('ctl00$MainContent$CldFecha$DdlAnio'))
	s1.select_by_visible_text(str(year))

	# Set "vigente" as a parameter.
	s1 = Select(browser.find_element_by_id('ctl00_MainContent_DdlEstadoComprobante'))
	s1.select_by_visible_text('Vigente')

	for x in months:
		# Set the Window context in the proper range to avoid errors.
		browser.execute_script("scrollBy(50,0);")
		#Delay for resource optimization.
		sleep(5)
		# Set month of calculation and submit
		s1 = Select(browser.find_element_by_name('ctl00$MainContent$CldFecha$DdlMes'))
		s1.select_by_visible_text(x)
		element = browser.find_element_by_id('ctl00_MainContent_BtnBusqueda').click()
		# Delay for resource optimization.
		sleep(15)
		browser.execute_script("scrollBy(150,0);")

		# XML Download Cycle, this cycle will downloadd all the xmls of the current month.
		xml = browser.find_elements_by_xpath('//*[@title="Descargar"]')
		for e in xml:
			e.click()
			sleep(3)
		# Message of completation a month.
		print('Full month done...')
		# Set the Window context in the proper range to avoid errors.
		browser.execute_script("scrollBy(0,0);")


try:
	# Global variables
	months = ['01','02','03','04','05','06','07','08','09','10','11','12']
	TDFFile = os.path.join(os.getcwd(), "TDF.xml");
	XMLdirectory = os.path.abspath(os.path.dirname(__file__));
	incomesConcepts = [];
	deductionsConcepts = [];
	listOfIncomes = [];
	listOfDeductions = [];
	incomesTotal = 0;
	deductionsTotal = 0;
	XMLFiles = [];
	year = 0

	firefox = init()
	year = login(firefox)
	# download(firefox , year)

<<<<<<< HEAD
	downloadPath = os.path.join(os.getcwd(), "2_XMLS");
	GetXMLs(downloadPath);
	GetIncomesConcepts();
	GetDeductionsConcepts();

=======
	downloadPath = os.path.join(os.getcwd(), "2_XMLS")
	GetXMLs(downloadPath);
	GetIncomesConcepts();
	GetDeductionsConcepts();
	print(str(Ingresos - Egresos))
>>>>>>> b7f85d7818d806879920030186b2f39917b7fb02
	# Close browser after whole download process.
	firefox.close()

except (NoSuchElementException, ElementClickInterceptedException) as e:
	print('Exception been raised...')
	print(e);
	firefox.navigate().refresh();