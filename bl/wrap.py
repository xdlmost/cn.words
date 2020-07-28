
def checkUser(a_func): 
    def wrapTheFunction(*args, **kwargs):
        from flask import request
        uid = request.args.get("uid")
        if uid is None:
            return "无效用户"

        from dao.dbinterface import queryUser
        user = queryUser(uid)
        if user is None:
            return "无效用户"
        kwargs["user"]=user
        return a_func(*args, **kwargs)
    return wrapTheFunction