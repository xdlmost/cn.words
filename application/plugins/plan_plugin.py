from flask import Blueprint ,request,render_template,redirect
from bl.wrap import checkUser

plugin = Blueprint('plan', __name__)

@plugin.route('/plan/today', methods=['GET'],endpoint="today")
@checkUser
def today(user):
    from bl.plan import TodayPlan
    plan=TodayPlan(user)
    from bl.getword import AppendSingleWordWithSimpleInfo
    for p in plan:
        AppendSingleWordWithSimpleInfo(user,p)
    return render_template('plan.html',user=user,words=plan)

@plugin.route('/plan/today/<int:index>', methods=['GET'],endpoint="todayIndex")
@checkUser
def todayIndex(index,user):
    if index<=0:
        return "无效的链接"
    from bl.plan import TodayPlan
    plan=TodayPlan(user)
    if 0==len(plan) or index>len(plan):
        return "无效的链接"
    word=plan[index-1]['word']
    from bl.getword import AppendSingleWordWithFullInfo
    navi,recordinfo=AppendSingleWordWithFullInfo(user,word,'plan',len(plan),index)
    return render_template('word.html',user=user,word=word,navi=navi,recordinfo=recordinfo)

@plugin.route('/plan/today/<int:index>/<go>/<int:max>', methods=['GET'],endpoint="go")
@checkUser
def go(index,go,max,user):
    newindex=-1
    if 'pre'==go:
        newindex=index-1
    elif 'next'==go:
        newindex=index+1
    if newindex>0 and newindex<=max:
        return redirect('/plan/today/%s?uid=%s'%(newindex,user.id))
    return redirect('/?uid=%s'%(user.id)) 

@plugin.route('/plan/today/<int:index>/<yn>/<int:rid>/<int:max>', methods=['GET'],endpoint="goyn")
@checkUser
def goyn(index,yn,rid,max,user):
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
    return redirect('/plan/today/%s/next/%s?uid=%s'%(index,max,user.id))