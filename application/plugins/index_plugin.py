from flask import Blueprint ,request,render_template
from bl.wrap import checkUser

plugin = Blueprint('index', __name__)

def _getLearnedInfo(user):
    res={}
    from dao.dbinterface import WordsCountViewed ,queryHotnessCountByUidGreaterThan80,WordsCount,queryAllPlan

    res['allCount']=WordsCount()
    
    res['viewedCount']=WordsCountViewed(user.id)
    res['viewedProgress']=round(res['viewedCount']*100/res['allCount'],2)

    from bl.hotnesssnapshot import updateSnapshot
    updateSnapshot(user)
    res['wellknownCount']=queryHotnessCountByUidGreaterThan80(user.id)
    res['wellknownProgress']=round(res['wellknownCount']*100/res['allCount'],2)

    planAllCount=queryAllPlan(user.id)
    planCount=0
    planDoneCount=0
    for p in planAllCount:
        planCount+=1
        if p.planCount==p.planDoneCount:
            planDoneCount+=1

    res['planCount']=planCount
    res['planDoneCount']=planDoneCount

    return res

@plugin.route('/index', methods=['GET'])
@plugin.route('/', methods=['GET'])
@checkUser
def index(user):
    from bl.plan import TodayPlan
    from bl.getword import GetReviewWordsAtDate ,AppendSingleWordWithSimpleInfo
    planWords=TodayPlan(user,True)
    for i in range(len(planWords)):
        AppendSingleWordWithSimpleInfo(user,planWords[i]['word'])
    reviewWords=GetReviewWordsAtDate(user,'today',True)
    for i in range(len(reviewWords)):
        AppendSingleWordWithSimpleInfo(user,reviewWords[i]['word'])
    from bl.gettime import Today,DateToStr

    return render_template('index.html',user=user,planWords=planWords,reviewWords=reviewWords,moreInfo=_getLearnedInfo(user),reviewDateStr=DateToStr(Today()))