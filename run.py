#!/usr/bin/env python3
import os, sys, time,argparse
from tqdm import tqdm
from prettytable import PrettyTable
from urllib.request import urlopen
from bs4 import BeautifulSoup

def parse_args():
    # Create the arguments
    parser = argparse.ArgumentParser(prog='Job Hunter')
    parser.add_argument("-jt", "--jobtitle", help="Job Title. Example: -jt System Administrator")
    parser.add_argument("-l", "--location", help="Location. Example: -l Berlin")
    parser.add_argument("-z", "--zipcode", help="Zipcode. Example: -l 3078TR")
    return parser.parse_args()

args = parse_args()

global companies
global titles
global locations
global websites
companies = []
titles = []
locations = []
websites = []

def search_indeed(jobtitle, location):
    global url1
    url1 = 'https://www.indeed.nl/jobs?q=%s&l=%s' % (jobtitle.replace(' ', '+'), location)
    soup = BeautifulSoup(urlopen(url1), 'html.parser')

    print('[i] Searching for jobs on Indeed.nl')

    find_company_names = soup.find_all('span', attrs={'class': 'company'})
    find_job_titles = soup.find_all('a', attrs={'data-tn-element': 'jobTitle'})
    find_locations = soup.find_all('span', attrs={'class': 'location'})

    for i in find_company_names:
        companies.append(i.text.strip())
        websites.append('https://www.indeed.nl')

    for i in find_job_titles:
        titles.append(i.text.strip())

    for i in find_locations:
        locations.append(i.text.strip())

    # Page 2
    url1 = 'https://www.indeed.nl/jobs?q=%s&l=%s&start=10' % (jobtitle.replace(' ', '+'), location)
    soup = BeautifulSoup(urlopen(url1), 'html.parser')

    print('[i] Searching for jobs on Indeed.nl on page 2')

    find_company_names = soup.find_all('span', attrs={'class': 'company'})
    find_job_titles = soup.find_all('a', attrs={'data-tn-element': 'jobTitle'})
    find_locations = soup.find_all('span', attrs={'class': 'location'})

    for i in find_company_names:
        companies.append(i.text.strip())
        websites.append('https://www.indeed.nl')

    for i in find_job_titles:
        titles.append(i.text.strip())

    for i in find_locations:
        locations.append(i.text.strip())

def search_stagemarkt(jobtitle, zip):
    global url2
    url2 = 'https://stagemarkt.nl/Zoeken/Home/Resultaten?t=%s&s=5&z=&l=Nederland&b=False&c=&lw=&n=&pg=1&srt=&e=false&ToonOpKaart=False&ViewType=Lijst&SeedValue=0&LeerbedrijfId=0&p=%s' % (jobtitle.replace(' ', '+'), zip)
    soup = BeautifulSoup(urlopen(url2), 'html.parser')

    print('[i] Searching for jobs on Stagemarkt.nl')

    find_company_names = soup.find_all('div', attrs={'class': 'list__item__title'})

    for i in find_company_names:
        companies.append(i.text.strip())
        titles.append(jobtitle)
        websites.append('https://www.stagemarkt.nl')

    # Page 2
    url2 = 'https://stagemarkt.nl/Zoeken/Home/Resultaten?t=%s&s=5&z=&l=Nederland&b=False&c=&lw=&n=&pg=2&srt=&e=false&ToonOpKaart=False&ViewType=Lijst&SeedValue=0&LeerbedrijfId=0&p=%s' % (jobtitle.replace(' ', '+'), zip)
    soup = BeautifulSoup(urlopen(url2), 'html.parser')

    print('[i] Searching for jobs on Stagemarkt.nl on page 2')

    find_company_names = soup.find_all('div', attrs={'class': 'list__item__title'})

    for i in find_company_names:
        companies.append(i.text.strip())
        titles.append(jobtitle)
        websites.append('https://www.stagemarkt.nl')

table = PrettyTable(['Num.', 'Job Title', 'Company', 'Website']) # Header
table.align = "l" # Text Align left

# Run
if args.jobtitle == None or args.location == None or args.zipcode == None:
    print('[ERROR] Please give a jobtitle, location, zipcode...')
else:
    search_indeed(args.jobtitle, args.location)
    search_stagemarkt(args.jobtitle, args.zipcode)
    c = 0

    for i in range(len(companies)):
        c +=1
        result = int(c), titles[i], companies[i], websites[i]
        table.add_row([result[0], result[1], result[2], result[3]])
    print(table)
    print('Found %i jobs\n' % len(companies))

    print('Source:')
    print('Indeed URL: %s' % url1)
    print('Stagemarkt URL: %s' % url2)
