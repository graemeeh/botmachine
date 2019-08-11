#! /usr/bin/env python3

import praw
from time import sleep
import markovify
import re
import nltk

posts=[]
usercomments=[]
text=""

with open("postsrepliedto.txt") as file:
    posts=file.read().splitlines()

guido="I deny dese accusations bein made by my fingatips. I been buyin stolen bataries from Gustavo fuh yeas I cant believe hed get his stugotz stuck in the soda machine at Tim hortons but I stand by da kids dat saw it. ITS A DAMN SHAME WHAT EVERYONE BUT ME HAS BEEN DOIN TO DA BROADS. Whoa whatta we got here a Puerto Rican a chinese and a Jew. Look at dese beautiful fuckin missles baby each one like a big fuckin finga I wanna kiss da sauce off of. Belissimo tomaduccios mama mia. what da fuck is dis violin parade bullsh- DATS RITE BABY BLUE LIVES MATTA!!!. Ey im freakin gay now just kidden heh heh seriously tho im not gay now im jus visitin. I neva meant ta say anyting dat was racialist [burping up sauce] I respect all races and people [more pasta barf] POCs are *kissing fingers*. PLEASE GET BACK IN DA KITCHEN BROADS WE NEED YOU. im in de uh sanitation bidness. Ey heres how ya fic da racism problems in dis country ya just (long string of censor beeps) bada bing (more beeps) bada boom Easyducio. Resto piecaliano to antny Scalia da best president of judging dis country ever had Ripe ole age of 79 dats 553 in dago years. Yea how do I orda a freakin blow job ova hea im just kiddin lemme get a cannoli"

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii')

def rip(user):
    global usercomments
    global text
    for comment in user:
        if comment not in usercomments:
            commentb=deEmojify(str(comment.body)) 
            usercomments.append(comment.id)
            text=(text+". "+commentb)
    return text

def unmention(b):
    g=[]
    g=b.split("/")
    if g[0]=="u" or g[0]=="U":
        a=str(g[1])
        return a
    else:
        return b

def program():
    global posts
    global usercomments
    global text
    reddit=praw.Reddit("bot2")
    for i in reddit.inbox.mentions():
        if str(i.id) not in posts:
            posts.append(i.id)
            k=str(i.body)
            B=k.split(" ")
            l=unmention(str(B[1]))
            with open("postsrepliedto.txt","w+") as file:
                for j in posts:
                    file.write(j+"\n")
            print("posting...")
            if l=="bot-o-tron":
                comment_model = markovify.Text(guido)
                i.reply(comment_model.make_sentence(test_output=False))
                print("ah, gabagool")
            else:
                user=reddit.redditor(l).comments.new()
                text=rip(user)
                i.reply(markovify.Text(text).make_sentence(tries=100))
                
            sleep(2)
            text=""
            print("replied to: "+i.id)
            
while True:
    program()
    sleep(5)
