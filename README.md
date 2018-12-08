# YouTube Video Comments Analysis

## Overview
Youtube Video Comments Sentiment Analysis and Spam Detection using Word2Vec model.

## Video search strings

### Video Domains
#### 1) Technical : Samsung VR HeadSet, Oculus, mac vs windows, iphone xs vs note 9, bitcoin vs ethereum

#### 2) Music : Taylor swift, Eminem - Not Afraid, coldpay, Maroon 5, Ed  Sheeran

#### 3) Sports : Golden State Warriors, nfl highlights, roger federer vs rafael nadal, formula 1 2018, Super Bowl LI

#### TV series : House of cards, game of thrones season 8, The Tonight show, The Big Bang Theory



## PROJECT EXECUTION INSTRUCTIONS

### Here are the instruction to run the code.

#### 1. clone git repository
git clone https://github.com/akechilte/comments_analysis
cd comments_analysis

#### 2. Download Youtube comments

python GetYoutubeComments.py <Credential> <SearchStringOutPutfileName> <Maxresults>

It takes four arguments.
a) Credential- YouTube developer account key
b) Search string- The videos that we are going to use.
c) OutPut fileName- The file where we will store ourcomments and replies.
d) Max results- The number of videos.

#### 3. Build Word2Vec Model
cd src
jupyter notebook
Run Doc2Vec-model.ipynb notebook

#### 4. Train Sentiment Analysis Classifier
jupyter notebook
Run SentimentAnalysis-model.ipynb


#### 5. Train Spam Detection Classifier
jupyter notebook
Run SpamDetection-model.ipynb


#### 6. Make Prediction
jupyter notebook
Run SentimentAnalysis-pred.ipynb
Run SpamDetection-pred.ipynb

#### 7. Generate  Visualization
python exploratoryanalysis.py





