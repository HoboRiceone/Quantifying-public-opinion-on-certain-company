import pandas as pd
import QPO_preprocessing
from emotion_predictor import EmotionPredictor
import csv
import matplotlib.pyplot as plt
def plotPieChart( Anger, Fear, Sadness, Surprise, Disgust, Joy,Anticipation,Trust,searchTerm,
                 noOfSearchTerms):
    labels = ['Anger [' + str(Anger) + '%]', 'Fear [' + str(Fear) + '%]',
              'Sadness [' + str(Sadness) + '%]', 'Surprise [' + str(Surprise) + '%]',
              'Disgust [' + str(Disgust) + '%]', 'Joy [' + str(Joy) + '%]',
              'Anticipation [' + str(Anticipation) + '%]', 'Trust [' + str(Trust) + '%]',]
    sizes = [Anger, Fear, Sadness, Surprise, Disgust, Joy, Anticipation,Trust]
    colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon','turquoise','cornflowerblue']
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def percentage(part, whole):
    temp = 100 * float(part) / float(whole)
    return format(temp, '.2f')

# Pandas presentation options

# pd.options.display.max_columns = 7      # maximal number of columns


# Predictor for Ekman's emotions in multiclass setting.
#m = QPO_preprocessing.pp_model(r'D:\untitled_folder\Amazon1.csv')
#r = m.processing()
r = pd.read_csv(r'D:\untitled_folder\Amazon1.csv')
tweets = []
count = 0
for index, row in r.iterrows():
    tweets.append(row['text'])
    count = count + 1
    if count == 1500:
        break
model = EmotionPredictor(classification='plutchik', setting='mc', use_unison_model=True)



predictions = model.predict_classes(tweets)

Anger = 0
Fear = 0
Sadness = 0
Surprise = 0
Disgust = 0
Joy = 0
Anticipation = 0
Trust = 0

Text_list = []
Emotion_list = []


for index, prediction in predictions.iterrows():
    Text_list.append(prediction['Tweet'])
    Emotion_list.append(prediction['Emotion'])
    if prediction['Emotion'] == "Anger":
        Anger = Anger + 1
    if prediction['Emotion'] == "Fear":
        Fear = Fear + 1
    if prediction['Emotion'] == "Sadness":
        Sadness = Sadness + 1
    if prediction['Emotion'] == "Surprise":
        Surprise = Surprise + 1
    if prediction['Emotion'] == "Disgust":
        Disgust = Disgust + 1
    if prediction['Emotion'] == "Joy":
        Joy = Joy + 1
    if prediction['Emotion'] == "Anticipation":
        Anticipation = Anticipation + 1
    if prediction['Emotion'] == "Trust":
        Trust = Trust + 1

Anger = percentage(Anger, count)
Fear = percentage(Fear, count)
Sadness = percentage(Sadness, count)
Surprise = percentage(Surprise, count)
Disgust = percentage(Disgust, count)
Joy = percentage(Joy, count)
Anticipation = percentage(Anticipation, count)
Trust = percentage(Trust, count)

print("Detailed Report: ")
print(str(Anger) + "% people thought it was Anger")
print(str(Fear) + "% people thought it was Fear")
print(str(Sadness) + "% people thought it was Sadness")
print(str(Surprise) + "% people thought it was Surprise")
print(str(Disgust) + "% people thought it was Disgust")
print(str(Joy) + "% people thought it was Joy")
print(str(Anticipation) + "% people thought it was Anticipation")
print(str(Trust) + "% people thought it was Trust")

plotPieChart(Anger, Fear, Sadness, Surprise, Disgust, Joy, Anticipation, Trust, "Amazon", count)

with open('my_result.csv', 'w') as file_object:
    fieldnames = ['text', 'emotion']
    writer = csv.DictWriter(file_object, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(Text_list)):
        writer.writerow({'title': Text_list[i],
                         'text': Emotion_list[i]})

print(predictions, '\n')



