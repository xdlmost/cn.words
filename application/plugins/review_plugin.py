from flask import Blueprint ,request,render_template,redirect
from bl.wrap import checkUser

plugin = Blueprint('review', __name__)

@plugin.route('/review/<dateStr>', methods=['GET'],endpoint="reviewIndex")
@checkUser
def reviewIndex(dateStr,user):
    from bl.getword import GetReviewWordsAtDate,AppendSingleWordWithSimpleInfo
    from dao.dbinterface import queryRecordsDates
    from bl.gettime import DateToStr ,StrToDate
    date=StrToDate(dateStr)
    if date is None :
        return '非法日期'
    dates=queryRecordsDates(user.id)
    datesStr='['
    for d in dates:
        datesStr+='"%s",'%(DateToStr(d.date))
        datesStr+=','
    datesStr=datesStr[:-2]+']'
    reviewWords=GetReviewWordsAtDate(user,date,True)
    for i in range(len(reviewWords)):
        AppendSingleWordWithSimpleInfo(user,reviewWords[i]['word'])
    return render_template('review.html',user=user,dates=datesStr,showdate=dateStr,showdateStr='%s学习记录'%(dateStr),reviewWords=reviewWords)

@plugin.route('/review/<dateStr>/<int:index>', methods=['GET'],endpoint="reviewToday")
@checkUser
def reviewToday(dateStr,index,user):
    date=None
    from bl.gettime import DateToStr ,StrToDate
    if 'today'==dateStr:
        date=dateStr
    else:
        date=StrToDate(dateStr)
        if date is None :
            return '非法日期'
    from bl.getword import GetReviewWordsAtDate
    words=GetReviewWordsAtDate(user,date)
    if not (index>0 and index<=len(words)):
        return "链接错误"
    word=words[index-1]['word']
    from bl.getword import AppendSingleWordWithFullInfo
    navi,recordinfo=AppendSingleWordWithFullInfo(user,word,'review',len(words),index,date)
    return render_template('word.html',user=user,word=word,navi=navi,recordinfo=recordinfo)

@plugin.route('/review/<dateStr>/<int:index>/<go>/<int:max>', methods=['GET'],endpoint="reviewGo")
@checkUser
def reviewGo(dateStr,index,go,max,user):
    newindex=-1
    if 'pre'==go:
        newindex=index-1
    elif 'next'==go:
        newindex=index+1
    if newindex>0 and newindex<=max:
        return redirect('/review/%s/%s?uid=%s'%(dateStr,newindex,user.id))
    if 'today'!=dateStr:
        return redirect('/review/%s?uid=%s'%(dateStr,user.id))
    return redirect('/?uid=%s'%(user.id)) 

# '/review/%s/%s/yes/%s/%s?uid=%s'%(dateStr,index,record.rid,count,uid)
@plugin.route('/review/<dateStr>/<int:index>/<yn>/<int:rid>/<int:max>', methods=['GET'],endpoint="reviewYn")
@checkUser
def reviewYn(dateStr,index,yn,rid,max,user):
    tag=0
    if "yes"==yn:
        tag=1
    elif 'no'==yn:
        tag=-1
    else:
        return "链接错误"
    from bl.wordaction import changeTagOfRecod
    record=changeTagOfRecod(user.id,rid,tag)
    if record is None:
        return "链接错误"
    return redirect('/review/%s/%s/next/%s?uid=%s'%(dateStr,index,max,user.id))