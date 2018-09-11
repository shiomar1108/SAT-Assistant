from selenium import webdriver

#Read Credentials
file = open("/home/shiomar/Desktop/SAT/1_Source/1_Keys/credenciales.txt", "r")
rfc = file.readline()
clave = file.readline()

#Initialize Firefox explorer
browser = webdriver.Firefox()
# Reach CDFI Portal
browser.get('https://portalcfdi.facturaelectronica.sat.gob.mx/')

element = browser.find_element_by_id('rfc')
element = element.send_keys(rfc)

#Write Password
element = browser.find_element_by_id('password')
element = element.send_keys(clave)

#Captcha part
text = raw_input("Write the Captcha")
element = browser.find_element_by_id('jcaptcha')
element = element.send_keys(text)

#Submit form
element = browser.find_element_by_id('submit').click()