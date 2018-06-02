import requests,json,ast
import random
from config import number_of_users, max_posts_per_user,max_likes_per_user
#from operator import itemgetter
def register(data):
    r = requests.post("http://127.0.0.1:8000/users/",data=data)
    jsonic = json.loads(r.text)
    bot_id = jsonic.get('id')
    data['id'] = bot_id
    return data 
def login(data):
    r = requests.post("http://127.0.0.1:8000/login/", data=data)
    jsonic = json.loads(r.text)
    token = jsonic.get('token')
    data['token'] = token 
    return data
bot_list = []
for i in range(0,number_of_users):
    num = str(i)
    data = {
        "username" : "Bot_" + num,
        "email" : "jeanclaude" + num + "@gmail.com",
        "password" : "beepimasheep",
    }
    
    bot = register(data)
    bot = login(bot)
    print(bot['username'] + "registered")
    num_posts = random.randrange(0,max_posts_per_user)
    post_list = []
    print("\nCreating posts\n")
    for k in range(0,num_posts):
        headers = {
            'Authorization' : "JWT " + bot['token']
        }
        post_data = {
            "title" : "This is a title",
            "body" : "Beep beep I'm a sheep - " + str(k)
        }
        r = requests.post("http://127.0.0.1:8000/posts/",data=post_data,headers=headers)
        #print(r.text)
        jsonic = json.loads(r.text)
        post_id = jsonic.get('id')
        post_list.append(post_id)
    bot['posts'] = post_list
    bot['likes'] = 0
    
    bot_list.append(bot)
''' 
                    LIKING 
'''

bot_list = sorted(bot_list, key=lambda k: len(k['posts']), reverse=True) #sort the bots by the number of posts
#print(bot_list)

#post_list = ast.literal_eval(jsonic)
def can_like(jsonic):
    for post in jsonic:
        print("LIKES", post['likes'])
        if((len(post['likes']))==0):
            return True
        print(post['id'])
        #print('jbg')
        return False


    #for post in post_list:
        #empty = []
#FINAL - CHECK 

for bot in bot_list:
    headers = {'Authorization' : "JWT " + bot['token']}
    r = requests.get("http://127.0.0.1:8000/posts/", headers=headers)
    jsonic = json.loads(r.text)
    for post in jsonic:
        #print(post['likes'])
        if(bot['likes']==max_likes_per_user):
            print("LIMIT REACHED")
            break
        if(bot['id']!=post['user']):
            if((len(post['likes']))==0):
                
                b_dic = next(mot for mot in bot_list if mot["id"] == post['user'])
                print("\n\n" + str(b_dic["posts"]) + "\n\n")
                num = random.choice(b_dic["posts"]) #does the random
                headers = {'Authorization' : "JWT " + bot['token']}
                r = requests.post("http://127.0.0.1:8000/likes/",data={'post_id' : num},headers=headers)
                bot['likes'] += 1
                print("Liking post with an id - two :", num)
            else:
                url = "http://127.0.0.1:8000/posts/user/" + str(post['user'])
                r = requests.get(url,headers=headers)
                jsonic = json.loads(r.text)  #here we check if one of the posts made by the user is liked or not
                if(can_like(jsonic)): 
                    b_dic = next(mot for mot in bot_list if mot["id"] == post['user'])
                    print("\n\n" + str(b_dic["posts"]) + "\n\n")
                    num = random.choice(b_dic["posts"]) #does the random
                    #headers = {'Authorization' : "JWT " + bot['token']}
                    r = requests.post("http://127.0.0.1:8000/likes/",data={'post_id' : num},headers=headers)
                    bot['likes'] += 1
                    print("Liking post with an id - three :", num)
## 