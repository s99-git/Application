import pymongo, datetime, time, hashlib

from bson.objectid import ObjectId
from .utils.class_user import User
from random import seed, randint


class PinguinDB:

    # commented out self.client is for guest DB access role instead of admin DB access
    def __init__(self):
        self.user = User()
        self.client = pymongo.MongoClient(
            "mongodb+srv://PinguinAdmin:D47b5PIrtJxIhnuV@pinguin-cluster.vvukk.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        # self.client = pymongo.MongoClient("mongodb+srv://guest:kYmIc3X8vSHcNTfy@pinguin-cluster.vvukk.mongodb.net/Pinguin?retryWrites=true&w=majority")

        # Definitions for the different databases
        # Databases that end in Pinguin do not have a different collection for each group
        self.groups = self.client.Groups.Pinguin
        self.users = self.client.Users.Pinguin
        self.invites = self.client.Invites
        self.forums = self.client.Forums
        self.calendars = self.client.Calendar
        self.documents = self.client.Documents
        self.tasks = self.client.Tasks

    # Changes stored user credentials
    def change_user(self, user_id, name, pword, _id, groups):
        self.user.user_id = user_id
        self.user.user_name = name
        self.user.pword = pword
        self.user._id = _id
        self.user.groups = groups
        # Sets the current group to be the first group the user has joined if they are in one
        # Can be changed later to save group on exit and use that as default group
        if (len(self.user.groups) >= 1):
            self.user.currentGroup = self.user.groups[0]
        return 1

    # Logs in the user
    def login(self, user_id, pword):
        # Encrypts password so that it is not stored as plaintext
        encPass = hashlib.sha256(pword.encode())
        # "encPass.hexdigest" is the alphanumeric representation of the encrypted password
        # Checks if a user exists with the entered username and password

        if (self.users.count_documents({'user_id': user_id})):

            user_doc = self.users.find_one({'user_id': user_id})
            if user_doc['pass'] != encPass.hexdigest():
                print("Incorrect password")
                return 0
            # Updates variables for logged in user's information, then confirms login
            self.change_user(user_doc['user_id'], user_doc['user_name'], user_doc['pass'], user_doc['_id'],
                             user_doc['groups'])
            print("login successful")

            return 1
        else:
            print('login unsucessful')
            return 0

    def current_user(self):
        userList = []
        userList.append(self.user._id)
        userList.append(self.user.user_id)
        userList.append(self.user.user_name)
        userList.append(self.user.currentGroup)
        #print(userList[0])
        #print(userList[1])
        #print(userList[2])
        return userList

    # Changes the current group to another group the user is in
    def change_group(self, group_id):

        if (group_id in self.user.groups):
            self.user.currentGroup = group
            #print(self.user.currentGroup)
            return 1
        else:
            print("User is not a member of given group")
            return 0

    def get_calendar_id(self,group_id):
        if(self.groups.find_one({"_id":group_id})):
            group = self.groups.find_one({"_id":group_id})
            return group['calendar_id']

    # Create a new account with the entered details
    def create_account(self, user_id, pword, name, trello_id):
        # Rejects the request if an account with that email already exists
        if (self.users.find_one({"user_id": user_id})):
            print('User already exists')
            return 0
        else:
            self.user.user_id = user_id
            encPass = hashlib.sha256(pword.encode())
            self.user.pword = encPass.hexdigest()
            self.user.user_name = name
            self.user.trello_id = trello_id

            user_account = {"user_id": self.user.user_id,
                            "user_name": self.user.user_name,
                            "pass": self.user.pword,
                            "role": "user",
                            "groups": [],
                            "invites": [],
                            "trello_id": trello_id}

            self.users.insert_one(user_account)

            self.user._id = self.users.find_one({"user_id": self.user.user_id}).get("_id")

            return 1

    def set_trello_id(self,trello_id):
        self.users.update_one({"_id":self.user._id},{"$set":{"trello_id":trello_id}})

    # Create a group
    def create_group(self, name, description, calendar_id):
        if (self.groups.find_one({"group_name": name})):
            print('Group of that name already exists')
            return 0
        else:

            group_post = {"group_name": name,
                          "owner": self.user._id,
                          "description": description,
                          "members": [self.user._id],
                          "invites": [],
                          "calendar_id": calendar_id}

            self.groups.insert_one(group_post)

            groupFind = self.groups.find_one({"group_name": name}).get("_id")
            self.user.groups.append(groupFind)
            self.users.update_one({"_id": self.user._id}, {"$push": {"groups": groupFind}})

    # Checks if the user is the owner of the group
    def check_ownership(self, group_id, user_id):
        groupCheck = self.groups.find_one({"_id": ObjectId(group_id)})
        if user_id == groupCheck['owner']:
            return 1
        else:
            return 0

    def remove_user(self, user_id):
        if(user_id == self.user._id):
            print("Error, cannot remove self from group")
            return 0

        self.groups.update_one({"_id":self.user.currentGroup}, {"$pull": {"members":user_id}})
        self.users.update_one({'_id':user_id},{"$pull": {"groups":self.user.currentGroup}})
        return 1

    def delete_group(self):
        memberList = []
        memberList = self.groups.find_one({'_id':self.user.currentGroup}).get('members')

        for x in memberList:
            self.users.update_one({'_id':x}, {"$pull": {"groups":self.user.currentGroup}})

        self.groups.delete_one({'_id':self.user.currentGroup})
        for x in self.user.groups:
            if (x == self.user.currentGroup):
                self.user.groups.remove(x)
                if (len(self.user.groups) >= 1):
                    self.user.currentGroup = self.user.groups[0]


    def testConnections(self):
        print(self.db.list_collection_names())

    def get_groups(self):
        groupList = []
        for x in self.groups.find():
            if x.get("_id") in self.user.groups:
                groupList.append(x)
                #print(x)
        return groupList


    def send_invite(self, reciever_id):

        if (not self.users.find_one({"_id": reciever_id})):
            print("User not found")
            return 0

        post = {'sender_name': self.user.user_name,
                'sender': self.user._id,
                'group_id': self.user.currentGroup,
                'receiver': reciever_id
                }

        self.users.update_one({"_id": reciever_id}, {"$push": {"invites": post}})
        self.groups.update_one({"_id": self.user.currentGroup}, {"$push": {"invites": post}})

        return 1

    def invite_find(self):

        inviteList = []
        for x in self.users.find_one({'_id': self.user._id}).get("invites"):
            inviteList.append(x)
            print(x)
        return inviteList


    # Forums Window
    def invite_accept(self, group_id):

        #remove the invite

        inviteList = self.users.find_one({"_id":self.user._id}).get("invites")
        for x in inviteList:
            if x['group_id'] == group_id:
                inviteFind = x

        self.groups.update_one({"_id":group_id}, {"$pull": {"invites":inviteFind}})
        self.users.update_one({"_id":self.user._id}, {"$pull": {"invites":inviteFind}})


        #add them to the group
        self.user.groups.append(group_id)
        self.users.update_one({"_id":self.user._id}, {"$push": {"groups":group_id}})
        self.groups.update_one({"_id":group_id}, {"$push": {"members":self.user._id}})
        return 1

    def invite_deny(self, group_id):
        inviteList = self.users.find_one({"_id": self.user._id}).get("invites")
        for x in inviteList:
            if x['group_id'] == group_id:
                inviteFind = x

        self.groups.update_one({"_id": group_id}, {"$pull": {"invites": inviteFind}})
        self.users.update_one({"_id": self.user._id}, {"$pull": {"invites": inviteFind}})

        return 1

    def send_post(self, message):
        post = {'author': self.user._id,
                'group': self.user.currentGroup,
                'message': message,
                'date': datetime.datetime.utcnow()
                }
        groupFind = self.groups.find_one({'_id': self.user.currentGroup}).get("group_name")
        self.forums[groupFind].insert_one(post)
        return 1

    def retrieve_all_posts(self):
        postList = []
        groupFind = self.groups.find_one({'_id': self.user.currentGroup}).get("group_name")
        for x in self.forums[groupFind].find():
            #print(x)
            postList.append(x)
        return postList

    def delete_post(self, post_id):

        groupFind = self.groups.find_one({'_id':self.user.currentGroup}).get("group_name")
        self.forums[groupFind].delete_one({"_id":post_id})

    def calendar_add(self, description, date):

        calendarPost = {'author': self.user._id,
                        'group': self.user.currentGroup,
                        'day': date.day,
                        'month': date.month,
                        'year': date.year,
                        'description': description
                        }

        groupFind = self.groups.find_one({'_id': self.user.currentGroup}).get("group_name")
        self.calendars[groupFind].insert_one(calendarPost)

        return 1

    def retrieve_calendar_posts(self, date, time):
        calendarList = []
        groupFind = self.groups.find_one({'_id': self.user.currentGroup}).get("group_name")
        if time == "month":
            for x in self.calendars[groupFind].find({'month': date.month}):
                print(x)
                calendarList.append[x]
        elif time == "year":
            for x in self.calendars[groupFind].find({'year': date.year}):
                print(x)
                calendarList.append[x]
        elif time == "day":
            for x in self.calendars[groupFind].find({'day': date.day}):
                print(x)
                calendarList.append[x]

        return calendarList

    def delete_calendar(self, calendar_id):

        groupFind = self.groups.find_one({'_id':self.user.currentGroup}).get("group_name")
        self.calendars[groupFind].delete_one({"_id":calendar_id})

    def document_add(self, title, type, link):

        post = {
            'author': self.user.user_name,
            'group': self.user.currentGroup,
            'title': title,
            'type' : type,
            'doc': link
        }
        groupFind = self.groups.find_one({'_id': self.user.currentGroup}).get("group_name")
        self.documents[groupFind].insert_one(post)
        return 1

    def retrieve_document(self, doc_name, group_id):
        groupFind = self.groups.find_one({'_id':group_id}).get('group_name')
        doc_id = self.documents[groupFind].find_one({'title':doc_name}).get('_id')
        return doc_id

    def retrieve_docs(self):
        docList = []
        groupFind = self.groups.find_one({'_id': self.user.currentGroup}).get("group_name")
        for x in self.documents[groupFind].find():
            docList.append(x)
        return docList

    def delete_doc(self, doc_id):

        groupFind = self.groups.find_one({'_id':self.user.currentGroup}).get("group_name")
        self.documents[groupFind].delete_one({"_id":doc_id})

    def user_lookup(self, user_id):
        if (self.users.find_one({'_id': user_id})):
            userFind = self.users.find_one({'_id': user_id})
            return userFind
        else:
            return 0

    def user_lookup_by_email(self, email):
        if (self.users.find_one({'user_id': email})):
            userFind = self.users.find_one({'user_id': email})
            return userFind
        else:
            return 0

    def group_lookup(self, group_id):
        if (self.groups.find_one({'_id': group_id})):
            groupFind = self.groups.find_one({'_id': group_id})
            return groupFind
        else:
            return 0

    # Error Management
    def errorHandler(self, error):

        return

    def create_many_accounts(self, men, women):
        seed(time.time())

        for man in range(men):
            name = names.get_first_name(gender='male')
            number = str(randint(100, 999))
            pword = "pinguin"
            user_id = name + number + "@gmail.com"
            self.create_account(user_id, pword, name)

        for woman in range(women):
            name = names.get_first_name(gender='female')
            number = str(randint(100, 999))
            pword = "pinguin"
            user_id = name + number + "@gmail.com"
            self.create_account(user_id, pword, name)

    def create_emails(self, num):
        seed(time.time())
        invites = ""
        for x in range(num):
            if (x % 2 == 0):
                name = names.get_first_name(gender='male')
                invite = name + "@gmail.com,"

            else:
                name = names.get_first_name(gender='female')
                invite = name + "@gmail.com,"

            invites += invite
        # print(invites)
        return invites

    def create_many_groups(self, group_num):
        seed(time.time())
        for i in range(group_num):
            group_name = generate_slug(3)
            invites = self.create_emails(6)
            self.create_group(group_name, "Test Description", invites)

