import datetime
import itertools

YEAR = 2017
N_PAPERS_IN_SIGNATURE = 5
N_DAYS_IN_WEEK = 7
N_PAGES_ON_PAPER = 2
N_WEEKS_ON_PAGE = 2
N_WEEKS_ON_PAPER = N_PAPERS_IN_SIGNATURE * N_PAGES_ON_PAPER * N_WEEKS_ON_PAGE
def forEachWeek(pageFn):
    daysOnPage = N_WEEKS_ON_PAGE * N_DAYS_IN_WEEK #14
    daysOnPaper = N_PAGES_ON_PAPER * daysOnPage #24
    daysInSignature = N_PAPERS_IN_SIGNATURE * daysOnPaper
    for signatureI in grouper(daysInSignature, iterYearDates(YEAR)):
        print(signatureI, len(signatureI))
        def sn(i):
            return signatureI[(i-1)*7:i*7]

        for p1,p2,p3,p4 in iterImposition():
            pageFn(sn(p4), sn(p1))
            pageFn(sn(p2), sn(p3))
        print()

def grouper(n, iterable):
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, n))
       if not chunk:
           return
       yield chunk

def iterImposition():
    for p in range(N_PAPERS_IN_SIGNATURE):
        p1 = p*2 + 1
        p4 = N_WEEKS_ON_PAPER - (p * 2)

        p2 = p1 + 1
        p3 = p4 - 1
        yield( (p1,p2,p3,p4) )


def iterYearDates(year):
    #from SamAgenda script because its smart way to do it
    date = datetime.date(year, 1,1)
    date -= datetime.timedelta(days = date.weekday() % 7)
    tdDay = datetime.timedelta(days=1)
    for i in range(371): # 53 weeks
        yield date
        date += tdDay


if __name__ == '__main__':
    def f(left, right):
        print('left', left)
        print('right', right)

    forEachWeek(f)
