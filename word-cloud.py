from wordcloud import WordCloud
import pandas as pd
import nltk
import re
import matplotlib.pyplot as plt

def alpha_filter(w):
  # pattern to match a word of non-alphabetical characters
    pattern = re.compile('^[^a-z]+$')
    if (pattern.match(w)):
        return True
    else:
        return False

def pre_process(r):                               #processing the comments, turn them into the format that can be analyzed
  r = nltk.word_tokenize(r)                           #tokenization
  r = [w.lower() for w in r]                          #turn them into lower case
  r = [word for word in r if not any(c.isdigit() for c in word)]            #delete all the numbers
  stop = nltk.corpus.stopwords.words('english')                     #delete all the stop words
  r = [w for w in r if not alpha_filter(w)]
  r = [x for x in r if x not in stop]
  r = [y for y in r if len(y) > 2]
  wnl = nltk.WordNetLemmatizer()                          #lemmatizing
  r= [wnl.lemmatize(t) for t in r]
  text = " ".join(r)
  return text


def remove_at(text, lang):
    result = []
    for i in range(len(text)):
        if lang[i] != 'en':
            continue
        tweet = text[i]
        tweet = re.sub(r'@\w*', '', tweet)
        tweet = re.sub(r'^RT[\s]+', '', tweet)
        tweet = re.sub(r'https?://\S+[\r\n\s]*', '', tweet)
        tweet = re.sub(r'#', '', tweet)
        tweet = re.sub(r'&amp;', '', tweet)
        result.append(tweet)
        word = text[i].split(' ')
        print('1')
        for j in word:
            if('@' in j) or ('#' in j) or ("http" in j) or ('&' in j):
                word.remove(j)
        a = " ".join(word)
        result.append(a)
    return result

f0 = pd.read_csv("Tesla.csv")
f0_text = f0['text']
f0_lang = f0['lang']

f = open("text.txt",'w',encoding = 'utf-8')

text = f0_text.tolist()
lang = f0_lang.tolist()
train_text = remove_at(text, lang)

for i in range(len(train_text)):
    train_text[i] = pre_process(train_text[i])

for i in train_text:
    f.write(i)

f.close()

f2 = open("text.txt",'r',encoding='utf-8').read()

wordcloud = WordCloud(
        background_color="white", #set background
        width=1500,              #Set width
        height=960,              #set Heigh
        margin=10               #set margin
        ).generate(f2)

plt.imshow(wordcloud)
# Eliminate axis
plt.axis("off")
# show image
plt.show()
# save image
wordcloud.to_file('Tesla.png')
plt.close()








