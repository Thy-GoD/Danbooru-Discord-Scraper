# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 20:52:15 2022

@author: Thigh GoD
"""
import requests
import sys
import time

# Containers/Functions

url='https://danbooru.donmai.us/posts.json?api_key=YOUR-API-KEY&login=YOUR-LOGIN-USER&limit=200&tags=' # edit this.
url_container=[]
error_container=0
nsfw_rating_dictionary={
    "g":"General",
    "s":"Sensitive",
    "q":"Questionable",
    "e":"Explicit"
    }
unaccepted_rating_container=0
spam_docs_folder='ABSOLUTE PATH OF FOLDER FOR STORING SPAM DOCS (txt files).' # edit this.
banned_tags=['beastiality','big_belly','stomach_bulge','bestiality','futanari','amputee']
# Editable Banned Tags List. (Be as strict as possible, some anomolies may leak.)

def Check_tags(tags):
    global banned_tags
    for i in banned_tags:
        if i in tags:
            return True
    return False
    

# Main Menu

print()
print("Welcome to the Lewd Spam Docs creator/discord poster, it's a two in one tool!")
input('Press enter to continue\n>>>')
print()
print("Use default Webhook (Testing server) or another server's?")
choice=input('type "default" or press enter\n>>>')

# Webhook selection

if choice=="default":
    webhook="ENTER TESTING CHANNEL'S WEBHOOK" # edit this.
else:
    webhook=input('Please enter a webhook URL: \n>>>')
    
# Tag Selection

print()
time.sleep(1)

tag=input("What are the tags? (maximum of two, use a '+' between the two)" +'\n' + '>>>')

if " " in tag:
    tag= tag.replace(' ','_')
    
url+=tag+'&page='



# Rating selection

print()
print('Danbooru has 4 "nsfw" ratings.\n')
print('g = general (Fully SFW)')
print('s = sensitive (Somewhat NSFW)')
print('q = questionable (Almost Explicit NSFW)')
print('e = explicit (Full NSFW)\n')
nsfw_rating=input('Type any of the letters given/"all" if all are selected (example g for SFW results).\nThen press enter. (If more than 1 rating is picked, type them with no spaces)\n>>>')

# Checks if all selected or not.

if nsfw_rating=='all':
    nsfw_rating_container=['g','s','q','e']
else:
    nsfw_rating_container=[*nsfw_rating]

print()
for i in nsfw_rating_container:
    print(f"{nsfw_rating_dictionary[i]} rating has been selected")
    
input("Press enter to run the bot.....")
print()
    

page_number=1 
# Page number set to 1, to avoid unneeded logs. (page 0, results 0 etc.)


# Actual code for the bot (technically a script, but can be turned into a bot.)

condition=True

while condition:
    
    new_url=url+str(page_number)
    
    time.sleep(5)
    headers= {
        'User-Agent':"ENTER USER AGENT HERE" # edit this.
        }
    
    r=requests.get(new_url,headers=headers)

    data=r.json()

    for i in data:
        
        try:
            if 'id' not in i:
                error_container+=1
            elif 'file_url' not in i:
                error_container+=1
            elif '.zip' in i['file_url']:
                error_container+=1   
            elif i['rating'] not in nsfw_rating_container:
                unaccepted_rating_container+=1
                
            elif Check_tags(i['tag_string'].split()):
                error_container+=1
                
            else:
                link=i['file_url']+"\n Artist: " +i['tag_string_artist']
                url_container.append(link)
                
                discord_message= {
                    'content':link
                        }
    
                requests.post(webhook,json=discord_message) # Code that posts the images.
        except:
            error_container+=1
    
    # Statistics Info.
    print('Current Page number is: ' + str(page_number))
    print('Current amount of links posted/recorded is: ' + str(len(url_container)))
    print('Current Rating-Blocked links: ' + str(unaccepted_rating_container))
    print()
            
            
    page_number+=1
            
    if len(data)==0:
        condition=False
            

        
        
# Post-Process Information

print()
print('There are ' + str(error_container) + ' Deleted/Banned Or Invalid Files.')
print(f'Leaving {str(len(url_container))} out of {str(unaccepted_rating_container+len(url_container)+error_container)} links to be processed.')

if len(url_container)==0:
    print('No Results have been found, double-check the tags given.')
    input('')
    sys.exit() 

# Can be edited to re-loop back to the script, or leave it to exit upon invalid tags.

file_name=input('Enter the name of Docs\n' + '>>>')

print()

print(f"'{file_name}' has been chosen as file name")

with open(f'{spam_docs_folder}{file_name}.txt','w') as f:
    for i in range(0, len(url_container), 5):
        f.write('\n'.join(url_container[i:i+5])+ '\n' + '\n')

                
print()
input(f"Links have been copied into the .txt file: '{file_name}'")

## End of Code







        



    
    
    

    











    


