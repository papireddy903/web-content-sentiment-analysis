# %%
import numpy as np
import pandas as pd
import requests 
from bs4 import BeautifulSoup
from textblob import TextBlob
import pyphen
import spacy
nlp = spacy.load('en_core_web_sm')
dic = pyphen.Pyphen(lang='en')

# %%
data = pd.read_excel("D:/Blackcoffer/Input.xlsx")
excel_df = pd.read_excel("D:/Blackcoffer/Output Data Structure.xlsx")

# %%
data.head()
excel_df.head()

# %%
for url in data['URL']:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.h1
    body = soup.body
    extracted_text = ''
    if body:
        paragraphs = body.find_all('p')
        filtered_paragraphs = [p for p in paragraphs if "entry-title" not in p.get("class", [])]
        for paragraph in filtered_paragraphs:
            # print(paragraph)
            if 'entry-title td-module-title' not in paragraph.get('class', ''):
                extracted_text += " " + paragraph.get_text()
        print(extracted_text)
        doc = nlp(extracted_text)
        positive_score = 0
        negative_score = 0
        polarity_score = 0
        subjectivity_score = 0
        avg_sentence_length = 0
        percentage_complex_words = 0
        fog_index = 0
        avg_words_per_sentence = 0
        complex_word_count = 0
        word_count = 0
        syllable_per_word = 0
        personal_pronouns = 0
        avg_word_length = 0

        blob = TextBlob(extracted_text)

        polarity_score = blob.sentiment.polarity
        subjectivity_score = blob.sentiment.subjectivity

        if polarity_score>0:
            positive_score = polarity_score 
            negative_score = 0 
        elif polarity_score<0:
            positive_score = 0
            negative_score = -polarity_score 
        print("polarity_score : ",polarity_score)
        print("subjectivity_score : ",subjectivity_score)
        print("positive_score : ",positive_score)
        print("negative_score : ",-negative_score)
        sentences = []
        for sentence in doc.sents:
            sentences.append(sentence.text)
        # print(sentences)
        
        total_words = sum(len(sentence.split()) for sentence in sentences)
        print("avg_sentence_length : ",total_words//len(sentences))
        
        tokens = [token for token in doc if not token.is_space]
        total_word_length = 0
        for token in tokens:
            total_word_length += len(token.text)
            if token.pos_=='PRON' and token.dep_ =="nsubj":
                personal_pronouns +=1 
            syllables = dic.inserted(token.text).count('-') + 1
            if syllables > 2:
                complex_word_count += 1
            syllable_per_word += syllables
        
        percentage_complex_words = (complex_word_count / total_words)*100 if total_words>0 else 0 

        fog_index = 0.4 * (percentage_complex_words + avg_sentence_length)

        print("percentage_complex_words : ",percentage_complex_words)
        print("fog_index : ",fog_index)

        avg_words_per_sentence = total_words // len(sentences)

        print("avg_words_per_sentence : ",avg_words_per_sentence)
        print("complex_word_count : ",complex_word_count)
        print("word_count : ",total_words)
        print("syllable_per_word : ",syllable_per_word/total_words)
        print("personal_pronouns : ",personal_pronouns)
        print("avg_word_length : ",total_word_length/total_words)


    row_index = excel_df[excel_df['URL'] == url].index[0]
    
    excel_df.loc[row_index, 'POSITIVE SCORE'] = positive_score
    excel_df.loc[row_index, 'NEGATIVE SCORE'] = negative_score
    excel_df.loc[row_index, 'POLARITY SCORE'] = polarity_score
    excel_df.loc[row_index, 'SUBJECTIVITY SCORE'] = subjectivity_score
    excel_df.loc[row_index, 'AVG SENTENCE LENGTH'] = total_words//len(sentences)
    excel_df.loc[row_index, 'PERCENTAGE OF COMPLEX WORDS'] = percentage_complex_words
    excel_df.loc[row_index, 'FOG INDEX'] = fog_index
    excel_df.loc[row_index, 'AVG NUMBER OF WORDS PER SENTENCE'] = avg_words_per_sentence
    excel_df.loc[row_index, 'COMPLEX WORD COUNT'] = complex_word_count
    excel_df.loc[row_index, 'WORD COUNT'] = total_words
    excel_df.loc[row_index, 'SYLLABLE PER WORD'] = syllable_per_word/total_words
    excel_df.loc[row_index, 'PERSONAL PRONOUNS'] = personal_pronouns
    excel_df.loc[row_index, 'AVG WORD LENGTH'] = total_word_length/total_words
    excel_df.to_excel('Output Data Structure.xlsx', index=False)

# %%
excel_df.head()


