import telebot
import re


class TelegramBotGGG:
    TelBot = None
    DB = None

    def __init__(self, token, db):
        self.TelBot = telebot.TeleBot(token, parse_mode=None)
        self.DB = db

    def getTelBot(self):
        return self.TelBot

    def lessenAll(self):
        @self.TelBot.message_handler(func=lambda message: True)
        def all_msgs(message):
            if "addUser" in message.text:
                userPass = list(filter(None, re.split(r"\n+|addUser", message.text)))
                if userPass[0][:2] == "98":
                    self.addUserToGroup(message.chat.id, userPass[0], userPass[1])

            if "delUser" in message.text:
                username = list(filter(None, re.split(r"\n+|delUser", message.text)))
                if username[0][:2] == "98":
                    self.removeUserFromGroup(message.chat.id, username[0])

    def addUserToGroup(self, groupId, username, password):
        isUserExist = self.DB["groups"].count_documents({"users": {"$elemMatch": {"username": username}}, "chatId": groupId}) != 0

        if isUserExist:
            self.TelBot.send_message(groupId, "exist! User " + username + " :)")
            return

        self.DB["groups"].update_one({"chatId": groupId}, {
            "$push": {
                "users": {"username": username, "password": password}
            }
        }, upsert=True)

        self.TelBot.send_message(groupId, "submitted! User " + username + " :)")

    def removeUserFromGroup(self, groupId, username):
        self.DB["groups"].update_one({"chatId": groupId}, {
            "$pull": {
                "users": {"username": username}
            }
        })
        self.TelBot.send_message(groupId, "deleted! User " + username + " :)")
