from words import game_words
from random import choice


l = game_words
a = choice(l)

curr_word = []
for i in a:
    curr_word.append(i)


print("_ _ _ _ _")
n = 6
while(n>0):
    word_dict = dict()
    for i in curr_word:
        if(i in word_dict):
            pass
        else:
            word_dict[i] = curr_word.count(i)
    guess = []
    x = input()
    for i in x:
        guess.append(i)
    print(guess)
    
    # 0 = gray
    # 1 = yellow
    # 2 = green

    reply=[0]*5
    for i in range(len(guess)):
        if(guess[i]==curr_word[i] and word_dict[guess[i]]>0):
            reply[i]+=2
            word_dict[guess[i]]-=1
    for i in range(len(guess)):
        if(guess[i]!=curr_word[i] and guess[i] in curr_word and word_dict[guess[i]]>0):
            if(reply[i]==0):
                reply[i]+=1

    for i in range(len(reply)):
        if(reply[i]==0):
            reply[i] = "0"
        elif(reply[i]==1):
            reply[i] = "1"
        else:
            reply[i]="2"
    print(reply)
    if(reply==["2"]*len(curr_word)):
        print("You Win")
        break
    n-=1
    if(n==0):
        print("You Lose")
        print(f"The word was: {a}\n{curr_word}")