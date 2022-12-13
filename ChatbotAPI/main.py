from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import tensorflow
from tensorflow import keras
from keras import models 
import json
import numpy as np
import pickle
import nltk
from nltk.corpus import stopwords
import random
import requests
import spacy
URL='http://127.0.0.1:8000/'

app = FastAPI()
listgreet=['greeting','goodbye','thanks','options']
class ChatBot(BaseModel):
    question:str
    PROCESS:int
    DISEASE:str
    MEDICINE:str




model=models.load_model('ChatBotModel.h5')
words=pickle.load(open('word.pkl','rb'))
intents = json.loads(open('intents.json').read())
processdata={}
classes = pickle.load(open('classes.pkl','rb'))
lemmatizer=nltk.WordNetLemmatizer()
nlp= spacy.load(r"./output/model-last") 

#load the best model


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return np.array(bag)

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    print(res)
    ERROR_THRESHOLD = 0.1
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result
def EntityDiseasePrediction(question):
    doc=nlp(question)
    response={}
    for d in doc.ents:
        if d.label_=='DISEASE':
            response[d.label_]=d.text
            return response['DISEASE']
        else:
            return ""
def IntentPrediction(question):
    ints =  predict_class(question,model)
    print(ints)
    res,tag = getResponse(ints, intents)
    print(res,tag)
    return res,tag

def IntentConfirmation(res1,tag):
    intent=""
    intent1=""
    for k,v in res1.items():
        if k != 'DISEASE':
            intent1=k
        if intent1=="" and tag!="":
            intent=tag
        if tag=="" and intent1!="":
            intent=intent1
        if tag!="" and intent1!="":
            intent=tag
        if tag=="" and intent1=="":
            question=input("do you whant to know the cause ,prevention,treatment or medicine fro this disease")
            intent=tag
        disease=res1['DISEASE']
        print(disease,intent)
        return [disease,intent],1
 

@app.post('/chatbot/first')
async def entitydiseaseprediction(answer:ChatBot):
    data=answer.dict()
    print(data)
    question=data['question']
    PROCESS=data['PROCESS']
    DISEASE=data['DISEASE']
    MEDICINE=data['MEDICINE']
 

    if PROCESS==1:
        DISEASE=question
        PROCESS=2
        return "ASK",PROCESS,question,MEDICINE
        
    if PROCESS==0:
        ints =  predict_class(question,model)
        print(ints)
        res = getResponse(ints, intents)
        PROCESS=0
        if ints[0]['intent']=='notknowing':
            PROCESS=1
            return 'notknowing',PROCESS,DISEASE,MEDICINE
        if ints[0]['intent'] in ['cause','prevention','medicine','treatment']:
            if DISEASE=='':
                return forCausePrevMedTreat(ints=ints,question=question,res=res,medicine=MEDICINE,dis=DISEASE)
            if DISEASE!='':
                if ints[0]['intent']=='cause':
                    PROCESS=2
                if ints[0]['intent']=='prevention':
                    PROCESS=5
                if ints[0]['intent']=='medicine':
                    PROCESS=4
                if ints[0]['intent']=='treatment':
                    PROCESS=3
            return res,PROCESS,DISEASE,MEDICINE
        return res,PROCESS,DISEASE,MEDICINE
        
    if PROCESS==2 or PROCESS==3 or PROCESS==4 or PROCESS==5 or PROCESS==6 or PROCESS==7 :
        ints =  predict_class(question,model)
        if ints[0]['intent']!='accept':
            res = getResponse(ints, intents)
            if ints[0]['intent'] in ['cause','prevention','medicine','treatment']:
                return forCausePrevMedTreat(ints=ints,question=question,res=res,medicine=MEDICINE,dis=DISEASE)
            return res,0,DISEASE,MEDICINE
        if PROCESS==2 and ints[0]['intent']=='accept':
                PROCESS=3
                ints[0]['intent']=""
                return "treatment",PROCESS,DISEASE,MEDICINE
        if PROCESS==3 and ints[0]['intent']=='accept':
                ints[0]['intent']=""
                PROCESS=4
                return "medicine",PROCESS,DISEASE,MEDICINE
       
        if PROCESS==4 and ints[0]['intent']=='accept':
                ints[0]['intent']=""
                PROCESS=5
                return "prescription",PROCESS,DISEASE,MEDICINE
        if PROCESS==5 and ints[0]['intent']=='accept':
                ints[0]['intent']=""
                PROCESS=6
                return "effects",PROCESS,DISEASE,MEDICINE
        if PROCESS==6 and ints[0]['intent']=='accept':
                ints[0]['intent']=""
                PROCESS=7
                return "prevention",PROCESS,DISEASE,MEDICINE
        if PROCESS==7 and ints[0]['intent']=='accept':
                ints[0]['intent']=""
                PROCESS=0
                return "followup",PROCESS,DISEASE,MEDICINE


        
def forCausePrevMedTreat(ints,question,res,medicine,dis):
        disease=EntityDiseasePrediction(question)
        if disease!='':
            DISEASE=disease
            print('disease',disease)
        else:
            DISEASE=dis
            print('disease',dis)
        if ints[0]['intent']=='cause':
            PROCESS=2
            return 'cause',PROCESS,DISEASE,medicine
        if ints[0]['intent']=='prevention':
            PROCESS=5
            return 'prevention',PROCESS,DISEASE,medicine
        if ints[0]['intent']=='medicine':
            PROCESS=4
            return 'medicine',PROCESS,DISEASE,medicine
        if ints[0]['intent']=='treatment':
            PROCESS=3
            return 'treatment',PROCESS,DISEASE,medicine
        return res,PROCESS,DISEASE,medicine

 

def sendrequest(url,body,method):
    if method=='POST':
         response=requests.post(url,body)
         return response.json()
def cleansymptoms(symp):
    sym=symp.strip()
    symptoms=sym.replace(" ","_")
    body={
            "symptoms":symptoms
            }
    app_json = json.dumps(body)
    url='http://127.0.0.1:8001/predict/diseases'
    return url,app_json
if __name__=='__main__':
    uvicorn.run(app,host='0.0.0.0',port=8002)
