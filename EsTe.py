import os
import re
import sys
import csv
import selenium
import pandas as pd
from csv import writer
from csv import reader
from csv import DictReader
from selenium import webdriver
import zipfile, urllib.request, shutil

#selenium chrome driver
PATH = "./chromedriver"
lista_supporto = ['']


def estrai_temi_giornali(testata):
    themes      = [0]*8
    url_testata = ''
    if testata == "nytimes":
        url_testata = "nytimes.com"
    elif testata == "bbc":
        url_testata == "bbc.co.uk"
    #apertura file in modalità lettura
    with open('file_zip.csv','r') as file_con_url:
        csv_reader = DictReader(file_con_url)
        #iterazione riga per riga
        for riga in csv_reader:
            #estraggo l'url
            url = riga['ZIP URL']
            try:
                #estrazione la data dall'url
                #formato data : yyyymmddhhmmss
                regex_data  = r"\d{14}"
                data        = re.findall(regex_data, url)
            except:
                print("Errore estrazione data")
            
            #zip file
            nome_zip = data[0]+".gkg.csv.zip"
            
            try:
                with urllib.request.urlopen(url) as response, open(nome_zip, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
            except:
                print("ERRORE: download zip")
        
            try:
                with zipfile.ZipFile(nome_zip) as zf:  #extract zip file
                    zf.extractall()
            except:
                print("ERRORE: estrazione csv")
            try:
                nome_file =  data[0]+".gkg.csv"  #CSV file names
                f = csv.reader(open(nome_file),delimiter='\t')
            except:
                print("ERRORE: apertura csv")
            
            data_completa = data[0][0]+data[0][1]+data[0][2]+data[0][3]+'/'+data[0][4]+data[0][5]+'/'+data[0][6]+data[0][7]
            if len(themes) == 8:
                themes.insert(0,data_completa)
            try:
                for row in f:
                    data_row = row[1][0]+row[1][1]+row[1][2]+row[1][3]+'/'+row[1][4]+row[1][5]+'/'+row[1][6]+row[1][7]
                    if data_row == themes[0]:
                        try:
                            if row[3] == url_testata:
                                elementi = row[7].split(';')            
                                #ATTACCHI INFORMATICI E INTERNET
                                if  "CYBER_ATTACK" in elementi:
                                    themes[1] += 1
                                #MIGRAZIONE
                                if "AFFECT" in elementi or "DISPLACED" in elementi or "IMMIGRATION" in elementi or "REFUGEES" in elementi or "SOC_MASSMIGRATION" in elementi:
                                    themes[2] += 1
                                #AMBIENTE
                                if "ENV_BIOFUEL" in elementi or "ENV_CLIMATECHANGE" in elementi or "ENV_DEFORESTATION" in elementi or "ENV_GEOTHERMAL" in elementi or "ENV_GREEN" in elementi or "ENV_HYDRO" in elementi or "ENV_METALS" in elementi or "ENV_MINING" in elementi or "ENV_NATURALGAS" in elementi or "ENV_NUCLEARPOWER" in elementi or "ENV_OVERFISH" in elementi or  "ENV_POACHING" in elementi or "ENV_SOLAR" in elementi or "ENV_SPECIESENDANGERED" in elementi or "ENV_SPECIESEXTINCT" in elementi or "ENV_WATERWAYS" in elementi or "ENV_WINDPOWER" in elementi or "NATURAL_DISASTER" in elementi or "WATER_SECURITY" in elementi or "SELF_IDENTIFIED_ENVIRON_DISASTER" in elementi:
                                    themes[3] += 1
                                #TERRORISMO
                                if "EXTREMISM" in elementi or "IDEOLOGY" in elementi or "JIHAD" in elementi or "SEPARATISTS" in elementi or "SUICIDE_ATTACK" in elementi or "TERROR" in elementi:
                                    themes[4] += 1
                                #VIOLENZA DI GENERE E DISCRIMINAZIONE
                                if "DISCRIMINATION" in elementi or "GENDER_VIOLENCE" in elementi or "LGBT" in elementi:
                                    themes[5] += 1
                                #ORGANIZZAZIONI CRIMINALI:
                                if "CRIME_CARTELS" in elementi or "CRIME_COMMON_ROBBERY" in elementi or "CRIME_ILLEGAL_DRUGS" in elementi or  "DRUG_TRADE" in elementi or "SOC_GENERALCRIME" in elementi:
                                    themes[6] += 1
                                #GUERRA E PACE 
                                if "ARMEDCONFLICT" in elementi or "FIREARM_OWNERSHIP" in elementi or "MIL_SELF_IDENTIFIED_ARMS_DEAL" in elementi or  "MIL_WEAPONS_PROLIFERATION" in elementi or "MILITARY" in elementi or "MILITARY_COOPERATION" in elementi or "PEACEKEEPING" in elementi or "SLFID_MILITARY_BUILDUP" in elementi or "SLFID_MILITARY_READINESS" in elementi or "SLFID_MILITARY_SPENDING" in elementi or "SLFID_PEACE_BUILDING" in elementi or "TAX_WEAPONS" in elementi or "WMD" in elementi:
                                    themes[7] +=1
                                #ELEZIONI
                                if "ELECTION" in elementi:
                                    themes[8] += 1
                                   
                        except Exception as e:
                           print(e)
                    else:
                        with open(testata+'.csv', 'a', newline='') as output:
                            writer = csv.writer(output)
                            writer.writerow(themes)
                        themes.clear()
                        themes = [0]*8
                        themes.insert(0,data_completa)
            except Exception as e:
                print(e)
            
            
            print("file"+nome_file+"completato")
            os.remove(nome_file)
            os.remove(nome_zip)


def get_zip_url():
    zip_url     = []                                                        #get all url to dowload
    driver      = webdriver.Chrome(PATH)
    xpath       = "html/body/pre"                                           #path of the items to save
    main_url    = 'http://data.gdeltproject.org/gdeltv2/masterfilelist.txt' #URL to download from
    #regex for find url 
    url_regex   = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    gkg         = "gkg"
    
    driver.get(main_url)
    
    print("Search for elements...")
    
    prova       =  driver.find_element_by_xpath(xpath)
    testo_prova = prova.text
    find_url    = re.findall(url_regex,testo_prova)  #find url 
    
    print("Close browser...")
    
    driver.quit()

    print("Link extraction...")
    # u = url string 
    # e1,e2,e3,e4 = empty elements
    for (u,e1,e2,e3,e4) in find_url:
        if gkg in u: #find only the correct url
            zip_url.append(u)
    zip_url.reverse()
    #save all urls in cvs file
    with open('file_zip.csv','a+',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['ZIP URL'])
        for url in zip_url:
            writer.writerow([url])


if __name__ == "__main__":
    #lista contenente i temi 
    header = ["DATA","ATTACCHI INFORMATICI E INTERNET","MIGRAZIONE","AMBIENTE", "TERRORISMO","VIOLENZA DI GENERE E DISCRIMINAZIONE","ORGANIZZAZIONI CRIMINALI", "GUERRA E PACE","ELEZIONI"]

    chiave = sys.argv[1]
    nome = chiave+".csv"
    f = open(nome, 'w')
    writer = csv.DictWriter(f,fieldnames=header)
    writer.writeheader()
    f.close()

    # get_zip_url()
    estrai_temi_giornali(chiave)
    print('FINE')
