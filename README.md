# golestan-grade-grabber
inspired by [golestan-grade-checker](https://github.com/alitoufighi/golestan-grade-checker)
#### (dockerized!)

Tired of refreshing for grades coming, So It's the answer :) 

The Bot can be used from Telegram PVs or can be added to group. New grades going to send to you.

It's now up and running in [@GolestanGradeGrabberbot](https://t.me/GolestanGradeGrabberbot)
## usage:
First create a ```.env``` file from ```.evn.example```. Then put your mongo database info and Telegram Token.

[```IRAN_HTTP_PROXY```](https://github.com/MrMohebi/golestan-grade-grabber/blob/master/.env.example#L20) is needed because Golestan System is ONLY available by iran IPs and also Telegram is baned in Iran; so you have to run this project in other countries servers and proxied it throws Iran (God bless them :D).

To change time for interval checking
change [this number](https://github.com/MrMohebi/golestan-grade-grabber/blob/master/main.py#L9) in your favorite in seconds.
### Telegram Bot Commands
> - ```addUser```
> 
> add user to be checked for that group or PV
> 
> ```
> addUser
> USERNAME
> PASSWORD  
> ```

> - ```delUser```
> 
> delete user to be checked from that group or PV
> 
> ```
> delUser
> USERNAME
> ```


### Docker
customise docker files for yourself, Its base on my conditions and servers :) (heart)*3 

### database schema
> ```mongodb
> db.createCollection("groups")
> db.createCollection("lessens")
> db.createCollection("users")
>```
