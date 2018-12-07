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



def SENTIMENT(filepath ):
    
    path = filepath +'\\video_comments_analysis_sentiments.csv'
    ''' Read the file data '''
    df = pd.read_csv(path, sep='\t' ,names = ["Comment", "CreateTimeStamp", "Type", "videoID","videoTitle", "FNAME", "SENTIMENT_RF", "SENTIMENT_KN"])
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
       
       
    ''' Random Forest and KNeighbors Sentiment data analysis'''
     

    fig3 = plt.figure(figsize=(12,8))
    df1 = df.groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('Count').reset_index().sort_values(by='Count', ascending=False).head(15) 
    df2= df[df['SENTIMENT_RF']=='1'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('POSITIVE_SENT_RF').reset_index()
    df3= df[df['SENTIMENT_KN']=='1'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('POSITIVE_SENT_KN').reset_index()  
    df4= df[df['SENTIMENT_RF']=='0'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('NEGATIVE_SENT_RF').reset_index()
    df5= df[df['SENTIMENT_KN']=='0'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('NEGATIVE_SENT_KN').reset_index()  
    df7 = pd.merge(df1[['videoID']], df2, on='videoID', how='inner')
    df7 = pd.merge(df7, df3, on='videoID', how='inner')
    df7 = pd.merge(df7, df4, on='videoID', how='inner')
    df7 = pd.merge(df7, df5, on='videoID', how='inner')
    df7 = df7.set_index('videoID')
#    print(df7)
    df7.plot(kind='bar',rot=45,width=.8,figsize=(12,8), color= ('b','g', 'r', 'k'))
    plt.savefig('Sentiemnt_Analysis.png')
    
    

    ''' venn deigram for Sentiment values '''
    
    fig4 = plt.figure(figsize=(12,8))
    df3 = df
    df3['KN'] =  np.where( (df3['SENTIMENT_KN'] == df3['SENTIMENT_RF']), 'True'+'-'+df3['CreateTimeStamp'], 'KN'+'-' + df3['CreateTimeStamp'])
    df4 = df
    df4['RF'] =  np.where((df4['SENTIMENT_RF'] == df4['SENTIMENT_KN']), 'True'+'-'+df4['CreateTimeStamp'], 'RF'+'-' + df4['CreateTimeStamp'])
    my_list = df3["KN"].tolist()
#    print(my_list)
    my_list2 = df4["RF"].tolist()
    venn2([set(my_list), set(my_list2)], set_labels = ('KNeighbors Classifier', 'Random Forest Classifier'))
    #plt.title('KNeighbors and Random Forest True Sentiments')
    fig4.savefig('Venn_SentimentAnalysis.png')
    plt.gca().set_axis_on()
    plt.show()
    
def Spam_data(filepath):  
    
    path = filepath +'\\video_comments_analysis_spam.csv'
    ''' Read the file data '''
    df = pd.read_csv(path, sep='\t' ,names = ["Comment", "CreateTimeStamp", "Type", "videoID","videoTitle", "FNAME", "SPAM_IND_RF","SPAM_IND_KN"])
    df = df.iloc[1:]
    
    '''SPAM data analysis '''
    
    df1 = df.groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('Count').reset_index().sort_values(by='Count', ascending=False).head(15) 
    df2= df[df['SPAM_IND_RF']=='1'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('SPAM_RF').reset_index()
    df3= df[df['SPAM_IND_KN']=='1'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('SPAM_KN').reset_index()  
    df4= df[df['SPAM_IND_RF']=='0'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('NON_SPAM_RF').reset_index()
    df5= df[df['SPAM_IND_KN']=='0'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('Non_SPAM_KN').reset_index()  
    df7 = pd.merge(df1[['videoID']], df2, on='videoID', how='inner')
    df7 = pd.merge(df7, df3, on='videoID', how='inner')
    df7 = pd.merge(df7, df4, on='videoID', how='inner')
    df7 = pd.merge(df7, df5, on='videoID', how='inner')
    df7 = df7.set_index('videoID')
#    print(df7)
    df7.plot(kind='bar',rot=45,width=.8,figsize=(12,8))
    #plt.title('Spam Analysis - Top 10 Video')
    plt.xlabel('Video ID')
    plt.ylabel('Comment Count')
    plt.savefig('Spam_Analysis.png')
 
    ''' venn deigram for true values '''

    
    fig5 = plt.figure(figsize=(8,8))
    df10 = df
    
    conditions = [
    (df10['SPAM_IND_KN'] == df10['SPAM_IND_RF']),
    (df10['SPAM_IND_KN'] == '1') & (df10['SPAM_IND_RF'] == '0'),
    (df10['SPAM_IND_KN'] == '0') & (df10['SPAM_IND_RF'] == '1')]
    choices = ['Random Forest & KNeighbors', 'KNeighbors', 'Random Forest']
    df10['SPAM'] = np.select(conditions, choices, default='NA')
 #   df5 = df5.groupby(['SPAM']).CreateTimeStamp.agg('count').to_frame('Count').reset_index()
       
  #  print(df10)
    df10.SPAM.value_counts().plot(kind='pie',  autopct='%.2f')
    fig5.savefig('Pie_SPAM.png')

   
def SENTIMENT_SPAM(filepath):
    path1 =filepath +'\\video_comments_analysis_sentiments.csv'
    fig7 = plt.figure(figsize=(12,8))
    df = pd.read_csv(path1, sep='\t' ,names = ["Comment", "CreateTimeStamp", "Type", "videoID","videoTitle", "FNAME", "SENTIMENT_RF", "SENTIMENT_KN"])
    df = df.iloc[1:]
    
    path2 = filepath +'\\video_comments_analysis_spam.csv'
    df3 = pd.read_csv(path2, sep='\t' ,names = ["Comment", "CreateTimeStamp", "Type", "videoID","videoTitle", "FNAME", "SPAM_IND_RF","SPAM_IND_KN"])
    df3 = df3.iloc[1:]
    
    df1 = df.groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('Count').reset_index().sort_values(by='Count', ascending=False).head(15) 
    df2 = df[df['SENTIMENT_KN']=='1'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('SENTIMENT').reset_index()  
    df3 = df3[df3['SPAM_IND_KN']=='1'].groupby(['videoID']).CreateTimeStamp.agg('count').to_frame('SPAM').reset_index()  
    df4 = pd.merge(df1[['videoID']], df2, on='videoID', how='inner') 
    df4 = pd.merge(df4, df3, on='videoID', how='inner')  
    print(df4)
    df4 = df4.set_index('videoID')
    df4.plot(kind='bar',rot=45,width=.8,figsize=(12,8))
    plt.savefig('Sentiment_SPAM_Analysis.png')
    
# =============================================================================
def main():
    
    ''' provide file path'''
    print("Plese provide the output file path (like c:\\Users \\USER\\) :")
    filepath = input()
    ''' Call functions from main function '''
    SENTIMENT(filepath )
    Spam_data(filepath)
    SENTIMENT_SPAM(filepath)
    
    

    
         
   

    

    
main()