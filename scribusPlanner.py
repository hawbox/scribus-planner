#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=C0103

import sys

try:
    # Please do not use 'from scribus import *' . If you must use a 'from import',
    # Do so _after_ the 'import scribus' and only import the names you need, such
    # as commonly used constants.
    import scribus
except ImportError as err:
    print("This Python script is written for the Scribus scripting interface.")
    print("It can only be run from within Scribus.")
    sys.exit(1)

import json
import dates

YEAR = 2017
PAPER = scribus.PAPER_A4
MARGIN = 32
nLines = 7
nSmallLines = 5
lineHeight = (PAPER[0] - (MARGIN*2))/(nLines+1)
width = PAPER[1] - (MARGIN*2)
dayTopHeight = 2*(lineHeight / (nSmallLines+3))
smallLineHeight = lineHeight / (nSmallLines+3)
xstart = MARGIN
ystart = MARGIN + dayTopHeight

def iterDayLines():
    y = ystart
    for i in range(nLines):
        xend = xstart+width
        yield (xend, y)
        y += lineHeight 



def masterPage():

    #create day lines
    scribus.createMasterPage('planner')
    scribus.editMasterPage('planner')
    for xend, y in iterDayLines():
        line = scribus.createLine(xstart, y, xend, y)
        scribus.setLineWidth(2, line)
        for j in range(nSmallLines):
            smallWidth = (width) / 2 - MARGIN
            smally = y+(j*smallLineHeight)+smallLineHeight
            smallLineL = scribus.createLine(xstart, smally, xstart+smallWidth, smally)
            smallLineR = scribus.createLine(xend-smallWidth, smally, xend, smally)

    #bonuses
    scribus.setVGuides([PAPER[1]/2])
    #txt = scribus.createText(300, 300, 100, 100)
    #scribus.setText('\x1e', txt)
    scribus.closeMasterPage()

def loadData():
    with open('namedays.json', 'r') as f:
        data = f.read()
    namedays = json.loads(data)
    out = {i:{} for i in range(1,13)}
    for nd_date, nd_name in namedays:
        nd_year, nd_month, nd_day = nd_date.split('-')
        out[nd_month][nd_day] = nd_name
    return out


def main(argv):
    """This is a documentation string. Write a description of what your code
    does here. You should generally put documentation strings ("docstrings")
    on all your Python functions."""
    #########################
    #  YOUR CODE GOES HERE  #
    #########################
    scribus.statusMessage(str(scribus.PAPER_A4))
    scribus.newDocument(scribus.PAPER_A4, #paper
                        (MARGIN, MARGIN, MARGIN, MARGIN), #margins
                        scribus.LANDSCAPE, #orientation
                        0, #firstPageNumber
                        scribus.UNIT_MILLIMETERS, #unit
                        scribus.PAGE_1, #pagesType
                        0, #firstPageOrder
                        0, #numPages
                        )
    masterPage()

    d = loadData()
    """
    We want to make pamphlet (signature) of 5 x A4 papers printed from both sides with 2 weeks on each side
    2sided 4imposition refer imposition.py
    """

    def pageFn(left, right):
        page = scribus.newPage(-1,  'planner')
        fontHeight = 20
        fontWidth = 20
        i = 0
        for xend, y in iterDayLines():
            tLeft = scribus.createText(xstart, y - fontHeight, fontWidth, fontHeight)
            scribus.setText(str(left[i]), tLeft)
            tRight = scribus.createText(xend - fontWidth, y - fontHeight, fontWidth, fontHeight)
            scribus.setText(str(right[i]), tRight)
            i += 1
    dates.forEachWeek(pageFn)


def main_wrapper(argv):
    """The main_wrapper() function disables redrawing, sets a sensible generic
    status bar message, and optionally sets up the progress bar. It then runs
    the main() function. Once everything finishes it cleans up after the main()
    function, making sure everything is sane before the script terminates."""
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        # Exit neatly even if the script terminated with an exception,
        # so we leave the progress bar and status bar blank and make sure
        # drawing is enabled.
        if scribus.haveDoc():
            scribus.setRedraw(True)
        scribus.statusMessage("")
        scribus.progressReset()

# This code detects if the script is being run as a script, or imported as a module.
# It only runs main() if being run as a script. This permits you to import your script
# and control it manually for debugging.
if __name__ == '__main__':
    main_wrapper(sys.argv)

