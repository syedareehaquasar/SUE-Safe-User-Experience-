# -*- coding: utf-8 -*-
"""UrlFeatureExtract.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uUPkzUr55Kdxxdk8oYENol4-8V-8LISd

# Loading saved model
"""

import pickle

# load model from file
loaded_model = pickle.load(open("/content/drive/My Drive/SUE/XGBoostClassifier.pkl", "rb"))
loaded_model

"""# Feature Extraction

## Importing packages required
"""

import sys
import csv
import pandas as pd
import regex
#provides the capabilities to create, manipulate and operate on IPv4 and IPv6 addresses and networks.
#used for extracting having_ip_address feature 
import ipaddress 
#!pip install 2to3
#import 2to3
!pip install tldextract
from tldextract import extract
import ssl

!pip install urllib
import urllib
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import bs4, re
#!pip install google-search
#from googlesearch.googlesearch import GoogleSearch
!pip install python-whois
import whois
from datetime import datetime
import time
import requests
import urllib.request
from urllib.parse import urlencode
import subprocess
import urllib3, requests, json
import socket

def having_IPhaving_IP_Address(url):
    try:
        ipaddress.ip_address(url)
        return -1
    except:
        return 1
# having_IPhaving_IP_Address("www.google.com")

def URLURL_Length(url):
    if (len(url) < 54) :
        return 1
    elif (len(url) < 75):
      return 0
    else:
        return -1
# URLURL_Length("hjvscsdavjavcjh")

def Shortining_Service(url):
    shortining = regex.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                    'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                    'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                    'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                    'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                    'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                    'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', url)
    if shortining:
        return -1
    else:
        return 1
# Shortining_Service("www.rgsdfgad")

def having_At_Symbol(url):
    at_symbol = regex.findall(r'@',url)
    if(len(at_symbol) == 0): #if @ symbol is not in url then its safe
        return 1
    else:
        return -1
# having_At_Symbol("www.goog@le.com")

def double_slash_redirecting(url):
    locate_double_slash = [x.start(0) for x in re.finditer('//', url)] #making list of each individual character
    if locate_double_slash[len(locate_double_slash)-1] > 6: #checking if // occures after 6th position
        return -1
    else:
        return 1

# double_slash_redirecting("http//:vshdhjkjhds")

def Prefix_Suffix(domain):
    if('-' in domain):
        return -1
    else:
        return 1
        
# Prefix_Suffix("gitlab-kk")

def having_Sub_Domain(hostname):
    if len(re.findall("\.", hostname)) == 0:
        return 1
    elif len(re.findall("\.", hostname)) == 1:
        return 0
    else:
        return -1

# having_Sub_Domain("google")

def SSLfinal_State(url):
    try:
      # check wheather contains https
      if (regex.search('^https', url)):
        usehttps = 1
      else:
        usehttps = 0
      subDomain, domain, suffix = extract(url)
      host_name = domain + "." + suffix
      context = ssl.create_default_context()
      sct = context.wrap_socket(socket.socket(), server_hostname=host_name)
      sct.connect((host_name, 443))
      certificate = sct.getpeercert()
      issuer = dict(x[0] for x in certificate['issuer'])
      certificate_Auth = str(issuer['commonName'])
      certificate_Auth = certificate_Auth.split()
      if (certificate_Auth[0] == "Network" or certificate_Auth == "Deutsche"):
          certificate_Auth = certificate_Auth[0] + " " + certificate_Auth[1]
      else:
          certificate_Auth = certificate_Auth[0]
      trusted_Auth = ['AC Camerfirma, S.A', 'Actalis', 'Agencia Notarial de Certificación (ANCERT)', "ANCERT",  'Amazon', 'Asseco Data Systems S.A. (previously Unizeto Certum)', "Unizeto Certum", 'Comodo', 'Symantec', 'GoDaddy', 'GlobalSign', 'DigiCert', 'StartCom', 'Entrust', 'Verizon',
                        'A-Trust','Trustwave', 'Unizeto', 'Buypass', 'QuoVadis', 'Deutsche Telekom', 'Network Solutions', ''
                        'SwissSign', 'Google Trust Services (GTS)', "GTS", 'Government of Australia' ,'IdenTrust', 'Secom', 'TWCA', 'GeoTrust', 'Thawte', 'Doster', 'VeriSign', 'Google',
                        'Government of India, Ministry of Communications & Information Technology, Controller of Certifying Authorities (CCA)', "CCA", 
                        'Symantec', 'VeriSign', 'Sectigo', 'Let\'s', 'Network Solutions','cPanel', 'Cloudflare', 'DigiCert']

      startingDate = str(certificate['notBefore'])
      endingDate = str(certificate['notAfter'])
      startingYear = int(startingDate.split()[3])
      endingYear = int(endingDate.split()[3])
      Age_of_certificate = endingYear - startingYear
      if ((usehttps == 1) and (certificate_Auth in trusted_Auth) and (Age_of_certificate <= 1)):
        return 1  # legitimate
      else:
        return -1  # phishing

    except:
        return -1

# SSLfinal_State("www.google.com")
# SSLfinal_State("https://www.youtube.com/")
# SSLfinal_State("http://www.Confirme-paypal.com/")

def Domain_registration_length(url):
  try:
    whois_database = whois.whois(url)
    updated_datetime = whois_database.updated_date
    # print(updated_datetime)
    exp_datetime = whois_database.expiration_date
    # print(exp_datetime)
    length_period = (exp_datetime[0]-updated_datetime[0]).days
    # print(length_period)
    if (length_period <= 365):
      return -1
    else:
      return 1
  except:
        return 0
# Domain_registration_length("https://colab.research.google.com/drive/1uUPkzUr55Kdxxdk8oYENol4-8V-8LISd#scrollTo=6_om8F99ELA0")

def soupssss(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')
  return soup

def favicon(url, soup):
  try:
    for head in soup.find_all('head'):
      for head.link in soup.find_all('link', href=True):
        dots = [x.start(0) for x in re.finditer('\.', head.link['href'])]
        if url in head.link['href'] or len(dots) == 1 or domain in head.link['href']:
          return 1
    return -1
  except:
    return 1

favicon("https://gitlab.com/syedareehaquasar/tswe-project", soupssss("https://gitlab.com/syedareehaquasar/tswe-project"))

def port(url, domain):
    try:
        port = domain.split(":")[1]
        if port:
            return -1
        else:
            return 1
    except:
        return 1

def HTTPS_token(url):
  # if re.findall(r"^https://", url):
  #   return 1
  # return -1
    check = re.search('https://|http://', url)
    if check:
      return 1
    check = re.search('http|https', url)
    if check:
        return -1
    else:
        return 1
# HTTPS_token("www.google.com")

def Request_url(url, soup, domain):
    i = 0
    success = 0
    if soup == -999:
        return -1
    else:
        for img in soup.find_all('img', src= True):
           dots= [x.start(0) for x in re.finditer('\.', img['src'])]
           if url in img['src'] or domain in img['src'] or len(dots)==1:
              success = success + 1
           i=i+1

        for audio in soup.find_all('audio', src= True):
           dots = [x.start(0) for x in re.finditer('\.', audio['src'])]
           if url in audio['src'] or domain in audio['src'] or len(dots)==1:
              success = success + 1
           i=i+1

        for embed in soup.find_all('embed', src= True):
           dots=[x.start(0) for x in re.finditer('\.',embed['src'])]
           if url in embed['src'] or domain in embed['src'] or len(dots)==1:
              success = success + 1
           i=i+1

        for iframe in soup.find_all('iframe', src= True):
           dots=[x.start(0) for x in re.finditer('\.',iframe['src'])]
           if url in iframe['src'] or domain in iframe['src'] or len(dots)==1:
              success = success + 1
           i=i+1

        try:
           percentage = success/float(i) * 100
           if percentage < 22.0 :
              return 1
           elif((percentage >= 22.0) and (percentage < 61.0)) :
              return 0
           else :
              return -1
        except:
            return 1

def Url_of_Anchor(url, soup, domain):
    return 0
    percentage = 0
    i = 0
    unsafe = 0
    if soup == -999:
        return -1
    else:
        for a in soup.find_all('a', href=True):
        # 2nd condition was 'JavaScript ::void(0)' but we put JavaScript because the space between javascript and :: might not be
                # there in the actual a['href']
            if "#" in a['href'] or "javascript" in a['href'].lower() or "mailto" in a['href'].lower() or not (url in a['href'] or domain in a['href']):
                unsafe = unsafe + 1
            i = i + 1


        try:
            percentage = unsafe / float(i) * 100
        except:
            return 1

        if percentage < 31.0:
            return 1
        elif ((percentage >= 31.0) and (percentage < 67.0)):
            return 0
        else:
            return -1

def Links_in_tags(url, soup, domain):
  good = 0
  bad =0
  for link in soup.find_all('link', href= True):
    count =[x.start(0) for x in re.finditer('\.',link['href'])]
    if url in link['href'] or domain in link['href'] or len(count) == 1:
      bad += 1
    good += 1

  for script in soup.find_all('script', src= True):
    count =[x.start(0) for x in re.finditer('\.',script['src'])]
    if url in script['src'] or domain in script['src'] or len(count) == 1 :
      bad += 1
    good += 1

  try:
    percentage = bad / float(good) * 100
    if percentage < 17.0 :
      return 1
    elif((percentage >= 17.0) and (percentage < 81.0)) :
      return 0
    else :
      return -1

  except:
    return 1

def SFH(url, soup):
    try:
      for form in soup.find_all('form', action= True):
        if form['action'] =="" or form['action'] == "about:blank" :
          return -1
        elif url not in form['action'] and domain not in form['action']:
          return 0
        else:
          return 1
      return 1
                 
    except:
        return -1

def Submitting_to_email(response):
    if response == "":
        return -1
    else:
        if re.findall(r"[mail\(\)|mailto:?]", response.text):
            return -1
        else:
            return 1

#.
def Abnormal_URL(response):
    if response == "":
        return -1
    else:
        if response.text == "":
            return -1
        else:
            return 1

def Redirect(response):
  if len(response.history) <= 1:
    return 1
  else:
    return 0

def on_mouseover(response):
  if re.findall("<script>.+onmouseover.+</script>", response.text):
    return -1
  else:
    return 1

def RightClick(response):
  if re.findall(r"event.button ?== ?2", response.text):
    return -1
  else:
    return 1

def popUpWindow(response):
  if re.findall(r"alert\(", response.text):
    return -1
  else:
    return 1

def Iframe(response):
  if re.findall(r"[<iframe>|<frameBorder>]", response.text):
    return -1
  else:
    return 1

def age_of_domain(url):
    try:
        domain_name = whois.whois(url)
        if isinstance(domain_name.creation_date, list):
            creation_date = domain_name.creation_date[0]
        else:
            creation_date = domain_name.creation_date

        creation_date = str(creation_date).split(' ')[0]

        if isinstance(domain_name.expiration_date, list):
            expiration_date = domain_name.expiration_date[0]
        else:
            expiration_date = domain_name.expiration_date

        expiration_date = str(expiration_date).split(' ')[0]


        creation_date = datetime.strptime(str(creation_date), '%Y-%m-%d')
        expiration_date = datetime.strptime(str(expiration_date), '%Y-%m-%d')
        ageofdomain = abs((expiration_date - creation_date).days)
        #print(ageofdomain)
        if (ageofdomain/30) > 6:
            return 1
        else:
            return -1
    except:
        return -1

def DNSRecord(url):
    dns = 0
    try:
        d = whois.whois(url)
    except:
        dns = -1
    if dns == -1:
        return -1
    else:
        return 1

def web_traffic(url):
    try:
        with urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url) as response:
            html = response.read()
    except:
        return -1

    tree = ET.fromstring(html.decode())
    try:
        rank = (tree.findall('*/REACH'))[0].attrib['RANK']
    except:
        return -1
    if (int(rank)<100000):
        return 1
    else:
        return -1
web_traffic("www.google.com")

#
def Page_Rank(global_rank):
  return 0
    # try:
    #     if global_rank > 0 and global_rank < 100000:
    #         return 1
    #     else:
    #         return -1
    # except:
    #     return 1
# Page_Rank("ashdnkjbckjb")

#
def Google_Index(url):
  return 0
    # site = search(url, 5)
    # if site:
    #     return 1
    # else:
    #     return -1

# Google_Index("hmnva")

def Links_pointing_to_page(response):
  num_of_links = len(re.findall(r"<a href=", response.text))
  if num_of_links == 0:
    return 1
  elif num_of_links <= 2:
    return 0
  else:
    return -1

def Statical_report(url):
    hostname = url
    scaned_hostname = [(x.start(0), x.end(0)) for x in re.finditer('https://|http://|www.|https://www.|http://www.', hostname)]
    length_hostname = int(len(scaned_hostname))
    if length_hostname != 0:
        y = scaned_hostname[0][1]
        hostname = hostname[y:]
        scaned_hostname = [(x.start(0), x.end(0)) for x in re.finditer('/', hostname)]
        length_hostname = int(len(scaned_hostname))
        if length_hostname != 0:
            hostname = hostname[:scaned_hostname[0][0]]
    url_match=re.search('at\.ua|usa\.cc|baltazarpresentes\.com\.br|pe\.hu|esy\.es|hol\.es|sweddy\.com|myjino\.ru|96\.lt|ow\.ly',url)
    try:
        ip_address = socket.gethostbyname(hostname)
        ip_match=re.search('146\.112\.61\.108|213\.174\.157\.151|121\.50\.168\.88|192\.185\.217\.116|78\.46\.211\.158|181\.174\.165\.13|46\.242\.145\.103|121\.50\.168\.40|83\.125\.22\.219|46\.242\.145\.98|107\.151\.148\.44|107\.151\.148\.107|64\.70\.19\.203|199\.184\.144\.27|107\.151\.148\.108|107\.151\.148\.109|119\.28\.52\.61|54\.83\.43\.69|52\.69\.166\.231|216\.58\.192\.225|118\.184\.25\.86|67\.208\.74\.71|23\.253\.126\.58|104\.239\.157\.210|175\.126\.123\.219|141\.8\.224\.221|10\.10\.10\.10|43\.229\.108\.32|103\.232\.215\.140|69\.172\.201\.153|216\.218\.185\.162|54\.225\.104\.146|103\.243\.24\.98|199\.59\.243\.120|31\.170\.160\.61|213\.19\.128\.77|62\.113\.226\.131|208\.100\.26\.234|195\.16\.127\.102|195\.16\.127\.157|34\.196\.13\.28|103\.224\.212\.222|172\.217\.4\.225|54\.72\.9\.51|192\.64\.147\.141|198\.200\.56\.183|23\.253\.164\.103|52\.48\.191\.26|52\.214\.197\.72|87\.98\.255\.18|209\.99\.17\.27|216\.38\.62\.18|104\.130\.124\.96|47\.89\.58\.141|78\.46\.211\.158|54\.86\.225\.156|54\.82\.156\.19|37\.157\.192\.102|204\.11\.56\.48|110\.34\.231\.42',ip_address)  
    except:
        return -1

    if url_match:
        return -1
    else:
        return 1

"""# Feature Extraction Final Function"""

def final(url):
  subDomain, domain, suffix = extract(url)
  hostname = subDomain + domain + suffix
  
  # Converts the given URL into standard format
  if not re.findall(r"^https?", url):
    url = "http://" + url

  # Stores the response of the given URL
  try:
      response = requests.get(url)
      soup = BeautifulSoup(response.text, 'html.parser')
  except:
      response = ""
      soup = -999
  
  if soup == -999:
    return [-1] * 30

  # Extracts global rank of the website
  try:
    global_rank = int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
  except:
    global_rank = -1
  
  return [having_IPhaving_IP_Address(url),URLURL_Length(url),Shortining_Service(url),having_At_Symbol(url), double_slash_redirecting(url), Prefix_Suffix(domain), having_Sub_Domain(hostname), SSLfinal_State(url), Domain_registration_length(url), favicon(url, soup), port(url, domain), HTTPS_token(url), Request_url(url, soup, domain), Url_of_Anchor(url, soup, domain), Links_in_tags(url, soup, domain), SFH(url, soup), Submitting_to_email(response), Abnormal_URL(response) ,Redirect(response), on_mouseover(response), RightClick(response), popUpWindow(response), Iframe(response), age_of_domain(url), DNSRecord(url), web_traffic(url), Page_Rank(global_rank), Google_Index(url), Links_pointing_to_page(response), Statical_report(url)]

"""# Model Testing"""

col = ["having_IPhaving_IP_Address",	"URLURL_Length",	"Shortining_Service",	"having_At_Symbol",	"double_slash_redirecting",	"Prefix_Suffix",	"having_Sub_Domain",	"SSLfinal_State",	"Domain_registeration_length",	"Favicon",	"port",	"HTTPS_token",	"Request_URL",	"URL_of_Anchor",	"Links_in_tags",	"SFH",	"Submitting_to_email",	"Abnormal_URL",	"Redirect",	"on_mouseover",	"RightClick",	"popUpWidnow",	"Iframe",	"age_of_domain",	"DNSRecord",	"web_traffic",	"Page_Rank",	"Google_Index",	"Links_pointing_to_page",	"Statistical_report"]

a = [[-1, -1,	1, 1, 1, -1, 0, 1, 1, 1, 1, 1, 1, -1, -1, -1, 1, 1, 0, 1, 1, 1, 1, -1, 1, 0, -1, 1, 0, 1]]
df = pd.DataFrame(a,  columns =  col)
df

test = pd.DataFrame([[-1] * 30], columns = col)
loaded_model.predict(test)

test = pd.DataFrame([final("https://rakuten.jp.wjuymvl.cn/")], columns = col)
loaded_model.predict(test)

test = pd.DataFrame([final("https://lms.wtef.talentsprint.com/login?next=/courses/course-v1%3ATS%2BWE_VC%2B2020/courseware/5398b7f9450c4f15aaebe685d9e4f611/7a94f058abd24455a92cbe77f304d959/")], columns = col)
loaded_model.predict(test)

test = pd.DataFrame([final("http://www.Confirme-paypal.com/")], columns = col)
loaded_model.predict(test)

l =[]
for n, i in enumerate(final("https://lms.wtef.talentsprint.com/login?next=/courses/course-v1%3ATS%2BWE_VC%2B2020/courseware/5398b7f9450c4f15aaebe685d9e4f611/7a94f058abd24455a92cbe77f304d959/")):
  l.append([str(i) + "-------------" + col[n]])
l

test = pd.DataFrame([final("www.google.com")], columns = col)
loaded_model.predict(test)

test = pd.DataFrame([final("https://www.facebook.com")], columns = col)
loaded_model.predict(test)