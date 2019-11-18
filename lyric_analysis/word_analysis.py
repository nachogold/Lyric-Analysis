# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 19:44:07 2019

@author: nachogold
"""
#Now we can work directly from the data in the SQL file and do analysis
import sqlite3
from matplotlib import pyplot as plt

conn = sqlite3.connect('songwordfreq.sqlite')
cur = conn.cursor()

#Create list with Spanish stopwords
fhand=open('stopwords-es.txt','r',encoding='utf-8')
stopwords=[]
for word in fhand:
    word=word.rstrip()
    stopwords.append(word)
#Same for english stopwords
fhand=open('stopwords-en.txt','r',encoding='utf-8')
en_stopwords=[]
for word in fhand:
    word=word.rstrip()
    en_stopwords.append(word)
    
# save all words to a list and save all frequencies to another list
reg_words=[]
reg_freqs=[]
cur.execute('SELECT word FROM Word_freq_reggaeton ORDER BY frequency DESC')
for row in cur:
    reg_words.extend(row)
cur.execute('SELECT frequency FROM Word_freq_reggaeton ORDER BY frequency DESC')
for row in cur:
    reg_freqs.extend(row)

# check if word is a stopword, if not, add it to a dictionary and use indices to add the frequency as value 
reg_clean=dict()
for i in reg_words:
    if i not in stopwords:
        if i not in en_stopwords:
            reg_clean[i]=(reg_freqs[(reg_words.index(i))])

# same for tango
tan_words=[]
tan_freqs=[]
cur.execute('SELECT word FROM Word_freq_tango ORDER BY frequency DESC')
for row in cur:
    tan_words.extend(row)
cur.execute('SELECT frequency FROM Word_freq_tango ORDER BY frequency DESC')
for row in cur:
    tan_freqs.extend(row)

tan_clean=dict()
for i in tan_words:
    if i not in stopwords:
        if i not in en_stopwords:
            tan_clean[i]=(tan_freqs[(tan_words.index(i))])


# now we have two clean dictionaries (without stopwords) ready for analysis

#show new word count after cleaning
print('Word count reggaeton: ',(len(reg_clean)),'\n')

# Sort the reg_clean dictionary by value
lst = list()
for key, val in list(reg_clean.items()):
    lst.append((val, key))
lst.sort(reverse=True)
xaxis=list()
yaxis=list()
stopcounter=0
for key, val in lst:
    #limit the words shown to 25
    if stopcounter == 25: break
    else:
        xaxis.append(val)
        yaxis.append(key)
        stopcounter+=1
#use matplotlib to graph a horizontal bar chart to display word frequency
plt.rcdefaults()
fig, ax = plt.subplots()
ax.barh(xaxis, yaxis, align='center')
ax.set_yticks(xaxis)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Frequency')
ax.set_title('Reggaeton word frequency')

plt.show()


# same for Tango
print('Word count tango: ',(len(tan_clean)),'\n')

# Sort the tan_clean dictionary by value
lst = list()
for key, val in list(tan_clean.items()):
    lst.append((val, key))
lst.sort(reverse=True)
xaxis=list()
yaxis=list()
stopcounter=0
for key, val in lst:
    if stopcounter == 25: break
    else:
        xaxis.append(val)
        yaxis.append(key)
        stopcounter+=1
#use matplotlib to graph a horizontal bar chart to display word frequency
plt.rcdefaults()
fig, ax = plt.subplots()
ax.barh(xaxis, yaxis, align='center')
ax.set_yticks(xaxis)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Frequency')
ax.set_title('Tango word frequency')

plt.show()


#Show amount of words previous to cleaning - Jusst for debugging

#print('Reggaeton word count previous to cleaning:')
#cur.execute('SELECT COUNT(word) FROM Word_freq_reggaeton')
#for row in cur:
#     print(row)
#print('Tango word count previous to cleaning:')
#cur.execute('SELECT COUNT(word) FROM Word_freq_tango')
#for row in cur:
#     print(row)

cur.close()