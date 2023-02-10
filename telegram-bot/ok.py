import logging
import pandas as pd
import numpy as np
import openpyxl
import gspread
import google.auth
import json
import time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from telegram.ext import Updater, MessageHandler, Filters , CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

#validate credentials
creds = ServiceAccountCredentials.from_json_keyfile_name('client.json' , scope)
client=gspread.authorize(creds)
sheet=client.open('userdata').sheet1

# Enable logging
service = build('sheets', 'v4', credentials=creds)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
service = build('sheets', 'v4', credentials=creds)
SPREADSHEET_ID='1tgOpO3ytwhtl0mWDijq0B3ssjcjwvu9e6zZT_d_uPtA'

# READING THE VALUES IN THE SPEAD SHEET
spreadsheet = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='A:E').execute()
values = result.get('values', [])
# print(values)

logger = logging.getLogger(__name__)
flag = 0 
there =1
# registered=0
# Define a dictionary to store the user's name and age
user_data = {}

allowed_intrest=["" , "BB" , "CC" , "DD" , "EE" , "FF"]
print(allowed_intrest)


# Define a function that will be called when the bot receives a message
def message(update, context):
    # Get the user's message
    message = update.message.text
    user_id = update.effective_user.id
    
    global flag

    if 'name' not  in user_data :
        if(len(message)>4):
        # The user has already provided their name, so assume they are providing their age
            user_data['name'] = message.capitalize()
            update.message.reply_text(f"NICE TO MEET YOU {user_data['name']}!" )
            update.message.reply_text(f"LET ME KNOW A LITTLE BIT ABOUT YOU!" )
        else :
            update.message.reply_text(f"THAT DOSENT SEEM LIKE YOUR FULL NAME , TRY AGAIN?" )


    elif 'desc' not in user_data and 'name' in user_data :
        if len(message)>50 : 
                user_data['desc'] = message.capitalize()
                update.message.reply_text("THAT A GOOD WAY TO DESC YOURSELF , NOW , ENTER A VALID LINKEDIN ID , AND LETS GET STARTED")
        else:
                update.message.reply_text("THATS VERY LESS ABOUT YOU , HOW ABOUT YOU LET US KNOW MORE AGAIN! , MAKE IT A MINIMUM 50")


    elif 'linkedin' not in user_data and 'desc' in user_data :
        temp="https://www.linkedin.com/"
        if(message.startswith(temp) and len(message)>len(temp)):
            user_data['linkedin'] = message
            update.message.reply_text("COOL , NOW LET US KNOW YOUR FIELD OF INTREST")
            update.message.reply_text("ENTER YOUR FIELDS OF INTREST SEPRATED BY SINGLE SPACES ,KINDA LIKE THIS \n")
            time.sleep(1)
            update.message.reply_text("\ncrypto blockchain web3")
        else:
            update.message.reply_text("DOSENT SEEM LIKE A VALID LINKEDIN URL , TRY AGAIN MAYBE?")


    elif 'intrest' not in user_data and 'linkedin' in user_data : 
        message=message.upper()
        intrest_list=message.split()
        print(intrest_list)
        global result
        global values
        if(len(intrest_list)<=3):
            intrest_list_set=set(intrest_list)     
            checker=1    
            for i in intrest_list_set : 
                if i not in allowed_intrest : 
                    checker=0
                    update.message.reply_text('OOPS , CURRENTLY THERE ARE NO PEOPLE IN "' + i+'" CATEGORY , MAYBE ADD SOMETHING ELSE INSTEAD OF IT?')
            if checker==1:
                updatedtext = json.dumps(message.split())
                user_data['intrest']=message
                update.message.reply_text("NOW WE ARE READT TO GO 🚀")
                sheet.append_row([user_id , user_data['name'] ,user_data['desc'] ,user_data['linkedin'] , updatedtext ])
                update.message.reply_text("WELCOME TO THE CLUB BUD 🚀")
                #making sure to get the most updated value
                result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='A:E').execute()
                0
        else: 
            update.message.reply_text("OOPS , THATS TOO MUCH DATA TO HANDLE , HOW ABOUT WE REDUCE IT DOWN TO THREE OR LESS?")






def main():
    updater = Updater("5988401652:AAHHWkTChtJ6wOzFSmfJYx1hREYZefqXsbw", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()




# function to update the intrests 
    # if message.startswith("Update"):   
    #     lis=message.split()
    #     lis.pop(0)
    #     updatedtext = json.dumps(lis)
    #     for row in values:
    #         if row[0]==str(user_id):
    #             print("found"     )
    #             service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,range=f'E{values.index(row)+1}',valueInputOption='RAW',body={'values': [[updatedtext]]}).execute()
    #             update.message.reply_text("UPDATED YOUR INTRESTS!")
    #             print("done")
    #             break


# function to allow only new users
    # global registered
    # if(registered==0) : 
    #     for row in values :
    #         if(row[0]==str(user_id)) : 
    #             registered=1
    #             update.message.reply_text(f"HEY {row[1]}  , WELCOME BACK♥ {row[1]}")
    # if registered==0 and (flag==0 or message=="/start" or message=="hi" or message=="Hi" ):
    #     update.message.reply_text(f"WELCOME ♥ ")
    #     update.message.reply_text(f"LOOKS LIKE YOU ARE A NEW USER! PLEASE ENTER YOUR NAME!")
    #     flag=1


# function to find user 
    # find=["Web3" , "crypto" , "aja"]
    # result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='A:E').execute()
    # values = result.get('values', [])
    # potential_user=[]
    # for i in find :
    #     for j in values:
    #         if(j[4].find(i)!=-1):
    #                 user=[]
    #                 user.append(j[1])
    #                 user.append(j[2])
    #                 user.append(j[3])
    #                 user.append(j[4])
    #                 potential_user.append(user)
    #                 update.message.reply_text("found user ")
    # print(potential_user)