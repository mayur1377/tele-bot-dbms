import random
import logging
import json
import sqlite3
import re
import time
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
from telegram import __version__ as TG_VER
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
conn = sqlite3.connect("students.db")
cursor = conn.cursor()
# cursor.execute("CREATE TABLE studentss ( teleid STRING PRIMARY KEY , usn STRING, name STRING, year STRING , branch STRING , number STRING , email STRING)")
# conn.commit()


# conn = sqlite3.connect("skills.db")
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE skills (usn string , skills string)")
# conn.commit()



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
OPTION ,NAME , BRANCH ,USN ,YEAR  , CONTACT ,EMAIL  ,CLUBIN , SKILLENTER ,STUDENTEND ,SEARCHUSNCLUB , SENDMSG ,  SKILLUPDATE ,  ADMINNAME  , ADMINPW ,ADMININ , GETUSN ,  SEARCHUSN ,  CLUBENTER ,   CLUBPW   ,CLUBOPT ,  CLUBNEWPW , INTREST2  , GENDER  , SEARCH , SHOWREQ  = range(26)
students={}
temp={}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # above code is to be remove
    global students
    global temp
    students[str(update.effective_user.id)]={
        "id":"" , 
        "usn":"" , 
        "name":"" , 
        "year":"" ,
        "branch":"" , 
        "contact":"" ,
        "email":"" ,
        "skills":"" , 
    }
    temp[str(update.effective_user.id)]={
        "club":""
    }
    reply_keyboard = [["STUDENT", "CLUB ADMIN" , "ADMIN"]]
    await update.message.reply_text(
        """Hello PEEPs ,  Welcome to SKILL FINDER!\nLet me know if you are a\nStudent , Club Member or Admin"""
             ,  reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
    )   
    return  OPTION


async def option (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option=update.message.text
    if(option=="STUDENT"):
            global students
            currid=str(update.effective_user.id)
            conn = sqlite3.connect('students.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM studentss WHERE teleid='{currid}'")
            result = cursor.fetchone()
            global students
            if result: 
                    # print(result[2])
                    students[str(update.effective_user.id)]["usn"]=result[1]
                    students[str(update.effective_user.id)]["name"]=result[2]
                    students[str(update.effective_user.id)]["year"]=result[3]
                    students[str(update.effective_user.id)]["branch"]=result[4]
                    students[str(update.effective_user.id)]["contact"]=result[5]
                    students[str(update.effective_user.id)]["email"]=result[6]
                    reply_keyboard = [["UPDATE ", "LOGOUT"]]
                    await update.message.reply_text(
                        "WELCOME BACK "+result[2] + "! \nWHAT DO YOU WANT ME TO DO?" 
                    ,  reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
                    ),
                    )
                    return STUDENTEND
            else: 
                await update.message.reply_text(
                "Looks like you are a new user! \nLet's get you registered first!😊"
                )
                return USN            
        
    elif(option=="CLUB ADMIN"):
        reply_keyboard = [["EXISTING CLUB", "NEW CLUB"]]
        await update.message.reply_text(
            "HEY CLUB ADMIN! CHOOSE OPTION FROM BELOW !\n\n"
             ,  reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
        ),
        )
        return CLUBIN   
    elif(option=="ADMIN"):
        await update.message.reply_text(
        "Please enter admin username"
        )
        return ADMINNAME
        


async def usn (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    studentusn=update.message.text
    if(len(studentusn)==10):
            students[str(update.effective_user.id)]["usn"]=studentusn.upper()
            await update.message.reply_text(
            "WHAT'S YOUR NAME!?"
            )
            return NAME
    else:
            await update.message.reply_text(
            "PLEASE PROVIDE PROPER USN 🤨"
            )
            return USN


async def name (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    studentname=update.message.text
    students[str(update.effective_user.id)]["name"]=studentname.upper()
    if(len(studentname)<=4):
        await update.message.reply_text(
        "THAT DOSENT SEEM LIKE A NAME , PLEASE ENTER PROPER ONE 🙂"
        )
        return NAME
    else :         
        await update.message.reply_text(
        "Nice to meet you " + studentname + "! ☺\n"
        "WHICH YEAR ARE YOU IN NOW?"
        )
        return YEAR




async def year (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    studentyear=update.message.text
    if(studentyear>="1" and studentyear<="4"):
        students[str(update.effective_user.id)]["year"]=studentyear.upper()
        await update.message.reply_text(
            "WHICH BRANCH ARE YOU IN!?"
        )
        return BRANCH

    # if(studentyear!="1" or studentyear!="2" or studentyear!="3" or studentyear!="4") : 
    #     await update.message.reply_text(
    #     "PLEASE ADD PROPER YEAR , LIKE 1 , 2 , 3 or 4"
    #     )
    #     return YEAR
    else : 
        await update.message.reply_text(
             "PLEASE ENTER A PROPER YEAR \nie : 1,2,3 or 4  🤨"
        )
        return YEAR

async def branch (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    studentbranch=update.message.text
    students[str(update.effective_user.id)]["branch"]=studentbranch.upper()
    await update.message.reply_text(
        "What is your phone number?"
    )
    return CONTACT

async def contact (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    studentnumber=update.message.text
    if(len(studentnumber)==10 and studentnumber.isdigit()):
        students[str(update.effective_user.id)]["contact"]=studentnumber
        await update.message.reply_text(
            "Let me know you email!"
        )
        return EMAIL
    else:
        await update.message.reply_text(
           "please enter proper phone number 🙂"
        )
        return CONTACT

    


async def email (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    studentemail=update.message.text
    students[str(update.effective_user.id)]["email"]=studentemail
    def is_valid_email(email):
        regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        return re.search(regex, email)
    email=studentemail
    if is_valid_email(email):
        # print(f"{email} is a valid email address")
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO studentss ( teleid , usn, name , year , branch , number , email ) VALUES ( ? , ?, ?, ? , ? , ? , ?)", 
        (
        str(update.effective_user.id) , 
        students[str(update.effective_user.id)]["usn"]  , 
        students[str(update.effective_user.id)]["name"] , 
        students[str(update.effective_user.id)]["year"] , 
        students[str(update.effective_user.id)]["branch"] , 
        students[str(update.effective_user.id)]["contact"] ,  
        students[str(update.effective_user.id)]["email"]   
        ))
        conn.commit()
        await update.message.reply_text(
        "well done\nnow enter your SKILLS to register,so to get into the perfect CLUB of your skill! \nCurrently SIT has the following clubs which are ⇩\n" 
        "DMC\nVULCANS\nAURORA\nDECODERS\n"
        "please enter your skills seperated by space"
        "example : MUSIC DANCE ACTING TECH"
        )
        return SKILLENTER
    else:
        # print(f"{email} is not a valid email address")
        await update.message.reply_text(
         "PROPER EMAIL please 👀"
        )
        return EMAIL




async def skillenter (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    skills=update.message.text
    skills=skills.upper()
    def get_valid_words():
        conn = sqlite3.connect("clubs.db")
        c = conn.cursor()
        c.execute("SELECT intrest FROM clubs")
        return [row[0] for row in c.fetchall()]

    valid_words = get_valid_words()
    

    def is_valid_string(s):
        words = s.split()
        return all(word in valid_words for word in words)
    if is_valid_string(skills):
        conn = sqlite3.connect("skills.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO skills (usn, skills ) VALUES ( ?, ?)", 
        (
            # str(update.effective_user.id) , 
            students[str(update.effective_user.id)]["usn"]  , 
            skills
        ))
        conn.commit()
        reply_keyboard = [["UPDATE ", "LOGOUT"]]
        await update.message.reply_text(
        "congratulations 🎉🎉🥳 your skills is registered now!\nWe will let you know if someone messages you!\nwhat to do next 🙃\n\n"
             ,  reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
        ),
        )
        return STUDENTEND
    else: 
        await update.message.reply_text(
        "ENTER PROPER SKILLS\n" 
        # "music  tech  acting  dance"
        "please enter your skills seperated by space\n"
        "example : art tech "
        )
        return SKILLENTER

async def studentend (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option=update.message.text
    if(option=="LOGOUT"):
            reply_keyboard = [["STUDENT", "CLUB ADMIN" , "ADMIN"]]
            await update.message.reply_text(
            "LOGGING OUT! \n\n"
             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
            )   
            return  OPTION
    elif(option=="UPDATE"):
        await update.message.reply_text(
            "PLEASE ENTER YOUR UPDATED SKILLS"
        )
        return SKILLUPDATE

async def skillupdate (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    skills=update.message.text
    skills=skills.upper()
    def get_valid_words():
        conn = sqlite3.connect("clubs.db")
        c = conn.cursor()
        c.execute("SELECT intrest FROM clubs")
        return [row[0] for row in c.fetchall()]

    valid_words = get_valid_words()
    # print("Reach here")

    def is_valid_string(s):
        words = s.split()
        return all(word in valid_words for word in words)
    if is_valid_string(skills):
        conn = sqlite3.connect("skills.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE skills SET skills = ? WHERE usn = ?", (skills, students[str(update.effective_user.id)]["usn"] ))
        conn.commit()
        reply_keyboard = [["UPDATE ", "LOGOUT"]]
        await update.message.reply_text(
        "congratulations 🎉🎉🥳 your skills are updated now!\nWe will let you know if someone messages you!\nwhat to do next 🙃\n\n"
             ,  reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
        ),
        )
        return STUDENTEND
    else: 
        await update.message.reply_text(
        "ENTER PROPER SKILLS" 
        "music , tech , acting , dance"
        "please enter your skills seperated by space"
        "example : art tech music dance"
        )
        return SKILLENTER
        
    










async def clubin (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # reply_keyboard = [["EXISTING CLUB", "NEW CLUB"]
    option=update.message.text
    if(option=="EXISTING CLUB"):
        reply_keyboard = [["DMC", "VULCANS" , "AURORA" , "DECODERS"]]
        await update.message.reply_text(
        "WHICH CLUB ARE YOU IN?" 
        ,  reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
        ),
        )
        return CLUBENTER
    elif(option=="NEW CLUB"):
        await update.message.reply_text(
        "PLEASE CONTACT ADMIN TO ADD YOU CLUB! 📞--> 9741906435"
        )


async def clubenter (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option=update.message.text
    temp[str(update.effective_user.id)]["club"]=option
    await update.message.reply_text(
        "WELCOME ! PLEASE ENTER YOUR PASSWORD"
    )
    return CLUBPW

async def clubpw (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option=update.message.text
    conn = sqlite3.connect("clubs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM clubs WHERE club_name=?", (temp[str(update.effective_user.id)]["club"],))
    correct_password = cursor.fetchone()
    print(correct_password)
    if(correct_password and correct_password[0] != option):
        reply_keyboard = [["STUDENT", "CLUB ADMIN" , "ADMIN"]]
        await update.message.reply_text(
            "incorrect PASSWORD \n"
            "if forgetton password , please contact admin" 
             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )   
        return  OPTION
    else : 
        reply_keyboard = [["UPDATE PASSWORD", "SEND MESSAGE" , "SHOW ALL USERS" , "LOGOUT"]]
        await update.message.reply_text(
            "WELCOME CLUB " + temp[str(update.effective_user.id)]["club"] +" !\n" 
            "what can we do you for today!?"

             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ) 
        )
        return  CLUBOPT

async def clubopt (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option=update.message.text
    if(option=="UPDATE PASSWORD"):
        await update.message.reply_text(
        "ENTER NEW PASSWORD"
        )   
        return CLUBNEWPW
    elif(option=="SEND MESSAGE"):
        await update.message.reply_text(
        "PLEASE ENTER THE USN TO WHOM YOU WANNA SEND MESSAGE"
        )   
        return SEARCHUSNCLUB
        
    elif(option=="SHOW ALL USERS"):
        clubname=temp[str(update.effective_user.id)]["club"]
        x={}
        x["DMC"]="MUSIC"
        x["VULCANS"]="DANCE"
        x["AURORA"]="ACTING"
        x["DECODERS"]="TECH"
        currintrest=x[clubname]
        def search_students_with_skill(currintrest):
            conn = sqlite3.connect("skills.db")
            c = conn.cursor()
            c.execute("SELECT usn FROM skills WHERE skills LIKE ?", ('%' + currintrest + '%',))
            return [row[0] for row in c.fetchall()]
        studentsusn = search_students_with_skill(currintrest)
        def get_student_names_by_usn(usn_list):
            conn = sqlite3.connect("students.db")
            c = conn.cursor()
            query = "SELECT name FROM studentss WHERE usn IN ({})".format(','.join(['?']*len(usn_list)))
            c.execute(query, usn_list)
            return [row[0] for row in c.fetchall()]
        student_names = get_student_names_by_usn(studentsusn)
        usn_to_name = {}
        for name in student_names:
            conn = sqlite3.connect("students.db")
            c= conn.cursor()
            c.execute("SELECT usn FROM studentss WHERE name = ?", (name,))
            result = c.fetchone()
            if result:
                usn = result[0]
                usn_to_name[usn] = name
        print(usn_to_name)
        message="Here is the list of all users \n"
        for usn, name in usn_to_name.items():
            message += "USN: {} - > Name: {} \n".format(usn, name)

        if(len(student_names)==0):
                    reply_keyboard = [["UPDATE PASSWORD", "SEND MESSAGE" , "SHOW ALL USERS" , "LOGOUT"]]
                    await update.message.reply_text(
                    "NO USER FOUND , what to do next??"
                    ,  reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
                ),
                )
        else : 
                reply_keyboard = [["UPDATE PASSWORD", "SEND MESSAGE" , "SHOW ALL USERS" , "LOGOUT"]]
                await update.message.reply_text(
                    message
                    ,  reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
                ),
                )
                return CLUBOPT
    elif(option=="LOGOUT"):
            reply_keyboard = [["STUDENT", "CLUB ADMIN" , "ADMIN" ]]
            await update.message.reply_text(
            "LOGGING OUT! \n\n"
             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
            )   
            return  OPTION

imp=""          
async def searchusnclub (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    currusn=update.message.text
    global imp
    imp=currusn
    clubname=temp[str(update.effective_user.id)]["club"]
    x={}
    x["DMC"]="MUSIC"
    x["VULCANS"]="DANCE"
    x["AURORA"]="ACTING"
    x["DECODERS"]="TECH"
    currintrest=x[clubname]
    def search_students_with_skill(currintrest):
            conn = sqlite3.connect("skills.db")
            c = conn.cursor()
            c.execute("SELECT usn FROM skills WHERE skills LIKE ?", ('%' + currintrest + '%',))
            return [row[0] for row in c.fetchall()]
    studentsusn = search_students_with_skill(currintrest)
    if currusn in studentsusn : 
        await update.message.reply_text(
                    "PLEASE TYPE THE RECRUITMENTS DETAILS BELOW WHICH WILL BE SENT TO THE USER"
        )
        return SENDMSG

    else: 
        reply_keyboard = [["UPDATE PASSWORD", "SEND MESSAGE" , "SHOW ALL USERS" , "LOGOUT"]]
        await update.message.reply_text(
                    "NO USER FOUND , what to do next??"
                    ,  reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
        ),
        )
        return CLUBOPT

async def sendmsg (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option=update.message.text
    global imp
    message= "this is an message from club " + temp[str(update.effective_user.id)]["club"] + "\n"
    message+=option
    message+="\n"
    message+="\n\nTHIS IS AN AUTOMATED MESSAGE , PLEASE DO NOT REPLY"
    def send_message(chat_id, text):
        bot_token = '5889738520:AAGYoXEZ5xzHIbn-At_U0k9yl5NmHkdEy7c'
        send_message_url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage'
        response = requests.post(send_message_url, json={'chat_id': chat_id, 'text': text})
        if response.status_code != 200:
            raise ValueError('Failed to send message: {}'.format(response.content))



    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    usn = imp
    cursor.execute("SELECT teleid FROM studentss WHERE usn = ?", (usn,))   
    result = cursor.fetchone()
    if result:
        chatids = result[0]
    else:
        chatids= None
    conn.commit()
    conn.close()
    send_message(chat_id=chatids, text=message)
    reply_keyboard = [["UPDATE PASSWORD", "SEND MESSAGE" , "SHOW ALL USERS" , "LOGOUT"]]
    await update.message.reply_text(
                    "message sent"
                    ,  reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
        ),
    )
    return CLUBOPT









async def clubnewpw (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option=update.message.text
    conn = sqlite3.connect("clubs.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE clubs SET password=? WHERE club_name=?", (option, temp[str(update.effective_user.id)]["club"]))
    conn.commit()
    reply_keyboard = [["UPDATE PASSWORD", "SEND MESSAGE" , "SHOW ALL USERS" , "LOGOUT"]]
    await update.message.reply_text(
           "NEW PASSWORD SET"
             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ) 
    )
    return  CLUBOPT






    






async def adminname (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option=update.message.text
    if(option=="admin"):
        await update.message.reply_text(
        "password?"
        )
        return ADMINPW
    else : 
        reply_keyboard = [["STUDENT", "CLUB ADMIN" , "ADMIN"]]
        await update.message.reply_text(
            "incorrect \n"
            "taking you back page" 
             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )   
        return  OPTION

async def adminpw (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option=update.message.text
    reply_keyboard = [["STUDENT"]]
    if(option=="password12345"):
        reply_keyboard = [["SHOW USER" , "DELETE BY USN" , "SEARCH USER" , "LOGOUT"]]
        await update.message.reply_text(
            "Welcome Admin! \n"
            "WHAT TO DO ?" 
             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )  
        return ADMININ
    else : 
        reply_keyboard = [["STUDENT", "CLUB ADMIN" , "ADMIN"]]
        await update.message.reply_text(
            "incorrect \n\n"
            "taking you back page" 
             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )   
        return  OPTION


async def adminin (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option=update.message.text
    if(option=="SHOW USER"):
        cursor = conn.cursor()
        cursor.execute("SELECT usn,name FROM studentss")
        studentlist= cursor.fetchall()
        message = "List of students: \n"
        for i in studentlist:
             message += "{}  \n".format(i)
             message += "\n"
        # update.message.reply_text(message)
        if(len(message)<20): message+="NO USERS FOUND \n"
        else : message+="HERE ARE A LIST OF STUDENT \n"
        message+="what to do next?"
        reply_keyboard = [["SHOW USER" , "DELETE BY USN" , "SEARCH USER" ,"LOGOUT"]]
        await update.message.reply_text(
        message
         ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )
        return ADMININ
    elif(option=="DELETE BY USN"):
        await update.message.reply_text(
        "ENTER STUDENT USN WHICH IS TO BE DELETED"
        )
        return GETUSN
    elif(option=="SEARCH USER"):
        await update.message.reply_text(
        "ENTER STUDENT USN WHICH IS TO BE searched"
        )
        return SEARCHUSN
    elif(option=="LOGOUT"):
            reply_keyboard = [["STUDENT", "CLUB ADMIN" , "ADMIN" ]]
            await update.message.reply_text(
            "LOGGING OUT! \n\n"
             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
            )   
            return  OPTION




async def getusn (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    usn=update.message.text
    c = conn.cursor()
    c.execute("SELECT usn FROM studentss WHERE usn=?", (usn,))
    if c.fetchone() is None:
        reply_keyboard = [["SHOW USER" , "DELETE BY USN" , "SEARCH USER"]]
        # reply_keyboard = [["STUDENT", "CLUB ADMIN" , "ADMIN"]]
        await update.message.reply_text(
                    "usn does ot exist "
                    "taking you back page" 
             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )
        return ADMININ
    else:
        c = conn.cursor()
        c.execute("DELETE FROM studentss WHERE usn=?", (usn,))
        conn.commit()
        reply_keyboard = [["SHOW USER" , "DELETE BY USN" , "SEARCH USER"]]
        await update.message.reply_text(
        "done , take u back"
                   ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )
        return ADMININ


async def searchusn (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    usn=update.message.text
    c=conn.cursor()
    c.execute("SELECT usn FROM studentss WHERE usn=?", (usn,))
    if c.fetchone() is None:
        reply_keyboard = [["SHOW USER" , "DELETE BY USN" , "SEARCH USER" , "LOGOUT"]]
        # reply_keyboard = [["STUDENT", "CLUB ADMIN" , "ADMIN"]]
        await update.message.reply_text(
                    "usn does ot exist "
                    "taking you back " 
             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )
        return ADMININ
    else:
        usn=update.message.text
        # print("printing usn : ")
        # print(usn)
        c = conn.cursor()
        c.execute("SELECT * FROM studentss WHERE usn=?", (usn,))
        studentlist= c.fetchall()
        print(studentlist)
        # message = "students info: \n"
        var=tuple()
        for i in studentlist:
             var=i
            #  message += "{}  \n".format(i)
            #  message += "\n"
        # update.message.reply_text(message)
        message=""
        message+="\n"
        message+="what to do next?"
        message = "students info : \n"
        message +="USN : " + str(var[0])
        message +="\nNAME : " +str(var[1])
        message +="\nYEAR : " +str(var[2])
        message +="\nBRANCH : " +str(var[4])
        message +="\nPHONE NUMBER : " +str(var[5])
        message +="\nEMAIL : " +str(var[6])
        message+="\nWHAT TO DO NEXT?"


        reply_keyboard = [["SHOW USER" , "DELETE BY USN" , "SEARCH USER" , "LOGOUT"]]
        await update.message.reply_text(
        message
                   ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )
        return ADMININ















def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5889738520:AAGYoXEZ5xzHIbn-At_U0k9yl5NmHkdEy7c").build()
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME : [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            BRANCH : [MessageHandler(filters.TEXT & ~filters.COMMAND, branch)],
            USN : [MessageHandler(filters.TEXT & ~filters.COMMAND, usn)],
            YEAR : [MessageHandler(filters.TEXT & ~filters.COMMAND, year)],
            CONTACT : [MessageHandler(filters.TEXT & ~filters.COMMAND, contact)],
            EMAIL : [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            SKILLENTER : [MessageHandler(filters.TEXT & ~filters.COMMAND, skillenter)],
            CLUBIN : [MessageHandler(filters.TEXT & ~filters.COMMAND, clubin)],
            ADMINNAME : [MessageHandler(filters.TEXT & ~filters.COMMAND, adminname)],
            ADMINPW : [MessageHandler(filters.TEXT & ~filters.COMMAND, adminpw)],
            ADMININ : [MessageHandler(filters.TEXT & ~filters.COMMAND, adminin)],
            GETUSN : [MessageHandler(filters.TEXT & ~filters.COMMAND, getusn)],
            SEARCHUSN : [MessageHandler(filters.TEXT & ~filters.COMMAND, searchusn)],
            CLUBENTER : [MessageHandler(filters.TEXT & ~filters.COMMAND, clubenter)],
            CLUBPW : [MessageHandler(filters.TEXT & ~filters.COMMAND, clubpw)],
            CLUBOPT : [MessageHandler(filters.TEXT & ~filters.COMMAND, clubopt)],
            CLUBNEWPW : [MessageHandler(filters.TEXT & ~filters.COMMAND, clubnewpw)],
            STUDENTEND : [MessageHandler(filters.TEXT & ~filters.COMMAND, studentend)],
            SKILLUPDATE : [MessageHandler(filters.TEXT & ~filters.COMMAND, skillupdate)],
            SEARCHUSNCLUB : [MessageHandler(filters.TEXT & ~filters.COMMAND, searchusnclub)],
            SENDMSG : [MessageHandler(filters.TEXT & ~filters.COMMAND, sendmsg)],
























            OPTION : [MessageHandler(filters.TEXT & ~filters.COMMAND, option)],
            OPTION : [MessageHandler(filters.TEXT & ~filters.COMMAND, option)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

































# async def gender (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     user = update.message.from_user
#     await update.message.reply_text(
#         "COOL"
#         "COOL",
#     )
#     return ConversationHandler.END
# async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Stores the info about the user and ends the conversation."""
#     user = update.message.from_user
#     logger.info("Bio of %s: %s", user.first_name, update.message.text)
#     await update.message.reply_text("Thank you! I hope we can talk again some day.")

#     return ConversationHandler.END




# async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Cancels and ends the conversation."""
#     user = update.message.from_user
#     logger.info("User %s canceled the conversation.", user.first_name)
#     await update.message.reply_text(
#         "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
#     )

#     return ConversationHandler.END