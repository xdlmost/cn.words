import dao.dbinterface as bi
def GetWord(qword):
    return bi.queryWord(qword)

def getWordByLevel(qlevel,qindex):
    return bi.queryWordByLevel(qlevel,qindex)


def getNextWordByLevel(qlevel,qindex):
    from dao.models import Word
    word=bi.queryWordByLevel(qlevel,qindex+1)
    if word is None:
        word=bi.queryWordByLevel(qlevel+1,1)
    return word

def getNextWordByLevelWithHotness(uid,qlevel,qindex):
    word=getNextWordByLevel(qlevel,qindex)
    if word is not None:
        appendHotnessInfo(uid,word)
    return word

def getPreWordByLevel(qlevel,qindex):
    from dao.models import Word
    word=bi.queryWordByLevel(qlevel,qindex-1)
    if word is None:
        word=bi.queryWordByLevel(qlevel-1,250)
    return word

def getPreWordByLevelWithHotness(uid,qlevel,qindex):
    word=getPreWordByLevel(qlevel,qindex)
    if word is not None:
        appendHotnessInfo(uid,word)
    return word

def allWord():
    words=bi.queryAllWords()
    return words

def allWordWithHotness(uid):
    words=allWord()
    for w in words:
        w.hotness=appendHotnessInfo(uid,w)
    return words

def _getWordRecordInfo(word,uid):
    info={
        'all':0,
        'yes':0,
        'no':0,
        'explore':0,
        'plan':0,
        'review':0,
        'query':0,
        'list':[]
    }
    sortedRecords=sorted(word.Records, key=lambda record: record.time)
    for r in sortedRecords:
        if r.uid==uid:
            if r.tag==1:
                info['yes']+=1
            elif r.tag==-1:
                info['no']+=1
            
            info[r._from]+=1
            info['all']+=1
            info['list'].append(r)
    return info

def _appendTagFlag(user,word,atDate):
    records=word.Records
    for r in records:
        if r.date==atDate and r.uid==user.id:
            if word.tagFlag is None:
                word.tagFlag=r.tag
            else:
                if word.tagFlag==0 and r.tag!=0:
                    word.tagFlag=r.tag
                if word.tagFlag!=0:
                    break

def _appendPlanFlag(user,word,atDate):
    plans=word.plans
    for p in plans:
        if p.date==atDate and p.uid==user.id:
            word.planFlag=p.learned
            break

def AppendSingleWordWithSimpleInfo(user,word):
    from bl.hotness import GetWordHotness
    from bl.gettime import Today
    today=Today()
    word.hotness=round(GetWordHotness(word,user,today),2)
    _appendTagFlag(user,word,today)
    _appendPlanFlag(user,word,today)

def AppendSingleWordWithFullInfo(user,word,fromSys,count=None,index=None,reviewDate=None):
    from bl.wordaction import appendRecord

    record=appendRecord(user.id,word,fromSys)
    AppendSingleWordWithSimpleInfo(user,word)
    navi=None
    if 'plan'==fromSys:
        from bl.wordnavi import naviFromPlan
        navi=naviFromPlan(user.id,word,record,count,index)
    elif 'query'==fromSys:
        from bl.wordnavi import naviFromQuery
        navi=naviFromQuery(user.id,word,record)
    elif 'explore'==fromSys:
        from bl.wordnavi import naviFromLevel
        navi=naviFromLevel(user.id,word,record)
    elif 'review'==fromSys:
        if reviewDate is None:
            from bl.wordnavi import naviFromReview
            navi=naviFromReview(user.id,word,record,count,index,reviewDate)
        else :
            from bl.wordnavi import naviFromReview
            navi=naviFromReview(user.id,word,record,count,index,reviewDate)
    return navi,_getWordRecordInfo(word,user.id)

def GetReviewWordsAtDate(user,date,useLink=False):
    dateInter=None
    dateInterStr=None
    if 'today'==date:
        dateInterStr='today'
        from bl.gettime import Today
        dateInter=Today()
    else:
        from bl.gettime import DateToStr
        dateInter=date
        dateInterStr=DateToStr(dateInter)
    from dao.dbinterface import queryRecordsAtDate
    records=queryRecordsAtDate(user.id,dateInter)
    words=[]
    wordsfilter=[]
    index=1
    for r in records:
        if r.word not in wordsfilter:
            nw={'word':r.word1}
            if useLink:
                nw['link']='/review/%s/%s?uid=%s'%(dateInterStr,index,user.id)
            words.append(nw)
            wordsfilter.append(r.word)
            index+=1
    return words


def GetLevelWords(user,level,useLink=False):
    from dao.dbinterface import queryWordsByLevel
    levelWords=queryWordsByLevel(level)
    words=[]
    for w in levelWords:
        nw={'word':w}
        if useLink:
            nw['link']='/explore/word/%s/%s?uid=%s'%(w.level,w.id,user.id)
        words.append(nw)
    return words