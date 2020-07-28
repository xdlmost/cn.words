def _getOrderSnapshotUnder80_fliterPlan(snapshot,plan):
    list=[]
    for s in snapshot:
        if s.hotness<=80 :
            list.append(s.word)
    for p in plan:
        if p['word'].word in list:
            list.remove(p.word)
    return list 

def _makeAPlan(user,date,plan,useLink):
    from bl.hotnesssnapshot import updateAndgetSnapshot
    snapshot=updateAndgetSnapshot(user)
    wordlist=_getOrderSnapshotUnder80=_getOrderSnapshotUnder80_fliterPlan(snapshot,plan)
    planToAdd=[]
    from dao.dbinterface import queryAllUnknownWords
    temp=queryAllUnknownWords(user.id)

    lenToCount=max(user.count-len(plan),0)
    newCount=int(lenToCount/6)
    reviewCount=lenToCount-newCount

    newIndex=0
    wordfilter=[]
    for p in plan:
        wordfilter.append(p['word'].word)

    while(reviewCount!=0 ):
        if len(wordlist)>0:
            word=wordlist.pop(0)
            while word in wordfilter and len(wordlist)>0:
                word=wordlist.pop(0)
            if word not in wordfilter:
                planToAdd.append(word)
                wordfilter.append(word)
                reviewCount-=1
        elif len(temp)>newIndex:
            word=temp[newIndex].word
            while word in wordfilter:
                newIndex+=1
                if len(temp)>=newIndex:
                    break
                word=temp[newIndex].word

            if word not in wordfilter:
                planToAdd.append(word)
                wordfilter.append(word)
                newIndex+=1
                reviewCount-=1
        else: 
            break

    while(newCount!=0 ):
        if len(temp)>newIndex:
            word=temp[newIndex].word
            while word in wordfilter :
                newIndex+=1
                if len(temp)>=newIndex:
                    break
                word=temp[newIndex].word
            if word not in wordfilter:
                planToAdd.append(word)
                wordfilter.append(word)
                newIndex+=1
                newCount-=1
        elif len(wordlist)>0:
            word=wordlist.pop(0)
            while word in wordfilter and len(wordlist)>0:
                word=wordlist.pop(0)
            if word not in wordfilter:
                planToAdd.append(word)
                wordfilter.append(word)
                newCount-=1
        else:
            break
    from dao.dbinterface import makePlan
    makePlan(planToAdd,user.id,date)
    return _queryPlan(user,date,useLink)

def _queryPlan(user,date,useLink):
    from dao.dbinterface import queryPlan
    plan=queryPlan(user.id,date)
    from bl.gettime import Today
    dateString='today'
    if  Today()!=date:
        pass
    words=[]
    index=1
    for p in plan:
        nw={'word':p.word1}
        word=p.word1
        if useLink:
            nw['link']='/plan/%s/%s?uid=%s'%(dateString,index,user.id)
        words.append(nw)
        index+=1
    return words


def TodayPlan(user, useLink=False):
    from bl.gettime import Today
    plan=_queryPlan(user,Today(),useLink)
    if user.count > len(plan):
        plan=_makeAPlan(user,Today(),plan,useLink)
    return plan
