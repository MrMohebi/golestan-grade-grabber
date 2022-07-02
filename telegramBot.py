import telebot
import re
import threading


class TelegramBotGGG:
    TelBot = None
    DB = None

    def __init__(self, token, db):
        self.TelBot = telebot.TeleBot(token, parse_mode=None)
        self.DB = db

        threading.Thread(target=self.TelBot.infinity_polling, daemon=True).start()

    def getTelBot(self):
        return self.TelBot

    def lessenAll(self):
        @self.TelBot.message_handler(commands=['start'])
        def send_welcome(message):
            text = "سلام چه طورین؟" + "\n" + \
                   "این ربات نمره های جدیدی که توی سایت گلستان براتون ثبت میشه رو ارسال میکنه که قراره نباشه روزی ده بار سایت رو چک کنین :)" + "\n" + \
                   "میتونین همینجا توی پیوی ببینین یا به گروه اضافش کنین که برای همتون اونجا ارسال کنه" + "\n" + \
                   "فقط یادتون باشه اگه به گروه اضافش کردین باید ربات رو ادمین کنین" + "\n" + \
                   "برای اینکه ببینین چه طور کار میکنه دستور /help رو وارد کنین"
            self.TelBot.reply_to(message, text)

        @self.TelBot.message_handler(commands=['help'])
        def send_welcome(message):
            self.TelBot.send_message(message.chat.id, "برا ثبت کاربر جدید این متن رو ارسال کنین👇")
            self.TelBot.send_message(message.chat.id, "addUser" + "\n" + "<USERNAME>" + "\n" + "<PASSWORD>")
            self.TelBot.send_message(message.chat.id, "مثال:")
            self.TelBot.send_message(message.chat.id, "addUser" + "\n" + "98408963" + "\n" + "123456789")
            self.TelBot.send_message(message.chat.id, "برای حذف کاربر هم این متن👇")
            self.TelBot.send_message(message.chat.id, "delUser" + "\n" + "<USERNAME>")
            self.TelBot.send_message(message.chat.id, "مثال:")
            self.TelBot.send_message(message.chat.id, "delUser" + "\n" + "98408963")
            self.TelBot.send_message(message.chat.id, "یوزر رو تغییر نمیتونین بدین(حوصلم نشد بزنمش)" + "\n" + " برای اینکه اطلاعات یوزر رو تغییر بدین. یه دور پاکش کنین از اول اضافش کنین :)")


        @self.TelBot.message_handler(func=lambda message: True)
        def all_msgs(message):
            if "addUser" in message.text:
                userPass = list(filter(None, re.split(r"\n+|addUser", message.text)))
                if userPass[0].isnumeric():
                    self.addUserToGroup(message.chat.id, userPass[0], userPass[1])

            if "delUser" in message.text:
                username = list(filter(None, re.split(r"\n+|delUser", message.text)))
                if username[0].isnumeric():
                    self.removeUserFromGroup(message.chat.id, username[0])

    def addUserToGroup(self, groupId, username, password):
        isUserExist = self.DB["groups"].count_documents(
            {"users": {"$elemMatch": {"username": username}}, "chatId": groupId}) != 0

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

    def sendNewScores(self, chatId, scoresArr):
        test = "نمرات جدید: " + scoresArr[0]["username"] + "\n\n"
        for eScore in scoresArr:
            try:
                score = float(eScore['score'])
            except:
                score = -1

            if score > 0:
                test += eScore['name'] + ": " + str(score) + "\n"
                if score < 10:
                    test += "خب اینو افتادی به سلامتی!" + "\n"

        self.TelBot.send_message(chatId, test)
