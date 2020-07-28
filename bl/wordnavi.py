
def _testHasYn(uid,word,record):
    from bl.gettime import Today
    today=Today()
    for r in word.Records:
        if r.uid==uid and r.time.date()==today and record is not None and record.rid!=r.rid:
            return False
    return True

def naviFromLevel(uid,word,record):
    navi={}
    _naviLevelNextPre(uid,word,navi)
    _naviYesNo(uid,word,record,navi)
    return navi

def naviFromQuery(uid,word,record):
    navi={}
    if _testHasYn(uid,word,record):
        navi['yes']='/query/word/yes/%s?uid=%s'%(record.rid,uid)
        navi['no']='/query/word/no/%s?uid=%s'%(record.rid,uid)
    return navi

def _naviLevelNextPre(uid,word,navi):
    from bl.getword import getNextWordByLevel,getPreWordByLevel
    next=getNextWordByLevel(word.level,word.id)
    if next is not None:
        navi['next']='/explore/word/%s/%s/next?uid=%s'%(word.level,word.id,uid)
    pre=getPreWordByLevel(word.level,word.id)
    if pre is not None:
        navi['pre']='/explore/word/%s/%s/pre?uid=%s'%(word.level,word.id,uid)

def _naviYesNo(uid,word,record,navi):
    if _testHasYn(uid,word,record):
        navi['yes']='/explore/word/%s/%s/yes/%s?uid=%s'%(word.level,word.id,record.rid,uid)
        navi['no']='/explore/word/%s/%s/no/%s?uid=%s'%(word.level,word.id,record.rid,uid)

def naviFromPlan(uid,word,record,count,index):
    navi={}
    if index>1:
        navi['pre']='/plan/today/%s/pre/%s?uid=%s'%(index,count,uid)
    if index<count:
        navi['next']='/plan/today/%s/next/%s?uid=%s'%(index,count,uid)
    if _testHasYn(uid,word,record):
        navi['yes']='/plan/today/%s/yes/%s/%s?uid=%s'%(index,record.rid,count,uid)
        navi['no']='/plan/today/%s/no/%s/%s?uid=%s'%(index,record.rid,count,uid)
    return navi
    
def naviFromReview(uid,word,record,count,index,date):
    dateStr=None
    if 'today'==date:
        dateStr='today'
    else:
        from bl.gettime import DateToStr
        dateStr=DateToStr(date)
    navi={}
    if index>1:
        navi['pre']='/review/%s/%s/pre/%s?uid=%s'%(dateStr,index,count,uid)
    if index<count:
        navi['next']='/review/%s/%s/next/%s?uid=%s'%(dateStr,index,count,uid)
    if _testHasYn(uid,word,record):
        navi['yes']='/review/%s/%s/yes/%s/%s?uid=%s'%(dateStr,index,record.rid,count,uid)
        navi['no']='/review/%s/%s/no/%s/%s?uid=%s'%(dateStr,index,record.rid,count,uid)
    return navi
