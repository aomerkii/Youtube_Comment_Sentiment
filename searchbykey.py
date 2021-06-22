
from googleapiclient.discovery import build
import pandas as pd
import demoji,re
from langdetect import detect
from textblob import TextBlob
import matplotlib as mpl
import matplotlib.pyplot as plt
from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS
import random

TempApi = ["AIzaSyC1w73iLDrc_V5iq-otwVZzx-C1OH9DBHk",
               "AIzaSyD6u0mXbRF1xvHTKbeBCHO4d6kVeuy_gcY",
               "AIzaSyAnPNaQU7D35nB-7Bbc4nFyCeMkDMY0Vd4",
               "AIzaSyDkPp-qGi6vHT_YCIUm6mBpl4ecw-JCyNo",
               "AIzaSyAgwDyRaJa1Bao6DwfPnN2cnFXILCvfh6g",
               "AIzaSyAyAPGovEXPai6VKhT8VmNZDuNwJeYCKHU",
               "AIzaSyAG2E7ybgiXbwvyQnNuNa7VXt97M5rWpVs",
               "AIzaSyAG2E7ybgiXbwvyQnNuNa7VXt97M5rWpVs",
               "AIzaSyB81jEJFJZ4PvbdRARdaC3mL0M5zNd9PwM",
               "AIzaSyDK4KdCEe19OVeHNz2xn4NGZfG5z3knnRs",
               "AIzaSyAUnFaNxoY7-VKiPuY6i38lmxNmBcCdD8Q",
               "AIzaSyB8N3bXmY_7hj5kjamtJmrhxrzd7pkgToU",
               "AIzaSyDN1EnXCpV2I3OjqhCzfByu9Wc-1hlNJ7c",
               "AIzaSyAP6gfSXJU8Gw4qM5FM9TXjTWQPJ7BdjKQ",
               "AIzaSyAMG4_TRmMNGZV5vkhw-6j59gEDlWbxlhs",
               "AIzaSyA6V6WoMAsFKzowJcPq8bPuuoBxT6YBXcM",
               "AIzaSyDc7Kmyn6f6YxTyMNWvJe6izThtuBWZjSU",
               "AIzaSyDrCUkrdQaZOX-yAVaftZC_2BoVi1yZ2XM",
               "AIzaSyB-qovr3B8llt02_sCwW0xb_Psn_1Ti6hs",
               "AIzaSyBzUMFv6BNR0OwvttGiOiHZMVsflEl066c",
               "AIzaSyAJuYfLo5g_1LjwAaRg5vng8WSPpMRx6e4",
               "AIzaSyAWDf6NazehW-f29SnSzv4ozG-8tEX9Chs",
               "AIzaSyDZyYuZ7vxc6Jtjjf-4oRFu-yvAGqKPnOw"]
#set api 
def setAPI():
    youTubeApiKey=TempApi[random.randint(0,len(TempApi)-1)]
    service=build('youtube','v3',developerKey=youTubeApiKey)
    return service

#function for searching query in youtube by using API
def youtube_search(querysearch):
    query=str(querysearch) 
    query_results=setAPI().search().list(part='snippet',q=query,order='relevance',type='video',relevanceLanguage='en',safeSearch='moderate').execute()
    return query_results
 
#listing the result of query
def show_list(keyword):
    querysearch=keyword
    query_results=youtube_search(querysearch)
    #creat empty list
    video_id=[]
    channel=[]
    video_title=[]
    video_desc=[]

    #loop for keeping query_results in list
    for item in query_results['items']:
        video_id.append(item['id']['videoId'])
        channel.append(item['snippet']['channelTitle'])
        video_title.append(item['snippet']['title'])
        video_desc.append(item['snippet']['description'])

    youtube_list={
            'video_id': video_id,
            'channel':channel,
            'video_title' :video_title,
            'video_desc':video_desc
         }

    youtube_df =pd.DataFrame(youtube_list,columns=youtube_list.keys())
    return youtube_df

#To select the video for analyzing
def choosevideo(keyword,row):
    querysearch=keyword
    query_results=youtube_search(querysearch)
    #creat empty list
    video_id=[]
    channel=[]
    video_title=[]
    video_desc=[]

    #loop for keeping query_results in list
    for item in query_results['items']:
        video_id.append(item['id']['videoId'])
        channel.append(item['snippet']['channelTitle'])
        video_title.append(item['snippet']['title'])
        video_desc.append(item['snippet']['description'])

    #specify the video
    video_id=video_id[row]
    video_desc=video_desc[row]
    video_title=video_title[row]
    channel=channel[row]

    #create empty lists
    video_id_pop = []
    channel_pop = []
    video_title_pop =[]
    video_desc_pop = []
    comments_pop =[]
    comment_id_pop =[]
    reply_count_pop =[]
    like_count_pop =[]

    comments_temp = []
    comment_id_temp = []
    reply_count_temp= []
    like_count_temp= []

    nextPage_token = None

    while 1:
        response = setAPI().commentThreads().list(
                        part ='snippet',
                        videoId = video_id,
                        maxResults = 100,
                        order = 'relevance',
                        textFormat = 'plainText',
                        pageToken = nextPage_token
                        ).execute()

        nextPage_token = response.get('nextPageToken')
        for item in response[ 'items']:
            comments_temp.append(item['snippet']['topLevelComment']['snippet']['textDisplay'])
            comment_id_temp.append(item['snippet']['topLevelComment']['id'])
            reply_count_temp.append(item['snippet']['totalReplyCount'])
            like_count_temp.append(item['snippet']['topLevelComment']['snippet']['likeCount'])
            comments_pop.extend(comments_temp)
            comment_id_pop.extend(comment_id_temp)
            reply_count_pop.extend(reply_count_temp)
            like_count_pop.extend(like_count_temp)

            video_id_pop.extend([video_id]*len(comments_temp))
            channel_pop.extend([channel]*len(comments_temp))
            video_title_pop.extend([video_title] *len(comments_temp))
            video_desc_pop.extend([video_desc]*len(comments_temp))                                                       
                                                             
        if nextPage_token is None:
            break

    output_video={
        'Video Title' :video_title_pop,
        'Video Description': video_desc_pop,
        'Video ID': video_id_pop,
        'comment': comments_pop,
        'Comment ID': comment_id_pop,
        'Replies': reply_count_pop,
        'Likes': like_count_pop
        }

    video_df =pd.DataFrame(output_video,columns=output_video.keys())
    return video_df

def sentiment(video_df):
    #drop the duplicates
    comments=video_df.drop_duplicates(subset=['comment'])
    comments=comments.reset_index(drop=True)
    
    #remove emoji
    comments['clean_comments']=comments['comment'].apply(lambda x: demoji.replace(x,""))
    
    #detect whether english language or not 
    comments['lang']=0
    for i in range(0,len(comments)):
        temp = comments.iloc[i,7]
        try:
            comments.iloc[i,8] = detect(temp)
        except:
            comments.iloc[i,8] = "error"

    #keep only english comments
    english_comm = comments[comments['lang'] == 'en']

    #Remove brackets & special characters
    copy=english_comm.copy()
    regex = r"[^0-9A-Za-z'\t]"
    copy['reg'] = copy['clean_comments'].apply(lambda x:re.findall(regex,x)) #remove special brackets
    copy['regular_comments'] = copy['clean_comments'].apply(lambda x:re.sub(regex,"  ",x)) #remove special characters
    copy['regular_comments'] = copy['clean_comments'].str.lower()
    copy['polarity']=copy['regular_comments'].apply(lambda x: TextBlob(x).sentiment.polarity) #sentiment analysis
    
    #classify class
    copy['class']='neutral'
    copy['class'][copy.polarity>0.25]='positive'
    copy['class'][copy.polarity<-0.25]='negative'

    dataset = copy[['Video ID','comment','regular_comments','class']].copy()
    return dataset

#creat wordcloud visualized 
def wordcloud(data):
    mpl.rcParams['figure.figsize']=(15,15) 
    mpl.rcParams['font.size']=12                #10 
    mpl.rcParams['savefig.dpi']=100             #72 
    mpl.rcParams['figure.subplot.bottom']=.1 

    stopwords = set(STOPWORDS)  #split sentence to word 
    wordcloud = WordCloud(
                          background_color='white',
                          stopwords=stopwords,
                          max_words=200,
                          max_font_size=40, 
                          random_state=42
                         ).generate(str(data['comment']))

    fig = plt.figure(1)
    plt.imshow(wordcloud)
    plt.axis('off')
    return fig


