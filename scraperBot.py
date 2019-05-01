#chatBot
#By DracoRanger

import asyncio
from datetime import datetime
from datetime import timedelta
import unicodedata
import os

import discord
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix='!', description='')

config = open('botData.txt', 'r')
conf = config.readlines() #push to array or do directly
token = conf[0][:-1]
server_id = conf[1][:-1]
writeLocl = conf[2][:-1]
cornell = conf[3][:-2]

def listToString(target):
    ret = '['
    for i in target:
        ret = ret + ' \'' + i +'\','
    ret = ret[:-1] + ']'
    return ret

def clearBuffer(names, buffers):
    for x,y in names,buffers:
        with open(writeLocl+x+'.txt', 'a') as file:
            file.write(y.decode('ascii'))
        y=bytes()


#TODO reverse logic, since it appears that lastmessage is the newer message
@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print(str(datetime.now()))
    print('------')

    #lineID, character ID, movieID, characterName, text of utterance
    lines = bytes()
    #characterID, replying to ID, movieID, list of lines in conversation
    conversation = bytes()

    os.remove(writeLocl+'lines'+'.txt')
    os.remove(writeLocl+'conversation'+'.txt')

    lineNum = 0
    delim = ' +++$+++ '
    currentConversation = {}

    for channel in client.get_server(server_id).channels:
        print('Attempting '+channel.name)
        moreRecent = False
        try:
            async for message in client.logs_from(channel, limit=1000000):
                if cornell == 'y':
                    if(moreRecent):
                        lines = lines + (str(lineNum) + delim + moreRecent.author.name + delim + channel.name + delim + moreRecent.author.name + delim + unicodedata.normalize('NFKD', moreRecent.content).replace('\n', ' ').replace('\r','')+'\n').encode('ascii', 'ignore')
                        if (moreRecent.author.name+' '+message.author.name) in currentConversation:
                            currentConversation[moreRecent.author.name+' '+message.author.name].append(str(lineNum))
                        else:
                            currentConversation[moreRecent.author.name+' '+message.author.name] = [str(lineNum)]
                        if(moreRecent.timestamp - message.timestamp > timedelta(seconds = 1200)):#assume that if 20 minutes have passed since last message, new conversation
                            for i in currentConversation:
                                conversation = conversation + (i.split(' ')[0]+delim+i.split(' ')[1]+delim+channel.name+delim+listToString(currentConversation[i])+'\n').encode('ascii','ignore')
                            currentConversation={}
                        else:
                            lineNum = lineNum + 1
                        moreRecent = message
                        if lineNum % 5000 == 0:
                            clearBuffer(['lines','conversation'],[lines,conversation])
                    else:
                        moreRecent = message
                else:
                    lines = lines + '>' + unicodedata.normalize('NFKD', message.content).replace('\n', ' ').replace('\r','')+'\n').encode('ascii', 'ignore')
                    lineNum = lineNum + 1
                    if lineNum % 5000 == 0:
                        clearBuffer(['lines','conversation'],[lines,conversation])

            print('scraped '+channel.name)
        except Exception as e:
            print('unable to access '+ channel.name)
            print('reason: '+str(e))
    if lineNum % 5000 == 0:
        clearBuffer(['lines','conversation'],[lines,conversation])
    print('complete')
client.run(token)
