import sys
import re

def phase1Func(f,fterms, fpdates, fprices, fads):
    for i in range(2):
        f.readline()
    while True:
        line = f.readline()
        if line.strip() == '</ads>':
            break
        else:
            aid = FuncCutStr(line, 'aid')
            # print(aid)
            ti = FuncCutStr(line, 'ti')
            for term in filter(ti):
                fterms.write(term + ':' + aid + '\n')
            desc = FuncCutStr(line, 'desc')
            for term in filter(desc):
                fterms.write(term + ':' + aid + '\n')
            
            date = FuncCutStr(line, 'date')
            cat = FuncCutStr(line, 'cat')
            loc = FuncCutStr(line, 'loc')
            price = FuncCutStr(line, 'price')
            fpdates.write(date + ':' + aid + ',' + cat + ',' + loc + '\n')
            fprices.write(price.rjust(12) + ':' + aid + ',' + cat + ',' + loc + '\n')

            ad = FuncCutStr(line, 'ad')
            fads.write(aid + ':' + ad + '\n')
    return

def FuncCutStr(line, key):
    return line.split('</'+key+'>')[0].split('<'+key+'>')[1]

def filter(term):
    term = term.replace('&apos;', ' ').replace('&quot;', ' ').replace('&amp;', ' ')
    term = re.sub(r'[&][#][0-9]+[;]','', term)
    
    format = 'abcdefghijklmnopqrstuvwxyz0123456789-_'
    term = term.lower()
    for c in term:
        if not c in format:
            term = term.replace(c, ' ')

    returnList = []
    terms = term.split(' ')
    for t in terms:
        t = t.strip()
        if len(t) > 2:
            returnList.append(t)
    
    return returnList


def main(path):
    path = './' + path
    f = open(path, 'r')
    fterms = open('terms.txt', 'w')
    fpdates = open('pdates.txt', 'w')
    fprices = open('prices.txt', 'w')
    fads = open('ads.txt', 'w')
    phase1Func(f, fterms, fpdates, fprices, fads)

    fterms.close()
    fpdates.close()
    fprices.close()
    fads.close()

main(sys.argv[1])

