
def getLevels(uid):
    from sqlalchemy import func
    from dao.models import db,Word,Record

    partRecord=db.session.query(Record.word).filter(Record.uid==uid).group_by(Record.word).subquery()

    levels=db.session.query(Word.level,func.count(partRecord.c.word).label('view') ).join(partRecord,isouter=True).group_by(Word.level).all()

    res=[]
    for i in levels:
        res.append({
            "level":i[0],
            "view":i[1],
        })
    return res

def testLevel(level):
    from dao.models import Word
    return Word.query.filter(Word.level==level).first() is not None

def WordsCountViewed(uid):
    from dao.models import db,Record
    tmp=db.session.query(Record.word).filter(Record.uid==uid).group_by(Record.word).all()
    return len(tmp)

def WordsCount():
    from dao.models import db,Word
    from sqlalchemy import func
    count=db.session.query(func.count(Word.word).label('count') ).first()
    return  count.count


############################################################################
################     User             ######################################
############################################################################

def queryUser(uid):
    from dao.models import User
    return User.query.filter(User.id==uid).first()

############################################################################
################     Record           ######################################
############################################################################

def addRecord(uid,wordEntery,fromSys):
    import datetime
    from dao.models import db,Record
    today=datetime.date.today()
    r=Record()
    r.uid=uid
    r.word=wordEntery.word
    r.time=datetime.datetime.now()
    r.date=today
    r.tag=0
    r._from=fromSys
    db.session.add(r)

    plan=None
    for p in wordEntery.plans :
        if today==p.date:
            plan=p
            break
    if plan is not None:
        plan.learned=True

    db.session.commit()
    return r

def queryRecord(rid):
    from dao.models import db,Record
    return Record.query.filter(Record.rid==rid).first()

def setRecord(record,tag):

    if record is not None:
        from dao.models import db
        record.tag=tag
        db.session.commit()
    return record

def queryRecords(uid):
    from dao.models import Record
    return Record.query.filter(Record.uid==uid).order_by(Record.time.asc()).all()

def queryRecordsAtDate(uid,date):
    from dao.models import Record
    return Record.query.filter(Record.uid==uid,Record.date==date).order_by(Record.time.asc()).all()

def queryRecordsDates(uid):
    from dao.models import db,Record
    return db.session.query(Record.date).filter(Record.uid==uid).order_by(Record.date.asc()).group_by(Record.date).all()

############################################################################
################     Words            ######################################
############################################################################

def queryAllWords():
    from dao.models import db,Word,Record
    words=Word.query.all()
    return words

def queryAllUnknownWords(uid):
    from dao.models import db,Word,Lasthot
    partRecord=Lasthot.query.filter(Lasthot.uid==uid).subquery()
    words=db.session.query(Word.word,partRecord.c.hotness).filter(partRecord.c.hotness==None).join(partRecord,isouter=True).order_by(Word.level.asc(),Word.id.asc()).all()
    return words

def queryWord(qword):
    from dao.models import Word
    word=Word.query.filter(Word.word==qword).first()
    return word

def queryWordByLevel(qlevel,qindex):
    from dao.models import Word
    word=Word.query.filter(Word.level==qlevel,Word.id==qindex).first()
    return word

def queryWordsByLevel(qlevel):
    from dao.models import Word
    word=Word.query.filter(Word.level==qlevel).order_by(Word.id.asc()).all()
    return word

############################################################################
################     Lasthot          ######################################
############################################################################

def queryHotnessByUid(uid):
    from dao.models import Lasthot
    return  Lasthot.query.filter(Lasthot.uid==uid).order_by(Lasthot.hotness.asc()).all()

def queryHotnessCountByUidGreaterThan80(uid):
    from sqlalchemy import func
    from dao.models import db,Lasthot
    count=db.session.query(func.count(Lasthot.word).label('count') ).filter(Lasthot.uid==uid,Lasthot.hotness>=80).first()
    return  count.count

def UpdateHotnessSnaphot(user,newSnaphot,date):
    from dao.models import db,Lasthot
    user.lasthotdate=date
    for sh in newSnaphot:
        shInDB=Lasthot.query.filter(Lasthot.word==sh['word'],Lasthot.uid==user.id).first()
        if shInDB is None:
            newhot=Lasthot()
            newhot.word=sh['word']
            newhot.uid=user.id
            newhot.hotness=sh['hot']
            db.session.add(newhot)
        else:
            shInDB.hotness=sh['hot']
    db.session.commit()

############################################################################
################     Plan          #########################################
############################################################################

def queryPlan(uid,date):
    from dao.models import Plan
    return Plan.query.filter(Plan.uid==uid,Plan.date==date).order_by(Plan.pid).all()

def queryAllPlan(uid):
    from sqlalchemy import func
    from dao.models import db,Plan
    return db.session.query(func.count(Plan.learned).label('planCount'),func.sum(Plan.learned).label('planDoneCount')).filter(Plan.uid==uid).group_by(Plan.date).all()

def makePlan(planToAdd,uid,date):
    from dao.models import db,Plan
    for p in planToAdd:
        np=Plan()
        np.uid=uid
        np.date=date
        np.word=p
        np.learned=False
        db.session.add(np)
    db.session.commit()