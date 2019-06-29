#!/usr/bin/python

from fbchat import Client
from fbchat.models import *
import logging
from time import sleep
from getpass import getpass

print('Please Wait Some Time It Take Some Time to Learn Conversation....\n')
# qustion and anwser file open and create a dictionary
Q = open('qus.txt', 'r', encoding='utf-8').readlines()  # create a ques file
A = open('ans.txt', 'r', encoding='utf-8').readlines()  # create a anwser file
# in that files Qus and Ans must be in same line
QA = {}
for q, a in zip(Q, A):
    """here this loop set the Qus as a key and Ans as a value of QA dictionary"""
    QA[q.replace('\n', '').lower()] = a.replace('\n', '')

sleep(5)


class Main_Client(Client):
    QA = QA
    bool = False  # it's just for a frist message when this bot is start frist time'
    color = {'Lite_purple': ThreadColor.BILOBA_FLOWER, 'Pink': ThreadColor.BRILLIANT_ROSE,
             'Brown_shade': ThreadColor.CAMEO, 'Sky_blue': ThreadColor.DEEP_SKY_BLUE, 'Farn': ThreadColor.FERN,
             'Lite_green': ThreadColor.FREE_SPEECH_GREEN, 'Golden_poppy': ThreadColor.GOLDEN_POPPY,
             'Lite_coral': ThreadColor.LIGHT_CORAL, 'Medium_slate_blue': ThreadColor.MEDIUM_SLATE_BLUE,
             'Messenger_blue': ThreadColor.MESSENGER_BLUE, 'Picton_blue': ThreadColor.PICTON_BLUE,
             'Pumpkin': ThreadColor.PUMPKIN, 'Red': ThreadColor.RADICAL_RED, 'Shocking': ThreadColor.SHOCKING,
             'Viking': ThreadColor.VIKING}  # It's for change the conversition color
    help = "Here You Find a list of commands\n1.Change Colour To [colour name]\n2.Show ChatColours\n3.Change Emoji To [emoji]\n4.Change Nickname To [Name]"  # help menu

    def onMessage(self, author_id, message_object, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        self.markAsRead(author_id)
        print(message_object)
        if message_object.text == None and len(message_object.attachments) > 0:
            self.send(Message(text='''Sorry!I can't read photo.'''), thread_id=thread_id, thread_type=thread_type)
        else:
            self.msg = message_object.text
            self.msg = self.msg.lower()
            print(self.msg)

        if author_id != self.uid:
            if Main_Client.bool == False:
                '''its for send a message for 1 time when this bot run for frist time'''
                self.messge_send = self.send(Message(
                    text='''How Can I Help You Sir.I am a Facebook Bot, Created By Bishal with Python\n'''),
                                             thread_id=thread_id, thread_type=thread_type)
            if 'change colour to' in self.msg:
                '''find that text in message if exist then find the color name from the class dict if found then change with that color else show a another message'''
                text = message_object.text
                text = text.split()
                print(text)
                self.colorname = text[-1].capitalize()
                print(self.colorname)
                if self.colorname in Main_Client.color.keys():

                    Main_Client.bool = True
                    t_c = Main_Client.color.get(self.colorname)
                    print(t_c)
                    self.changeThreadColor(t_c, thread_id=thread_id)
                    self.send(Message(text="Chat Colour Is Changed Successfully!🔍🔎"), thread_id=thread_id,
                              thread_type=thread_type)
                else:
                    self.send(Message(text=f'''Colour Is unavailable 😓'''), thread_id=thread_id,
                              thread_type=thread_type)
            elif 'Show ChatColours'.lower() in message_object.text.lower():
                '''It's send a messge of a list of colors name which is avabile'''
                Main_Client.bool = True
                colors = ''.join(f'{p+1}.' + i + "\n" for p, i in enumerate(Main_Client.color.keys()))
                showmsg = f'This Colours is available\n{colors}'
                self.send(Message(text=showmsg), thread_id=thread_id, thread_type=thread_type)
            elif message_object.text == 'help' or message_object.text == 'Help':
                '''send the help menu'''
                self.send(Message(text=Main_Client.help), thread_id=thread_id, thread_type=thread_type)
                Main_Client.bool = True
            elif 'Change Emoji To'.lower() in message_object.text.lower():
                '''its change emoji of this conversation'''
                text = message_object.text
                text = text.split()
                emoj = text[-1]
                try:
                    self.changeThreadEmoji(emoji=emoj, thread_id=thread_id)
                    self.send(Message(text=f'''Changed the emoji to {emoj}'''), thread_id=thread_id,
                              thread_type=thread_type)
                    Main_Client.bool = True
                except Exception as ex:
                    self.send(Message(text='Something is wrong!😟'), thread_id=thread_id, thread_type=thread_type)
            elif 'Change Nickname To'.lower() in message_object.text.lower():
                '''Set nickname by bot'''
                text = message_object.text
                text = text.split()
                nick = text[-1].capitalize()
                self.changeThreadTitle(nick, thread_id=thread_id, thread_type=thread_type)
                self.send(Message(text=f'Your Nickname  in changed to {nick} 😎'), thread_id=thread_id,
                          thread_type=thread_type)
                Main_Client.boot = True
            elif self.msg in Main_Client.QA.keys():
                '''Nothing special it's just for match of another person's message if that message is match with built-in questions(in a question file) then send a specific anwser of that ques or messge which is also built-in anwser(in a anwser file)'''
                getans = Main_Client.QA.get(self.msg)
                self.messge_send = self.send(Message(text=getans), thread_id=thread_id, thread_type=thread_type)
                Main_Client.bool = True
            else:
                Main_Client.bool = True
                '''if recived messg is not in you file then send a another messge'''
                self.messge_send = self.send(Message(text='''Sorry!! Sir.\nI Don't understand.😞'''),
                                             thread_id=thread_id, thread_type=thread_type)
        self.markAsDelivered(author_id, self.messge_send)


email = input('Enter Your email or username:')
passs = getpass('Enter Your Password:')
client = Main_Client(email, passs, logging_level=logging.DEBUG)
client.listen()

