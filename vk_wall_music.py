#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import vk_auth # from  http://alexkutsan.blogspot.com/2013/07/api-vk-python.html
import vkontakte, json
import sys, re
import collections
reload(sys)
sys.setdefaultencoding('utf-8')    # Setting default encoding

'''
This script gets last 100 posts from vkontakte wall and finds posts which have an audio attachment.
This script uses vk_auth module from  http://alexkutsan.blogspot.com/2013/07/api-vk-python.html 
'''


def get_links(login, password):
    '''
    Returns a links of posts, which have an audio attachment.
    Structure: [(URL, TITLE)] NOTE: Title is a part of post's text.
    '''
    token, user_id = vk_auth.auth(login, password, "4398787", "wall") #Authenticate, get token and uid
    vk = vkontakte.API(token=token)
    screen_name =  vk.users.get(uids=user_id, fields='screen_name')[0]['screen_name']

    res = vk.wall.get(count=100)  # Get posts

    links = []

    for post in res[1:]:  # Get posts only with audio attachment
        attachments = post.get('attachments')
        if attachments is not None:
            for att in attachments:
                if 'audio' in att.values():
                    author_id, post_id = str(post['from_id']), str(post['id'])
                    title = post['text'][:100]
                    links.append(('http://vk.com/%s?w=wall%s_%s' % (screen_name, author_id, post_id), title)) 
                    break         

    return links                
    
    
def generate_html(links):
    '''
    Generates HTML file with links.
    '''
    result_string = ''
    for link in enumerate(links):
        num = link[0] + 1 # Start with 1, not 0
        url = link[1][0]
        title_with_tags = link[1][1]
        title_without_tags = re.sub('<[^<]+?>', '', title_with_tags).replace('<', '') # Remove html tags and '<' symbols
        if title_without_tags:
            title_without_tags  += '...'
        result_string += '\t\t\t%d) <a href="%s">%s</a><br>\n' % (num, url,  title_without_tags or 'No name') # Adding link to results


    file = open('result.html', 'w') # Write to file
    res = file.write(
    '''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>VK Wall</title>
    </head>
    <body>
        <div class="links">\n%s\t</div>
    </body>
    </html>
    ''' % result_string
    )

def print_results(links):
    result_string = ''
    for link in enumerate(links):
        num = link[0] + 1
        url = link[1][0]
        result_string += '%d)\t%s\n' % (num, url)
    print result_string

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage: python vk_wall_music username password [-html]' 
        exit()
    print 'wait...'    
    username = sys.argv[1]
    password = sys.argv[2] 
    links = get_links(username, password)   
    if len(sys.argv) == 4:
        if sys.argv[3] == '-html':
            print 'HTML Mode: ON'
            generate_html(links) 
            print 'HTML is generated. Look at the result.html file.'
    else:
        print_results(links)  