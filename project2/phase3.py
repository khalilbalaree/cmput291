from bsddb3 import db
import re
import sys
import time
from datetime import datetime
from datetime import timedelta

database1 = None
database2 = None
database3 = None
database4 = None

curse1 = None
curse2 = None
curse3 = None
curse4 = None

def createDB():
    global database1, database2, database3, database4
    global curse1, curse2, curse3, curse4

    database1 = db.DB()
    #database1.set_flags(db.DB_DUP)
    database1.open("ad.idx", None, db.DB_HASH, db.DB_CREATE)
    curse1 = database1.cursor()
    '''iter = curse1.first()
    while iter:
        print(iter)
        iter = curse1.next()'''


    database2 = db.DB()
    database2.set_flags(db.DB_DUP)
    database2.open("da.idx", None, db.DB_BTREE, db.DB_CREATE)
    curse2 = database2.cursor()
    '''
    iter = curse2.first()
    for i in range(1,10000):
        print(iter)
        iter = curse2.next()'''

    database3 = db.DB()
    database3.set_flags(db.DB_DUP)
    database3.open("pr.idx", None, db.DB_BTREE, db.DB_CREATE)
    curse3 = database3.cursor()


    database4 = db.DB()
    database4.set_flags(db.DB_DUP)
    database4.open("te.idx", None, db.DB_BTREE, db.DB_CREATE)
    curse4 = database4.cursor()



def closeDB():
    global database1, database2, database3, database4
    global curse1, curse2, curse3,curse4

    curse1.close()
    database1.close()
    curse2.close()
    database2.close()
    curse3.close()
    database3.close()
    curse4.close()
    database4.close()

def userChoice():
    query = input("input: ").lower()
    if query == '':
        exit("Exiting program...")
    querys = convert(query)
    result = evaluateQuerys(querys)
    if result == False:
        exit("Exiting program...")
    full = False
    showAds(result, full)
    while True:
        choice = input("Brief or Full or Exit? ")
        if choice == "output=full":
            showAds(result, True)
        elif choice == "output=brief":
            showAds(result, False)
        elif choice == "exit":
            exit("Exiting program...")
        else:
            print("I can't understand this.")
            
def stripFunc(_str,line):
    res = line.split(_str)
    output = ""
    for i in range(len(res)):
        if i == 0:
            output += res[i]
        else:
            r = res[i].lstrip()
            output += _str + r
    return output

def convert(line):
    _list = ["date","price","cat","location","=","<",">"]
    for _str in _list:
        lineNew = stripFunc(_str, line)
        line = lineNew
    out = []
    line = line.split(" ")
    for li in line:
        if li != "":
            out.append(li)
    # print(out)
    return out

def initializeDicts(dictStoreLocation,dictStoreCategory):
    output = []
    minMoney = curse3.first()[0]
    result = curse3.set(minMoney)
    output.append(result[1].decode("utf-8"))
    while True:
        try:
            ne = curse3.next()
            output.append(ne[1].decode("utf-8"))
        except:
            break
    for each in output:
        newEach = each.split(',')
        if newEach[0] in dictStoreCategory:
            pass
        else:
            dictStoreCategory[newEach[0]] = newEach[1]
        if newEach[0] in dictStoreLocation:
            pass
        else:
            dictStoreLocation[newEach[0]] = newEach[2]

def evaluateQuerys(querys):
    locationSearchControl = True
    categorySearchControl = True
    result = {}
    dictStoreLocation = {}
    dictStoreCategory = {}
    #initializeDicts(dictStoreLocation,dictStoreCategory)
    # print(len(querys))
    numOfQuerys = len(querys)

    for query in querys:
        output = None
        '''
        if each == "output=full":
            full = True
            count -= 1
            continue
        elif each == "output=key":
            full = False
            count -= 1
            continue'''
        r'''\s*(=|>|<|>=|<=)\s*\d{4}/\d{1,2}/\d{1,2}'''
        if re.match(r"\Adate(=|>|<|>=|<=)\d{4}/\d{1,2}/\d{1,2}\Z",query):
            locationSearchControl =False
            categorySearchControl = False
            # print("date query matched!")
            queryStripted = query.strip("date")
            output = QueryByDate(queryStripted)
        elif re.match(r"\Aprice(=|>|<|>=|<=)\d*\Z",query):
            locationSearchControl =False
            categorySearchControl = False
            # print("price query matched")
            queryStripted = query.strip("price")
            output = QueryByPrice(queryStripted)
        elif re.match(r"\Alocation(=)[0-9a-zA-Z_-]*\Z",query):
            #special case can not directly search in database
            if locationSearchControl:
                #when first time we search location, we might not have any keys 
                #then put he query at very back, we seach the querys have keys
                querys.append(query)
                locationSearchControl = False
                continue
            else:
                #means this is the second time we search location
                queryStripted = query.split("=")[1]
                if not dictStoreLocation:
                    output = QueryByLocationSlow(queryStripted)
                else:
                    output = QueryByLocation(queryStripted,dictStoreLocation)
                    # print("location query matched")
        elif re.match(r"\Acat(=)[0-9a-zA-Z_-]*\Z",query):
            #special case can not directly search in database
            if categorySearchControl:
                querys.append(query)
                categorySearchControl = False
                continue
            else:
                 #means this is the second time we search category
                queryStripted = query.split("=")[1]
                if not dictStoreCategory:
                    output = QueryByCategorySlow(queryStripted)
                else:
                    
                    output = QueryByCategory(queryStripted,dictStoreCategory)
                    # print("category query matched")

        elif re.match(r'\A[0-9a-zA-Z_-]*\Z',query):
            # print("key words all matched!!!")
            output = QueryByKeyWord(query.lower(), True)
        elif re.match(r'\A[0-9a-zA-Z_-]*[%]\Z',query):
            # print("key words all matched with %!!!!")
            output = QueryByKeyWord(query.lower(), False)
        else:
            print("Incorrect format!")
            return False


        #save the output for each query
        if len(output) == 0:
            '''if len(sys.argv) == 3:
                outfile.write("Your grammar is not correct\n")
            else:'''
            print("No result found!")
            return False
        # print(len(output))
        for each in output:
            #only get the id, and store others in other dictionary
            newEach = each.split(',')
            # print(newEach)
            # print(newEach)
            if newEach[0] in result:
                result[newEach[0]] += 1
            else:
                result[newEach[0]] = 1

            if len(newEach) >1:
                #output are from date and price query
                if newEach[0] in dictStoreCategory:
                    pass
                else:
                    dictStoreCategory[newEach[0]] = newEach[1]
                if newEach[0] in dictStoreLocation:
                    pass
                else:
                    dictStoreLocation[newEach[0]] = newEach[2]
    # print(dictStoreCategory)
    # print(dictStoreLocation)
    return getFinalResult(result,numOfQuerys)


def QueryByPrice(queryStripted):
    output = []
    maxMoney = curse3.last()[0].decode("utf-8")
    if queryStripted[1] == "=":
        operator = queryStripted[0:2]
        numberOfMoney = queryStripted[2:]
    else:
        operator = queryStripted[0]
        numberOfMoney = queryStripted[1:]

    # for each operator choose the data from coressponding files
    #fill with space
    numberOfMoney = numberOfMoney.rjust(12)
    if operator == "=":
        numberOfMoney = numberOfMoney.encode("utf-8")
        try:
            result = curse3.set(numberOfMoney)
            output.append(result[1].decode("utf-8"))
        except:
            return output
        while True:
            try:
                ne = curse3.next()
                if ne[0] != numberOfMoney:
                    return output
                output.append(ne[1].decode("utf-8"))
            except:
                return output
    if operator == ">":
        numberOfMoney = str(int(numberOfMoney)+1)
        numberOfMoney = numberOfMoney.rjust(12)
        numberOfMoney = numberOfMoney.encode("utf-8")
        while True:
            try:
                result = curse3.set(numberOfMoney)
                output.append(result[1].decode("utf-8"))
                break
            except:
                if int(numberOfMoney.decode("utf-8")) > int(maxMoney):
                    return output
                numberOfMoney = str(int(numberOfMoney.decode("utf-8")) + 1)
                numberOfMoney = numberOfMoney.rjust(12)
                numberOfMoney = numberOfMoney.encode("utf-8")
        while True:
            try:
                ne = curse3.next()
                output.append(ne[1].decode("utf-8"))
            except:
                return output
    if operator == "<":
        result = curse3.first()
        while result[0].decode("utf-8") == '':
            numberOfMoney = numberOfMoney.encode("utf-8")
            if int(result[0].decode("utf-8")) >= int(numberOfMoney.decode("utf-8")):
                return output
            numberOfMoney = numberOfMoney.encode("utf-8")
            result = curse3.next()
        numberOfMoney = numberOfMoney.encode("utf-8")
        if int(result[0].decode("utf-8")) >= int(numberOfMoney.decode("utf-8")) :
            return output
        output.append(result[1].decode("utf-8"))
        while True:
            try:
                ne = curse3.next()
                if ne[0] >= numberOfMoney:
                    return output                
                output.append(ne[1].decode("utf-8"))
            except:
                return output  
    if operator == ">=":
        numberOfMoney = numberOfMoney.encode("utf-8")
        while True:
            try:
                result = curse3.set(numberOfMoney)
                output.append(result[1].decode("utf-8"))
                break
            except:
                if int(numberOfMoney.decode("utf-8")) > int(maxMoney):
                    return output
                numberOfMoney = str(int(numberOfMoney.decode("utf-8")) + 1)
                numberOfMoney = numberOfMoney.rjust(12)
                numberOfMoney = numberOfMoney.encode("utf-8")
        while True:
            try:
                ne = curse3.next()
                output.append(ne[1].decode("utf-8"))
            except:
                return output
    if operator == "<=":
        result = curse3.first()
        while result[0].decode("utf-8") == '':
            numberOfMoney = numberOfMoney.encode("utf-8")
            if int(result[0].decode("utf-8")) > int(numberOfMoney.decode("utf-8")) :
                return output
            output.append(result[1].decode("utf-8"))
            result = curse3.next()
        numberOfMoney = numberOfMoney.encode("utf-8")
        if int(result[0].decode("utf-8")) > int(numberOfMoney.decode("utf-8")):
            return output
        output.append(result[1].decode("utf-8"))
        while True:
            try:
                ne = curse3.next()
                if ne[0] > numberOfMoney:
                    return output                
                output.append(ne[1].decode("utf-8"))
            except:
                return output  
    #print(operator,numberOfMoney,output)
    return output

def QueryByDate(queryStripted):
    maxDate = curse2.last()[0].decode("utf-8")
    date = queryStripted[-10:]
    output = []
    if len(queryStripted) == 11:
        operator = queryStripted[0]
    elif len(queryStripted) == 12:
        operator = queryStripted[0:2]
    else:
        return output
    
    #for each operator choose the data from coressponding files
    if operator == "=":
        date = date.encode("utf-8")
        try:
            result = curse2.set(date)
            output.append(result[1].decode("utf-8"))
        except:
            return output
        while True:
            try:
                ne = curse2.next()
                if ne[0] != date:
                    return output
                output.append(ne[1].decode("utf-8"))
            except:
                return output
    if operator == ">":
        tempDatetime = datetime.strptime(date,"%Y/%m/%d")
        tempDatetime = tempDatetime+ timedelta(days=1)
        tempDate = tempDatetime.strftime("%Y/%m/%d")
        date = tempDate.encode("utf-8")
        while True:
            try:
                result = curse2.set(date)
                output.append(result[1].decode("utf-8"))
                break
            except:
                tempDate = date.decode("utf-8")
                tempDatetime = datetime.strptime(tempDate,"%Y/%m/%d")
                maxDateTime = datetime.strptime(maxDate,"%Y/%m/%d")
                if tempDatetime > maxDateTime:
                    return output
                tempDatetime = tempDatetime+ timedelta(days=1)
                tempDate = tempDatetime.strftime("%Y/%m/%d")
                date = tempDate.encode("utf-8")
        while True:
            try:
                ne = curse2.next()
                output.append(ne[1].decode("utf-8"))
            except:
                return output
    if operator == ">=":
        date = date.encode("utf-8")
        while True:
            try:
                result = curse2.set(date)
                output.append(result[1].decode("utf-8"))
                break
            except:
                tempDate = date.decode("utf-8")
                tempDatetime = datetime.strptime(tempDate,"%Y/%m/%d")
                maxDateTime = datetime.strptime(maxDate,"%Y/%m/%d")
                if tempDatetime > maxDateTime:
                    return output
                tempDatetime = tempDatetime+ timedelta(days=1)
                tempDate = tempDatetime.strftime("%Y/%m/%d")
                date = tempDate.encode("utf-8")
        while True:
            try:
                ne = curse2.next()
                output.append(ne[1].decode("utf-8"))
            except:
                return output
    if operator == "<":
        result = curse2.first()
        while result[0].decode("utf-8") == '':
            date = date.encode("utf-8")
            if result[0].decode("utf-8") >= date.decode("utf-8") :
                return output
            date = date.decode("utf-8")
            result = curse2.next()
        date = date.encode("utf-8")
        if result[0].decode("utf-8") >= date.decode("utf-8"):
            return output
        output.append(result[1].decode("utf-8"))
        while True:
            try:
                ne = curse2.next()
                if ne[0] >= date:
                    return output                
                output.append(ne[1].decode("utf-8"))
            except:
                return output  
    if operator == "<=":
        result = curse2.first()
        while result[0].decode("utf-8") == '':
            date = date.encode("utf-8")
            if result[0].decode("utf-8") > date.decode("utf-8") :
                return output
            date = date.decode("utf-8")
            result = curse2.next()
        date = date.encode("utf-8")
        if result[0].decode("utf-8") > date.decode("utf-8"):
            return output
        output.append(result[1].decode("utf-8"))
        while True:
            try:
                ne = curse2.next()
                if ne[0] > date:
                    return output                
                output.append(ne[1].decode("utf-8"))
            except:
                return output  

        
    #other operators...

def QueryByLocation(queryStripted,dictStoreLocation):
    output = []
    location = queryStripted
    thisDictStoreLocation = dictStoreLocation
    for key, value in thisDictStoreLocation.items():
        if value.lower() == location:
            output.append(key)
    return output

def QueryByCategory(queryStripted,dictStoreCategory):
    output = []
    category = queryStripted
    thisDictStoreCategory = dictStoreCategory
    for key, value in thisDictStoreCategory.items():
        if value.lower() == category:
            output.append(key)
    return output


def QueryByLocationSlow(queryStripted):
    output = []
    location = queryStripted
    iter = curse3.first()[1].decode("utf-8")
    while iter:
        iter = iter.split(",")
        # print(iter[2],location)
        if iter[2].lower() == location:
            output.append(iter[0])
        iter = curse3.next()
        if iter != None:
            iter = iter[1].decode("utf-8")
    return output

def QueryByCategorySlow(queryStripted):
    output = []
    category = queryStripted
    iter = curse3.first()[1].decode("utf-8")
    while iter:
        iter = iter.split(",")
        # print(iter[1],category)
        if iter[1].lower() == category:
            output.append(iter[0])
        iter = curse3.next()
        if iter != None:
            iter = iter[1].decode("utf-8")
    return output


def QueryByKeyWord(queryStripted, isExactSearch):
    # print(queryStripted)
    terms = []
    if not isExactSearch:
        keyword = queryStripted.strip("%")
        iter = curse4.first()
        while iter:
            if iter[0].decode("utf-8").startswith(keyword):
                if iter[1].decode("utf-8") not in terms:
                    terms.append(iter[1].decode("utf-8"))
            iter = curse4.next()
                
    else:
        keyword = queryStripted.encode("utf-8")
        iter = curse4.set(keyword)
        while iter:
            if iter[0].decode("utf-8") == queryStripted:
                if iter[1].decode("utf-8") not in terms:
                    terms.append(iter[1].decode("utf-8"))
            iter = curse4.next()
            if iter == None:
                break
    return terms


def getFinalResult(_list, numOfQuerys):
    printList = []
    # print(numOfQuerys)
    for id, count in _list.items():
        if count == numOfQuerys:
            printList.append(id)
    return printList

def showAds(result,full):
    if full:
        for res in result:
            iter = curse1.set(res.encode("utf-8"))
            print(res+" : "+iter[1].decode("utf-8"))
    else:
        for res in result:
            iter = curse1.set(res.encode("utf-8"))
            ad = iter[1].decode("utf-8")
            title = ad.split('</ti>')[0].split('<ti>')[1]
            print(res+" : "+title)
    # print(len(result))

def main():
    print(db.__version__)
    print(db.version())
    createDB()
    userChoice()
    closeDB()

if __name__ == "__main__":
    main()
