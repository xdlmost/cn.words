def _update(user,recordEntryList,date):
    newSnaphot=[]
    from bl.hotness import HotnessWithoutBase,HotnessWithBase
    for recordEntry in recordEntryList:
            newSnaphot.append({
                'word':recordEntry['word'],
                'hot': HotnessWithoutBase(recordEntry['records'],date)
            })

    from dao.dbinterface import UpdateHotnessSnaphot
    UpdateHotnessSnaphot(user,newSnaphot,date)

def _SnaphotToDict(HardnessSnaphots):
    dict={}
    for hs in HardnessSnaphots:
        dict[hs.word]=hs
    return dict
def _makeRecordEntryList(user):
    recordEntryList=[]
    temprecordEntryList={}
    from dao.dbinterface import queryRecords
    for record in queryRecords(user.id):
        if record.word not in temprecordEntryList:
            temprecordEntryList[record.word]=[]
        temprecordEntryList[record.word].append(record)
    for key in temprecordEntryList:
        recordEntryList.append({
            'word':key,
            'records':temprecordEntryList[key]})
    return recordEntryList

def _updateSnapshotToDate(user,date):
    if user.lasthotdate is not None:
        if date<=user.lasthotdate:
            return None
    _update(user,_makeRecordEntryList(user),date)

def _getSnapshot(user):
    from dao.dbinterface import queryHotnessByUid
    return queryHotnessByUid(user.id)

def _SnapshotIsUpdateAtDate(user,date):
    return user.lasthotdate==date
 
def updateSnapshot(user):
    from bl.gettime import Yesterday
    yesterday=Yesterday()
    if not _SnapshotIsUpdateAtDate(user,yesterday):
        _updateSnapshotToDate(user,yesterday)

def updateAndgetSnapshot(user):
    updateSnapshot(user)
    return _getSnapshot(user)