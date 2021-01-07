import requests
from bs4 import BeautifulSoup
from sys import argv
import re
import os
def getvideos():
    search_term=argv[1]
    search_type=argv[2]
    try:
        url="https://invidious.snopyta.org/search?q="+search_term
        r = requests.get(url, stream=True)
        page = BeautifulSoup(r.content, 'html.parser')
    except:
        print("Failed.Please try again later.")
        return
    if search_type=="c":
        results=page.find_all(href=re.compile("/channel/"))
        results=[result for result in results if search_term.lower() in result.text.lower()]
        result_url="https://invidious.snopyta.org"+results[0].attrs['href']+"?page="
    else:
        result_url=url+"&page="
    page_num=1
    while True:
        channel=page
        if page_num!=1 or search_type=='c':
            r = requests.get(result_url+str(page_num), stream=True)
            channel = BeautifulSoup(r.content, 'html.parser')
        links=channel.find_all(href=re.compile("/watch?"))
        lengths=[link.text.strip() for link in links[::2]]
        links = links[1::2]
        video_links=["https://www.youtube.com"+link.attrs['href'] for link in links]
        titles=[link.text for link in links]
        for i in range(0,len(titles)):
            print("{:<3} {:<100} {:<10}".format(str(i+1),titles[i],lengths[i]))
        choice=int(input("Which video do you want to play?"))
        while choice!=0:
            youtube_link=video_links[choice-1]
            os.system("vlc "+youtube_link)
            choice=int(input("Play another?"))
        choice=int(input("Next Page?"))
        if choice!=0:
            page_num+=1
        else:
            break
if __name__ == "__main__":
    getvideos()





