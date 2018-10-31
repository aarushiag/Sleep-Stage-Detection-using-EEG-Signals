# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 23:23:48 2018

@author: AARUSHI"""
import csv
file = open('30secepoch1.csv','w')
writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
with open('SC4012EC-Hypnogram_data_annotations.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        print(row)
        if(line_count>0):
            dur =int(row[1])
            print(dur)
            while(dur>0):                
                writer.writerow([row[0],'30',row[2]])
                print([row[0],'30',row[2]])
                dur = dur-30
        line_count+=1