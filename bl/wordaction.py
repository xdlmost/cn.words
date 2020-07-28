import dao.dbinterface as bi

def appendRecord(uid,word,fromSys):
    return bi.addRecord(uid,word,fromSys)

def changeTagOfRecod(uid,rid,tag):
    record=bi.queryRecord(rid)
    if record is not None:
        import datetime
        today=datetime.date.today()
        if record.uid==uid and record.time.date()==today:
            return bi.setRecord(record,tag)
    return None