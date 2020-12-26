# Quantifying-public-opinion-on-certain-company
This is a social-network-mining project to quantify public opinion on certain company.
The whole idea of this project is based on the class CIS600 of Syracuse University.

## Requirements
### For this you will need:
* twitter
* time
* pandas 
* wordcloud
* nltk
* matplotlib
* re

These can be installed via:
pip install twitter
pip install times
pip install pandas
pip install wordcloud
pip install nltk
pip install matplotlib
pip install re

### Setup:
You must first set up a Twitter APP
Input this data into the config file with your keys.

For using the preprocessing module, please copy the QPO_preprocessing.py file to the path where you run the training program and 
import QPO_preprocessing

To apply the preprocessing, you need to create a preprocessing model first. For example:
model = pp_model(¡®Dell.csv¡¯)
The only parameter is the file path which you want to train.

After creation, you can apply the basic process ¡®model.processing()¡¯, the sampling based on user ¡®model.userBasedSample(df, 1)¡¯ and the sampling based on date ¡®model.dateBasedSample(df)¡¯ Or, you can just use ¡®model.full_processing()¡¯ to get all the preprocessing effects.


For emotion recognition:
h5py==2.9.0
Keras==1.1.0
numpy==1.16.0
pandas==0.24.1
python-dateutil==2.8.0
pytz==2018.9
PyYAML==5.1
scipy==1.2.1
six==1.12.0
Theano==1.0.4

For another method please download the newest textblob. 
Use any python IDE and modify the path for tweets input in file SA.py and demo.py

