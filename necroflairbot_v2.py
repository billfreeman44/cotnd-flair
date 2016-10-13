import praw 
import json
#import time
import urllib
import re
import datetime
#import time


f = open('secret_passwords.txt', 'r')
steamapi=f.readline()
password=f.readline()
f.close()
now = datetime.datetime.now()
user_agent = "Edits flairs on /r/necrodancer - made by mynameismunka"
username='necroflairbot'
steamapi=steamapi[0:-1]
n_pages_max=500



def valid_username(uname):
    #MIN_USERNAME_LENGTH = 3
    #MAX_USERNAME_LENGTH = 20
    user_rx = re.compile(r"\A[\w-]+\Z", re.UNICODE)
    if len(uname) < 3 or len(uname) > 20:
        return False
    if user_rx.match(uname):
        return True
    return False


def addstring_general(output_version,output_namearr,version,poststring,addstring):
    isoutput=False
    for i in range(len(output_version)):
        if output_version[i] == version:
            if isoutput == True:
                addstring=addstring+',\n'
            addstring=addstring+"a.author[href*='user/"+output_namearr[i]+"']:after"
            isoutput=True
    if isoutput == True:
        addstring=addstring+"\n{\n"
        addstring=addstring+"content:url(%%"+poststring+"%%);\n"
        addstring=addstring+"position: relative;\n "
        addstring=addstring+"top: 2px; left: 3px;\n "
        addstring=addstring+"vertical-align: bottom;\n"
        addstring=addstring+"}\n"
    return addstring




def addstring_AC(output_version,output_namearr,output_total,num_coins,addstring):
    isoutput=False
    for i in range(len(output_version)):
        if output_version[i] == 'AC' and output_total[i] == num_coins:
            if isoutput == True:
                addstring=addstring+',\n'
            addstring=addstring+"a.author[href*='user/"+output_namearr[i]+"']:after"
            isoutput=True
    if isoutput == True:
        addstring=addstring+"\n{\n"
        addstring=addstring+"content:url(%%resource-coin"+str(num_coins)+"%%);\n"
        addstring=addstring+"position: relative;\n "
        addstring=addstring+"top: 2px; left: 3px;\n "
        addstring=addstring+"vertical-align: bottom;\n"
        addstring=addstring+"}\n"
    return addstring





rankarray=['cadence_rank','bard_rank',
           'bolt_rank','dove_rank',
           'eli_rank','aria_rank',
           'melody_rank','dorian_rank','monk_rank',
           'coda_rank','all_character_rank',
           'story_mode_rank']

rankarray_output=['Cadence','Bard',
           'Bolt','Dove',
           'Eli','Aria',
           'Melody','Dorian','Monk',
           'Coda','All Characters',
           'Story Mode']

ach_list=['ACH_HARDCORE_CADENCE','ACH_HARDCORE_ARIA',
          'ACH_HARDCORE_BARD','ACH_HARDCORE_BOLT',
          'ACH_HARDCORE_MONK','ACH_HARDCORE_DOVE',
          'ACH_HARDCORE_ELI','ACH_HARDCORE_MELODY',
          'ACH_HARDCORE_DORIAN','ACH_ARIA_LOWPERCENT']


output_namearr=[] #reddit names
output_altarr=[] #string after name
output_version=[] #none < AC < TT < WR < CODA
#none, achievements, top ten, world record, coda beater.
output_steam_id=[]

output_namearr.append('rspeer')
output_steam_id.append('76561198010696153')
output_altarr.append('')
output_version.append('none')

output_namearr.append('BulletNick')
output_steam_id.append('76561198049600266')
output_altarr.append('')
output_version.append('none')







addstring=''
r = praw.Reddit(user_agent=user_agent)
r.config.decode_html_entities = True

r.login(disable_warning=True,username=username,password=password)
#r.send_message('mynameismunka','sup','test message yo')

page_numbers=range(1,n_pages_max) #pages 1 to 100
for page in page_numbers:
    print "on page ",page
    necrolab_score_url='http://www.necrolab.com/api/score_rankings/latest_rankings?page='+str(page)
    response = urllib.urlopen(necrolab_score_url)
    jsondata= json.loads(response.read())

    mode="Score"
    #loop through every name
    for lab_entry in jsondata['data']:
        website=lab_entry['website']
        if website != None:        
            if "reddit" in website and "/" in website:
                split_username=website.split('/')
                username=split_username[-1]
                if len(username) == 0:
                    username=split_username[-2]
                if valid_username(username):
                    print username," - Found! "+mode
                    if username not in output_namearr:
                        output_namearr.append(username)
                        output_steam_id.append(lab_entry['steam_id'])
                        output_altarr.append('')
                        output_version.append('none')
                    index=output_namearr.index(username)
                    #check if valid high score
                    for i in range(len(rankarray)):
                        if lab_entry[rankarray[i]] != None:
                            if lab_entry[rankarray[i]] <11:
                                if lab_entry[rankarray[i]] == 1:
                                    output_version[index] = 'WR'
                                    output_altarr[index]=output_altarr[index]+" * "+rankarray_output[i]+" "+mode+" WR! "
                                else:
                                    if output_version[index] != 'WR':
                                        output_version[index]='TT' # top ten
                                    output_altarr[index]=output_altarr[index]+" * "+rankarray_output[i]+\
                                                          " "+mode+" Rank "+str(lab_entry[rankarray[i]])

    necrolab_score_url='http://www.necrolab.com/api/speed_rankings/latest_rankings?page='+str(page)
    response = urllib.urlopen(necrolab_score_url)
    jsondata= json.loads(response.read())

    mode="Speed"
    #loop through every name
    for lab_entry in jsondata['data']:
        website=lab_entry['website']
        if website != None:        
            if "reddit" in website and "/" in website:
                split_username=website.split('/')
                username=split_username[-1]
                if len(username) == 0:
                    username=split_username[-2]
                if valid_username(username):
                    print username," - Found! "+mode
                    if username not in output_namearr:
                        output_namearr.append(username)
                        output_steam_id.append(lab_entry['steam_id'])
                        output_altarr.append('')
                        output_version.append('none')
                    index=output_namearr.index(username)
                    #check if valid high score
                    for i in range(len(rankarray)):
                        if lab_entry[rankarray[i]] != None:
                            if lab_entry[rankarray[i]] <11:
                                if lab_entry[rankarray[i]] == 1:
                                    output_version[index] = 'WR'
                                    output_altarr[index]=output_altarr[index]+" * "+rankarray_output[i]+" "+mode+" WR! "
                                else:
                                    if output_version[index] != 'WR':
                                        output_version[index]='TT' # top ten
                                    output_altarr[index]=output_altarr[index]+" * "+rankarray_output[i]+\
                                                          " "+mode+" Rank "+str(lab_entry[rankarray[i]])

    necrolab_score_url='http://www.necrolab.com/api/deathless_score_rankings/latest_rankings?page='+str(page)
    response = urllib.urlopen(necrolab_score_url)
    jsondata= json.loads(response.read())

    mode="Deathless"
    #loop through every name
    for lab_entry in jsondata['data']:
        website=lab_entry['website']
        if website != None:        
            if "reddit" in website and "/" in website:
                split_username=website.split('/')
                username=split_username[-1]
                if len(username) == 0:
                    username=split_username[-2]
                if valid_username(username):
                    print username," - Found! "+mode
                    if username not in output_namearr:
                        output_namearr.append(username)
                        output_steam_id.append(lab_entry['steam_id'])
                        output_altarr.append('')
                        output_version.append('none')
                    index=output_namearr.index(username)
                    #check if valid high score
                    for i in range(len(rankarray)-2):
                        if lab_entry[rankarray[i]] != None:
                            if lab_entry[rankarray[i]] <11:
                                if lab_entry[rankarray[i]] == 1:
                                    output_version[index] = 'WR'
                                    output_altarr[index]=output_altarr[index]+" * "+rankarray_output[i]+" "+mode+" WR! "
                                else:
                                    if output_version[index] != 'WR':
                                        output_version[index]='TT' # top ten
                                    output_altarr[index]=output_altarr[index]+" * "+rankarray_output[i]+\
                                                          " "+mode+" Rank "+str(lab_entry[rankarray[i]])





output_total=[]
for i in range(len(output_version)):

    apicall='http://api.steampowered.com/ISteamUserStats/'+\
    'GetUserStatsForGame/v0002/?appid=247080&key='+steamapi+\
    '&steamid='+str(output_steam_id[i])+'&format=json'
    #print apicall
    response = urllib.urlopen(apicall)
    #print response
    try:
        jsondata= json.loads(response.read())
        total=0
        for ach in jsondata['playerstats']['achievements']:
            #ZypherK is dirty h4x0r
            if ach['name'] == 'ACH_HARDCORE_CODA' \
                and output_namearr[i] !=  'ZypherK':
                output_version[i]='CODA'
            if ach['name'] in ach_list:
                total=total+1
        output_total.append(total)
        if total > 0:
            if output_version[i] != 'CODA' and output_version[i] != 'WR' and output_version[i] != 'TT':
                output_version[i] = 'AC'
    except:
        output_total.append(0)
    print output_namearr[i]

              









#CODA outputs.
addstring=addstring_general(output_version,output_namearr,'CODA','lute-boss-head',addstring)
addstring=addstring+'\n'
addstring=addstring_general(output_version,output_namearr,'WR','world-record',addstring)
addstring=addstring+'\n'
addstring=addstring_general(output_version,output_namearr,'TT','topten',addstring)
addstring=addstring+'\n'
for i in range(10):
    addstring=addstring_AC(output_version,output_namearr,output_total,i+1,addstring)
    addstring=addstring+'\n'

print
print
print
print addstring






#alt text for users
#for i in range(len(output_wrarr)):
#    if output_altarr[i] != '':
#        addstring=addstring+"a.author[href*='user/"+output_namearr[i]+"']:hover:after {"
#        addstring=addstring+"content: '"+output_altarr[i]+"' }\n"

for i in range(len(output_namearr)):
    if output_altarr[i] != '':
        print output_namearr[i]+" - "+output_altarr[i]


# OUTPUT THE CSS.
stylesheet=r.get_stylesheet('necrodancer')
styletext=stylesheet['stylesheet']
stylesplit=styletext.split("/*BOT EDITS ABOVE*/")
style_response=r.set_stylesheet('necrodancer',addstring+" \n/*"+now.strftime("%Y-%m-%d %H:%M")+"*/\n\n\n/*BOT EDITS ABOVE*/\n"+stylesplit[1])
##
##print style_response
##print "end of necroflairbot"
##time.sleep(5)
print "exiting"
