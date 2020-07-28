from flask import Blueprint ,request,render_template,redirect
from bl.wrap import checkUser

plugin = Blueprint('explore', __name__)

@plugin.route('/explore/levels', methods=['GET'],endpoint="levels")
@checkUser
def levels(user):
    from dao.dbinterface import getLevels
    return  render_template('levels.html',user=user,levels=getLevels(user.id))

@plugin.route('/explore/level/<int:level>', methods=['GET'],endpoint="level")
@checkUser
def level(level,user):
    from bl.getword import GetLevelWords,AppendSingleWordWithSimpleInfo
    words=GetLevelWords(user,level,True)
    for i in range(len(words)):
        AppendSingleWordWithSimpleInfo(user,words[i]['word'])
    
    return  render_template('level.html',user=user,levelWords=words,levelTitle='第%s级字列表'%(level))

#####################################################################
###################    Word   #######################################
#####################################################################

@plugin.route('/explore/word/<int:level>/<int:index>', methods=['GET'],endpoint="word")
@checkUser
def word(level,index,user):
    from bl.getword import getWordByLevel
    from bl.getword import AppendSingleWordWithFullInfo
    word=getWordByLevel(level,index)
    if word is None:
        return "无查询汉字"
    navi,recordinfo=AppendSingleWordWithFullInfo(user,word,'explore')
    return render_template('word.html',user=user,word=word,navi=navi,recordinfo=recordinfo)

@plugin.route('/explore/word/<int:level>/<int:index>/<go>', methods=['GET'],endpoint="wordgo")
@checkUser
def wordgo(level,index,user,go):
    if "next"==go:
        from bl.getword import getNextWordByLevel
        word=getNextWordByLevel(level,index)
        if word is None:
            return '没有后一个字了'
        else:
            return redirect('/explore/word/%s/%s?uid=%s'%(word.level,word.id,user.id))
    elif 'pre'==go:
        from bl.getword import getPreWordByLevel
        word=getPreWordByLevel(level,index)
        if word is None:
            return '没有前一个字了'
        else:
            return redirect('/explore/word/%s/%s?uid=%s'%(word.level,word.id,user.id))
    return "链接错误"

@plugin.route('/explore/word/<int:level>/<int:index>/<yn>/<int:rid>', methods=['GET'],endpoint="wordyn")
@checkUser
def wordyn(level,index,user,yn,rid):
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
    return redirect('/explore/word/%s/%s/next?uid=%s'%(level,index,user.id))



