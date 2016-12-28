#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=C0103

import json

def loadData():
    with open('namedays.json', 'r') as f:
        namedays = json.loads(f.read())
    with open('holidays.json', 'r') as f:
        holidays = json.loads(f.read())
    with open('special.json', 'r') as f:
        specials = json.loads(f.read().decode('utf8'))

    out = {i:{ j:[] for j in range(1,32)} for i in range(1,13)}
    for nd_name, nd_date in namedays:
        #scribus.messageBox('',  str(a)
        nd_year, nd_month, nd_day = nd_date.split('-')
        out[int(nd_month)][int(nd_day)].extend(nd_name.split(' '))

    for nd_name, nd_date in holidays:
        nd_year, nd_month, nd_day = nd_date.split('-')
        if nd_year and nd_month and nd_day:
            out[int(nd_month)][int(nd_day)].append(nd_name)

    for nd_name, nd_date in specials:
        nd_year, nd_month, nd_day = nd_date.split('-')
        if nd_year and nd_month and nd_day:
            out[int(nd_month)][int(nd_day)].append(nd_name)

    return out

if __name__ == '__main__':
    print(loadData())

