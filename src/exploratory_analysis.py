# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 17:18:10 2018

@author: Vishal Bhoyar
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib_venn import venn2



def SENTIMENT():
    ''' Read the file data '''
    df = pd.read_csv("video_comments_analysis_sentiments.csv", sep='\t' ,names = ["Comment", "CreateTimeStamp", "Type", "videoID","videoTitle", "FNAME", "SENTIMENT_RF", "SENTIMENT_KN"])
    df = df.iloc[1:]
    
    ''' Plot Comments Count chart '''
    
    sns.set_style('white')
    fig1 = plt.figure(figsize=(12,8))
    ax = df['FNAME'].value_counts().plot(kind='bar')
    #plt.title('Video Comments Count for Input Data Files')
    ax.set_xticklabels(ax.get_xticklabels(),rotation=30)
    plt.xlabel("File Name")
    plt.ylabel("Comments Count")
    fig1.savefig('Comment_count_by_file.png')
       
       
    ''' Random Forest data analysis'''
     
    sns.set_style('white')
    fig2 = plt.figure(figsize=(12,8))
    df1 = df.groupby(['videoID']).Comment.agg('count').to_frame('vidiocount').reset_index().sort_values(by='vidiocount', ascending=False).head(10)   
    df2 = pd.merge(df, df1, on='videoID', how='inner') 
    df2['SENTIMENT_RF'] =  np.where(df2['SENTIMENT_RF'] == '0', 'False', 'True')
    g =sns.countplot(x='videoID',hue='SENTIMENT_RF',data=df2)
    #plt.title('Random Forest Classifier Analysis - Top 10 Video')
    g.set_ylabel('Comment Count')
    g.set_xlabel('Video ID')
    g.set_xticklabels(g.get_xticklabels(),rotation=45)
    fig2.savefig('Top 10 Random Forest.png')
     
    '''KNeighbors data analysis '''
    
    sns.set_style('white')
    fig3 = plt.figure(figsize=(12,8))
    df1 = df.groupby(['videoID']).Comment.agg('count').to_frame('vidiocount').reset_index().sort_values(by='vidiocount', ascending=False).head(10)   
    df2 = pd.merge(df, df1, on='videoID', how='inner') 
    df2['SENTIMENT_KN'] =  np.where(df2['SENTIMENT_KN'] == '0', 'False', 'True')
    g =sns.countplot(x='videoID',hue='SENTIMENT_KN',data=df2)
    #plt.title('KNeighbors Classifier Analysis - Top 10 Video')
    g.set_ylabel('Comment Count')
    g.set_xlabel('Video ID')
    g.set_xticklabels(g.get_xticklabels(),rotation=45)
    fig3.savefig('Top 10 KNeighborsClassifier.png')
      

    ''' venn deigram for true values '''
    
    fig4 = plt.figure(figsize=(12,8))
    df3 = df
    df3['KN'] =  np.where((df3['SENTIMENT_KN'] == '1') & (df3['SENTIMENT_KN'] == df3['SENTIMENT_RF']), 'True'+'-'+df3['CreateTimeStamp'], 'KN'+'-' + df3['CreateTimeStamp'])
    df3['RF'] =  np.where((df3['SENTIMENT_RF'] == '1') & (df3['SENTIMENT_RF'] == df3['SENTIMENT_KN']), 'True'+'-'+df3['CreateTimeStamp'], 'RF'+'-' + df3['CreateTimeStamp'])
    my_list = df3["KN"].tolist()
#    print(my_list)
    my_list2 = df3["RF"].tolist()
    venn2([set(my_list), set(my_list2)], set_labels = ('KNeighbors Classifier', 'Random Forest Classifier'))
    #plt.title('KNeighbors and Random Forest True Sentiments')
    fig4.savefig('Classifier True Sentiment Analysis.png')
    plt.gca().set_axis_on()
    plt.show()
    
def Spam_data():  
    
    ''' Read the file data '''
    df = pd.read_csv("video_comments_analysis_spam.csv", sep='\t' ,names = ["Comment", "CreateTimeStamp", "Type", "videoID","videoTitle", "FNAME", "SPAM_IND_RF","SPAM_IND_KN"])
    df = df.iloc[1:]
    
    '''SPAM data analysis '''
    
    df1 = df.groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('Count').reset_index().sort_values(by='Count', ascending=False).head(10) 
    df2= df[df['SPAM_IND_RF']=='1'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('TRUE_SPAM_RF').reset_index()
    df3= df[df['SPAM_IND_RF']=='0'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('FALSE_SPAM_RF').reset_index()
    df4= df[df['SPAM_IND_KN']=='1'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('TRUE_SPAM_KN').reset_index()  
    df5= df[df['SPAM_IND_KN']=='0'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('FALSE_SPAM_KN').reset_index()  
    df7 = pd.merge(df1, df2, on='videoID', how='inner')
    df7 = pd.merge(df7, df3, on='videoID', how='inner')
    df7 = pd.merge(df7, df4, on='videoID', how='inner')
    df7 = pd.merge(df7, df5, on='videoID', how='inner')
    df7 = df7.set_index('videoID')
#    print(df7)
    df7.plot(kind='bar',rot=45,width=.8,figsize=(12,8))
    #plt.title('Spam Analysis - Top 10 Video')
    plt.xlabel('Video ID')
    plt.ylabel('Comment Count')
    plt.savefig('Spam Analysis - Top 10 Video.png')
 
    ''' venn deigram for true values '''
    
    fig6 = plt.figure(figsize=(12,8))
    df3 = df
    df3['KN'] =  np.where((df3['SPAM_IND_KN'] == '1') & (df3['SPAM_IND_KN'] == df3['SPAM_IND_RF']), 'True'+'-'+df3['CreateTimeStamp'], 'KN'+'-' + df3['CreateTimeStamp'])
    df3['RF'] =  np.where((df3['SPAM_IND_RF'] == '1') & (df3['SPAM_IND_RF'] == df3['SPAM_IND_KN']), 'True'+'-'+df3['CreateTimeStamp'], 'RF'+'-' + df3['CreateTimeStamp'])
    my_list = df3["KN"].tolist()
#    print(my_list)
    my_list2 = df3["RF"].tolist()
    venn2([set(my_list), set(my_list2)], set_labels = ('KNeighbors Classifier', 'Random Forest Classifier'))
    #plt.title('KNeighbors and Random Forest True Spam')
    fig6.savefig('Classifier True Spam Analysis.png')
    plt.gca().set_axis_on()
    plt.show()
    
def main():
    
    ''' Call functions from main function '''
    Spam_data()
    SENTIMENT()
    
         
   

    

    
main()