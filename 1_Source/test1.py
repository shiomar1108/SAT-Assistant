from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests
import os, sys
from selenium.common.exceptions import *
import shutil
import xml.etree.ElementTree as ET
from Tkinter import *
from Tkinter import Tk
from Tkinter import PhotoImage
import webbrowser
from PIL import Image, ImageTk

try:
    TDFFile = os.path.join(os.getcwd(), "TDF.xml");
    XMLdirectory = os.path.abspath(os.path.dirname(__file__));
    incomesConcepts = [];
    deductionsConcepts = [];
    incomesTotal = 0;
    deductionsTotal = 0;
    XMLFiles = [];


    # Function to list all XML's files
    def GetXMLs(path):
        dirs = os.listdir(path)
        for file in dirs:
            if file.endswith('.xml'):
                XMLFiles.append(os.path.join(path, file));

    # Function to get a sub-tree from a XML file
    def GetXMLTree(fileName, treeToFind):
        tree = [];
        for root in ET.parse(fileName).getroot().iter(treeToFind):
            for child in root:
                tree.append(child);
        return tree;


    # Function to get an elemento from a XML file
    def GetXMLElement(fileName, nodeToFind, description, attrib):
        namespaces = {'cfdi': 'http://www.sat.gob.mx/cfd/3'};
        for element in ET.parse(fileName).getroot().iter():
            ele = element.find(nodeToFind, namespaces)
            if (ele != None):
                if (ele.get("Descripcion") == description):
                    return float(ele.get(attrib));
        return 0;


    # Function to get incomesConcepts
    def GetIncomesConcepts():
        incomesTotal = 0;
        incomesConcepts = GetXMLTree(TDFFile, 'Ingresos');
        for file in XMLFiles:
            for element in incomesConcepts:
                incomesTotal = incomesTotal + GetXMLElement(file, element.get("Node"), element.get("Descripcion"),
                                                            element.get("Atributo"));
        print(str(incomesTotal));


    # Function to get deductionConcepts
    def GetDeductionsConcepts():
        deductionsTotal = 0;
        deductionsConcepts = GetXMLTree(TDFFile, 'Deducciones');
        for file in XMLFiles:
            for element in deductionsConcepts:
                deductionsTotal = deductionsTotal + GetXMLElement(file, element.get("Node"), element.get("Descripcion"),
                                                                  element.get("Atributo"));
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

    def Get_values():
        global a, b, c
        a = rfc_entry.get()
        b = pswd_entry.get()
        c = captcha_entry.get()
        print(a)
        print(b)
        print(c)
        proces()


    def callback(event):
        webbrowser.open_new(r"https://www.sat.gob.mx/personas/ayuda")


    def exit(self):
        global gui
        gui.destroy()

    def proces():
        current = browser.current_url
        url_captcha = current == 'https://portalcfdi.facturaelectronica.sat.gob.mx/'
        while not url_captcha:
            # Write RFC.
            element = browser.find_element_by_id('rfc')
            element = element.send_keys(a)

            # Write Password.
            element = browser.find_element_by_id('password')
            element = element.send_keys(b)

            # Saving Captcha image.
            imgPath = os.path.join(os.getcwd(), '3_Captcha')
            shutil.rmtree(imgPath)
            sleep(1)
            os.makedirs(imgPath)
            pic = browser.find_element_by_xpath("//label[@for='jcaptcha']")
            get_captcha(browser, pic, os.path.join(imgPath, 'captcha.png'))

            # Captcha part.
            #text = raw_input("Write the Captcha...  ")
            element = browser.find_element_by_id('jcaptcha')
            element = element.send_keys(c)

            # Submit form.
            element = browser.find_element_by_id('submit').click()

            current = browser.current_url
            url_captcha = current == 'https://portalcfdi.facturaelectronica.sat.gob.mx/'
            # Delay for resource optimization.
            sleep(5)
            element = browser.find_element_by_xpath('//*[@title="Facturas Recibidas"]').click()
            # element = browser.find_element_by_id('ctl00_MainContent_BtnBusqueda').click()
            sleep(5)

            # Select date conditions.
            element = browser.find_element_by_id('ctl00_MainContent_RdoFechas')
            element.send_keys(Keys.SPACE)
            sleep(2)

            # Set the Window context in the proper range to avoid errors.
            browser.execute_script("scrollBy(50,0);")

            # Set year of calculation.
            s1 = Select(browser.find_element_by_name('ctl00$MainContent$CldFecha$DdlAnio'))
            ###########################################
            s1.select_by_visible_text("2017")

            # Set "vigente" as a parameter.
            s1 = Select(browser.find_element_by_id('ctl00_MainContent_DdlEstadoComprobante'))
            s1.select_by_visible_text('Vigente')

            for x in months:
                # Set the Window context in the proper range to avoid errors.
                browser.execute_script("scrollBy(50,0);")
                # Delay for resource optimization.
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

    # Global variables
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    # Read Credentials from file and year for calculations.
    file = open(os.path.join(os.getcwd(), "1_Keys/credenciales.txt"), "r")
    #rfc = file.readline()
    #clave = file.readline()
    year = file.readline()
    file.close()

    # Configure Firefox Web Driver to set the absolute path for the XML files.
    downloadPath = os.path.join(os.getcwd(), "2_XMLS")
    shutil.rmtree(downloadPath)
    sleep(1)
    os.makedirs(downloadPath)
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", downloadPath)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

    # Initialize Firefox explorer.
    browser = webdriver.Firefox(firefox_profile=profile)

    # Resize the window to the screen width/height
    browser.set_window_size(1000, 500)

    # Reach CDFI Portal
    browser.get('https://portalcfdi.facturaelectronica.sat.gob.mx/')

    current = browser.current_url
    url_captcha = current == 'https://portalcfdi.facturaelectronica.sat.gob.mx/'

    # Saving Captcha image.
    imgPath = os.path.join(os.getcwd(), '3_Captcha')
    shutil.rmtree(imgPath)
    sleep(1)
    os.makedirs(imgPath)
    pic = browser.find_element_by_xpath("//label[@for='jcaptcha']")
    get_captcha(browser, pic, os.path.join(imgPath, 'captcha.png'))

    gui = Tk()
    rfc_entry = StringVar()
    pswd_entry = StringVar()
    captcha_entry = StringVar()
    path = r'C:\Users\AxeSalazar\Documents\GitHub\SAT-Assistant\1_Source\3_Captcha\captcha.png'
    # img = ImageTk.PhotoImage(Image.open(path))
    # omg = img.resize((250, 250), img.ANTIALIAS)
    size = 125, 200
    im = Image.open(path)
    im.thumbnail(size, Image.ANTIALIAS)
    img = ImageTk.PhotoImage(im)
    gui.geometry("500x500")
    # make sure first is capital and second is not
    gui.title("Log in")
    #FACTURAS_text = Text(gui, height=10, width=15)
    #FACTURAS_text.grid(column=0, row=1)
    #FACTURAS_text.insert(INSERT, "Factura 01\n")
    #FACTURAS_text.insert(INSERT, "Factura 02\n")
    #FACTURAS_text.insert(END, "Factura 03")
    #XMLS = Label(gui, text="XML's").grid(row=0, column=0)
    RFC = Label(gui, text="R.F.C").grid(row=1, column=1)
    PASSWORD = Label(gui, text="Password").grid(row=2, column=1)
    RFC_TEXTO = Entry(gui,  textvariable = rfc_entry).grid(row=1, column=2)
    PASSWORD_TEXTO = Entry(gui,  textvariable =pswd_entry).grid(row=2, column=2)
    SUBMIT = Button(gui ,text="Submit", command=lambda: Get_values()).grid(row=6, column=3)
    #Devolucion_Label = Label(gui, text="Tu devolucion").grid(row=7, column=1)
    #Devolucion_Entry = Entry(gui).grid(row=8, column=1)
    #Reporte_Label = Label(gui, text="Reporte").grid(row=7, column=3)
    #Enviar = Button(gui, text="enviar").grid(row=8, column=3)
    link = Label(gui, text="Ayuda", fg="blue", cursor="hand2")
    link.grid(column=4, row=0)
    link.bind("<Button-1>", callback)
    link = Label(gui, text="Salir", fg="blue", cursor="hand2")
    link.grid(column=5, row=0)
    link.bind("<Button-1>", exit)

    Captcha = Label(gui, image=img)
    Captcha.grid(row=6, column=1)
    Captcha_entry = Entry(gui,  textvariable = captcha_entry).grid(row=6, column=2)

    downloadPath = os.path.join(os.getcwd(), "2_XMLS")
    GetXMLs(downloadPath);
    GetIncomesConcepts();

    # Close browser after whole download process.
    #browser.close()

    gui.mainloop()


    # Close browser after whole download process.
    browser.close()
except (NoSuchElementException, ElementClickInterceptedException) as e:
    print('Exception been raised...')
    print(e);
    browser.execute_script('arguments[0].scrollIntoView(true);', refresh_button)
    refresh_button.click()