import random
import logging
import json
import sqlite3
import re
import time
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
# cursor.execute("CREATE TABLE studentss ( usn STRING PRIMARY KEY, name STRING, year STRING , branch STRING , number STRING , email STRING)")
# conn.commit()


# conn = sqlite3.connect("skills.db")
# cursor = conn.cursor()
# cursor.execute("CREATE TABLE skills (usn string , skills string)")
# conn.commit()



logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
OPTION ,NAME , BRANCH ,USN ,YEAR  , CONTACT ,EMAIL  ,CLUBIN , SKILLENTER ,STUDENTEND , SKILLUPDATE ,  ADMINNAME  , ADMINPW ,ADMININ , GETUSN ,  SEARCHUSN ,  CLUBENTER ,   CLUBPW   ,CLUBOPT ,  CLUBNEWPW ,                  LINKEDIN ,  DESC   , INTREST , INTREST2 , HELPER , GENDER  , SEARCH , SHOWREQ , DISPLAYUSER , DISPLAYOPTION= range(30)
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
            "Hey there ! Welcome ! \n\n"
            "Let me know if you are a student or a club member first!" 
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
                        "WELCOME BACK !"+result[2] + "WHAT DO YOU WANT ME TO DO?" 
                    ,  reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
                    ),
                    )
                    return STUDENTEND
            else: 
                await update.message.reply_text(
                "WELCOME FRESHER ! ENTER USN"
                )
                return USN            
        
    elif(option=="CLUB ADMIN"):
        reply_keyboard = [["EXISTING CLUB", "NEW CLUB"]]
        await update.message.reply_text(
            "HEY CLUB ADMIN! LET US GET YOU STARTED !\n\n"
             ,  reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
        ),
        )
        return CLUBIN   
    elif(option=="ADMIN"):
        await update.message.reply_text(
        "enter admin username"
        )
        return ADMINNAME
        
    


        # await update.message.reply_text("FINDING USERS FOR YOU")
        # x=str(update.effective_user.id)
        # cursor.execute("SELECT intrest FROM users2 WHERE  id=?" , (x , ))
        # rows = cursor.fetchone()
        # message=rows[0]
        # intrest_list=message.split(',')
        # users[str(update.effective_user.id)]["user"]={}
        # users[str(update.effective_user.id)]["x"]=0
        # for i in intrest_list : 
        #     query = "SELECT * FROM users2 WHERE intrest LIKE '%{}%'".format(i)
        #     cursor.execute(query)
        #     rows = cursor.fetchall()
        #     for row in rows:
        #         id = row[0]
        #         name = row[1]
        #         bio = row[2]
        #         linkedin = row[3]
        #         intrest= row[4]
        #         users[str(update.effective_user.id)]["user"][users[str(update.effective_user.id)]["x"]]= {
        #             "id" : id , 
        #             "name": name,
        #             "bio": bio,
        #             "linkedin": linkedin,
        #             "intrest": intrest
        #         }
        #         users[str(update.effective_user.id)]["x"]+=1
        # if(len(users)==0):
        #     await update.message.reply_text("NO USERS FOUND , MAYBE TRY AGAIN LATER ?")
        #     return HELPER
        # else : 
        #     # print("there are the potential user \n")
        #     # print(users[str(update.effective_user.id)]["user"])
        #     users[str(update.effective_user.id)]["keys"]=list( users[str(update.effective_user.id)]["user"].keys())
        #     random.shuffle(users[str(update.effective_user.id)]["keys"])
        #     users[str(update.effective_user.id)]["size"]=0
        #     return DISPLAYUSER


async def usn (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    studentusn=update.message.text
    if(len(studentusn)==10):
            students[str(update.effective_user.id)]["usn"]=studentusn.upper()
            await update.message.reply_text(
            "cool , NAME?"
            )
            return NAME
    else:
            await update.message.reply_text(
            "ENTER PROPER USN"
            )
            return USN


async def name (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    studentname=update.message.text
    students[str(update.effective_user.id)]["name"]=studentname.upper()
    if(len(studentname)<5):
        await update.message.reply_text(
        "THAT DOSENT SEEM LIKE A NAME , PLEASE ENTER PROPER ONE"
        )
        return NAME
    else :         
        await update.message.reply_text(
        "Nice to meet you " + studentname + "!\n"
        "Enter YOUR YEAR"
        )
        return YEAR




async def year (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    studentyear=update.message.text
    if(studentyear>="1" and studentyear<="4"):
        students[str(update.effective_user.id)]["year"]=studentyear.upper()
        await update.message.reply_text(
            "COOL , ENTER BRANCH?"
        )
        return BRANCH

    # if(studentyear!="1" or studentyear!="2" or studentyear!="3" or studentyear!="4") : 
    #     await update.message.reply_text(
    #     "PLEASE ADD PROPER YEAR , LIKE 1 , 2 , 3 or 4"
    #     )
    #     return YEAR
    else : 
        await update.message.reply_text(
            "enter proper year"
        )
        return YEAR

async def branch (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    studentbranch=update.message.text
    students[str(update.effective_user.id)]["branch"]=studentbranch.upper()
    await update.message.reply_text(
        "cool , NUMBER ?"
    )
    return CONTACT

async def contact (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    studentnumber=update.message.text
    if(len(studentnumber)==10 and studentnumber.isdigit()):
        students[str(update.effective_user.id)]["contact"]=studentnumber
        await update.message.reply_text(
            "cool , EMAIL"
        )
        return EMAIL
    else:
        await update.message.reply_text(
            "enter proper phone number"
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
        "cool , now lets enter your skills , so thay club can find you easily  , currently the clubs which are available are" 
        "music , tech , acting , dance"
        "please enter your skills seperated by commas"
        "example : art,tech,music,dance"
        )
        return SKILLENTER
    else:
        # print(f"{email} is not a valid email address")
        await update.message.reply_text(
        "ENTER PROPER EMAIL"
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
            " data is stored , what to do next\n\n"
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
            "let us update your skills"
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
    print("Reach here")

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
            " data is stored , what to do next\n\n"
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
        "PLEASE CONTACT ADMIN TO ADD YOU CLUB!"
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
            "incorrect \n\n"
            "if forgetton password , please contact admin" 
             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )   
        return  OPTION
    else : 
        reply_keyboard = [["UPDATE PASSWORD", "SEARCH USERS" , "SHOW ALL USERS" , "LOGOUT"]]
        await update.message.reply_text(
            "WELCOME CLUB" + temp[str(update.effective_user.id)]["club"] + 
            " what can we do you for today!?"

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
    elif(option=="SEARCH USERS"):
        cursor = conn.cursor()
        cursor.execute("SELECT usn,name FROM studentss WHERE")
        studentlist= cursor.fetchall()
        message = "List of students: \n"
        for i in studentlist:
             message += "{}  \n".format(i)
             message += "\n"
        # update.message.reply_text(message)
        if(len(message)<20): message+="NO USERS FOUND \n"
        else : message+="HERE ARE A LIST OF STUDENT \n"
        message+="what to do next?"
        reply_keyboard = [["UPDATE PASSWORD", "SEARCH USERS" , "SHOW ALL USERS" , "LOGOUT"]]
        await update.message.reply_text(
        message
         ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )
    elif(option=="LOGOUT"):
            reply_keyboard = [["STUDENT", "CLUB ADMIN" , "ADMIN"]]
            await update.message.reply_text(
            "LOGGING OUT! \n\n"
             ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
            )   
            return  OPTION
    elif(option=="SHOW ALL USERS"):
        clubname=temp[str(update.effective_user.id)]["club"]
        x={}
        x["DMC"]="MUSIC"
        x["VULCANS"]="DANCE"
        x["AURORA"]="ACTING"
        x["DECODES"]="TECH"
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
            query = "SELECT name FROM students WHERE usn IN ({})".format(','.join(['?']*len(usn_list)))
            c.execute(query, usn_list)
            return [row[0] for row in c.fetchall()]
        student_names = get_student_names_by_usn(studentsusn)
        print(student_names)
       
        if(len(student_names)==0):
                    reply_keyboard = [["UPDATE PASSWORD", "SEARCH USERS" , "SHOW ALL USERS" , "LOGOUT"]]
                    await update.message.reply_text(
                    "NO USER FOUND , what to do next??"
                    ,  reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
                ),
                )
        else : 
                reply_keyboard = [["UPDATE PASSWORD", "SEARCH USERS" , "SHOW ALL USERS" , "LOGOUT"]]
                await update.message.reply_text(
                    student_names 
                    ,  reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
                ),
                )
            




async def clubnewpw (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option=update.message.text
    conn = sqlite3.connect("clubs.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE clubs SET password=? WHERE club_name=?", (option, temp[str(update.effective_user.id)]["club"]))
    conn.commit()
    reply_keyboard = [["UPDATE PASSWORD", "SEARCH USERS" , "SHOW ALL USERS" , "LOGOUT"]]
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
            "incorrect \n\n"
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
            "correct \n\n"
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
        reply_keyboard = [["SHOW USER" , "DELETE BY USN" , "SEARCH USER"]]
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
        reply_keyboard = [["SHOW USER" , "DELETE BY USN" , "SEARCH USER"]]
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
        print("printing usn : ")
        print(usn)
        c = conn.cursor()
        c.execute("SELECT * FROM studentss WHERE usn=?", (usn,))
        studentlist= c.fetchall()
        print(studentlist)
        message = "students info: \n"
        for i in studentlist:
             message += "{}  \n".format(i)
             message += "\n"
        # update.message.reply_text(message)
        message+="\n"
        message+="what to do next?"
        reply_keyboard = [["SHOW USER" , "DELETE BY USN" , "SEARCH USER"]]
        await update.message.reply_text(
        message
                   ,  reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )
        return ADMININ
















async def desc (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global users
    users[str(update.effective_user.id)]["bio"]=update.message.text
    if(len(users[str(update.effective_user.id)]["bio"])<10):
        await update.message.reply_text(
            "That's to less , tell me more about yourself so I get to know you better!")
        return DESC
    elif(len(users[str(update.effective_user.id)]["bio"])>100):
        await update.message.reply_text(
            "WOAH ! THATS TOO MUCH , HOW ABOUT MAKING IT LESS TO 100 CHARS!?")
        return DESC
    else :
        await update.message.reply_text(
        "Good to know about you!\n" 
        "Now ! Enter your linkedin url so that people can connect with you through it!"
         )
        return LINKEDIN

async def linkedin (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global users
    users[str(update.effective_user.id)]["linkedin"]=update.message.text
    if(users[str(update.effective_user.id)]["linkedin"].startswith("https://www.linkedin.com/")):
        await update.message.reply_text(
        "Great!\n"
        "Let me help you find people of similar intrest ! \n"
        "Share your three intrest areas sererated by commas \n\n\n" 
        "eg: crypto , tech  , web3\n"
        "you can change these interests later on😄"
        )
        return INTREST

    await update.message.reply_text(
            "THAT DOSENT SEEM LIKE A VALID LINKEDIN URL , MAYBE TRY ENTERING YOUR LINKEDIN URL AGAIN!?"
    )
    return LINKEDIN

async def intrest (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global users
    reply_keyboard = [["UPDATE CURRENT INTRESTS!", "FIND CONNECTIONS!", "SEE REQUESTS"]]
    if(len(users[str(update.effective_user.id)]["intrest_list"])==0):
        message=update.message.text
        message = message.replace(' ', '')
        users[str(update.effective_user.id)]["intrest_list"]=message
        cursor.execute("INSERT INTO users2 (id, name, bio , linkedin , intrest ) VALUES (?, ?, ?, ? , ?)", 
        (
        str(update.effective_user.id) , 
        users[str(update.effective_user.id)]["name"]  , 
        users[str(update.effective_user.id)]["bio"] , 
        users[str(update.effective_user.id)]["linkedin"] , 
        users[str(update.effective_user.id)]["intrest_list"] 
        
        ))
        conn.commit()
        updatedtext = json.dumps(message.split())
        await update.message.reply_text(
            "GOT TO KNOW YOUR INTREST  🚀\n"
            "LETS GET YOU STARTED 🚀 🚀" , 
            reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )
        return HELPER
    else:
        message=update.message.text
        message = message.replace(' ', '')
        users[str(update.effective_user.id)]["intrest_list"]=message
        x=str(update.effective_user.id)
        cursor.execute("UPDATE users2 SET intrest = ? WHERE id = ?" ,( message , str(update.effective_user.id)))
        conn.commit()
        await update.message.reply_text(
            "UPDATED YOUR INTREST , LESSGOO 🚀 \n"
            "LETS GET BACK WHERE YOU LEFT OFF\n" , 
            reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder="CHOOSE FROM THE BUTTONS BELOW 👇"
            ),
        )
        return HELPER

#HELPER FUNCITON IS USED TO SHOW LIKE UK , WHERE TO GO AFTER SELECTING SOMETHING FROM THE INLINE KEYBOAD
async def helper (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    global users
    option=update.message.text
    if(option=="UPDATE CURRENT INTRESTS!"):
        await update.message.reply_text(
       "lets updates your intrests\n\n PLEASE ENTER YOUR NEW INTRESTS BELOW"  ,  reply_markup=ReplyKeyboardRemove(),
        )
        return  INTREST
    elif(option=="FIND CONNECTIONS!"):
        await update.message.reply_text("FINDING USERS FOR YOU")
        x=str(update.effective_user.id)
        cursor.execute("SELECT intrest FROM users2 WHERE  id=?" , (x , ))
        rows = cursor.fetchone()
        message=rows[0]
        intrest_list=message.split(',')
        users[str(update.effective_user.id)]["user"]={}
        users[str(update.effective_user.id)]["x"]=0
        for i in intrest_list : 
            query = "SELECT * FROM users2 WHERE intrest LIKE '%{}%'".format(i)
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                id = row[0]
                name = row[1]
                bio = row[2]
                linkedin = row[3]
                intrest= row[4]
                users[str(update.effective_user.id)]["user"][users[str(update.effective_user.id)]["x"]]= {
                    "id" : id , 
                    "name": name,
                    "bio": bio,
                    "linkedin": linkedin,
                    "intrest": intrest
                }
                users[str(update.effective_user.id)]["x"]+=1
        if(len(users)==0):
            await update.message.reply_text("NO USERS FOUND , MAYBE TRY AGAIN LATER ?")
            return HELPER
        else : 
            # print("there are the potential user \n")
            # print(users[str(update.effective_user.id)]["user"])
            users[str(update.effective_user.id)]["keys"]=list( users[str(update.effective_user.id)]["user"].keys())
            random.shuffle(users[str(update.effective_user.id)]["keys"])
            users[str(update.effective_user.id)]["size"]=0
            return DISPLAYUSER

async def displayuser (update: Update, context: ContextTypes.DEFAULT_TYPE) :
    global users
    if(users[str(update.effective_user.id)]["size"]==len(users[str(update.effective_user.id)]["keys"])-1):
        reply_keyboard = [["UPDATE CURRENT INTRESTS!", "FIND CONNECTIONS!", "SEE REQUESTS"]]
        await update.message.reply_text("THATS ALL THE USERS WE FOUND , LETS GET BACK SHALL WE?" , 
           reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True , input_field_placeholder=""
            ),)
        return HELPER
    else :
        print(users[str(update.effective_user.id)]["user"][users[str(update.effective_user.id)]["keys"][users[str(update.effective_user.id)]["size"]]]["name"])
        users[str(update.effective_user.id)]["size"]+=1
        reply_keyboard = [["CONNECT" , "FIND MORE"]]
        await update.message.reply_text( "THINK I'VE FOUND A POTENTIAL USER FOR YOU"
            "FOUND A USER " + "\nNAME: " + users[str(update.effective_user.id)]["user"][users[str(update.effective_user.id)]["keys"][users[str(update.effective_user.id)]["size"]]]["name"]  +
        "\nBIO : " + users[str(update.effective_user.id)]["user"][users[str(update.effective_user.id)]["keys"][users[str(update.effective_user.id)]["size"]]]["bio"] + 
        "\nINTREST :" + users[str(update.effective_user.id)]["user"][users[str(update.effective_user.id)]["keys"][users[str(update.effective_user.id)]["size"]]]["intrest"] , 
                reply_markup=ReplyKeyboardMarkup(
                        reply_keyboard, one_time_keyboard=True , input_field_placeholder=""
        ) , )
        return DISPLAYOPTION


async def displayoption (update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    option=update.message.text
    global users
    if(option=="FIND MORE") : 
        return DISPLAYUSER
    elif(option=="CONNECT"):
        reply_keyboard = [["UPDATE CURRENT INTRESTS!", "FIND CONNECTIONS!", "SEE REQUESTS"]]
        await update.message.reply_text("HERE IS THEIR LINKEDIN ID " + users[str(update.effective_user.id)]["user"][users[str(update.effective_user.id)]["keys"][users[str(update.effective_user.id)]["size"]]]["linkedin"],  
        reply_markup=ReplyKeyboardMarkup(
                        reply_keyboard, one_time_keyboard=True , input_field_placeholder=""
        ) , )
        return HELPER

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






















            OPTION : [MessageHandler(filters.TEXT & ~filters.COMMAND, option)],
            OPTION : [MessageHandler(filters.TEXT & ~filters.COMMAND, option)],
            DESC : [MessageHandler(filters.TEXT & ~filters.COMMAND, desc)],
            LINKEDIN : [MessageHandler(filters.TEXT & ~filters.COMMAND, linkedin)],
            INTREST : [MessageHandler(filters.TEXT & ~filters.COMMAND, intrest)],
            HELPER : [MessageHandler(filters.Regex("^(UPDATE CURRENT INTRESTS!|FIND CONNECTIONS!|SEE REQUESTS)$"), helper)] , 
            DISPLAYUSER : [MessageHandler(filters.TEXT & ~filters.COMMAND, displayuser )] , 
            DISPLAYOPTION : [MessageHandler(filters.TEXT & ~filters.COMMAND, displayoption )] ,
            # INTREST2 : [MessageHandler(filters.TEXT & ~filters.COMMAND, intrest2)],
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