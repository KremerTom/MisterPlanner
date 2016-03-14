
from google.appengine.ext import db
from google.appengine.api import users

import mpusers
import webapp2
import json


class GroupInfo(db.Model):
    groupId = db.StringProperty()
    host = db.StringProperty(required=True)
    groupName = db.StringProperty(required=True)


class GroupMember(db.Model):
    groupId = db.StringProperty(required=True)
    userId = db.StringProperty(required=True)


# Create a GroupMember entry for each member (not including host)
def addToGroup(groupid, phoneNums):
    noProblems = True

    for num in phoneNums:
        qq = GroupMember.all()
        qq.filter("groupId =", groupid)
        uId = mpusers.getUserIdByNumber(num)
        if uId is None:
            tempUser = mpusers.createShadowUser(num)
            uId = tempUser.userId
        qq.filter("userId =", uId)
        if qq.get() is None:
            gm = GroupMember(groupId=groupid, userId=uId)
            gm.put()
        else:
            noProblems = False

    return noProblems


# Add an arry of phone numbers to a given groupId
class AddToGroup(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        nums = self.request.get("numbers").split()
        groupid = self.request.get("groupid")

        success = addToGroup(groupid, nums)

        dict = {"result": success}

        self.response.write(json.dumps(dict))



def createGroup(name, hostId, phoneNums):
    # Check if host id actually exists
    user = mpusers.getUserByID(hostId)
    if user is None:
        print "That host id doesn't exist"
        return

    group = GroupInfo(groupName=name, host=hostId)
    q = GroupInfo.all()
    q.filter("name =", name)
    q.filter("host =", hostId)
    match = q.get()

    if match is None:
        # Create the GroupInfo entry, including the groupId
        group_key = group.put()
        temp_group = db.get(group_key)
        gId = str(group_key.id())
        temp_group.groupId = gId
        temp_group.put()

        # Create a GroupMember entry for each member (not including host)
        success = addToGroup(gId, phoneNums)
        if success:
            print "successfully wrote " + name
            return temp_group
        else:
            return None
    else:
        print "There is already a group with that name for that user"
        return None


# Given a group name, a list of phone numbers (space separated), and an optional hostid,
# create a groupinfo entity and as many groupmember entities as required.
class CreateGroup(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        groupName = self.request.get("name")
        hostId = self.request.get("userid")
        if hostId == None or hostId == "":
            hostId = mpusers.userIdFromGoogleId(users.get_current_user().user_id())
        nums = self.request.get("numbers").split()

        group = createGroup(groupName, hostId, nums)

        if group is not None:
            self.response.write(json.dumps(convertGroupInfoToDict(group)))
        else:
            self.response.write({})

        return


def getGroupsByHost(userid):
    q = GroupInfo.all()
    q.filter("host =", userid)

    temp = []

    for i in q.run():
        gId = i.groupId

        qq = GroupMember.all()
        qq.filter("groupId =", gId)

        dict = convertGroupInfoToDict(i)
        dict["Users"] = []

        for j in qq.run():
            dict["Users"].append(str(j.userId))

        temp.append(dict)
    return temp

    # EXTREMELY SLOW
    # CHANGE YOUR APPROACH
    #
    # while thisGroup is not None:
    #     gId = thisGroup.groupId
    #     print gId
    #     qq = GroupMember.all()
    #     qq.filter("groupId =", gId)
    #     member = qq.get()
    #     dict = convertGroupInfoToDict(thisGroup)
    #     dict["Users"] = []
    #
    #     while member is not None:
    #         print member.userId
    #         dict["Users"].append(member.userId)
    #         member = qq.get()
    #
    #
    #     temp.append(dict)
    #     thisGroup = q.get()
    #
    # return temp


# API for getting all the Groups (by combining GroupInfo with array of userIDs from GroupMember)
# of a host given the userid
class GetGroupsByHost(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'

        print "started"
        userid = self.request.get("userid")
        if userid is None:
            self.request.write(json.dumps({}))
            return

        groups = getGroupsByHost(userid)
        print "got groups"
        dict = {}
        dict["groups"] = groups

        print dict

        self.response.write(json.dumps(dict))



def convertGroupInfoToDict(group):
    dict = {}
    dict["GroupID"] = str(group.groupId)
    dict["HostID"] = str(group.host)
    dict["Name"] = str(group.groupName)
    return dict


groupsAPI = [('/creategroup', CreateGroup), ('/addtogroup', AddToGroup), ('/getgroupsbyhost', GetGroupsByHost)]
