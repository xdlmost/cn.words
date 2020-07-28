from flask import Blueprint ,request,render_template,redirect
from bl.wrap import checkUser

plugin = Blueprint('query', __name__)

@plugin.route('/query/word', methods=['GET'],endpoint="wordq")
@checkUser
def wordq(user):

    q = request.args.get("q")
    if q is None:
        return "无查询汉字"
    from bl.getword import GetWord
    word=GetWord(q)
    if word is None:
        return "无查询汉字"
    from bl.getword import AppendSingleWordWithFullInfo
    navi,recordinfo=AppendSingleWordWithFullInfo(user,word,'query')
    return render_template('word.html',user=user,word=word,navi=navi,recordinfo=recordinfo)

@plugin.route('/query/word/<yn>/<int:rid>', methods=['GET'],endpoint="wordyn")
@checkUser
def wordyn(user,yn,rid):
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
    return redirect('/?uid=%s'%(user.id))