#!/usr/bin/env python

#Author: Clay Shieh
#Find new changes (if any) @ http://gitlab.clayshieh.com/root/hkn-test-scraper

from bs4 import BeautifulSoup
import urllib2, urllib
from multiprocessing.dummy import Pool as ThreadPool
import os

base_dir = "tests/"
url = 'https://hkn.eecs.berkeley.edu/exams/'
base = 'https://hkn.eecs.berkeley.edu'
init_page = urllib2.urlopen(url)
soup = BeautifulSoup(init_page.read())
entries = soup.find_all('td')
classes = [(x.a.contents[0].split("-")[0].strip(), base + x.a["href"]) for x in entries]
results = []

def part1():
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    for c in classes:
        cn = c[0]
        class_dirpath = base_dir + cn
        if not os.path.exists(class_dirpath):
            os.makedirs(class_dirpath)

def part2():
    global results
    pool = ThreadPool(10) 

    def find_data(cdata):
        dirname = cdata[0]
        print "Doing: " + dirname
        url = cdata[1]
        page = urllib2.urlopen(url)
        try:
            soup = BeautifulSoup(page.read())
            semesters = soup.find_all('tr')
            labels = [x.contents[0] for x in semesters.pop(0).find_all('th')] # label row
            page_data = []
            for sem in semesters:
                row_data = []
                data = sem.find_all('td')

                for i, d in enumerate(data):
                    if i == 0:#term
                        row_data.append(d.contents[0].strip())
                    else:
                        refs = d.find_all('a')
                        #print refs
                        if refs:
                            if i == 1: # instructor name
                                row_data.append(d.a.contents[0])
                            else:
                                tmp = []
                                for a in refs:
                                    tmp.append((a.contents[0], base + a['href']))
                                row_data.append(tmp)
                        else:
                            row_data.append('None')
                base_fname = row_data.pop(0) + " - " + row_data.pop(0) + " - "
                for j, x in enumerate(labels[2:]):
                    fname = base_fname + x + " - "
                    if row_data[j] != "None":
                        for y in row_data[j]:
                            durl = y[1]
                            ffname = fname + y[0]
                            print "Downloading: " + durl
                            urllib.urlretrieve(durl, base_dir + dirname + "/" + ffname + "." + durl.split(".")[-1].strip())
            return []
            
        except Exception:
            pass
        page.close()
    results = pool.map(find_data, classes)
    pool.close() 
    pool.join() 


if __name__ == '__main__':
    part1() #creates directory tree
    part2() #downloads the files in parallel