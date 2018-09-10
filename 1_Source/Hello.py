from selenium import webdriver

#Initialize Firefox explorer
browser = webdriver.Firefox()
# Reach CDFI Portal
browser.get('https://portalcfdi.facturaelectronica.sat.gob.mx/')
#Click e.firma option to avoid captcha
browser.find_element_by_css_selector('.btn.btn-default').click()

#Set private key from file
element = browser.find_element_by_id('btnPrivateKey').click()


#browser.find_element_by_id('btnCertificate').click()