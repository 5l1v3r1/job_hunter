#!/usr/bin/env python3
import os, sys, time,argparse
from prettytable import PrettyTable
from urllib.request import urlopen
from bs4 import BeautifulSoup

def parse_args():
    # Create the arguments
    parser = argparse.ArgumentParser(prog='Job Hunter')
    parser.add_argument("-jt", "--jobtitle", help="Job Title. Example: -jt System Administrator/Ethical hacker/Linux System Administrator")
    parser.add_argument("-l", "--location", help="Location. Example: -l Berlin")
    parser.add_argument("-z", "--zipcode", help="Zipcode. Example: -z 3078TR")
    parser.add_argument("-i", "--interval", help="Interval to search for jobs in seconds (default: 10). Example: -i 10")
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

    #print('[i] Searching for jobs as [%s] on Indeed.nl' % jobtitle)

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

    #print('[i] Searching for jobs as [%s] on Indeed.nl on page 2' % jobtitle)

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

    #print('[i] Searching for jobs as [%s] on Stagemarkt.nl' % jobtitle)

    find_company_names = soup.find_all('div', attrs={'class': 'list__item__title'})

    for i in find_company_names:
        companies.append(i.text.strip())
        titles.append(jobtitle)
        websites.append('https://www.stagemarkt.nl')

    # Page 2
    url2 = 'https://stagemarkt.nl/Zoeken/Home/Resultaten?t=%s&s=5&z=&l=Nederland&b=False&c=&lw=&n=&pg=2&srt=&e=false&ToonOpKaart=False&ViewType=Lijst&SeedValue=0&LeerbedrijfId=0&p=%s' % (jobtitle.replace(' ', '+'), zip)
    soup = BeautifulSoup(urlopen(url2), 'html.parser')

    #print('[i] Searching for jobs as [%s] on Stagemarkt.nl on page 2' % jobtitle)

    find_company_names = soup.find_all('div', attrs={'class': 'list__item__title'})

    for i in find_company_names:
        companies.append(i.text.strip())
        titles.append(jobtitle)
        websites.append('https://www.stagemarkt.nl')

def result():
    c = len(companies)
    filepath = './log.csv'

    # Check if logfile exists, if not, create it
    if not os.path.isfile(filepath):
        with open(filepath, 'w+') as f:
            f.write('Num.,Job Title,Company,Website\n')
            f.close()
        print('[+] Created logfile at %s' % filepath)

    for i in range(len(companies)):
        result = str(c) + ')', titles[i], companies[i], websites[i]
        check = open(filepath).read()

        # If it's not a duplicate, print and save result
        if not companies[i] in check:
            c +=1
            print('%s %s %s %s' % (result[0].ljust(10), result[1].ljust(60), result[2].ljust(60), result[3].ljust(40)))
            with open(filepath, 'a+') as f:
                f.write('%s,%s,%s,%s\n' % (result[0], result[1], result[2], result[3]))
                f.close()

if not args.interval:
    interval = 5
else:
    interval = args.interval

# Run
if args.jobtitle == None or args.location == None or args.zipcode == None:
    print('[ERROR] Please give a jobtitle, location, zipcode...')
else:
    try:
        job = args.jobtitle.split('/')
        for i in job:
            print('[i] Monitoring for jobs as %s' % i)

        try:
            while True:
                for i in job:
                    search_indeed(i, args.location)
                    search_stagemarkt(i, args.zipcode)
                    result()
                time.sleep(interval)
        except KeyboardInterrupt:
            print('[i] Stopped...\n')
    except:
        print('[i] Monitoring for jobs as %s' % args.jobtitle)
        try:
            while True:
                search_indeed(args.jobtitle, args.location)
                search_stagemarkt(args.jobtitle, args.zipcode)
                result()
                time.sleep(interval)
        except KeyboardInterrupt:
            print('[i] Stopped...\n')
