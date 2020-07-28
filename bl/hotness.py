import bl.gettime as gettime

def _coldDown(hotness):
    rest=101-hotness
    return hotness-rest*rest*0.000725

def _cap0_100(i):
    if i<0:
        return 0
    elif i>100:
        return 100
    return i

def _fliterUser(oldrecords,uid,fromDate,toDate):
    records=[]
    for r in oldrecords:
        if r.uid==uid and (fromDate is None or r.date>fromDate) and (toDate is not None and r.date<=toDate):
            records.append(r)
    return records

def _fliterDateAndSortRecords(oldrecords,fromDate,toDate):
    if  toDate is None or (fromDate is not None and  fromDate > toDate):
        return None
    records=[]
    for r in oldrecords:
        theDay=r.time.date()
        if (fromDate is None or theDay>=fromDate) and theDay<=toDate:
            records.append(r)
    sortedRecords=sorted(records, key=lambda record: record.time, reverse=True)
    return sortedRecords

def _uionfyAndReverse(sortedRecords):
    theDate=None
    finalList=[]
    for sr in sortedRecords:
        thisDate=sr.time.date()
        if theDate==thisDate:
            item=finalList[0]
            if 0!=sr.tag:
                if 0!=item['tag']:
                    pass
                else:
                    item['tag']=sr.tag
                if -1==sr.tag:
                    break
        else:
            finalList.insert(0,{
                "date":thisDate,
                "tag":sr.tag,
            })
            theDate=thisDate
    return finalList

def _calculateHotness(base,finalList,toDate):

    hotness=None
    fromDate=None
    if base is None :
        if 0==len(finalList):
            return -1
        else:
            hotness=0
            fromDate=finalList[0]['date']
    else:
        if toDate is None or base['date']>toDate:
            return None
        else:
            if len(finalList)>0 and finalList[0]['date']<base['date']:
                return None
            hotness=base['hotness']
            fromDate=base['date']

    dateIndex=fromDate
    oneDay=gettime.OneDay()

    while dateIndex<=toDate:
        hotness=_cap0_100(_coldDown(hotness))
        if len(finalList)>0:
            if finalList[0]['date']==dateIndex:
                tag=finalList.pop(0)['tag']
                if 0==tag:
                    hotness=_cap0_100(hotness+20)
                elif -1==tag:
                    hotness=0
                elif 1==tag:
                    hotness=_cap0_100(hotness+50)
        dateIndex+=oneDay
    return hotness

def _getHotness(oldrecords,toDate):
    sortedRecords=_fliterDateAndSortRecords(oldrecords,None,toDate)
    if sortedRecords is None:
        return -1
    finalList=_uionfyAndReverse(sortedRecords)
    return _calculateHotness(None,finalList,toDate)


def _getHotnessWithBase(oldrecords,toDate,base):
    sortedRecords=_fliterDateAndSortRecords(oldrecords,base['date'],toDate)
    if sortedRecords is None:
        return None
    finalList=_uionfyAndReverse(sortedRecords)
    return _calculateHotness(base,finalList,toDate)

def GetWordHotness(word,user,toDate):
    lastHots=word.lastHots
    theLH=None
    for lh in lastHots:
        if lh.uid==user.id:
            theLH=lh
            break
    if theLH is not None:
        records=_fliterUser(word.Records,user.id,user.lasthotdate,toDate)
        return _getHotnessWithBase(
            records,toDate,{
            'date':user.lasthotdate,
            'hotness':theLH.hotness})
    else:
        records=_fliterUser(word.Records,user.id,None,toDate)
        return _getHotness(records,toDate)
 

def HotnessWithoutBase(oldrecords,toDate):
    return _getHotness(oldrecords,toDate)

def HotnessWithBase(oldrecords,toDate,base):
    return _getHotnessWithBase(oldrecords,toDate,base)