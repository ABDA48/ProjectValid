from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import uvicorn
import numpy as np
from tensorflow.keras.utils import load_img, img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.models import load_model
from scipy import spatial
app = FastAPI()

bagFeature=pickle.load(open("models/bagFeature.pkl","rb"))
symptoms_features=pickle.load(open("models/symptoms_features.pkl","rb"))
disease_symptoms=pickle.load(open("models/diseas_features.pkl","rb"))
Heartmodel=pickle.load(open('models/heart_disease_model.pck','rb'))
Pneumoniamodel=load_model('models/Pneumoniadetection.h5')
Diabetemodel = pickle.load(open('models/diabetsModel.pck', 'rb'))
class DiabetesDiseases(BaseModel):
    pregnancies:float
    glucose:float
    bloodPressure:float
    skinThickness:float
    insulin:float
    bmI:float
    diabetesPedigreeFunction:float
    age:float

class HeartDiseases(BaseModel):
    age:float
    sex:float
    cp:float
    trestbps:float
    chol:float
    fbs:float
    restecg:float
    thalach:float
    exang:float
    oldpeak:float
    slope:float
    ca:float
    thal:float
class PneumoniaDiseases(BaseModel):
    path:str
class GeneralDiseases(BaseModel):
    symptoms:str

@app.post('/predict/diabetes')
async def predict_species(values: DiabetesDiseases):
        data=values.dict()
       
        input_data = (
            data['pregnancies'], data['glucose'], data['bloodPressure'], data['skinThickness'],
            data['insulin'], data['bmI'], data['diabetesPedigreeFunction'],data['age']
        )
        input_data_as_numpy_array = np.asarray(input_data)

        # reshape the array as we are predicting for one instance
        input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

        prediction = Diabetemodel.predict(input_data_reshaped)
        print(prediction)

        if (prediction[0] == 0):
            return 'Peson not Diabetic'
        else:
            return 'Peson  Diabetic'

@app.post('/predict/heart')
async def predict_species(values: HeartDiseases):
    data=values.dict()
    input_data = (
            data['age'], data['sex'], data['cp'], data['trestbps'],
            data['chol'], data['fbs'], data['restecg'],data['thalach'],
             data['exang'],data['oldpeak'],data['slope'],data['ca'],
             data['thal']
        )
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
    prediction = Heartmodel.predict(input_data_reshaped)
    print(prediction)
        
    if (prediction[0]== 0):
        return 'The Person does not have a Heart Disease'
    else:
        return 'The Person has Heart Disease'

@app.post('/predict/pneumonia')
async def predict_species(imgPath: PneumoniaDiseases):
    
    data=imgPath.dict()
    #C:/Users/jaola/Documents/GitHub/Project CP3/normalPneu.jpeg
    img=load_img(data['path'],target_size=(224,224))
    x=img_to_array(img)
    x=np.expand_dims(x, axis=0)
    img_data=preprocess_input(x)
    
    classes=Pneumoniamodel.predict(img_data)
    result=int(classes[0][0])
    if result==0:
       return "Person is Affected By PNEUMONIA"
    else:
       return "Result is Normal"
@app.post('/predict/diseases')
async def predict_species(symptoms: GeneralDiseases):
    data=symptoms.dict()
    bag=createbag(data['symptoms'])
    diagnosis_percent={}
    for i in range(len(bagFeature)):
        result = 1 - spatial.distance.cosine(bagFeature[i][1], bag) 
        diagnosis_percent[bagFeature[i][0]]=result*100
    diagnosis_percent=sorted(diagnosis_percent.items(),key=lambda x:x[1],reverse=True)
    n=4
    disease={}
    diseaselist=[]
    percentage=[]
    for i in range(n):
        diseaselist.append(diagnosis_percent[i][0])
        percentage.append(diagnosis_percent[i][1])
    disease={
      'diseaselist':diseaselist,
      'percentage':percentage,
      'statut':'accepted'
    }

    if percentage[0]<80:
        print(diseaselist,percentage)
        sympto=reduceDiseasePercentage(data['symptoms'],diseaselist,percentage)
        quest=askmoreSympto(list(sympto))
        value={
            "question":quest,
            "curentSymptom":data['symptoms'],
            'diseaselist':diseaselist,
            'percentage':percentage,
            'statut':'refused'
        }
        return value
    disease=dict(disease)
    return  disease
def reduceDiseasePercentage(symp,diseaselist,percentage):
    symptom=symp.split(',')
    sympts=[]
    for d in diseaselist:
        diseaseSympt=disease_symptoms[d];
        for s in symptom:
            if s in diseaseSympt:
                diseaseSympt.remove(s)
        sympts.extend(diseaseSympt)
    print(set(sympts))
    return set(sympts)
def askmoreSympto(sympto):
    d=[]
    m=[]
    n=5
    for i in range(len(sympto)):
        d.append(sympto[i])
        if len(d)==n:
            m.append(d)
            d=[]
    return m

def createbag(symptoms):
      symptoms=symptoms.split(',')
      bag=[]
      for val in symptoms_features:
          bag.append(1) if val in symptoms else bag.append(0)
      return bag


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)


