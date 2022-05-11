from fastapi import FastAPI
import joblib

# Analisis de datos
import pandas as pd
import numpy as np

# Procesamiento de texto
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Paquetes de Machine Learning
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# Guardar modelo
import joblib

app = FastAPI()

IE = joblib.load("D:/TODO/FIB/TFG/PersonalityAnalysisWithML/api/IE.joblib")
NS = joblib.load("D:/TODO/FIB/TFG/PersonalityAnalysisWithML/api/NS.joblib")
FT = joblib.load("D:/TODO/FIB/TFG/PersonalityAnalysisWithML/api/FT.joblib")
JP = joblib.load("D:/TODO/FIB/TFG/PersonalityAnalysisWithML/api/JP.joblib")

list_personality = []
list_posts = []
modelnames= [IE,NS,FT,JP]
personality_type = [ "IE: Introversion (I) / Extroversion (E)", "NS: Intuition (N) / Sensing (S)", 
                "FT: Feeling (F) / Thinking (T)", "JP: Judging (J) / Perceiving (P)"  ]
b_Pers = {'I':0, 'E':1, 'N':0, 'S':1, 'F':0, 'T':1, 'J':0, 'P':1}
b_Pers_list = [{0:'I', 1:'E'}, {0:'N', 1:'S'}, {0:'F', 1:'T'}, {0:'J', 1:'P'}]

def translate_back(personality):
    # transformar el vector binario en personalidad mbti
    s = ""
    for i, l in enumerate(personality):
        s += b_Pers_list[i][l]
    return s

def translate_personality(personality):
    # transformar mbti a un vector binario
    return [b_Pers[l] for l in personality]

def pre_process_text1():
    list_posts = []
    data = pd.read_csv('../../data/processed/dataP.csv')

    for row in data.iterrows():
        posts = row[1].posts
        list_posts.append(posts)

    # Resultado
    list_posts = np.array(list_posts)
    return list_posts

def treat_post(msg:str):
    list_posts= pre_process_text1()

    # Vectorizar los posts de la base de datos a una matriz de conteo de tokens para el modelo
    cntizer = CountVectorizer(analyzer="word", 
                                max_features=1000,  
                                max_df=0.7,
                                min_df=0.1) 
                                
    # la característica debe ser de n-grama de la palabra 
    # Aprender el diccionario de vocabulario y devolver la matriz término-documento
    X_cnt = cntizer.fit_transform(list_posts)

    # Transformar la matriz de recuento en una representacion normalizada tf o tf-idf
    tfizer = TfidfTransformer()

    # Aprender el vector idf (fit) y transformar una matriz de recuento a una representacion tf-idf
    X_tfidf =  tfizer.fit_transform(X_cnt).toarray()

    #contando las 10 primeras palabras
    reverse_dic = {}
    for key in cntizer.vocabulary_:
        reverse_dic[cntizer.vocabulary_[key]] = key
    top_10 = np.asarray(np.argsort(np.sum(X_cnt, axis=0))[0,-10:][0, ::-1]).flatten()
    [reverse_dic[v] for v in top_10]

    def pre_process_text(data, remove_stop_words=True, remove_mbti_profiles=True):
        lemmatiser = WordNetLemmatizer()

        # Identificar stopwords
        useless_words = stopwords.words("english")

        # Eliminarlas de los posts
        unique_type_list = ['INFJ', 'ENTP', 'INTP', 'INTJ', 'ENTJ', 'ENFJ', 'INFP', 'ENFP',
            'ISFP', 'ISTP', 'ISFJ', 'ISTJ', 'ESTP', 'ESFP', 'ESTJ', 'ESFJ']
        unique_type_list = [x.lower() for x in unique_type_list]
        list_personality = []
        list_posts = []
        for row in data.iterrows():
            posts = row[1].posts

            # Elimina URL 
            temp = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ', posts)

            # Elimina caracteres que no son palabras
            temp = re.sub("[^a-zA-Z]", " ", temp)

            # Quita espacios innecesarios
            temp = re.sub(' +', ' ', temp).lower()

            # Eliminar las palabras que se repiten con varias letras
            temp = re.sub(r'([a-z])\1{2,}[\s|\w]*', '', temp)

            # Elimina las stopwords
            if remove_stop_words:
                temp = " ".join([lemmatiser.lemmatize(w) for w in temp.split(' ') if w not in useless_words])
            else:
                temp = " ".join([lemmatiser.lemmatize(w) for w in temp.split(' ')])
                
            # Eliminar las palabras de la personalidad MBTI de los mensajes
            if remove_mbti_profiles:
                for t in unique_type_list:
                    temp = temp.replace(t,"")

            # Datos ya limpios
            list_posts.append(temp)

        # Resultado
        list_posts = np.array(list_posts)
        return list_posts

    my_posts = msg
    # The type is just a dummy so that the data prep function can be reused
    mydata = pd.DataFrame(data={'type': ['INFJ'], 'posts': [my_posts]})
    my_posts= pre_process_text(mydata, remove_stop_words=True, remove_mbti_profiles=True)
    my_X_cnt = cntizer.transform(my_posts)
    my_X_tfidf =  tfizer.transform(my_X_cnt).toarray()
    return my_X_tfidf

@app.get("/")
def index():
    return{'Hello'}

@app.post("/predict")
def predict(msg:str):
    prediction= []
    final_msg= treat_post(msg)
    for l in range(len(personality_type)):
        # hacer predicciones para los datos
        y_pred = modelnames[l].predict(final_msg)
        prediction.append(y_pred[0])

    return{
        'prediction': translate_back(prediction)
    }
