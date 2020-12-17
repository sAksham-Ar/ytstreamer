import requests
from bs4 import BeautifulSoup
from sys import argv
import os
def getvideos():
    search_term=argv[1]
    search_type=argv[2]
    try:
        url="https://invidious.snopyta.org/search?q="+search_term
    except Exception as e:
        print(str(e))
    page = BeautifulSoup(requests.get(url, timeout=15).text, 'lxml')
    results=page.find_all('a',href=True)
    if search_type=="c":
        for result in results:
            result_url=result.attrs['href']
            if result_url[:9]=="/channel/":
                result_url="https://invidious.snopyta.org"+result_url+"?page="
                break
    else:
        result_url=url+"&page="
    page_num=1
    while True:
        channel=BeautifulSoup(requests.get(result_url+str(page_num), {}).text, 'lxml')
        links=channel.find_all('a',href=True)
        video_links=[]
        titles=[]
        lengths=[]
        for link in links:
            video_url=link.attrs['href']
            if video_url[:7]=="/watch?" and video_url not in video_links:
                video_links.append(video_url)
                lengths.append(link.find_next('p').text)
                titles.append(link.find_next('a').text)
        for i in range(0,len(titles)):
            print("{:<3} {:<100} {:<10}".format(str(i+1),titles[i],lengths[i]))
        choice=int(input("Which video do you want to play?"))
        while choice!=0:
            youtube_link="https://www.youtube.com"+video_links[choice-1]
            os.system("vlc "+youtube_link)
            choice=int(input("Play another?"))
        choice=int(input("Next Page?"))
        if choice!=0:
            page_num+=1
        else:
            break
if __name__ == "__main__":
    getvideos()





