import pygame
from pygame import mixer# getting mixer
import pygame_menu
# will help to make ther grpahs
from matplotlib import pyplot as plt
import numpy as np

import screen_brightness_control as sbc
import random
import smtplib
from email.message import EmailMessage
from typing import Tuple, Optional
import sqlite3
import re
import csv
import os
#initisilising pygame and mixer
pygame.init()
mixer.init()


#defining global variables
global title_screen
global sound
global screen

#defining the contstants
SCREEN_HEIGHT = 1500
SCREEN_WIDTH = 900
FPS = 60
paused = False
music_on = False
x_scroll = 0
y_scroll = 0
bg_scroll = 0
level = 1

# what charctaer it will display; 1 is for red player and 2 is for the blue player.
character_value = 1# initilising the vairbale


#creating the internal clock
clock = pygame.time.Clock()
#Creating the screen
screen = pygame.display.set_mode((SCREEN_HEIGHT, SCREEN_WIDTH))

#loading in background
background_img = pygame.image.load("C:\Al Faysal\python\game_background_3\\background.png")#  loading in the backgorund image for the GUI
menu_img = pygame.image.load("C:\Al Faysal\python\game_background_3\\menu_bg.png")# loading in the image for the instructions/controls page


# creating a font for the leaderboard
Lfont = pygame.font.Font(None,80)
# setting sound
sound = pygame_menu.sound.Sound()
sound.load_example_sounds()#loading built in sounds



# prints all the columns/ data that's in the database.
conn = sqlite3.connect("Player-data.db")
cur = conn.cursor()
cur.execute("SELECT * FROM Player")
datas = cur.fetchall()
for data in datas:
    print(data)


# prints all the columns/ data that's in the database.
conn = sqlite3.connect("Player-data.db")
cur = conn.cursor()
cur.execute("""SELECT username, score1 AS score, 'level 1' FROM Player 
UNION ALL
SELECT  username, score2 AS score, 'level 2'  FROM Player
UNION ALL
SELECT  username, score3 AS score, 'level 3' FROM Player
ORDER BY score DESC LIMIT 6;

""")# putting each levels into one large list and then ordering it, for every level putting it into a variable so it can be called later
# outputs username, score and then the level it was acheived on in that order
datas = cur.fetchall()
for data in datas:
    print(data)

    
def graph1():# graph for level 1
    # gets the data for the graph
    conn = sqlite3.connect("Player-data.db")
    cur = conn.cursor()
    cur.execute("SELECT score1 FROM Player ORDER BY score1 NULLS FIRST; ")# orders database in ascending order by the score 1 column
    datas = cur.fetchall()
    list1 = []# the scores in yhe x avis
    list2 = []# the cumalitve frequency at the y axis
    frequency = 0
    for data in datas:
        frequency += 1# keeps track of the number tha tit's on
        list2.append(frequency)
        values = f"{data[0]}"
        if values == "None":
            values = 0
        else:
            values = int(values)# making the vlaues all turn into integers
        list1.append(values)

    graph = np.cumsum(list1)

    #creatign the figure and the axis
    plt.plot(list1 , list2, marker = "o")
    plt.xlabel("score")
    plt.ylabel("cumalitve frequency")
    plt.title("level 1 score")
    plt.grid(True)# adds in the grid
    plt.show()

def graph2():# graph for level 2
    # gets the data for the graph
    conn = sqlite3.connect("Player-data.db")
    cur = conn.cursor()
    cur.execute("SELECT score2 FROM Player ORDER BY score2 NULLS FIRST; ")# orders database in ascending order by the score 2 column
    datas = cur.fetchall()
    list1 = []# the scores in yhe x avis
    list2 = []# the cumalitve frequency at the y axis
    frequency = 0
    for data in datas:
        frequency += 1# keeps track of the number tha tit's on
        list2.append(frequency)
        values = f"{data[0]}"
        if values == "None":
            values = 0
        else:
            values = int(values)# making the vlaues all turn into integers
        list1.append(values)

    graph = np.cumsum(list1)

    #creatign the figure and the axis
    plt.plot(list1 , list2, marker = "o")
    plt.xlabel("score")
    plt.ylabel("cumalitve frequency")
    plt.title("level 2 score")
    plt.grid(True)# adds in the grid
    plt.show()

def graph3(): # graph for level 3 
    # gets the data for the graph
    conn = sqlite3.connect("Player-data.db")
    cur = conn.cursor()
    cur.execute("SELECT score3 FROM Player ORDER BY score3 NULLS FIRST; ")# orders database in ascendingorder by the score 3 column
    datas = cur.fetchall()
    list1 = []# the scores in yhe x avis
    list2 = []# the cumalitve frequency at the y axis
    frequency = 0
    for data in datas:
        frequency += 1# keeps track of the number tha tit's on
        list2.append(frequency)
        values = f"{data[0]}"
        if values == "None":
            values = 0
        else:
            values = int(values)# making the vlaues all turn into integers
        list1.append(values)

    graph = np.cumsum(list1)

    #creatign the figure and the axis
    plt.plot(list1 , list2, marker = "o")
    plt.xlabel("score")
    plt.ylabel("cumalitve frequency")
    plt.title("level 3 score")
    plt.grid(True)# adds in the grid
    plt.show()

def graphall():
    conn = sqlite3.connect("Player-data.db")
    cur = conn.cursor()
    cur.execute(""" SELECT score1 AS score FROM Player 
    UNION ALL
    SELECT score2 AS score FROM Player
    UNION ALL
    SELECT score3 AS score FROM Player
    ORDER BY score NULLS FIRST;

    """)# putting each levels into one large list and then ordering it, for every level putting it into a variable so it can be called later
    # outputs username, score and then the level it was acheived on in that order
    datas = cur.fetchall()
    list1 = []# the scores in yhe x avis
    list2 = []# the cumalitve frequency at the y axis
    frequency = 0
    for data in datas:
        frequency += 1# keeps track of the number tha tit's on
        list2.append(frequency)
        values = f"{data[0]}"
        if values == "None":
            values = 0
        else:
            values = int(values)# making the vlaues all turn into integers
        list1.append(values)

    graph = np.cumsum(list1)

    #creatign the figure and the axis
    plt.plot(list1 , list2, marker = "o")
    plt.xlabel("score")
    plt.ylabel("cumalitve frequency")
    plt.title("all level  score")
    plt.grid(True)# adds in the grid
    plt.show()

        
def update_music( enabled: bool) -> None:# the music for the GUI
    global music_on
    
    if enabled:
        music_on = True
        pygame.mixer.music.load("C:\Al Faysal\python\sound\GUI.mp3 ")# the GUI music
        pygame.mixer.music.set_volume(0.6)#adjust the volume
        pygame.mixer.music.play(-1, 0.0, 5000)# -1 means that it'll loop forever.
       
    else:
        music_on = False
        pygame.mixer.music.stop()
        


def update_menu_sound( enabled: bool) -> None:# the sound effects for the GUI

   
    if enabled:
        title_screen.set_sound(sound, recursive=True)
        print('sound is on')
    else:
        title_screen.set_sound(None, recursive=True)
        print('sound is off')


def background():
    screen.fill((255, 255, 255))
    screen.blit(background_img,(0,0))

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' #validating email address


def account_input():
    username_data = create_user.get_value()
    password_data = create_password .get_value()
    renter_password_data = renter_password.get_value()
    email_address  = emailtext.get_value()#gets the string inputted into the entry field

    conn = sqlite3.connect("Player-data.db")
    data_insert_query = """INSERT INTO PLAYER (username, password, email)Values
    (?, ?, ?)"""
    data_insert_tuple = (username_data, password_data, email_address)
    
    if (re.search(regex,email_address)):      
        enter_accountbtn.readonly = False# if everthing is ok then the button will not be disbaled anymore.
        account_verify.hide()# hides any prevois error messages.
        
        conn.execute(data_insert_query, data_insert_tuple)#     sometimes it doesn't work as there is a space before the text is entred into the entry field
        conn.commit()
        conn.execute("DELETE FROM Player WHERE rowid NOT IN( SELECT min( rowid) FROM Player GROUP BY username);")
        conn.commit()

        conn.close()#puts data into a database.

            
   
    else:
        enter_accountbtn.readonly = True
        account_verify.set_title("email in incorrect form")# if email in incorrect form then prints an error message.
        account_verify.show()
    
    
    if username_data == "":
        account_verify.set_title("please enter something into the entry fields")# checks that something is entered into the user name entry field.
        account_verify.show()
        enter_accountbtn.readonly = True

       
    elif len(username_data)<= 3:
        account_verify.set_title("username must be at least 3 characters.")#checks if username is at least 3 characters long.
        account_verify.show()
        enter_accountbtn.readonly = True
   
                   

    elif len(password_data) <= 10:
        account_verify.set_title("password must be at least 10 characters.")#checks if password is at least 10 characters long.
        account_verify.show()
        enter_accountbtn.readonly = True
        
    elif re.search(r'[!@#$£%&]', password_data) is None:
         account_verify.set_title("Password must conatain at least one special character.")#checks if password contains special character.
         account_verify.show()
         enter_accountbtn.readonly = True
         
    elif re.search(r'\d', password_data) is None:
         account_verify.set_title("password must contain numbers")#checks if password contains any numbers.
         account_verify.show()
         enter_accountbtn.readonly = True
         
    elif re.search('[A-Z]', password_data) is None:
         account_verify.set_title("password must contain at least one capital letter.")#checks if password has capital letters in it.
         account_verify.show()
         enter_accountbtn.readonly = True

        
    elif password_data == "":
        account_verify.set_title("please enter something into the entry fields")# checks if something is inputted into the password entry field.
        account_verify.show()
        enter_accountbtn.readonly = True

    elif renter_password_data == "":
        account_verify.set_title("please enter something into the entry fields")#checks if something is inputted into the confrim password entry field.
        account_verify.show()
        enter_accountbtn.readonly = True

    elif renter_password_data != password_data:
        account_verify.set_title("the password rentered must be equal to the password that was just set")# checks if the input for the password entry field is different to the input of the confirm password entry field.
        account_verify.show()
        enter_accountbtn.readonly = True

    elif email_address == "":#checks if something is entred into the email address entry field.
        account_verify.set_title("please enter something into the entry field.")
        account_verify.show()
        enter_accountbtn.readonly = True


def register_input():
    
    code_input = str(entercode.get_value())# checks to see if the input at theenter code entry field is
                                            #is the same as the string value of the random 8 digit number

    if code_input == number:
        enter_registerbtn.readonly = False
    else:
        register_verify.set_title("Incorrect code; please try again")
        register_verify.show()
        enter_registerbtn.readonly = True
        
    



def forgotten_input():
    Fusername = new_username.get_value()
    Femail = email_forgotten.get_value()
    Fpassword = new_password.get_value()
    Fconfirm = confirm_password.get_value()

    conn = sqlite3.connect("Player-data.db")# connects to databse
    cur = conn.cursor()
    statment1 = f"SELECT username from Player WHERE username='{Fusername}' AND email = '{Femail}';"# selects the username and password of the first user
    cur.execute(statment1)# executs command
    conn.commit()
    update_query = "UPDATE Player SET password = (?) where username = (?)"# statement which will help to update the table.
    update_tuple = (Fpassword, Fusername)# tuple containing the variables which will be placed into the question marks
    if len(Fpassword) <= 10:
        verify_forgotten.set_title("password must be at least 10 characters.")#checks if password is at least 10 characters long.
        verify_forgotten.show()
        enter_forgotbtn.readonly = True
    elif re.search(r'[!@#$£%&]', Fpassword) is None:
         verify_forgotten.set_title("Password must conatain at least one special character.")#checks if password contains special character.
         verify_forgotten.show()
         enter_forgotbtn.readonly = True
    elif re.search(r'\d', Fpassword) is None:
         verify_forgotten.set_title("password must contain numbers")#checks if password contains any numbers.
         verify_forgotten.show()
         enter_forgotbtn.readonly = True
    elif re.search('[A-Z]', Fpassword) is None:
         verify_forgotten.set_title("password must contain at least one capital letter.")#checks if password has capital letters in it.
         verify_forgotten.show()
         enter_forgotbtn.readonly = True

        
    elif Fpassword == "":
        verify_forgotten.set_title("please enter something into the entry fields")# checks if something is inputted into the password entry field.
        verify_forgotten.show()
        enter_forgotbtn.readonly = True

    elif Fconfirm == "":
        verify_forgotten.set_title("please enter something into the entry fields")#checks if something is inputted into the confrim password entry field.
        verify_forgotten.show()
        enter_forgotbtn.readonly = True

    elif Fconfirm != Fpassword:
        verify_forgotten.set_title("the password rentered must be equal to the password that was just set")# checks if the input for the password entry field is different to the input of the confirm password entry field.
        verify_forgotten.show()
        enter_forgotbtn.readonly = True
    elif not cur.fetchone():# if username/ password input is not in database; buttton won't work
        verify_forgotten.set_title("incorrect user details; please try again")
        verify_forgotten.show()
        enter_forgotbtn.readonly = True
    elif cur.fetchone:# if username/email input is in the databse; button will work.
        enter_forgotbtn.readonly = False
        verify_forgotten.hide()
        cur.execute(update_query, update_tuple)# will update the new password into the database.
        conn.commit()
#        cur.execute("SELECT * FROM Player")# comment this out if you have db browser.
#        print(cur.fetchall())# also comment this out if you have db browser.
def login_input():
    Lusername = username.get_value()# gets value form the username entry field.
    Lpassword = password.get_value()# gets value from the password entry field.

    conn = sqlite3.connect("Player-data.db")# connects to databse
    cur = conn.cursor()
    statment = f"SELECT username from Player WHERE username='{Lusername}' AND Password = '{Lpassword}';"# selects the username and password of the first user
    cur.execute(statment)# executs command
    conn.commit()
    

    if not cur.fetchone():# if username/ password input is not in database; buttton won't work
        login_verify.set_title("incorrect user details; please try again")
        login_verify.show()
        enter_login.readonly = True
    else:# if username/password input is in the database; button will work.
        enter_login.readonly = False
        login_verify.hide()
        

    


number = str(random.randint(10000000, 99999999))
print(number)




# These functions will determine which player will be displayed.If it is recorded as "M" in the database then itll display the red player
#if it's recorded as "F" then it'll display the blue player.
        
def change_M():# function when user registers

    username_data = create_user.get_value()#  gets the value of the username entered in the registration page
    
    conn = sqlite3.connect("Player-data.db")# connects to databse
    cur = conn.cursor()
    char_update_query=  """UPDATE Player SET gender = 'M' where username = (?); """
    update_tuple = (username_data,)
    cur.execute(char_update_query, update_tuple)
    conn.commit()
    conn.close()
    characterbtn.readonly = False
    


def change_F():# function when user registers
    
    username_data = create_user.get_value() #  gets the value of the username entered in the registration page
    
    conn = sqlite3.connect("Player-data.db")# connects to databse
    cur = conn.cursor()
    char_update_query=  """UPDATE Player SET gender = 'F' where username = (?); """
    update_tuple = (username_data,)
    cur.execute(char_update_query, update_tuple)
    conn.commit()
    conn.close()
    characterbtn.readonly = False


def switch_M():# function if user switches from settings page
    Lusername = username.get_value()
    conn = sqlite3.connect("Player-data.db")# connects to databse
    cur = conn.cursor()
    char_update_query=  """UPDATE Player SET gender = 'M' where username = (?); """
    update_tuple = (Lusername,)
    cur.execute(char_update_query, update_tuple)
    conn.commit()
    conn.close()

def switch_F():# function if user switches from settings page
    Lusername = username.get_value()
    conn = sqlite3.connect("Player-data.db")# connects to databse
    cur = conn.cursor()
    char_update_query=  """UPDATE Player SET gender = 'F' where username = (?); """
    update_tuple = (Lusername,)
    cur.execute(char_update_query, update_tuple)
    conn.commit()
    conn.close()

def leadscore1():# gets the database
    game_state.state_handler = game_state.Lscore1

def leadscore2():
    game_state.state_handler = game_state.Lscore2

def leadscore3():
    game_state.state_handler = game_state.Lscore3
def allscore():
    game_state.state_handler = game_state.score_all


# creating a theme
NONE = pygame_menu.widgets.MENUBAR_STYLE_NONE
theme1 = pygame_menu.themes.Theme(background_color = (211, 211, 211, 211),
                title_bar_style = NONE,
                widget_padding = 10)

theme2 = pygame_menu.themes.Theme(background_color = (255, 255, 255, 50), # creating a themse for the instructions page
                title_bar_style = NONE,
                widget_padding = 10)
instructions_img = pygame_menu.baseimage.BaseImage(
    "C:\Al Faysal\python\game_background_3\controls.png",# loading in image
     pygame_menu.baseimage.IMAGE_MODE_FILL,(0,0))

theme2.background_color = instructions_img# making the backgorund color the image for the second theme

#defining page variables:
title_screen = pygame_menu.Menu(" ", SCREEN_HEIGHT,
                                SCREEN_WIDTH, theme = theme1)#creates the body and theme of the title screen


Login_page = pygame_menu.Menu(" ", SCREEN_HEIGHT, SCREEN_WIDTH, theme = theme1)
Forgotten_page = pygame_menu.Menu("  ", SCREEN_HEIGHT, SCREEN_WIDTH, theme = theme1)
registration_page = pygame_menu.Menu("  ", SCREEN_HEIGHT, SCREEN_WIDTH, theme = theme1)
account_page =  pygame_menu.Menu("  ", SCREEN_HEIGHT, SCREEN_WIDTH, theme = theme1)
character_page = pygame_menu.Menu("  ", SCREEN_HEIGHT, SCREEN_WIDTH, theme = theme1)
main_menu_page = pygame_menu.Menu("  ", SCREEN_HEIGHT, SCREEN_WIDTH, theme = theme1)
instructions_page = pygame_menu.Menu("  ", SCREEN_HEIGHT, SCREEN_WIDTH, theme = theme2)
level_page =  pygame_menu.Menu("  ", SCREEN_HEIGHT, SCREEN_WIDTH, theme = theme1)
leaderboard_menu_page =  pygame_menu.Menu("  ", SCREEN_HEIGHT, SCREEN_WIDTH, theme = theme1)
settings_page =  pygame_menu.Menu("  ", SCREEN_HEIGHT, SCREEN_WIDTH, theme = theme1)
###  creating the title screen ###

loginbtn = title_screen.add.button("Login", Login_page)
registerbtn = title_screen.add.button("Register", account_page)
title = title_screen.add.label("wanderer's adventure", font_size = 125)


SFX_switch1 = title_screen.add.toggle_switch("SFX ", 0, single_click = True,# the sound effects
                                             state_text = ( "OFF" , "ON" ),
                                            state_values = (False, True), onchange = update_menu_sound)


music_switch1 = title_screen.add.toggle_switch("music", 0, single_click = True,
                                               state_text = ("OFF", "ON"), state_values = (False, True), onchange = update_music)# the music


    #moving; scaling; settinging border; and setting a background color to the buttons.
loginbtn.set_border(3, (0, 0, 0), inflate = (0,0))
loginbtn.set_background_color((229, 228, 226), inflate = (0,0))
loginbtn.resize(180, 90, smooth = True)
loginbtn.translate(20,50)



registerbtn.set_border(3, (0, 0, 0), inflate = (0,0))
registerbtn.set_background_color((229, 228, 226), inflate = (0,0))
registerbtn.resize(180, 90, smooth = True)
registerbtn.translate(20,100)


SFX_switch1.translate(-600, 200)
music_switch1.translate(-610, 50)
    #movin the title:
title.translate(0, -350)

###  creating the login page ###

username = Login_page.add.text_input("username:", default = "", maxchar = 15, input_underline = '_')
password = Login_page.add.text_input("Password:", maxchar = 20, password = True,
                                     input_underline='_', maxwidth = 25)
forgotbtn = Login_page.add.button("forgotten password?", Forgotten_page)
backbtn = Login_page.add.button("back", pygame_menu.events.BACK)
Login = Login_page.add.label("Logging in", font_size = 75)
enter_login = Login_page.add.button("Enter", main_menu_page)
login_verify = Login_page.add.label(" ", font_size = 34, font_color =(255, 0, 0))


Login.translate(0, -500)

username.set_border(3, (0, 0, 0), inflate = (0,0))
username.set_background_color((229, 228, 226), inflate = (0,0))
username.translate(0, 60)
username.set_padding((15, 90, 5, 10))


password.set_border(3, (0, 0, 0), inflate = (0,0))
password.set_background_color((229, 228, 226), inflate = (0,0))
password.translate(0, 90)

forgotbtn.translate(0, 85)

enter_login.set_border(3, (0, 0, 0), inflate = (0,0))
enter_login.set_background_color((229, 228, 226), inflate = (0,0))
enter_login.resize(110, 55, smooth = True)
enter_login.translate(300,-150)
enter_login.set_onselect(login_input)
enter_login.readonly = True


backbtn.set_border(3, (0, 0, 0), inflate = (0,0))
backbtn.set_background_color((229, 228, 226), inflate = (0,0))
backbtn.resize(180, 90, smooth = True)
backbtn.translate(-600,290)

login_verify.hide()

###  creating the forgotten password page ###
new_username = Forgotten_page.add.text_input("Enter username:", default = "",input_underline='_', maxchar = 15)
#text entry field for email addess in forgotten password page
email_forgotten = Forgotten_page.add.text_input("Enter email address:", default = "",input_underline='_', maxchar = 31)
new_password = Forgotten_page.add.text_input("Enter new Password:", password = True,  maxchar = 20, input_underline='_')
confirm_password = Forgotten_page.add.text_input("Confirm Password:", password = True, maxchar = 20, input_underline='_')
backbtn = Forgotten_page.add.button("back", pygame_menu.events.BACK)
forgotten_password = Forgotten_page.add.label("forgotten password", font_size = 75)
enter_forgotbtn = Forgotten_page.add.button("Enter", pygame_menu.events.BACK, back_count = 2)
verify_forgotten = Forgotten_page.add.label(" ", font_size = 34, font_color =(255, 0, 0))

forgotten_password.translate(0, -500)


new_username.set_border(3, (0, 0, 0), inflate = (0,0))
new_username.set_background_color((229, 228, 226), inflate = (0,0))
new_username.translate(0, 60)
new_username.set_padding((5, 410, 5, 10))

new_password.set_border(3, (0, 0, 0), inflate = (0,0))
new_password.set_background_color((229, 228, 226), inflate = (0,0))
new_password.translate(0, 120)
new_password.set_padding((5, 365, 5, 10))

confirm_password.set_border(3, (0, 0, 0), inflate = (0,0))
confirm_password.set_background_color((229, 228, 226), inflate = (0,0))
confirm_password.translate(0, 150)
confirm_password.set_padding((5, 395, 5, 10))

email_forgotten.set_border(3, (0, 0, 0), inflate = (0,0))
email_forgotten.set_background_color((229, 228, 226), inflate = (0,0))
email_forgotten.translate(0, 90)

enter_forgotbtn.set_border(3, (0, 0, 0), inflate = (0,0))
enter_forgotbtn.set_background_color((229, 228, 226), inflate = (0,0))
enter_forgotbtn.resize(110, 55, smooth = True)
enter_forgotbtn.translate(300,-50)
enter_forgotbtn.set_onselect(forgotten_input)# only prints one set of inputs(could be because of multiple events?)
enter_forgotbtn.readonly = True

backbtn.set_border(3, (0, 0, 0), inflate = (0,0))
backbtn.set_background_color((229, 228, 226), inflate = (0,0))
backbtn.resize(180, 90, smooth = True)
backbtn.translate(300,45)
# to avoid back button error you have to make the variable be bthe same e.g same backbtn variable to each of the pages.
backbtn.translate(-600,290)

verify_forgotten.translate(0, -30)
verify_forgotten.hide()



### creating the account creation page ###


create_user = account_page.add.text_input("create username:", default = "", maxchar = 15, input_underline='_')
create_password = account_page.add.text_input("create password:", password = True, maxchar = 20, input_underline='_')
renter_password = account_page.add.text_input("confirm password:", password = True,  maxchar = 20, input_underline='_')
emailtext = account_page.add.text_input("Enter email address:", default = "", input_underline='_', maxchar = 31)
enter_accountbtn = account_page.add.button("Enter", registration_page)
backbtn = account_page.add.button("back",pygame_menu.events.BACK)
account_creation = account_page.add.label("Account creation", font_size = 75)
account_verify = account_page.add.label(" ", font_size = 34, font_color =(255, 0, 0))


create_user.set_border(3, (0, 0, 0), inflate = (0,0))
create_user.set_background_color((229, 228, 226), inflate = (0,0))
create_user.translate(5, 60)
create_user.set_padding((10, 400, 10, 10))

create_password.set_border(3, (0, 0, 0), inflate = (0,0))
create_password.set_background_color((229, 228, 226), inflate = (0,0))
create_password.translate(5, 120)
create_password.set_padding((10, 400, 10, 10))

renter_password.set_border(3, (0, 0, 0), inflate = (0,0))
renter_password.set_background_color((229, 228, 226), inflate = (0,0))
renter_password.translate(5, 150)
renter_password.set_padding((10, 395, 0, 5))


enter_accountbtn.set_border(3, (0, 0, 0), inflate = (0,0))
enter_accountbtn.set_background_color((229, 228, 226), inflate = (0,0))
enter_accountbtn.resize(110, 55, smooth = True)
enter_accountbtn.translate(500,230)
enter_accountbtn.readonly = True
enter_accountbtn.set_onselect(account_input)



emailtext.set_border(3, (0, 0, 0), inflate = (0,0))
emailtext.set_background_color((229, 228, 226), inflate = (0,0))
emailtext.translate(0, 185)

backbtn.set_border(3, (0, 0, 0), inflate = (0,0))
backbtn.set_background_color((229, 228, 226), inflate = (0,0))
backbtn.resize(180, 90, smooth = True)
backbtn.translate(-550,271)

account_verify.hide()


account_creation.translate(0, -535)

### sending code ####

EMAIL_ADDRESS = "testgame04072006@gmail.com"
EMAIL_PASSWORD = "hbgl ongt ceui gduc"

def send_email():    
    msg = EmailMessage()
    msg["subject"] = "your 8 digit code"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = emailtext.get_value()
    msg.set_content( "your 8 digit code is:  " + number)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)# logging into the gmail account of the sender.

        smtp.send_message(msg)

### creating the registration page ###

entercode = registration_page.add.text_input("Enter 8 digit code:",  maxchar = 8, input_underline='_',
                                             input_type=pygame_menu.locals.INPUT_INT)
resendbtn = registration_page.add.button("send code", send_email)
enter_registerbtn = registration_page.add.button("Enter", character_page)
register = registration_page.add.label("Registration process", font_size = 75)
backbtn = registration_page.add.button("back",pygame_menu.events.BACK)
register_verify =registration_page.add.label(" ", font_size = 34, font_color =(255, 0, 0))

register.translate(0, -450)


entercode.set_border(3, (0, 0, 0), inflate = (0,0))
entercode.set_background_color((229, 228, 226), inflate = (0,0))
entercode.translate(0, 0)

enter_registerbtn.set_border(3, (0, 0, 0), inflate = (0,0))
enter_registerbtn.set_background_color((229, 228, 226), inflate = (0,0))
enter_registerbtn.resize(110, 55, smooth = True)
enter_registerbtn.translate(150,-35)
enter_registerbtn.set_onselect(register_input)
enter_registerbtn.readonly = True

resendbtn.set_border(3, (0, 0, 0), inflate = (0,0))
resendbtn.set_background_color((229, 228, 226), inflate = (0,0))
resendbtn.resize(110, 55, smooth = True)
resendbtn.translate(-180,20)


backbtn.set_border(3, (0, 0, 0), inflate = (0,0))
backbtn.set_background_color((229, 228, 226), inflate = (0,0))
backbtn.resize(180, 90, smooth = True)
backbtn.translate(-550,150)

register_verify.hide()

### creating the character page ###


# image for charcater1
character1 =  character_page.add.button(" ", change_M, background_color =  pygame_menu.baseimage.BaseImage(
    "C:\Al Faysal\python\characters\player1\idle\\0.png",# loading in image of charcater1
     pygame_menu.baseimage.IMAGE_MODE_FILL,(0,0)))
                            
# image for charcater2
character2 =   character_page.add.button(" ", change_F, background_color =  pygame_menu.baseimage.BaseImage(
    "C:\Al Faysal\python\characters\player2\idle\\0.png",# loading in image of character2 
     pygame_menu.baseimage.IMAGE_MODE_FILL,(0,0)))



choosecharacter = character_page.add.label("Choose your character", font_size = 75)
backbtn = character_page.add.button("back",pygame_menu.events.BACK)
characterbtn = character_page.add.button("Enter", main_menu_page)



character1.set_border(3, (0, 0, 0), inflate = (0,0))
character1.resize(100, 150, smooth = True)
character1.translate(-250,320)
character1.set_padding((50, 50))


character2.set_border(3, (0, 0, 0), inflate = (0,0))
character2.resize(100, 150, smooth = True)
character2.translate(150,-25)
character2.set_padding((50, 50))




choosecharacter.translate(0,-700)


backbtn.set_border(3, (0, 0, 0), inflate = (0,0))
backbtn.set_background_color((229, 228, 226), inflate = (0,0))
backbtn.resize(180, 90, smooth = True)
backbtn.translate(-550,-100)

characterbtn.set_border(3, (0, 0, 0), inflate = (0,0))
characterbtn.set_background_color((229, 228, 226), inflate = (0,0))
characterbtn.resize(110, 55, smooth = True)
characterbtn.translate(500,-250)

characterbtn.readonly = True


### creating the main menu page ###
settingsbtn = main_menu_page.add.button("settings", settings_page)
leaderboardbtn = main_menu_page.add.button("Leaderboard", leaderboard_menu_page)
levelselectbtn = main_menu_page.add.button("Play", level_page)
instructionbtn = main_menu_page.add.button("instructions", instructions_page)
Exitbtn = main_menu_page.add.button("Exit", pygame.QUIT )
Main_menu = main_menu_page.add.label("Main menu", font_size = 75)



settingsbtn.set_border(3, (0, 0, 0), inflate = (0,0))
settingsbtn.set_background_color((229, 228, 226), inflate = (0,0))
settingsbtn.resize(110, 55, smooth = True)
settingsbtn.translate(450,-95)
settingsbtn.set_padding((10, 10))

instructionbtn.set_border(3, (0, 0, 0), inflate = (0,0))
instructionbtn.set_background_color((229, 228, 226), inflate = (0,0))
instructionbtn.resize(110, 55, smooth = True)
instructionbtn.translate(-450,-300)
instructionbtn.set_padding((10, 10))

levelselectbtn.set_border(3, (0, 0, 0), inflate = (0,0))
levelselectbtn.set_background_color((229, 228, 226), inflate = (0,0))
levelselectbtn.resize(180, 90, smooth = True)
levelselectbtn.translate(20,0)

leaderboardbtn.set_border(3, (0, 0, 0), inflate = (0,0))
leaderboardbtn.set_background_color((229, 228, 226), inflate = (0,0))
leaderboardbtn.resize(180, 90, smooth = True)
leaderboardbtn.translate(20,300)







Exitbtn.set_border(3, (0, 0, 0), inflate = (0,0))
Exitbtn.set_background_color((229, 228, 226), inflate = (0,0))
Exitbtn.resize(180, 90, smooth = True)
Exitbtn.translate(-600,240)

Main_menu.translate(0, -550)

### creating the instructions page ###

backbtn = instructions_page.add.button("back",pygame_menu.events.BACK)
instructions = instructions_page.add.label("Instructions", font_size = 75)



backbtn.set_border(3, (0, 0, 0), inflate = (0,0))
backbtn.set_background_color((229, 228, 226), inflate = (0,0))
backbtn.resize(180, 90, smooth = True)
backbtn.translate(-550,300)

instructions.translate(0, -450)




def level1():
    pygame.mixer.music.stop()# stopping the first GUI music
    if music_on == True:
        pygame.mixer.music.load("C:\Al Faysal\python\sound\gameplay.mp3")# loading in the gameplay music
        pygame.mixer.music.set_volume(0.6)#adjust the volume
        pygame.mixer.music.play(-1, 0.0, 5000)# -1 means that it'll loop forever.#playing music
    
    game_state.state_handler = game_state.level_1

    
    global static_time
    static_time = pygame.time.get_ticks() // 1000# starts the static time
    global score
    score = 0
    global level
    level = 1
    level_data = reset()
    #loading in the levels:
    with open(f"level.no{level}.csv", newline = "") as csvfile:
        viewer = csv.reader(csvfile, delimiter = ",")# creating an object which only views the values in the csv file.
        for x, row in enumerate(viewer):# without the enumerate the result will only return a string; the program can handle integers but not strings.
                for y, tile in enumerate(row):
                    level_data[x][y] = int(tile)
    world = World()
    player, Health_bar, magic_bar = world.process_data(level_data)
    pygame.display.flip()
    return level 
def level2():
    pygame.mixer.music.stop()# stopping the first GUI music
    if music_on == True:
        pygame.mixer.music.load("C:\Al Faysal\python\sound\gameplay.mp3")# loading in the gameplay music
        pygame.mixer.music.set_volume(0.6)#adjust the volume
        pygame.mixer.music.play(-1, 0.0, 5000)# -1 means that it'll loop forever.#playing music
    game_state.state_handler = game_state.level_2
    global static_time
    static_time = pygame.time.get_ticks() // 1000
    global score
    score = 0
    global level
    level = 2
    x_scroll = 0
    y_scroll = 0
    level_data = reset()
    #loading in the levels:
    with open(f"level.no{level}.csv", newline = "") as csvfile:
        viewer = csv.reader(csvfile, delimiter = ",")# creating an object which only views the values in the csv file.
        for x, row in enumerate(viewer):# without the enumerate the result will only return a string; the program can handle integers but not strings.
                for y, tile in enumerate(row):
                    level_data[x][y] = int(tile)
    world = World()
    player, Health_bar, magic_bar = world.process_data(level_data)
    pygame.display.flip()
    return level
    
def level3():
    pygame.mixer.music.stop()# stopping the first GUI music
    if music_on == True:
        pygame.mixer.music.load("C:\Al Faysal\python\sound\gameplay.mp3")# loading in the gameplay music
        pygame.mixer.music.set_volume(0.6)#adjust the volume
        pygame.mixer.music.play(-1, 0.0, 5000)# -1 means that it'll loop forever.#playing music
    game_state.state_handler = game_state.level_3
    global static_time
    static_time = pygame.time.get_ticks() // 1000
    global score
    score = 0
    global level
    level = 3
    x_scroll = 0
    bg_scroll = 0
    level_data = reset()
    #loading in the levels:
    with open(f"level.no{level}.csv", newline = "") as csvfile:
        viewer = csv.reader(csvfile, delimiter = ",")# creating an object which only views the values in the csv file.
        for x, row in enumerate(viewer):# without the enumerate the result will only return a string; the program can handle integers but not strings.
                for y, tile in enumerate(row):
                    level_data[x][y] = int(tile)
    world = World()
    player, Health_bar, magic_bar = world.process_data(level_data)
    pygame.display.flip()

    return level

    

    
### creating the level select page ###

Plevel1btn = level_page.add.button("level 1", level1)
Plevel2btn = level_page.add.button("level 2", level2)
Plevel3btn= level_page.add.button("level 3", level3)
Pendlessbtn = level_page.add.button("Endless mode")
Level_select = level_page.add.label("Level select", font_size = 75)
backbtn = level_page.add.button("back",pygame_menu.events.BACK)





Plevel1btn.set_border(3, (0, 0, 0), inflate = (0,0))
Plevel1btn.set_background_color((229, 228, 226), inflate = (0,0))
Plevel1btn.resize(180, 90, smooth = True)
Plevel1btn.translate(0,40)

Plevel2btn.set_border(3, (0, 0, 0), inflate = (0,0))
Plevel2btn.set_background_color((229, 228, 226), inflate = (0,0))
Plevel2btn.resize(180, 90, smooth = True)
Plevel2btn.translate(0,70)

Plevel3btn.set_border(3, (0, 0, 0), inflate = (0,0))
Plevel3btn.set_background_color((229, 228, 226), inflate = (0,0))
Plevel3btn.resize(180, 90, smooth = True)
Plevel3btn.translate(0,100)

Pendlessbtn.set_border(3, (0, 0, 0), inflate = (0,0))
Pendlessbtn.set_background_color((229, 228, 226), inflate = (0,0))
Pendlessbtn.resize(180, 90, smooth = True)
Pendlessbtn.translate(0,130)

backbtn.set_border(3, (0, 0, 0), inflate = (0,0))
backbtn.set_background_color((229, 228, 226), inflate = (0,0))
backbtn.resize(180, 90, smooth = True)
backbtn.translate(-600,80)

Level_select.translate(0, -500)

### creating the leaderboard menu page ###

Llevel1btn = leaderboard_menu_page.add.button("level 1", leadscore1)
graph1btn = leaderboard_menu_page.add.button("graph", graph1)

Llevel2btn = leaderboard_menu_page.add.button("level 2", leadscore2)
graph2btn = leaderboard_menu_page.add.button("graph", graph2)

Llevel3btn= leaderboard_menu_page.add.button("level 3", leadscore3)
graph3btn = leaderboard_menu_page.add.button("graph", graph3)

Lallbtn = leaderboard_menu_page.add.button("all levels", allscore)
graphallbtn = leaderboard_menu_page.add.button("graph", graphall)
leaderboard_menu = leaderboard_menu_page.add.label("Leaderboards", font_size = 75)
backbtn = leaderboard_menu_page.add.button("back",pygame_menu.events.BACK)





Llevel1btn.set_border(3, (0, 0, 0), inflate = (0,0))
Llevel1btn.set_background_color((229, 228, 226), inflate = (0,0))
Llevel1btn.resize(180, 90, smooth = True)
Llevel1btn.translate(0,140)

graph1btn.set_border(3, (0, 0, 0), inflate = (0,0))
graph1btn.set_background_color((229, 228, 226), inflate = (0,0))
graph1btn.resize(180, 90, smooth = True)
graph1btn.translate(-400,60)

Llevel2btn.set_border(3, (0, 0, 0), inflate = (0,0))
Llevel2btn.set_background_color((229, 228, 226), inflate = (0,0))
Llevel2btn.resize(180, 90, smooth = True)
Llevel2btn.translate(0,130)

graph2btn.set_border(3, (0, 0, 0), inflate = (0,0))
graph2btn.set_background_color((229, 228, 226), inflate = (0,0))
graph2btn.resize(180, 90, smooth = True)
graph2btn.translate(-400,50)

Llevel3btn.set_border(3, (0, 0, 0), inflate = (0,0))
Llevel3btn.set_background_color((229, 228, 226), inflate = (0,0))
Llevel3btn.resize(180, 90, smooth = True)
Llevel3btn.translate(0,100)

graph3btn.set_border(3, (0, 0, 0), inflate = (0,0))
graph3btn.set_background_color((229, 228, 226), inflate = (0,0))
graph3btn.resize(180, 90, smooth = True)
graph3btn.translate(-400,20)

graphallbtn.set_border(3, (0, 0, 0), inflate = (0,0))
graphallbtn.set_background_color((229, 228, 226), inflate = (0,0))
graphallbtn.resize(180, 90, smooth = True)
graphallbtn.translate(-400, -10)


Lallbtn.set_border(3, (0, 0, 0), inflate = (0,0))
Lallbtn.set_background_color((229, 228, 226), inflate = (0,0))
Lallbtn.resize(180, 90, smooth = True)
Lallbtn.translate(0,70)


backbtn.set_border(3, (0, 0, 0), inflate = (0,0))
backbtn.set_background_color((229, 228, 226), inflate = (0,0))
backbtn.resize(180, 90, smooth = True)
backbtn.translate(-600,-90)

leaderboard_menu.translate(0, -700)

### creating the settings page ###
brightnesslbl = settings_page.add.label("Screen brightness:", font_size = 40)
musiclbl = settings_page.add.label("Music:", font_size = 40)
SFXlbl = settings_page.add.label("SFX:", font_size = 40)
character_changelbl = settings_page.add.label("character:", font_size = 40)
backbtn = settings_page.add.button("back",pygame_menu.events.BACK)
settingslbl = settings_page.add.label("Settings page", font_size = 75)
#adding an on/off switch for music and SFX.
music_switch = settings_page.add.toggle_switch(" ", 0, single_click = True,
                                               state_text = ("OFF", "ON"), state_values = (False, True), onchange = update_music)
SFX_switch = settings_page.add.toggle_switch(" ", 0, single_click = True,
                                             state_text = ( "OFF" , "ON" ), state_values = (False, True), onchange = update_menu_sound)

#adding a slider for the brightness setting.
brightness_slider = settings_page.add.range_slider(" ", (50), (1, 100), increment = (1)
                                                   ,  value_format=lambda x: str(int(x)))
#creating a function that detects the chnage of the slider value:
def slider_change(val: int)-> None:
    sbc.set_brightness(val)
    print(brightness_slider.get_value())
brightness_slider.set_onchange(slider_change)
#adding in final buttons

change1btn =  settings_page.add.button(" ", switch_M, background_color =  pygame_menu.baseimage.BaseImage(
    "C:\Al Faysal\python\characters\player1\idle\\0.png",# loading in image
     pygame_menu.baseimage.IMAGE_MODE_FILL,(0,0)))
                            
# image for charcater2
change2btn =   settings_page.add.button(" ", switch_F, background_color =  pygame_menu.baseimage.BaseImage(
    "C:\Al Faysal\python\characters\player2\idle\\0.png",# loading in image
     pygame_menu.baseimage.IMAGE_MODE_FILL,(0,0)))


brightnesslbl.set_background_color((229, 228, 226), inflate = (0,0))
brightnesslbl.set_border(3, (0, 0, 0), inflate = (0,0))
brightnesslbl.set_padding((10, 70))
brightnesslbl.translate(-400, 100)

musiclbl.set_background_color((229, 228, 226), inflate = (0,0))
musiclbl.set_border(3, (0, 0, 0), inflate = (0,0))
musiclbl.set_padding((10, 180))
musiclbl.translate(-400, 150)


SFXlbl.set_background_color((229, 228, 226), inflate = (0,0))
SFXlbl.set_border(3, (0, 0, 0), inflate = (0,0))
SFXlbl.set_padding((10, 200))
SFXlbl.translate(-400, 200)

character_changelbl.set_background_color((229, 228, 226), inflate = (0,0))
character_changelbl.set_border(3, (0, 0, 0), inflate = (0,0))
character_changelbl.set_padding((10, 145))
character_changelbl.translate(-400, 250)

change2btn.set_border(3, (0, 0, 0), inflate = (0,0))
change2btn.resize(180, 180, smooth = True)
change2btn.translate(400,-450)

change1btn.set_border(3, (0, 0, 0), inflate = (0,0))
change1btn.resize(180, 180, smooth = True)
change1btn.translate(0,-273)

backbtn.set_border(3, (0, 0, 0), inflate = (0,0))
backbtn.set_background_color((229, 228, 226), inflate = (0,0))
backbtn.resize(180, 90, smooth = True)
backbtn.translate(-600,440)

music_switch.translate(0, -280)
SFX_switch.translate(0, -230)
brightness_slider.translate(0, -530)

settingslbl.translate(0, -420)


####################################CREATING THE GAME ITSELF ##############################
#player inputs
move_left = False
move_right = False
ai_moving_left = False
ai_moving_right = False
attack2 = False
#creating game variables
X_THRESH = 72
Y_THRESH = 100
ROWS = 32
MAX_COLUMNS = 350
MAX_LEVELS = 4
tile_size = SCREEN_HEIGHT// ROWS
TILE_TYPES = 11# how many different types of images is in my folder
gravity = 1
drag = 1
#loading images
sky_img = pygame.image.load("C:game_background_3\layers\sky.png").convert_alpha()#loads the sky
cloud_1 = pygame.image.load("C:game_background_3\layers\clouds_1.png").convert_alpha()#loads the first set of clouds
clouds_2 =  pygame.image.load("C:game_background_3\layers\clouds_2.png").convert_alpha()#loads in the second set of clouds
ground_1 =  pygame.image.load("C:game_background_3\layers\ground_1.png").convert_alpha()#loads in the first set of gorund
ground_2 =  pygame.image.load("C:game_background_3\layers\ground_2.png").convert_alpha()#loads in the second set of ground
ground_3 =  pygame.image.load("C:game_background_3\layers\ground_3.png").convert_alpha()#loadsin in the third set of ground
rock = pygame.image.load("rocks2.png").convert_alpha()#loads in the rocks


restart_btn = pygame.image.load("C:\Al Faysal\python\GUI\\restart.png").convert_alpha()#loading in the restart button
replay_btn = pygame.image.load("C:\Al Faysal\python\GUI\\replay.png").convert_alpha()#loading in the replay button
pause_btn = pygame.image.load("C:\Al Faysal\python\GUI\\pause.png").convert_alpha()#loading in the pause button
play_btn = pygame.image.load("C:\Al Faysal\python\GUI\\play.png").convert_alpha()#loading in the play button
home_btn = pygame.image.load("C:\Al Faysal\python\GUI\\home.png").convert_alpha()#loading in the home button
music_btn = pygame.image.load("C:\Al Faysal\python\GUI\\music.png").convert_alpha()#loading in the music button
silent_btn = pygame.image.load("C:\Al Faysal\python\GUI\\silent.png").convert_alpha()#loading in the silent button


home_btn2 = pygame.image.load("C:\Al Faysal\python\GUI\\home.png").convert_alpha()#loading in the play button
next_btn = pygame.image.load("C:\Al Faysal\python\GUI\\next.png").convert_alpha()

sort_btn = pygame.image.load("C:\Al Faysal\python\GUI\\sort.png").convert_alpha()# loading in the sorting button
#creating the timer
seconds = 0
minutes = 0

font = pygame.font.SysFont("'arial'", 70)# font and size of my timer
timer_text = font.render("{}:{}".format(minutes, seconds), True, (255, 255, 255))# how it will be displayed
timer_rect = timer_text.get_rect()# the rectnalge of the timer
timer_rect.center = 300, 50# the position on the screen


score = 0
score_text = font.render("score: {}".format(score), True, (255, 255, 255))
score_rect = timer_text.get_rect()# the rectangle of the score
score_rect.center = 900, 50# the position on the screen




 
#creating a button class for the tiles
class tile_button():
	def __init__(self,x, y, image, scale):
		width = image.get_width()# width is the image's width.
		height = image.get_height()#height is the image's height
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))# tranforms the images by the height and width
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):# draws the buttons onto the scree.
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

#creating the buttons
#pause screen
restart = tile_button(1500//2 - 200, 900 - 500,restart_btn, 0.5)
replay = tile_button(1500//2 + 600 , 50,replay_btn, 0.1)
pause = tile_button(1500//2 - 200 , 50, pause_btn, 0.2)
play = tile_button(1500//2 - 200, 900 - 600,play_btn, 0.5)
home = tile_button(1500//2 - 200, 900 - 300,home_btn, 0.5)
music = tile_button(300 , 50, music_btn, 0.2)
silent = tile_button(1200 , 50, silent_btn, 0.2)

#end screen
home2 = tile_button(200, 900 - 100,home_btn2, 0.25)
Next = tile_button(1200, 900 - 100,next_btn, 0.25)

# leaderboard
sort = tile_button(1200, 900 - 100,sort_btn, 0.25)

# storing the tile images on the list:
tile_list = []
for x in range(TILE_TYPES):# iterates through my file and loads each of the images.
   img = pygame.image.load(f"C:tiles/{x}.png").convert_alpha()
   img = pygame.transform.scale(img, (tile_size, tile_size))
   tile_list.append(img)

def level_background():
    screen.fill((255, 255, 224))# fills screen with yellow
    width = sky_img.get_width()
    for x in range(5):# loops the images 5 times; this means that when I scroll right;
                      # the yellow won't shown until I've passed the same image 5 times.
        screen.blit(sky_img, ((x* width) -bg_scroll * 0.5, 0))
        screen.blit(cloud_1, ((x* width) -bg_scroll* 0.6, 0))
        screen.blit(rock, ((x* width) -bg_scroll* 0.65, 0))
        screen.blit(clouds_2, ((x* width) -bg_scroll * 0.9, 0))
        screen.blit(ground_1, ((x* width) -bg_scroll* 0.85, 0))
        screen.blit(ground_2 , ((x* width) -bg_scroll* 0.75, 0))
        screen.blit(ground_3, ((x* width)-bg_scroll, 0))

        


def reset():
    # reset every groups
    enemies.empty()
    projectile_group.empty()
    goal_group.empty()
    obstacle_group.empty()

    # relaoding in any levles
    #creating empty tile list:
    data = []
    for row in range(ROWS):
        r = [-1] * MAX_COLUMNS# "-1" is for tiles which are meant to be empty.
        data.append(r)
    return data
    
class characters(pygame.sprite.Sprite):# class to create many different characters
    def __init__(self,character, x, y, scale, speed, health):# creates the actual; character
            self.alive = True#checking if the player is alive.
            pygame.sprite.Sprite.__init__(self)
            self.character = character
            self.speed = speed# speed of the character
            self.direction = 1#  direction of the character
            self.vel_y = 0# the velocity in the y direction
            self.vel_x = 0
            self.shoot_cooldown = 0
            self.attack_cooldown = 0
            self.attacking_cooldown = 30# this will stop the player from holding the attack button
            self.jump_count = 0# keeps track of how many times the player jumped
            self.jump = False# the jumping mechanic of the player
            self.in_air = True# checks if the player is in air
            self.dash = False# the dashing mechanic
            self.dash_power = 100# by how nmuch the player dashes by
            self.dash_cooldown = 0
            self.attack1 = False
            self.attack2 = False
            self.onwall = False
            self.wall_jump = False
            self.flip = False# flips the character by the y axis
            self.damage = False
            self.damage_counter = 0
            self.health = health# the health of the player
            self.heal = False
            self.heal_counter = 0# how long the player has to hold down the "heal" button
            self.heal_animation = False
            self.magic = 100
            self.animation_list = []# list of the aniamtions
            self.index = 0# what frame it's in
            self.action = 0# what state the plpayer is in
            self.update_time = pygame.time.get_ticks() # will help to switch the images over

            

            #loading in the diffrent animatiosn fo the player:
            if self.character == f"player{character_value}":
                animation_types = ["idle", "running", "jumping", "hit", "healing", "attack1", "death", "attack2", "climb"]
                for animation in animation_types:
                #resetting temp list 
                    temp_list = []
                #count number of frames in each file
                    num_of_frames = len(os.listdir(f'C:\Al Faysal\python\characters\{self.character}\{animation}'))
                    for i in range(num_of_frames):
                        img = pygame.image.load(f'C:\Al Faysal\python\characters\{self.character}\{animation}\{i}.png').convert_alpha()
                        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                        temp_list.append(img)
                    self.animation_list.append(temp_list)
            #  loading in the different animations for the minatuar enemey
            if self.character == "minataur":
                animation_types = ["idle", "walking", "attack1", "attack2", "hit", "death"]
                for animation in animation_types:
                #resetting temp list 
                    temp_list = []
                #count number of frames in each file
                    num_of_frames = len(os.listdir(f'C:\Al Faysal\python\characters\{self.character}\{animation}'))
                    for i in range(num_of_frames):
                        img = pygame.image.load(f'C:\Al Faysal\python\characters\{self.character}\{animation}\{i}.png').convert_alpha()
                        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                        temp_list.append(img)
                    self.animation_list.append(temp_list)

            #  loading in the different animations for the flying bat enemy
            if self.character == "bat":
                animation_types = ["idle", "attack", "hit", "fodder", "fodder2", "death"]
                for animation in animation_types:
                #resetting temp list 
                    temp_list = []
                #count number of frames in each file
                    num_of_frames = len(os.listdir(f'C:\Al Faysal\python\characters\{self.character}\{animation}'))
                    for i in range(num_of_frames):
                        img = pygame.image.load(f'C:\Al Faysal\python\characters\{self.character}\{animation}\{i}.png').convert_alpha()
                        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                        temp_list.append(img)
                    self.animation_list.append(temp_list)


            #  loading in the different animations for the muschroom enemy
            if self.character == "mushroom":
                animation_types = ["idle", "attack", "hit", "fodder", "fodder2", "death"]
                for animation in animation_types:
                #resetting temp list 
                    temp_list = []
                #count number of frames in each file
                    num_of_frames = len(os.listdir(f'C:\Al Faysal\python\characters\{self.character}\{animation}'))
                    for i in range(num_of_frames):
                        img = pygame.image.load(f'C:\Al Faysal\python\characters\{self.character}\{animation}\{i}.png').convert_alpha()
                        img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                        temp_list.append(img)
                    self.animation_list.append(temp_list)

                    
        
            self.image = self.animation_list[self.action][self.index]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)#positions the rectnalge onto the screen at the coordinates)
            self.width = self.image.get_width()# the widht of the image
            self.height = self.image.get_height()# gets the height of the image

            ### creating ai variables
            self.move_counter = 0
            self.vision = pygame.Rect(0, 0, 250, self.height)# the vision for the enemies
            self.idle = False
            self.idle_counter = 50
            self.kill_counter = 0

    global score
    def minataur_attack1(self):
        self.update_action(2)
    def minataur_attack2(self):
        self.update_action(3)


    def update(self):
        self.update_animation()
        self.check_alive()

        if self.shoot_cooldown > 0:# countdown
            self.shoot_cooldown -= 1
    def movement(self, move_left, move_right):
        # reset movement variables
        global gravity
        x_scroll = 0
        y_scroll = 0
        dx = 0
        dy = 0

        if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1# image flips over
        if move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1# image stays the same

        if self.jump is True and self.jump_count < 2:#player can only jump twice without resetting.
            self.jump_count += 1
            self.vel_y = -15
            self.jump = False
            self.in_air = True
            
        if self.in_air == False:# resets the jump counter when the player is on the ground
            self.jump_count = 0
        
    
        if self.dash == True and move_right == True:# dashes right
            self.flip  = False# deosn't flip images
            dx += self.dash_power# moves right
            self.dash_cooldown = 15# prevents double dashing
            self.dash = False
 

        if self.dash == True and move_left == True:# dashes left
            self.flip  = True# flips the image
            dx -= self.dash_power#moves left
            self.dash_cooldown = 15# prevents double dashing
            self.dash = False

        if self.dash_cooldown > 0:
            self.dash_cooldown -=1
   
            
        if self.damage == True:
            self.damage_counter += 1
            if self.character == f"player{character_value}":
                player.attack1 = False
        if self.damage_counter > FPS * 1:
            self.damage_counter = 0
            self.damage = False

        if self.magic > 100:
            self.magic = 100
        if self.magic <0:
            self.magic = 0

            
        if self.attack1 == True:
            self.attacking_cooldown -=1# stops player from holding attack button
            self.attack_cooldown = 10# stops player from spamming the attack button
            self.update_action(5)

        if self.attack_cooldown > 0:
            self.attack_cooldown -=1

        if self.attacking_cooldown <= 0:
            self.attack1 = False# stop the player's attack aniamtion
            self.attacking_cooldown = 30# reset cooldown

            
        if self.heal == True and (move_left or move_right or self.in_air) == False:# can't heal while moving
            if self.health < 100 :#  only heal when health is less than 100(can't heal when player has died)
                if self.magic > 20:# can only heal if the player has more than 10 magic points
                    self.heal_animation = True# plays the animation
                    self.heal_counter += 1# adds a counter
        if self.heal_counter > FPS * 2:# helas after 2 seconds(of holding the button down)
            self.heal_counter = 0# resets counter
            self.health += 30# regenerates health
            self.magic -= 20# takes away 20 magic points form the magic bar
            self.heal_animation = False# stops the animation
            if self.health > 100:
                self.health = 100
        if self.heal == True and (move_left or move_right or self.in_air) == True:# animation not played when moving and healing at the same time
            self.heal_animation = False
            self.heal_counter = 0# resetting the counter so player has to do the healing up animation all over again
        

        self.vel_y += gravity# adding gravity to the player character.
        if self.vel_y > 10:# adding a limit so the player doesn't deaccelerate forever
            self.vel_y 
        dy += self.vel_y# actually changes the displacment of the player in the y axis.

        
       #adding in the collision
        for tile in world.obstacle_list:
            #checkign collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
                self.onwall = True
                self.update_action(8)
                if self.onwall == True:
                    self.jump_count = 0# jump count is 0 therefore, player can jump infintelty.
                    self.vel_y = -0.25# the player can only go up by a little bit
                    self.vel_y += gravity# applies gravity
                    if self.vel_y > 10:# adding a limit so the player doesn't deaccelerate forever
                        self.vel_y
                dy += self.vel_y# actually moves the player 
                    
            else:
                self.onwall = False
                if self.onwall == False:
                    if self.jump is True and self.jump_count < 2:#  jumping wokrs normally
                        self.jump_count += 1
                        self.vel_y = -15
                        self.jump = False
                        self.in_air = True                

                                    
            #checking in the y direction
            if tile[1].colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                #checking for if the player clips through ground when jumping(ground is above the player)
                if self.vel_y < 0:#makes sure that the player doesn't spawn on top of a tile when jumping
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
   
                # checking if th player clips through ground when falling(ground is below the player)
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
    # if the player collides with any of the tiles form the obstacle group(lava, spikes, buzzsaws)           
        if pygame.sprite.spritecollide(self, obstacle_group, False):
            self.damage = True
            self.health -= 10# health goes down by 10
            self.vel_y = -15
            dx = - 15
            self.vel_y += gravity# adding gravity to the player character.
            self.vel_x += drag
            if self.vel_y > 10:# adding a limit so the player doesn't deaccelerate forever
                self.vel_y 
                dy += self.vel_y# actually changes the displacment of the player in the y axis.

        # if player collides with the goal
        level_complete = False
        if pygame.sprite.spritecollide(self, goal_group, False):
            level_complete = True
            
        #updating rectanlge postition
        self.rect.x += dx
        self.rect.y += dy

        #update scroll
        if self.character == f"player{character_value}":
            if (self.rect.right > SCREEN_WIDTH and bg_scroll < (world.level_length * tile_size) - SCREEN_HEIGHT) or (self.rect.left <X_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                x_scroll = -dx
        if self.character == f"player{character_value}":# scrolling downwards
            if self.rect.bottom > SCREEN_WIDTH - 200:
                y_scroll = -(self.rect.bottom - (SCREEN_WIDTH - 200))
                if self.rect.y > SCREEN_WIDTH - 200:
                    self.rect.y = SCREEN_WIDTH - 200
                
                
            elif player.rect.top < Y_THRESH:# scrollling upwards
                y_scroll = -(self.rect.top - Y_THRESH)
                if self.rect.y <Y_THRESH:# making it so player can't go above the threshold.
                    self.rect.y =  Y_THRESH
                
            else:
                y_scroll = 0

        return y_scroll, x_scroll, level_complete


    def AI(self):
        global gravity
        dx = 0
        dy = 0
            
        if self.alive and player.alive:
            
            if self.damage == True:# damage state not wokring
                self.update_action(4)
                self.damage_counter += 1
            if self.damage_counter > FPS * 1:
                self.damage_counter = 0
                self.damage = False

            if self.rect.colliderect(player.rect) and player.attack1 == True:# player attacks enemy
                    player.magic += 10
                    self.damage = True
                    self.health -= 10# decreases the minataurs hp
                    self.vel_y = -15
                    dx += player.speed * 10
                    self.vel_y += gravity# adding gravity to the player character.
                    self.vel_x += drag
                        
                    if self.vel_y > 10:# adding a limit so the player doesn't deaccelerate forever
                        self.vel_y 
                        dy += self.vel_y# actually changes the displacment of the player in the y axis.


            if self.rect.colliderect(player.rect) and player.attack1 == False:# player colliding with enemies
                player.damage = True
                if self.character == "minataur":
                    player.health -= 20# health goes down by 20 if minataur attacked player
                elif self.character == "bat":
                    player.health -= 5# health goes down by 5 if the bat attacked the player
                elif self.character == "mushroom":
                    player.health -= 10# health does down by 10 if the mushroom attacked the player


                    
                player.vel_y = -15
                dx = - 15
                player.vel_y += gravity# adding gravity to the player character.
                player.vel_x += drag
                if player.vel_y > 10:# adding a limit so the player doesn't deaccelerate forever
                    player.vel_y 
                    dy += player.vel_y# actually changes the displacment of the player in the y axis.
                
            if random.randint(1, 250) == 1 and self.idle == False:# a 1/200 chance for the enemy to enter idle state
                self.idle = True
                self.idle_counter = 50# how long beofre idle stops
    
            if self.vision.colliderect(player.rect) and self.direction == 1:# if the enemy sees the player on the right hand side
                self.rect.x += self.speed * 1.25# if minataur sees player then they will go faster
                self.flip = False
                self.idle = False
                if self.character == "minataur":
                    if random.randint(1, 4) == 1:
                        self.minataur_attack1()
                    else:
                        self.minataur_attack2()

                elif self.character == "bat":
                    self.update_action(1)

                elif self.character == "mushroom":
                    self.update_action(1)


            elif self.vision.colliderect(player.rect) and self.direction != 1:# if the enemy sees the player on the left hand side
                self.rect.x -= self.speed * 1.25
                self.flip = True
                self.idle = False
                if self.character == "minataur":
                    if random.randint(1, 4) == 1:
                        self.minataur_attack1()
                    else:
                        self.minataur_attack2()
                elif self.character == "bat":
                    self.update_action(1)

                elif self.character == "mushroom":
                    self.update_action(1)

            else:# enemy doesn't see the player 
                
                if self.idle == False:
                    self.idle_counter = 50
                    if self.move_counter > 45:
                        self.move_counter = 1
                        self.direction *= -1# flips the direction
                    else:
                        self.move_counter += 1
                        # updating the ai vision
                        self.vision.center = (self.rect.centerx + self.width * self.direction, self.rect.centery)# placing the vision rectnalge on top of the enemy
                        #pygame.draw.rect(screen, (255, 0, 0), self.vision)# drawing the vision rectangle.

                    if self.direction == 1:# right
                        self.rect.x += self.speed
                        self.flip = False
                        if not self.vision.colliderect(player.rect) and self.direction == 1:# right:
                            if self.character == "minataur":
                                self.update_action(1)#  walking
                            elif self.character == "bat":
                                self.update_action(0)
                    else:
                        self.rect.x -= self.speed# left
                        self.flip = True
                        if not self.vision.colliderect(player.rect) and self.direction != 1:# left:
                            if self.character == "minataur":
                                self.update_action(1)#  walking
                            elif self.character == "bat":
                                self.update_action(0)
                            elif self.character == "mushroom":
                                self.update_action(0)
                          
                else:#  idle is true
                    self.update_action(0)# idle
                    self.idle_counter -= 1# counting down
                    if self.idle_counter <= 0:#idle ended
                        self.idle = False# stops idle


        self.vel_y += gravity# adding gravity to the player character.
        if self.vel_y > 10:# adding a limit so the player doesn't deaccelerate forever
            self.vel_y 
        dy += self.vel_y# actually changes the displacment of the player in the y axis.
        
        #checking collisions for the enemies
        for tile in world.obstacle_list:
            #checkign collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #checking in the y direction
            if tile[1].colliderect(self.rect.x , self.rect.y + dy, self.width, self.height):
                #checking for if the enemy clips through ground when jumping(ground is above the player)
                if self.vel_y < 0:#makes sure that the enemy doesn't spawn on top of a tile when jumping
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
   
                # checking if th enemy clips through ground when falling(ground is below the enemy)
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x += x_scroll
        self.rect.y += y_scroll

        if self.character== "bat":# if it's the bat enemy make it hop/jump/fly
            self.rect.y -= 20

    def check_alive(self):
        global score
        if self.character == f"player{character_value}":
            if self.health <= 0:
                self.health = 0
                self.speed = 0# player can't move
                self.alive = False# player has "died".
                self.update_action(6)#death animation

        elif self.character == "minataur":
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                self.update_action(5)
                self.kill_counter +=1# start counter
                if self.kill_counter > FPS:  #after 1 second(after death animation)
                    self.kill()# remove the sprite
                    score += 300
                    player.magic += 20
                    print(score)
                    self.kill_counter = 0#reset counter

        elif self.character == "bat":# the bat enemy
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                
                self.rect.y += 20# makes the bat saty still when in death state
                
                self.update_action(5)# the death animation
                self.kill_counter +=1# start counter
                if self.kill_counter > FPS:  #after 1 second(after death animation)
                    self.kill()# remove the sprite
                    score += 100
                    player.magic += 20
                    print(score)
                    self.kill_counter = 0#reset counter


        elif self.character == "mushroom":# the bat enemy
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                self.update_action(5)# the death animation
                self.kill_counter +=1# start counter
                if self.kill_counter > FPS:  #after 1 second(after death animation)
                    self.kill()# remove the sprite
                    score += 150
                    player.magic += 20
                    print(score)
                    self.kill_counter = 0#reset counter
        return score
        print(score)


    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 25#increases cooldown
            fireball = projectile(player.rect.centerx + ( 0.7* player.rect.size[0] * player.direction), player.rect.centery - (player.height// 2 - 15), player.direction)
            projectile_group.add(fireball)# adds it to a group(makes it easier for collisions).
            player.magic -=15# decreases the player's magic bar
    def update_animation(self):
         animation_speed = 150# the speed of which the images switch over
         #update image depending on current frame
         self.image = self.animation_list[self.action][self.index]
         #check if enough time has passed
         if pygame.time.get_ticks() - self.update_time > animation_speed:
             self.update_time = pygame.time.get_ticks()
             self.index += 1# if enough time has passed then switch frames
        # loops animation
         if self.index >= len(self.animation_list[self.action]):# after it has iterated through all of the frames and has reached the last one
             if player.action  == 6 or self.action == 5:# don't loop if charcater has died
                 self.index= len(self.animation_list[self.action]) - 1
             else:
                 self.index = 0
         if self.index >= len(self.animation_list[self.action]):# after it has iterated through all of the frames and has reached the last one
             if player.action  == 7:# don't loop the player shooting
                 self.index= len(self.animation_list[self.action]) - 1
    def update_action(self, new_action):
        #checking if the new action is different ot the prevouis one
        if new_action != self.action:# if the new action is different to the first action; then switch the player action
             self.action = new_action
             #updating aniamtion settings
             self.index = 0
             self.update_time = pygame.time.get_ticks()
        
    def display(self):# draws characters onto screen
        screen.blit(pygame.transform.flip(self.image, self.flip, False),  self.rect)
 
class World():
    def __init__(self):
        self.obstacle_list = []# will help to do collisions with some of the tiles
    def process_data(self, data):# processes the level data an then outputs the image
        Lusername = username.get_value()
        global type1
        global character_value
         
        self.level_length = len(data[0])



        conn = sqlite3.connect("Player-data.db")
        cur = conn.cursor()
        query = "SELECT gender FROM Player where username = (?);"
        tuple1 = (Lusername, )
        cur.execute(query, tuple1)
        
        datas = cur.fetchall()
        conn.close()
        for value in datas:
            gender = f"{value[0]}"# get's the value of the gender
            if gender == "M":# if it's M then player1 will be displayed
                character_value = 1
            elif gender == "F":# if it's F then player2 will be displayed.
                character_value = 2

    
            
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:# ignores all of the empty lists
                    img = tile_list[tile]
                    img_rect = img.get_rect()# this will be needed for the collisions between the player and the levels.
                    img_rect.x = x * tile_size
                    img_rect.y = y * tile_size
                    tile_data = (img, img_rect)# sees what numbers correlates to what image.
                    if tile >= 0 and tile <= 2:# adds all the tiles(which don't damage the user) onto the same list.
                        self.obstacle_list.append(tile_data)
                    elif tile >= 3 and tile <= 5:# lava, spikes, buzzsaws
                        obstacle =  obstacles(img, x * tile_size, y * tile_size )
                        obstacle_group.add(obstacle)# adds these tiles into a specific sprite group
                    elif tile == 6:# the enging goal
                        goal =  Goal(img, x * tile_size, y * tile_size )
                        goal_group.add(goal)
                    elif tile == 7:# the player character
                        player = characters(f"player{character_value}", x * tile_size, y * tile_size, 0.25, 10, 100)
                        Health_bar = healthbar(10, 10, player.health, player.health)
                        magic_bar = Magicbar(10, 80, player.magic, player.magic)
                    elif tile == 8:
                        minataur = characters("minataur",  x * tile_size, y * tile_size, 1, 10, 200)
                        enemies.add(minataur)# adding minataur to the enemy group.
                    elif tile == 9:
                        bat = characters("bat",  x * tile_size, y * tile_size, 0.5, 5, 50)
                        enemies.add(bat)# adding minataur to the enemy group.
                    elif tile == 10:
                        mushroom = characters("mushroom",  x * tile_size, y * tile_size, 1, 3, 100)
                        enemies.add(mushroom)# adding minataur to the enemy group.

        return player, Health_bar, magic_bar

    
    def draw_tiles(self):# draws the tiles onto the screen
        for tile in self.obstacle_list:
            img_rect = tile[1]
            img_rect.x += x_scroll
            img_rect.y += y_scroll
            screen.blit(tile[0], img_rect)
            
        

class projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 12# speed of fireball
        self.direction = direction# direction of fireball
        self.flip = False# flip the fireball
        self.animation_list = []# list of the aniamtions
        self.index = 0# what frame it's in
        self.update_time = pygame.time.get_ticks()
        #loading in the animations
        for i in range(5):
            img = pygame.image.load(f"C:\Al Faysal\python\\fireball\{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * 2), int(img.get_height() * 2)))
            self.animation_list.append(img)
        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def update(self):
        self.update_animation()
        self.display()

        if player.direction == -1:# the fireball flips with the player
            self.flip = True
        else:
            self.flip = False
        #moving projectile
        self.rect.x += (self.direction * self.speed) + x_scroll
        self.rect.y += y_scroll

        #check if fireball is off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_HEIGHT:
            self.kill()# get rid of fireball if it's  off screen

        #check for collision with level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()# get rid of fireball if it collided with the world tiles

        #check collision with the enemies
            for enemy in enemies:
                if pygame.sprite.spritecollide(enemy, projectile_group, False):
                    if enemy.alive:
                        enemy.rect.x += self.speed * 5# knockback the enemy
                        
                        enemy.health -= 25# decreases the enemy health
                        self.kill()


    def update_animation(self):
         animation_speed = 150# the speed of which the images switch over
         #update image depending on current frame
         self.image = self.animation_list[self.index]
         #check if enough time has passed
         if pygame.time.get_ticks() - self.update_time > animation_speed:
             self.update_time = pygame.time.get_ticks()
             self.index += 1# if enough time has passed then switch frames
        # loops animation
         if self.index >= len(self.animation_list):# after it has iterated through all of the frames and has reached the last one
             self.index = 0
    def display(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),  self.rect)
                
        
class healthbar():
    def __init__(self, x, y, health, max_hp):
        self.x = x# the x position of  it
        self.y = y# the y position of it
        self.health = health# the current health
        self.max_hp = max_hp# the max health
    def draw(self, health):
        #updtaes health
        self.health = health
        #calculating health ratio
        ratio = self.health/ self.max_hp

        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 200, 50))# red healthbar
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 200 * ratio, 50))# the green health bar

class Magicbar():
    def __init__(self, x, y, magic, max_magic):
        self.x = x
        self.y = y
        self.magic = magic
        self.max_magic = max_magic
    def draw(self, magic):
        #updtaes health
        self.magic = magic
        #calculating health ratio
        ratio = self.magic/ self.max_magic

        pygame.draw.rect(screen, (220,220,220), (self.x, self.y, 180, 30))# the grey bar
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, 180 * ratio, 30))# the white bar

            
class obstacles(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size// 2, y +(tile_size - self.image.get_height()))# places the tiles on the correct position

    def update(self): #updating the obstacles.
        self.rect.x += x_scroll
        self.rect.y += y_scroll
class Goal(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size// 2, y +(tile_size - self.image.get_height()))# places the tiles on the correct position
        
    def update(self): #updating the obstacles.
        self.rect.x += x_scroll
        self.rect.y += y_scroll

#creating the sprite groups
enemies = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
goal_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

#creating empty list for the levels
level_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLUMNS# "-1" is for tiles which are meant to be empty.
    level_data.append(r)

#loading in the levels:
with open(f"level.no{level}.csv", newline = "") as csvfile:
                    viewer = csv.reader(csvfile, delimiter = ",")# creating an object which only views the values in the csv file.
                    for x, row in enumerate(viewer):# without the enumerate the result will only return a string; the program can handle integers but not strings.
                            for y, tile in enumerate(row):
                                level_data[x][y] = int(tile)

world = World()
player, Health_bar, magic_bar = world.process_data(level_data)

current_time = 0# the time for which the program has started to run
static_time = 0# the time after the button has been pressed
def base_level():
    global paused
    global music_on
    if paused == False:
        clock.tick(FPS)

        global seconds
        global minutes
        global static_time
        global timer_text
        global score
        global level
        global move_left
        global move_right
        global ai_moving_left
        global ai_moving_right
        global x_scroll
        global y_scroll
        global bg_scroll
        global world
        global player
        global Health_bar
        global magic_bar


        
        level_background()

        current_time = pygame.time.get_ticks() // 1000# the time after program has been run
        length_time = current_time - static_time# the actual time to be displayed
        seconds = length_time
        
        if seconds >= 60:
            static_time = pygame.time.get_ticks() // 1000# resetting time
            length_time = current_time - static_time# resetting time
            minutes += 1
            seconds = 0
        timer_text = font.render("{}:{}".format(minutes, seconds), False, (255, 255, 255))
        
        screen.blit(timer_text, timer_rect)# displays time onto screen

        score_text = font.render("score: {}".format(score), True, (255, 255, 255))# updating the score
        screen.blit(score_text, score_rect)# displaying the score



        
        world.draw_tiles()# draws all of the norma tiles onto the screen.

        if pause.draw(screen):# draws the pause button
            paused = True


        if replay.draw(screen):# if the replay button is clicked
                bg_scroll = 0
                static_time = pygame.time.get_ticks() // 1000# resetting time
                length_time = current_time - static_time# resetting time
                minutes = 0

                score = 0
                
                level_data = reset()
                #loading in the levels:
                with open(f"level.no{level}.csv", newline = "") as csvfile:
                    viewer = csv.reader(csvfile, delimiter = ",")# creating an object which only views the values in the csv file.
                    for x, row in enumerate(viewer):# without the enumerate the result will only return a string; the program can handle integers but not strings.
                            for y, tile in enumerate(row):
                                level_data[x][y] = int(tile)
                world = World()
                player, Health_bar, magic_bar = world.process_data(level_data) 
        
        Health_bar.draw(player.health)
        
        magic_bar.draw(player.magic)
        
        player.update()
        player.display()# draws player onto screen

        
        for enemy in enemies:# iterates through all the enemies.
            enemy.AI()
            enemy.update()
            enemy.display()


        
        if player.alive:#checking if the player is alive
        # update player actions
            if player.onwall:
                player.update_action(8)
            elif player.attack2 is True:
                player.update_action(7)#attack2 animation
            elif player.attack1 is True:
                player.update_action(5)# attack1 animation
            elif player.heal_animation == True:
                player.update_action(4)
            elif player.damage is True:# damaged state
                player.update_action(3)
            elif player.in_air:
                player.update_action(2)# jumping
            elif move_left or move_right:
                player.update_action(1)# running
            else:
                player.update_action(0)# idle
            
        
            y_scroll, x_scroll, level_complete = player.movement(move_left, move_right)
            bg_scroll -= x_scroll
            #check if player has completed level
            if level_complete == True:


                Cusername = username.get_value()# gets value form the username entry field.
                Cpassword = password.get_value()
                
                game_state.state_handler = game_state.end_screen
                game_state.total_time = length_time + (60 * minutes)# this will help to code in the score
                if game_state.total_time < 60:# if player beat level under a minute
                    game_state.total_score = score + 300
                elif game_state.total_time >= 60 and game_state.total_time < 120:# if player beat level between a minute and 2 minutes
                    game_state.total_score = score + 200
                elif game_state.total_time >= 120 and game_state.total_time < 160:# if player beat it over 2 minutes but under 160 seconds
                    game_state.total_score = score + 150
                else:# if player beat level 160 seconds or more
                    game_state.total_score = score + 50


                # putting the scores into the database
                conn = sqlite3.connect("Player-data.db")# connects to databse
                cur = conn.cursor()
                statment1 = f"SELECT username from Player WHERE username='{Cusername}' AND Password = '{Cpassword}';"# selects the username and password of the user who just logged in
                cur.execute(statment1)# executs command
                conn.commit()
                
                update_tuple = (int(game_state.total_score), Cusername,)# tuple for score
                time_tuple = (int(game_state.total_time), Cusername,)# tuple for time
                
                if level == 1:
                    cur.execute("SELECT score1 FROM Player WHERE username = ?", (Cusername,))
                    data_score = cur.fetchone()[0]# gets the score from the database

                    cur.execute("SELECT clear1 FROM Player WHERE username = ?", (Cusername,))
                    data_time = cur.fetchone()[0]# gets the time from the database

                    if game_state.total_score > data_score:
                        update_score =  """UPDATE PLAYER SET score1 = (?) where username = (?)"""# updates score for level 1

                        cur.execute(update_score, update_tuple)# will update the new score into the database.
                        conn.commit() 
                    if game_state.total_time < data_time:
                        update_time = """UPDATE PLAYER SET clear1 = (?) where username = (?)"""# updates time for level 1

                        cur.execute(update_time, time_tuple)# will update the new time into the database.
                        conn.commit()
                
                    
                elif level == 2:
                    cur.execute("SELECT score2 FROM Player WHERE username = ?", (Cusername,))
                    data_score = cur.fetchone()[0]# gets the score from the database

                    cur.execute("SELECT clear2 FROM Player WHERE username = ?", (Cusername,))
                    data_time = cur.fetchone()[0]# gets the time from the database

                    if game_state.total_score > data_score:
                        update_score =  """UPDATE PLAYER SET score2 = (?) where username = (?)"""# updates score for level 1

                        cur.execute(update_score, update_tuple)# will update the new score into the database.
                        conn.commit() 
                    if game_state.total_time < data_time:
                        update_time = """UPDATE PLAYER SET clear2 = (?) where username = (?)"""# updates time for level 1

                        cur.execute(update_time, time_tuple)# will update the new time into the database.
                        conn.commit()


                elif level == 3:
                    cur.execute("SELECT score3 FROM Player WHERE username = ?", (Cusername,))
                    data_score = cur.fetchone()[0]# gets the score from the database

                    cur.execute("SELECT clear3 FROM Player WHERE username = ?", (Cusername,))
                    data_time = cur.fetchone()[0]# gets the time from the database

                    if game_state.total_score > data_score:
                        update_score =  """UPDATE PLAYER SET score3 = (?) where username = (?)"""# updates score for level 1

                        cur.execute(update_score, update_tuple)# will update the new score into the database.
                        conn.commit() 
                    if game_state.total_time < data_time:
                        update_time = """UPDATE PLAYER SET clear3 = (?) where username = (?)"""# updates time for level 1

                        cur.execute(update_time, time_tuple)# will update the new time into the database.
                        conn.commit()

               
                score = 0
                static_time = pygame.time.get_ticks() // 1000# resetting time
                length_time = current_time - static_time# resetting time
                minutes = 0
                bg_scroll = 0
                x_scroll = 0
                y_scroll = 0
                level_data = reset()
                if level < MAX_LEVELS:
                    with open(f"level.no{level}.csv", newline = "") as csvfile:
                        viewer = csv.reader(csvfile, delimiter = ",")# creating an object which only views the values in the csv file.
                        for x, row in enumerate(viewer):# without the enumerate the result will only return a string; the program can handle integers but not strings.
                                for y, tile in enumerate(row):
                                    level_data[x][y] = int(tile)
                    world = World()
                    player, Health_bar, magic_bar = world.process_data(level_data)#





                    
        else:#player has died
            y_scroll = 0
            x_scroll = 0# everything stops scrolling when the player dies.
            if restart.draw(screen):# if the restart button is clciked:
                bg_scroll = 0

                
                static_time = pygame.time.get_ticks() // 1000# resetting time
                length_time = current_time - static_time# resetting time
                minutes = 0


                score = 0# resetting the score

                level_data = reset()
                #loading in the levels:
                with open(f"level.no{level}.csv", newline = "") as csvfile:
                    viewer = csv.reader(csvfile, delimiter = ",")# creating an object which only views the values in the csv file.
                    for x, row in enumerate(viewer):# without the enumerate the result will only return a string; the program can handle integers but not strings.
                            for y, tile in enumerate(row):
                                level_data[x][y] = int(tile)
                world = World()
                player, Health_bar, magic_bar = world.process_data(level_data)     

        obstacle_group.update()
        goal_group.update()
        projectile_group.update()
        obstacle_group.draw(screen)
        goal_group.draw(screen)
        projectile_group.draw(screen)

        
        events = pygame.event.get()

        
        for event in events:
            if event.type == pygame.QUIT:
                exit()

                
            #player input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_left = True# moves player character to the left
                if event.key == pygame.K_d:
                    move_right = True# moves player character to the right
                if event.key == pygame.K_w:
                    player.jump = True # if the "w" key is prssed then the player charater jumps
                if event.key == pygame.K_s:# The healing key
                    player.heal = True
                if event.key == pygame.K_SPACE and player.dash_cooldown <= 0:# if the space bar is pressed then the player will "dash"
                    player.dash = True
                if event.key == pygame.K_g and player.attack_cooldown <= 0:# the attack1
                    player.attack1 = True
                if event.key == pygame.K_h and player.magic >= 15:# player can't shoot if they don't have enough magic
                    player.attack2 = True #plays the animation
                    player.shoot()# actually shoots the fireball          

            
            if event.type == pygame.KEYUP:# if key is stopped being pressed; stops the player character
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_w:
                    player.jump = False
                if event.key == pygame.K_s:
                    player.heal = False
                    player.heal_animation = False
                if event.key == pygame.K_SPACE:
                    player.dash = False
                if event.key == pygame.K_g:
                    player.attack1 = False
                if event.key == pygame.K_h:
                    player.attack2 = False

    else:# game is paused
        screen.fill((255, 255, 255))
        screen.blit(menu_img,(0,0))
        
        if play.draw(screen):# draw the play button
            paused = False# if pressed; game is not paused.

        if music.draw(screen):
            #stop GUI music
            pygame.mixer.music.stop()
            music_on = True
            #play other music
            pygame.mixer.music.load("C:\Al Faysal\python\sound\gameplay.mp3")
            pygame.mixer.music.set_volume(0.6)#adjust the volume
            pygame.mixer.music.play(-1, 0.0, 5000)# -1 means that it'll loop forever.
        if silent.draw(screen):
            #stop gameplay music
            music_on = False
            pygame.mixer.music.stop()


        if home.draw(screen):
            paused = False

            pygame.mixer.music.stop()# stops gameplay music
            if music_on == True:
                pygame.mixer.music.load("C:\Al Faysal\python\sound\GUI.mp3")# loads in the GUI music
                pygame.mixer.music.set_volume(0.6)#adjust the volume
                pygame.mixer.music.play(-1, 0.0, 5000)# -1 means that it'll loop forever.

            
            y_scroll = 0
            x_scroll = 0
            bg_scroll = 0
            level_data = reset()
            #loading in the levels:
            with open(f"level.no{level}.csv", newline = "") as csvfile:
                viewer = csv.reader(csvfile, delimiter = ",")# creating an object which only views the values in the csv file.
                for x, row in enumerate(viewer):# without the enumerate the result will only return a string; the program can handle integers but not strings.
                        for y, tile in enumerate(row):
                            level_data[x][y] = int(tile)
            world = World()
            player, Health_bar, magic_bar = world.process_data(level_data)
            game_state.state_handler  = game_state.GUI# goes back to the GUI 


        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        


class Gamestate():# the event handler
    def __init__(self):
        self.state = "GUI"
        self.total_time = 0
        self.total_score = 0
    def GUI(self):# the GUI
        self.state = "GUI"
        background()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
                
                
#displays the title screen and the rest of the GUI
        if title_screen.is_enabled():
            title_screen.update(events)
            title_screen.draw(screen)
            title_screen.fps_limit = FPS
    def Lscore1(self):
        self.state = "Lscore1"

        # drawing background and buttons
        screen.fill((255, 255, 255))
        screen.blit(menu_img,(0,0))

        if home2.draw(screen):
            game_state.state_handler = game_state.GUI
        if sort.draw(screen):
            game_state.state_handler = game_state.Ltime1# toggles what's being compared

        # orders data in descending order
        conn = sqlite3.connect("Player-data.db")
        cur = conn.cursor()
        cur.execute("SELECT username, score1 FROM Player ORDER BY score1 DESC LIMIT 6")# orders database in descending order by the score 1 column
        datas = cur.fetchall()

        # draws in title
        title = font.render("Level 1", True, (255, 255, 255))# the username text
        # draws in the heading
        Utext = font.render("Username:", True, (255, 255, 255))# the username text
        Stext =  font.render("score:", True, (255, 255, 255))# the score text
        pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 , 1325, 85))# draws in the rectnalge which exaplains what the values are

        screen.blit(title, (650, 10))
        screen.blit(Utext, (60, 100))
        screen.blit(Stext, (1150, 100))
            
        n = 0
        x = 0
        list1 = []
        for data in datas:
            x += 1
            #Test in progress
            n += 90#The gap between each column
            text1 = f"{x}. {data[0]}"# gets the values in thr username
            text2 = f"{data[1]}"# gets values for the scores

            if text2 == "None":# Converts all of the None values to 0.
                text2 = "0"


            
            user_text = Lfont.render(text1, True, (72, 72, 72))# renders in all of the usernames
            score_text = Lfont.render(text2, True, (72, 72, 72))# renders in all of the scores

            #draws in the rows of the leaderboard
            pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 + n, 1325, 85))# draws in the border
            pygame.draw.rect(screen, (229, 228, 226), pygame.Rect(60, 95 + n, 1300, 75))# draws multipkle rectnagles.
            
            screen.blit(user_text, (60, 105 + n))
            screen.blit(score_text, (1200, 105 + n))



        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

    def Ltime1(self):
        self.state = "Ltime1"

        # drawing background and buttons
        screen.fill((255, 255, 255))
        screen.blit(menu_img,(0,0))

        if home2.draw(screen):
            game_state.state_handler = game_state.GUI
        if sort.draw(screen):
            game_state.state_handler = game_state.Lscore1

        # orders data in descending order
        conn = sqlite3.connect("Player-data.db")
        cur = conn.cursor()
        cur.execute("SELECT username, clear1 FROM Player LIMIT 6")# selects username and clear rate and orders them in ascending order
        datas = cur.fetchall()

        # draws in title
        title = font.render("Level 1", True, (255, 255, 255))# the username text
        # draws in the heading
        Utext = font.render("Username:", True, (255, 255, 255))# the username text
        Stext =  font.render("clear rate:", True, (255, 255, 255))# the score text
        pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 , 1325, 85))# draws in the rectnalge which exaplains what the values are

        screen.blit(title, (650, 10))
        screen.blit(Utext, (60, 100))
        screen.blit(Stext, (1100, 100))
            
        n = 0
        x = 0
        for data in datas:
            x += 1
            #Test in progress
            n += 90#The gap between each column
            text1 = f"{x}. {data[0]}"# gets the values in thr username
            text2 = f"{data[1]}"# gets values for the scores

            if text2 == "None":# Converts all of the None values to 0.
                text2 = "9999"

            
            user_text = Lfont.render(text1, True, (72, 72, 72))# renders in all of the usernames
            score_text = Lfont.render(text2, True, (72, 72, 72))# renders in all of the scores

            #draws in the rows of the leaderboard
            pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 + n, 1325, 85))# draws in the border
            pygame.draw.rect(screen, (229, 228, 226), pygame.Rect(60, 95 + n, 1300, 75))# draws multipkle rectnagles.
            
            screen.blit(user_text, (60, 105 + n))
            screen.blit(score_text, (1200, 105 + n))


        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
    

    def Lscore2(self):
        self.state = "Lscore2"

        # drawing background and buttons
        screen.fill((255, 255, 255))
        screen.blit(menu_img,(0,0))

        if home2.draw(screen):
            game_state.state_handler = game_state.GUI
        if sort.draw(screen):
            game_state.state_handler = game_state.Ltime2

        # orders data in descending order
        conn = sqlite3.connect("Player-data.db")
        cur = conn.cursor()
        cur.execute("SELECT username, score2 FROM Player ORDER BY score2 DESC LIMIT 6")# orders database in descending order by the score 1 column
        datas = cur.fetchall()

        # draws in title
        title = font.render("Level 2", True, (255, 255, 255))# the username text
        # draws in the heading
        Utext = font.render("Username:", True, (255, 255, 255))# the username text
        Stext =  font.render("score:", True, (255, 255, 255))# the score text
        pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 , 1325, 85))# draws in the rectnalge which exaplains what the values are

        screen.blit(title, (650, 10))
        screen.blit(Utext, (60, 100))
        screen.blit(Stext, (1150, 100))
            
        n = 0
        x = 0
        for data in datas:
            x += 1
            #Test in progress
            n += 90#The gap between each column
            text1 = f"{x}. {data[0]}"# gets the values in thr username
            text2 = f"{data[1]}"# gets values for the scores

            if text2 == "None":# Converts all of the None values to 0.
                text2 = "0"

            
            user_text = Lfont.render(text1, True, (72, 72, 72))# renders in all of the usernames
            score_text = Lfont.render(text2, True, (72, 72, 72))# renders in all of the scores

            #draws in the rows of the leaderboard
            pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 + n, 1325, 85))# draws in the border
            pygame.draw.rect(screen, (229, 228, 226), pygame.Rect(60, 95 + n, 1300, 75))# draws multipkle rectnagles.
            
            screen.blit(user_text, (60, 105 + n))
            screen.blit(score_text, (1200, 105 + n))


        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
    def Ltime2(self):
        self.state = "Ltime2"

        # drawing background and buttons
        screen.fill((255, 255, 255))
        screen.blit(menu_img,(0,0))

        if home2.draw(screen):
            game_state.state_handler = game_state.GUI
        if sort.draw(screen):
            game_state.state_handler = game_state.Lscore2

        # orders data in descending order
        conn = sqlite3.connect("Player-data.db")
        cur = conn.cursor()
        cur.execute("SELECT username, clear2 FROM Player LIMIT 6")# selects username and clear rate and orders them in ascending order
        datas = cur.fetchall()

        # draws in title
        title = font.render("Level 2", True, (255, 255, 255))# the username text
        # draws in the heading
        Utext = font.render("Username:", True, (255, 255, 255))# the username text
        Stext =  font.render("clear rate:", True, (255, 255, 255))# the score text
        pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 , 1325, 85))# draws in the rectnalge which exaplains what the values are

        screen.blit(title, (650, 10))
        screen.blit(Utext, (60, 100))
        screen.blit(Stext, (1100, 100))
            
        n = 0
        x = 0
        for data in datas:
            x += 1
            #Test in progress
            n += 90#The gap between each column
            text1 = f"{x}. {data[0]}"# gets the values in thr username
            text2 = f"{data[1]}"# gets values for the scores

            if text2 == "None":# Converts all of the None values to 0.
                text2 = "9999"

            
            user_text = Lfont.render(text1, True, (72, 72, 72))# renders in all of the usernames
            score_text = Lfont.render(text2, True, (72, 72, 72))# renders in all of the scores

            #draws in the rows of the leaderboard
            pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 + n, 1325, 85))# draws in the border
            pygame.draw.rect(screen, (229, 228, 226), pygame.Rect(60, 95 + n, 1300, 75))# draws multipkle rectnagles.
            
            screen.blit(user_text, (60, 105 + n))
            screen.blit(score_text, (1200, 105 + n))


        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

    def Lscore3(self):
        self.state = "Lscore3"

        # drawing background and buttons
        screen.fill((255, 255, 255))
        screen.blit(menu_img,(0,0))

        if home2.draw(screen):
            game_state.state_handler = game_state.GUI
        if sort.draw(screen):
            game_state.state_handler = game_state.Ltime3

        # orders data in descending order
        conn = sqlite3.connect("Player-data.db")
        cur = conn.cursor()
        cur.execute("SELECT username, score3 FROM Player ORDER BY score3 DESC LIMIT 6")# orders database in descending order by the score 3 column
        datas = cur.fetchall()

        # draws in title
        title = font.render("Level 3", True, (255, 255, 255))# the username text
        # draws in the heading
        Utext = font.render("Username:", True, (255, 255, 255))# the username text
        Stext =  font.render("score:", True, (255, 255, 255))# the score text
        pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 , 1325, 85))# draws in the rectnalge which exaplains what the values are

        screen.blit(title, (650, 10))
        screen.blit(Utext, (60, 100))
        screen.blit(Stext, (1150, 100))
            
        n = 0
        x = 0
        for data in datas:
            x += 1
            #Test in progress
            n += 90#The gap between each column
            text1 = f"{x}. {data[0]}"# gets the values in thr username
            text2 = f"{data[1]}"# gets values for the scores

            if text2 == "None":# Converts all of the None values to 0.
                text2 = "0"

            
            user_text = Lfont.render(text1, True, (72, 72, 72))# renders in all of the usernames
            score_text = Lfont.render(text2, True, (72, 72, 72))# renders in all of the scores

            #draws in the rows of the leaderboard
            pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 + n, 1325, 85))# draws in the border
            pygame.draw.rect(screen, (229, 228, 226), pygame.Rect(60, 95 + n, 1300, 75))# draws multipkle rectnagles.
            
            screen.blit(user_text, (60, 105 + n))
            screen.blit(score_text, (1200, 105 + n))


        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

    def Ltime3(self):
        self.state = "Ltime3"

        # drawing background and buttons
        screen.fill((255, 255, 255))
        screen.blit(menu_img,(0,0))

        if home2.draw(screen):
            game_state.state_handler = game_state.GUI
        if sort.draw(screen):
            game_state.state_handler = game_state.Lscore3

        # orders data in descending order
        conn = sqlite3.connect("Player-data.db")
        cur = conn.cursor()
        cur.execute("SELECT username, clear3 FROM Player LIMIT 6")# selects username and clear rate and orders them in ascending order
        datas = cur.fetchall()

        # draws in title
        title = font.render("Level 3", True, (255, 255, 255))# the username text
        # draws in the heading
        Utext = font.render("Username:", True, (255, 255, 255))# the username text
        Stext =  font.render("clear rate:", True, (255, 255, 255))# the score text
        pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 , 1325, 85))# draws in the rectnalge which exaplains what the values are

        screen.blit(title, (650, 10))
        screen.blit(Utext, (60, 100))
        screen.blit(Stext, (1100, 100))
            
        n = 0
        x = 0
        for data in datas:
            x += 1
            #Test in progress
            n += 90#The gap between each column
            text1 = f"{x}. {data[0]}"# gets the values in thr username
            text2 = f"{data[1]}"# gets values for the scores

            if text2 == "None":# Converts all of the None values to 0.
                text2 = "9999"

            
            user_text = Lfont.render(text1, True, (72, 72, 72))# renders in all of the usernames
            score_text = Lfont.render(text2, True, (72, 72, 72))# renders in all of the scores

            #draws in the rows of the leaderboard
            pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 + n, 1325, 85))# draws in the border
            pygame.draw.rect(screen, (229, 228, 226), pygame.Rect(60, 95 + n, 1300, 75))# draws multipkle rectnagles.
            
            screen.blit(user_text, (60, 105 + n))
            screen.blit(score_text, (1200, 105 + n))


        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

    def score_all(self):
        self.state = "score_all"

         # drawing background and buttons
        screen.fill((255, 255, 255))
        screen.blit(menu_img,(0,0))

        if home2.draw(screen):
            game_state.state_handler = game_state.GUI
        if sort.draw(screen):
            game_state.state_handler = game_state.time_all

        # orders data in descending order
        conn = sqlite3.connect("Player-data.db")
        cur = conn.cursor()
        cur.execute("""SELECT username, score1 AS score, 'level 1' FROM Player 
        UNION ALL
        SELECT  username, score2 AS score, 'level 2'  FROM Player
        UNION ALL
        SELECT  username, score3 AS score, 'level 3' FROM Player
        ORDER BY score DESC LIMIT 6;

        """)# putting each levels into one large list and then ordering it, for every level putting it into a variable so it can be called later
        # outputs username, score and then the level it was acheived on in that order
        datas = cur.fetchall()

        # draws in title
        title = font.render("All Levels", True, (255, 255, 255))# the username text
        # draws in the heading
        Utext = font.render("Username:", True, (255, 255, 255))# the username text
        Stext =  font.render("score:", True, (255, 255, 255))# the score text
        Ltext = font.render("level:", True, (255, 255, 255))# the score text
        pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 , 1325, 85))# draws in the rectnalge which exaplains what the values are

        screen.blit(title, (650, 10))
        screen.blit(Utext, (60, 100))
        screen.blit(Stext, (700, 100))
        screen.blit(Ltext, (1100, 100))
        
            
        n = 0
        x = 0
        for data in datas:
            x += 1
            #Test in progress
            n += 90#The gap between each column
            text1 = f"{x}. {data[0]}"# gets the values in thr username
            text2 = f"{data[1]}"# gets values for the scores
            text3 = f"{data[2]}"# gets the values for the levles

            if text2 == "None":# Converts all of the None values to 0.
                text2 = "0"

            
            user_text = Lfont.render(text1, True, (72, 72, 72))# renders in all of the usernames
            score_text = Lfont.render(text2, True, (72, 72, 72))# renders in all of the scores
            level_text = Lfont.render(text3, True, (72, 72, 72))# renders in all of the scores

            #draws in the rows of the leaderboard
            pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 + n, 1325, 85))# draws in the border
            pygame.draw.rect(screen, (229, 228, 226), pygame.Rect(60, 95 + n, 1300, 75))# draws multipkle rectnagles.
            
            screen.blit(user_text, (60, 105 + n))
            screen.blit(score_text, (700, 105 + n))
            screen.blit(level_text, (1100, 105 + n))


        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

    def time_all(self):
        self.state = "time_all"

        # drawing background and buttons
        screen.fill((255, 255, 255))
        screen.blit(menu_img,(0,0))

        if home2.draw(screen):
            game_state.state_handler = game_state.GUI
        if sort.draw(screen):
            game_state.state_handler = game_state.score_all

        # orders data in ascending order
        conn = sqlite3.connect("Player-data.db")
        cur = conn.cursor()
        cur.execute("""SELECT username, clear1 AS score, 'level 1' FROM Player WHERE clear1 IS NOT NULL
        UNION ALL
        SELECT  username, clear2 AS score, 'level 2'  FROM Player WHERE clear2 IS NOT NULL
        UNION ALL
        SELECT  username, clear3 AS score, 'level 3' FROM Player WHERE clear3 IS NOT NULL
        ORDER BY score ASC LIMIT 6;


        """)# putting each levels into one large list and then ordering it, for every level putting it into a variable so it can be called later
        # outputs username, times and then the level it was acheived on in that order
        datas = cur.fetchall()

        # draws in title
        title = font.render("All Levels", True, (255, 255, 255))# the username text
        # draws in the heading
        Utext = font.render("Username:", True, (255, 255, 255))# the username text
        Stext =  font.render("times:", True, (255, 255, 255))# the score text
        Ltext = font.render("level:", True, (255, 255, 255))# the score text
        pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 , 1325, 85))# draws in the rectnalge which exaplains what the values are

        screen.blit(title, (650, 10))
        screen.blit(Utext, (60, 100))
        screen.blit(Stext, (700, 100))
        screen.blit(Ltext, (1100, 100))
        
            
        n = 0
        x = 0
        for data in datas:
            x += 1
            #Test in progress
            n += 90#The gap between each column
            text1 = f"{x}. {data[0]}"# gets the values in thr username
            text2 = f"{data[1]}"# gets values for the times
            text3 = f"{data[2]}"# gets the values for the levles
            print(text3)

            if text2 == "None":# Converts all of the None values to 9999.
                text2 = "9999"

            
            user_text = Lfont.render(text1, True, (72, 72, 72))# renders in all of the usernames
            score_text = Lfont.render(text2, True, (72, 72, 72))# renders in all of the scores
            level_text = Lfont.render(text3, True, (72, 72, 72))# renders in all of the scores

            #draws in the rows of the leaderboard
            pygame.draw.rect(screen, (72, 72, 72), pygame.Rect(50, 90 + n, 1325, 85))# draws in the border
            pygame.draw.rect(screen, (229, 228, 226), pygame.Rect(60, 95 + n, 1300, 75))# draws multipkle rectnagles.
            
            screen.blit(user_text, (60, 105 + n))
            screen.blit(score_text, (700, 105 + n))
            screen.blit(level_text, (1100, 105 + n))


        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()


        
    def level_1(self):
        self.state = "level_1"
        base_level()
    def level_2(self):
        self.state = "level_2"
        base_level()
    def level_3(self):
        self.state = "level_3"
        base_level()
    def end_screen(self):
        global level
        global final_score_text
        global final_score_rect
        self.state = "end_screen"
        Lusername = username.get_value()

        
        screen.fill((255, 255, 255))
        screen.blit(menu_img,(0,0))

           # gets the highsocre of the player
        conn = sqlite3.connect("Player-data.db")
        cur = conn.cursor()
        if level == 1:
            statement = "SELECT score1 FROM Player WHERE username = (?) "# for levle 1 only
        elif level == 2:
            statement = "SELECT score2 FROM Player WHERE username = (?) "# for level 2 only
        elif level == 3:
            statement = "SELECT score3 FROM Player WHERE username = (?) "# for levle 3 only
        tuples = (Lusername, )
        cur.execute(statement, tuples)
        datas = cur.fetchall()
        for data in datas:
             text = f"{data[0]}"# gets only the value of the high score
             high_score_text = font.render("high score: {}".format(text), True, (255, 255, 255))# the high score
             screen.blit(high_score_text, high_score_rect)
             
             
        conn.close()

        final_score_text = font.render("score: {}".format(game_state.total_score), True, (255, 255, 255))# updating the score
        screen.blit(final_score_text, final_score_rect)# displaying the score

        final_time_text = font.render("time taken: {} seconds ".format(game_state.total_time), True, (255, 255, 255))# updating the time
        screen.blit(final_time_text, final_time_rect)# displaying the score

        if home2.draw(screen):
            game_state.state_handler = game_state.GUI
            pygame.mixer.music.stop()# stops gameplay music
            if music_on == True:
                pygame.mixer.music.load("C:\Al Faysal\python\sound\GUI.mp3")# loads in the GUI music
                pygame.mixer.music.set_volume(0.6)#adjust the volume
                pygame.mixer.music.play(-1, 0.0, 5000)# -1 means that it'll loop forever.
        if Next.draw(screen):

            y_scroll = 0
            x_scroll = 0# everything stops scrolling when the player dies.
            bg_scroll = 0

            
            static_time = pygame.time.get_ticks() // 1000# resetting time
            length_time = current_time - static_time# resetting time
            minutes = 0


            score = 0# resetting the score
            
            if level == 1:
                game_state.state_handler = game_state.level_2
                static_time = pygame.time.get_ticks() // 1000
                score = 0
                level = 2
                x_scroll = 0
                y_scroll = 0
                level_data = reset()
                #loading in the levels:
                with open(f"level.no{level}.csv", newline = "") as csvfile:
                    viewer = csv.reader(csvfile, delimiter = ",")# creating an object which only views the values in the csv file.
                    for x, row in enumerate(viewer):# without the enumerate the result will only return a string; the program can handle integers but not strings.
                            for y, tile in enumerate(row):
                                level_data[x][y] = int(tile)
                world = World()
                player, Health_bar, magic_bar = world.process_data(level_data)
                pygame.display.flip()
                return level
            
            elif level == 2:
                game_state.state_handler = game_state.level_3
                static_time = pygame.time.get_ticks() // 1000
                level = 3
                x_scroll = 0
                y_scroll = 0
                level_data = reset()
                #loading in the levels:
                with open(f"level.no{level}.csv", newline = "") as csvfile:
                    viewer = csv.reader(csvfile, delimiter = ",")# creating an object which only views the values in the csv file.
                    for x, row in enumerate(viewer):# without the enumerate the result will only return a string; the program can handle integers but not strings.
                            for y, tile in enumerate(row):
                                level_data[x][y] = int(tile)
                world = World()
                player, Health_bar, magic_bar = world.process_data(level_data)
                pygame.display.flip()
                return level
            else:# if the level is 3 or more; go back to GUI as there is no more levles.
                game_state.state_handler = game_state.GUI


        events = pygame.event.get()

        
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        


    def state_handler(self):
        if self.state == "GUI":
            self.GUI()
        if self.state == "level_1":
            self.level_1()
        if self.state == "level_2":
            self.level_2()
        if self.state == "level_3":
            self.level_3()
        if self.state == "end_screen":
            self.end_screen()
        if self.state == "Lscore1":
            self.Lscore1()
        if self.state == "Lscore2":
            self.Lscore2()
        if self.state == "Lscore3":
            self.Lscore3()
        if self.state == "Ltime1":
            self.Ltime1()
        if self.state == "Ltime2":
            self.Ltime2()
        if self.state == "Ltime3":
            self.Ltime3()
        if self.state == "score_all":
            self.score_all()
        if self.state == "time_all":
            self.time_all()
        
    
game_state = Gamestate()#this will help to run the different aspects of the game


font2 = pygame.font.SysFont("'arial'", 400)# font and size of the results


final_score_text = font2.render("score: {}".format(game_state.total_score), True, (255, 255, 255))# updating the score
final_score_rect = final_score_text.get_rect()
final_score_rect.center = 1500//2, 900// 2

final_time_text = font2.render("score: {}".format(game_state.total_time), True, (255, 255, 255))# updating the time
final_time_rect = final_score_text.get_rect()
final_time_rect.center = 1500//2, 700


text =  " "# initilises text
high_score_text = font2.render("high score: {}".format(text), True, (255, 255, 255))# updating the score
high_score_rect = high_score_text.get_rect()
high_score_rect.center = 1050, 300#placing the rectanlge onto the screen


while True:
    game_state.state_handler()# runs the GUI element of the game
    #sets the FPS.
    clock.tick(FPS)
#draws the background    
   

    pygame.display.update()
pygame.quit()
# credits for player character is penzilla
#background image by craftpix.net
# tilesheet from Kenny
