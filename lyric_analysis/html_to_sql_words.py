# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 11:05:52 2019

@author: nachogold
"""
#This file extracts the lyrics of several songs from letras.com
#By introducing the link to a genre, the program crawls through an specified number of songs
#Then, writes the word frequency of those songs (word and times it was used) to a SQL table
#This makes it easier to access the data by having it stored in the computer
#You can change the parameters to adjust the amount of songs parsed and the genre
#Then, use word_analysis.py to analyze the data, reading it directly from the SQL DB file

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import string
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#SONG LINKS FINDER
#This part allows us to gather all song links appearing in the genreurl (the genre of our choice) and save 
# a specified amount (chosen using song_quant_counter at the end of the for) to the songlinks list
#This list will then be gone through with a for loop, to enter each song link and save its lyrics in the following part

genreurl = ('https://www.letras.com/mais-acessadas/tango/')
html = urllib.request.urlopen(genreurl, context=ctx).read()
links = re.findall(b'href="(/.*?)"', html)
#we will save only the song links in songlinks, excluding all previous
#we then can tweak our for loop to go through a number of items (songs) in songlinks
songlinks=[]
count=0
song_quant_counter=0
for link in links:
    link=link.decode()
    if link == '/mais-acessadas/zouk/':
        count+=1
        continue
    if count == 1:
        count+=1
        continue
    if count == 2:
        full_link=('https://www.letras.com'+link)
        songlinks.append(full_link)
        song_quant_counter+=1
    #Below we can choose the amount of song links to save (I believe the site shows 1.000 songs)
    if song_quant_counter == 100:
        break



#LYRICS AND WORD FINDER
#Now, using the songlinks list we go through it, parsing the lyrics to each song and 
#saving the words to then calculate the frequency
        
#we create wordcounts, a dictionary that will store all the words from all songs and the amounts of time they appear
wordcounts=dict()
for songlink in songlinks:
    url = songlink
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve song lyrics. We retrieve all the paragraphs that contain lyrics (excluding the ones at the end that don't)
    #Save all the lyrics to the lyrics list
    tags = soup('p')
    lyrics=(tags[:-3])
    lyrics_words=[]
    for i in lyrics:
        a=i.decode()
        #in variable b we delete all HTML tags, set to lower case, delete punctuation (including spanish punctuation like ¿,¡), changing 'yeh' to 'yeah' (more changes like these could be added) and strip, so our string lines are ready to be split into words
        b =(a.replace('<br>',' ')).replace('<br/>',' ').replace('</br>',' ').replace('<br>',' ').replace('<p>','').replace('</p>','').replace('¿','').replace('¡','').replace('yeh','yeah').lower().translate(str.maketrans('', '', string.punctuation)).strip()
        #now that our text is parsed and cleaned, we split b into a list of words
        words=b.split()
        lyrics_words.extend(words)
    for word in lyrics_words:
        wordcounts[word] = wordcounts.get(word, 0) + 1




#WRITING THE DATA TO A SQL TABLE

#Now we need to write this data (the dictionary wordcounts) to a sql table, so we can then access that information without the need to use the internet
#For this we create a DB and a table and iterate through each word in the dictionary wordcounts, writing the key and its value to the Table
#We then print the table sorting by the word frequency            

import sqlite3

#to automatically name our table and prevent from overwriting one table with data from a different genre we use
#genreurl to get the genre (the last part of the url) and then use it every time we mention the table name
genrename=genreurl.split('/')
if genrename[-1] == '':
    genrename=str(genrename[-2])
else:
    genrename=str(genrename[-1])


conn = sqlite3.connect('songwordfreq.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Word_freq_'+genrename)
cur.execute('CREATE TABLE Word_freq_'+genrename+' (word TEXT, frequency INTEGER)')

for key in wordcounts:
    cur.execute('INSERT INTO Word_freq_'+genrename+' (word, frequency) VALUES (?, ?)', 
                (key, wordcounts[key]))
    conn.commit()

print('Word frequency:')
cur.execute('SELECT word, frequency FROM Word_freq_'+genrename+' ORDER BY frequency DESC LIMIT 25')
for row in cur:
     print(row)

cur.close()