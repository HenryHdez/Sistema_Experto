# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 21:03:32 2021

@author: hahernandez
"""

import pyodbc

cnxn = pyodbc.connect(driver='FreeTDS', 
              host='172.16.11.44\MSSQL2016DSC', 
              database='SistemaExpertoPanela', 
              user='WebSisExpPanela', 
              password='sIuusnOsE9bLlx7g60Mz')
cursor = cnxn.cursor()
print(cursor)
