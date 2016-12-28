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

import dates
import data

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

def mm(d):
    m = {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'Máj',
        6: 'Jún',
        7: 'Júl',
        8: 'Aug',
        9: 'Sep',
        10:'Okt',
        11:'Nov',
        12:'Dec'
    }
    return m[d.month]

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
    #scribus.messageBox('', str(scribus.getAllStyles()))
    scribus.closeMasterPage()



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
    scribus.createCharStyle('date1', 'Athelas Bold', 45)
    scribus.createCharStyle('month1', 'Athelas Bold', 16)
    scribus.createCharStyle('name1', 'Athelas Regular', 16)
    scribus.createParagraphStyle('dateL', alignment=scribus.ALIGN_LEFT, charstyle='date1')
    scribus.createParagraphStyle('monthL', alignment=scribus.ALIGN_LEFT, charstyle='month1')
    scribus.createParagraphStyle('nameL', alignment=scribus.ALIGN_LEFT, charstyle='name1')
    scribus.createParagraphStyle('dateR', alignment=scribus.ALIGN_RIGHT, charstyle='date1')
    scribus.createParagraphStyle('monthR', alignment=scribus.ALIGN_RIGHT, charstyle='month1')
    scribus.createParagraphStyle('nameR', alignment=scribus.ALIGN_RIGHT, charstyle='name1')
    masterPage()

    d = data.loadData()
    """
    We want to make pamphlet (signature) of 5 x A4 papers printed from both sides with 2 weeks on each side
    2sided 4imposition refer imposition.py
    """

    def pageFn(left, right):
        page = scribus.newPage(-1,  'planner')
        i = 0
        sizeDate = (20, 15)
        sizeMonth = (20, 7)
        sizeName = (290, 7)
        for xend, y in iterDayLines():
            try:
                tLeftDate = left[i]
                posLeftDate = (xstart, y - sizeDate[1])
                posLeftMonth = (xstart + sizeDate[0], y - sizeDate[1])
                posLeftName = (xstart + sizeDate[0], y - sizeName[1])
                tLeftName = ', '.join(d[tLeftDate.month][tLeftDate.day])
                objLeftDate = scribus.createText(*posLeftDate+sizeDate)
                objLeftMonth = scribus.createText(*posLeftMonth+sizeMonth)
                objLeftName = scribus.createText(*posLeftName+sizeName)
                scribus.setText(tLeftDate.strftime('%d'), objLeftDate)
                scribus.setText(mm(tLeftDate), objLeftMonth)
                scribus.setText(tLeftName, objLeftName)
                scribus.setStyle('dateL', objLeftDate)
                scribus.setStyle('monthL', objLeftMonth)
                scribus.setStyle('nameL', objLeftName)
            except IndexError:
                pass


            try:
                posRightDate = (xend - sizeDate[0], y - sizeDate[1])
                posRightMonth = (xend - sizeDate[0] - sizeMonth[0], y - sizeDate[1])
                posRightName = (xend - sizeDate[0] - sizeName[0], y - sizeName[1])
                tRightDate = right[i]
                tRightName = ', '.join(d[tRightDate.month][tRightDate.day])
                objRightDate = scribus.createText(*posRightDate+sizeDate)
                objRightMonth = scribus.createText(*posRightMonth+sizeMonth)
                objRightName = scribus.createText(*posRightName+sizeName)
                scribus.setText(tRightDate.strftime('%d'), objRightDate)
                scribus.setText(mm(tRightDate), objRightMonth)
                scribus.setText(tRightName, objRightName)
                scribus.setStyle('dateR', objRightDate)
                scribus.setStyle('monthR', objRightMonth)
                scribus.setStyle('nameR', objRightName)
            except IndexError:
                pass
            i += 1
    dates.forEachWeek(pageFn)
    scribus.deletePage(1)


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

