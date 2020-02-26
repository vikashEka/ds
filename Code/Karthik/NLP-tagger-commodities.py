#Importing all the libraries

import os  
import re
from nltk.tag import StanfordNERTagger      
import json
from flask import Flask,request 
import nltk
import pandas as pd
from flask_cors import CORS, cross_origin
import pathlib
import requests
import datefinder
from datetime import datetime
from dateparser.search import search_dates 

#Flask Setup
app = Flask(__name__)
CORS(app, support_credentials=True)
@app.route('/nlp/processSentence')  
@cross_origin(supports_credentials=True)

#Any changes you make in base or any where make sure the same changes are carried forward. 

#########################################################################
###############Stanford_base#############################################        
#########################################################################
#We are using the base library we have created/trained to get the output

def recognizer():
    headers_post = request.headers 
    appid = headers_post['appId']
    tenant_id = headers_post['X-TenantID']
    object_id = headers_post['X-Object']
    Authorization = headers_post['Authorization'] 
    
    URL = os.environ.get("properties_url_review")
    URL = str(URL)+"/property/platform_url"
    response1 = requests.get(URL,headers={"Content-Type":"application/json","X-TenantID" : tenant_id})
    ENV_URL=response1.json()
    ENV_URL=ENV_URL["propertyValue"]
    vf_url = str(ENV_URL) +"/cac-security/api/userinfo"
    response = requests.get(vf_url,headers={"Authorization":Authorization})
    #Validating authentication
    if response.status_code == 200:
        ROOT_PATH = os.environ.get("path_root_url")
        os.chdir(ROOT_PATH)
        df2 = str(tenant_id)+"/"+str(appid)+"/"+str(object_id)
        cwd = os.getcwd()
        cwd = pathlib.PureWindowsPath(cwd)
        cwd = cwd.as_posix()
        #Creating a new path if it doesnot exist
        if not os.path.exists(str(cwd) +"/" + str(df2)):
            os.makedirs(str(cwd) +"/" + str(df2))
        #stanford-new.jar is the file required which runs the model
        #corpus-tagging.ser.gz is the object function required
        exists = os.path.isfile(str(df2) + '/corpus-tagging.ser.gz')
        if exists:
            jar = 'stanford-ner.jar'
            model = str(df2) + "/corpus-tagging.ser.gz"
            sentence = request.args.get('sentence')
            if sentence !="":
                sentencex = "."#as we are deviding our model input with statements . is necessacry
                #Incase we have .. the we are replacing it with .
                sentence = sentence.replace('..','.')
                sentence = sentence+sentencex
                article = sentence[:]
                #The below function is to replace the date format in the input sentence
                #Here we are replacing the date format to a standardised format
                def find_match(sentence,df):
                    for i in range(df.shape[0]):
                        if sentence.find(df['rpl'][i]) !=-1:
                            sentence = sentence[:sentence.find(df['rpl'][i])] +  df['rpl1'][i] +  sentence[sentence.find(df['rpl'][i])+ len(df['rpl'][i]):]
                    return sentence
                
                #Few of the stop words we are taking care, we are removing them,Not necesaary although
                sentencek = sentence[:]
                stopwords=[' between ',' of ']
                for word in stopwords:
                    if word in sentencek:
                        sentencek=sentencek.replace(word," ")               
                #search_date is a function which finds the dates in a sentence.
                #Any format
                ls3 = search_dates(sentencek)
                if ls3 == None:
                    ls3 = []
                else:
                    ls3 = [t[::-1] for t in ls3]
                
                #the below lines of codes are to handle unreasonable dates is catches
                #Ex: of 20MT at times may be counted as date so we are converting them to find if thats exactlt date or not
                #If its not a date then it gives NaT and we remove them
                if ls3!=[]:
                    ls4 = pd.DataFrame(ls3)
                    ls4 = ls4.drop_duplicates()
                    ls4.columns = ["rpl1","rpl"]
                    ls4["rpl1"] = pd.to_datetime(ls4["rpl1"], errors='coerce')
                    ls4 = ls4.query('rpl1 != "NaT"')
                    ls4["rpl1"] = ls4["rpl1"].dt.strftime('%Y-%m-%d')
                    ls4 = ls4[pd.to_numeric(ls4['rpl'], errors='coerce').isna()]
                    ls4["rpl2"] = pd.to_datetime(ls4["rpl"], errors='coerce')
                    ls4 = ls4.query('rpl2 != "NaT"')
                    ls4 = ls4.drop(columns=['rpl2'])
                    ls4 = ls4.reset_index(drop = True)
                    ls4.index = ls4['rpl'].str.len()
                    ls4 = ls4.sort_index(ascending=True).reset_index(drop=True)
                    ls4["rpl1"] = ls4["rpl1"].map(str)+ ' '
#                    sentence = re.sub('\s+',' ', sentence)
                    sentence = find_match(sentencek,ls4)                    

                #Model inception
                #Model and Jar are already defined above
                sentence1 = sentence.lower()
                ner_tagger = StanfordNERTagger(model, jar, encoding='utf8')
                #we are tokenizing the words and we use it as a standard throughout instad of writing regex
                words = nltk.word_tokenize(sentence1)
                results = ner_tagger.tag(words)
                #Created a filter incase required after taggings are done in order to remove
                filter = ['T']
                ls2 = [(x,y) for (x,y) in results if y not in filter] 
                df = pd.DataFrame(ls2)  
                #As in some cases coffee is repeated multipple times we trained the model as product#$#quality
                #Below we are separating them
                new = df[1].str.rsplit("#$#",n=10,expand = True)
                lst_ip1 = nltk.word_tokenize(sentence)
                lst_ip3 = pd.DataFrame(lst_ip1)
                df[0]=lst_ip3[0]
                new["sentence"]=lst_ip3[0] 
                #After separation we are doing the word arrangements
                #Because we want coffee ABC as quality not ABC coffee
                df_new = pd.DataFrame()
                for label, content in new.items():
                    df_new1 = pd.DataFrame()
                    df_new1[0] = new["sentence"]
                    df_new1[1] = new[label]
                    df_new = df_new.append(df_new1, ignore_index=True)
                    df_new = df_new[df_new[0] != df_new[1]]
                    df_new = df_new.dropna()
                    df_new = df_new.drop_duplicates()
                    ls2 = list(df_new.itertuples(index=False, name=None))
                
                #here we are creating a JSON and sending it for the output
                d = {}
                for a, b in ls2:
                    d.setdefault(b, []).append(a)
                new_abc = [ [ ' '.join(d.pop(b)), b ] for a, b in ls2 if b in d ]
                sub_dict = json.dumps(new_abc)
                
                if new_abc!=[]:
                    new_abc = pd.DataFrame(new_abc)
                    new_abc.columns = ['sentence', 'output']
                    new_abc = new_abc[new_abc.output != 'T']
                    new_abc = new_abc.set_index('output')['sentence'].to_dict()
                    sub_dict = json.dumps(new_abc)
                    df = pd.DataFrame({'input':[sentence]})
                    df["output"] = [ls2]
                    #Creating an user entered file and saving it.Not required although
                    exists = os.path.isfile(str(df2) + "/user_entered.csv")
                    if exists:
                        df1=pd.read_csv(str(df2) + "/user_entered.csv")
                        df1 = df1.append(df) 
                        df1['New_ID'] = range(1, 1+len(df1))
                        df1.to_csv(str(df2) + "/user_entered.csv", sep=',',index=False)
            
                    else:
               
                        df.to_csv(str(df2) + "/user_entered.csv", sep=',',index=False)
                else:
                    sub_dict = {"blank":"blank"}
                    sub_dict = json.dumps(d)
            else:
                d = {}
                sub_dict = {"blank":"blank"}
                sub_dict = json.dumps(d)
                
        else:
            d = {}
            sub_dict = {"blank":"blank"}
            sub_dict = json.dumps(d)
            
        return sub_dict
    else:
        return 'Unsuccessful Auth'
#########################################################################
###############Recurrent Training########################################        
#########################################################################

#Recurrent reaining is the training set we are creating and manipulating the data in the form of training set.
        
@app.route('/nlp/tags',methods=['GET', 'POST'] ) 
@cross_origin(supports_credentials=True)


def upload():
    headers_post = request.headers 
    appid = headers_post['appId']
    tenant_id = headers_post['X-TenantID']
    object_id = headers_post['X-Object']
    Authorization = headers_post['Authorization'] 
    
    URL = os.environ.get("properties_url_review")
    URL = str(URL)+"/property/platform_url"
    response1 = requests.get(URL,headers={"Content-Type":"application/json","X-TenantID" : tenant_id})
    ENV_URL=response1.json()
    ENV_URL=ENV_URL["propertyValue"]
    vf_url = str(ENV_URL) +"/cac-security/api/userinfo"
    response = requests.get(vf_url,headers={"Authorization":Authorization})#    df1=pd.read_csv("C:/Users/kartik.patnaik/Desktop/mobileapp/new_test/stanford-ner-2018-10-16/train2/Book1.csv")
    if response.status_code == 200:
        ROOT_PATH = os.environ.get("path_root_url")
        os.chdir(ROOT_PATH)
        df2 = str(tenant_id)+"/"+str(appid)+"/"+str(object_id)
        user_input = request.get_json()
        #Make sure your input/Recurrent format is exactly mentioned in the doc 
        if user_input != {}:
            wanted_keys = ['sentence']
            wanted_keys1 = ['Tags']
            #Subsetting sentence
            sentence = {k: user_input[k] for k in set(wanted_keys) & set(user_input.keys())}
            sentence = list( sentence.values() )[0]
            #We are finding the dates in sentence and replacing it in a particular format
            #The same steps from base continues
            if sentence != None and sentence != '':
                sentence = sentence.lower()  
                article = sentence[:]
                def find_match(sentence,df):
                    for i in range(df.shape[0]):
                        if sentence.find(df['rpl'][i]) !=-1:
                            sentence = sentence[:sentence.find(df['rpl'][i])] +  df['rpl1'][i] +  sentence[sentence.find(df['rpl'][i])+ len(df['rpl'][i]):]
                    return sentence
               
                sentencek = sentence[:]
                stopwords=[' between ',' of ',' to ']
                for word in stopwords:
                    if word in sentencek:
                        sentencek=sentencek.replace(word," ")   
                
                ls3 = search_dates(sentencek)
                if ls3 == None:
                    ls3 = []
                else:
                    ls3 = [t[::-1] for t in ls3]
#                    ls3 = list(set(ls3+ls_1))
                #Treating date    
                if ls3!=[]:
                    ls4 = pd.DataFrame(ls3)
                    ls4 = ls4.drop_duplicates()
                    ls4.columns = ["rpl1","rpl"]
                    ls4["rpl1"] = pd.to_datetime(ls4["rpl1"], errors='coerce')
                    ls4 = ls4.query('rpl1 != "NaT"')
                    ls4["rpl1"] = ls4["rpl1"].dt.strftime('%Y-%m-%d')
                    ls4 = ls4[pd.to_numeric(ls4['rpl'], errors='coerce').isna()]
                    ls4["rpl2"] = pd.to_datetime(ls4["rpl"], errors='coerce')
                    ls4 = ls4.query('rpl2 != "NaT"')
                    ls4 = ls4.drop(columns=['rpl2'])
                    ls4 = ls4.reset_index(drop = True)
                    ls4.index = ls4['rpl'].str.len()
                    ls4 = ls4.sort_index(ascending=True).reset_index(drop=True)
                    ls4["rpl1"] = ls4["rpl1"].map(str)+ ' '
                    sentence = find_match(sentencek,ls4)                    
#                    return "Enter Text again remove - " #######END


                tags = {k: user_input[k] for k in set(wanted_keys1) & set(user_input.keys())}
                tags = list( tags.values() )[0]
                tags = {k:str(v) for k, v in tags.items()}
                def lower_dict(d):
                    new_dict = dict((k, v.lower()) for k, v in d.items())
                    return new_dict
                tags = lower_dict(tags)
                new_list = [] 
                for key, value in tags.items():
                    new_list.append([key, value])
                ui1 = pd.DataFrame(new_list)
                ui1.columns = ['action','sentence']
                ui1["sentence1"] = ""
               #Here we are replacing the dates in tags so thet we will do correct mapping
               
                for label, content in ui1["sentence"].items():
                    if search_dates(ui1["sentence"][label]) != None:
                        ui1["sentence1"][label] = "Found"
                    else:
                        ui1["sentence1"][label] = "Not Found"
                
                uik = ui1[ui1["sentence1"]=="Found"]
                uik["sentence"] = uik["sentence"].astype(str).str[:-6] #Strip time zone        
                uik["sentence"] = pd.to_datetime(uik["sentence"], errors='coerce')
                uik["sentence"] = uik["sentence"].dt.strftime('%Y-%m-%d')            
                uik = uik.query('sentence != "NaT"')
                uik = uik.drop(['sentence1'], axis=1)
                ui1 = ui1.drop(['sentence1'], axis=1)
                ui1 = ui1.append(uik, ignore_index=True) 

                k = ui1.apply(lambda row: nltk.word_tokenize(row['sentence']), axis=1)
                k = pd.DataFrame(k)
                k.columns = ["sentence"]
                new = k.sentence.apply(pd.Series)
                new["action"]=ui1["action"]
                df_new = pd.DataFrame()
                for label, content in new.items():
                    df_new1 = pd.DataFrame()
                    df_new1[0] = new["action"]
                    df_new1[1] = new[label]
                    df_new = df_new.append(df_new1, ignore_index=True)
                    df_new = df_new[df_new[0] != df_new[1]]
                    df_new = df_new.dropna()
                lst_ip1 = nltk.word_tokenize(sentence)
                lst_ip3 = pd.DataFrame(lst_ip1)
                lst_ip3.columns = ['sentence']
                df_new.columns = ['action','sentence']
                #df_new is tagged data frame
                #lst_ip3 is the sentence converted to data frame and transposed
                #################################################join
                result = pd.merge(lst_ip3,
                                 df_new,
                                 on='sentence', 
                                 how='left')
                
                result['action'] = result['action'].fillna('o')
                result['key'] = (result['sentence'] != result['sentence'].shift(1)).astype(int).cumsum()
                result =result.groupby(['key', 'sentence'])['action'].apply('#$#'.join).to_frame()
                result = result.reset_index()
                result['sentence'] = result['sentence'].map(str) + " " + result["action"]
                user_input3 = result['sentence']
                user_input3.to_csv(str(df2) +'/user_input3.tsv',header=False, index=False)
                user_input3 = pd.read_csv(str(df2) +'/user_input3.tsv', sep='\t',header = None)
                exists = os.path.isfile(str(df2) +'/dummy-corpus1.tsv')
                exists1 = os.path.isfile(str(df2) +'/dummy-corpus2.tsv')
                if exists and not exists1:
                    pa1 = pd.read_csv(str(df2) +'/dummy-corpus1.tsv', sep='\t',header = None)
                    pa2 = pa1.append(user_input3,ignore_index=True)
                    pa2 = pa2.append([". o"])
                elif exists1 and exists:
                    pa1 = pd.read_csv(str(df2) +'/dummy-corpus2.tsv', sep='\t',header = None)
                    pa2 = pa1.append(user_input3,ignore_index=True)
                    pa2 = pa2.append([". o"])  
                else:
                    pa2 = user_input3
                    pa2 = pa2.append([". o"])
                    
                #dummy corpus1 is the training dataset we are creating and we save it in the same part and later call the training file to train    
                pa2.to_csv(str(df2) +'/dummy-corpus1.tsv',header=False, index=False)
                cwd = os.getcwd()
                cwd = pathlib.PureWindowsPath(cwd)
                #don't chaange anything in below property file.
                #you can read NLTK docs
                cwd = cwd.as_posix()
                prop = "trainFile = "+ str(cwd) +"/" + str(df2) + """/dummy-corpus1.tsv
                serializeTo ="""+ str(cwd) +"/" + str(df2) +"""/corpus-tagging.ser.gz
                map = word=0,answer=1
                useClassFeature=true
                useWord=true
                useNGrams=true
                noMidNGrams=true
                maxNGramLeng=6
                usePrev=true
                useNext=true
                useSequences=true
                usePrevSequences=true
                maxLeft=1
                useTypeSeqs=true
                useTypeSeqs2=true
                useTypeySequences=true
                wordShape=chris2useLC
                useDisjunctive=true"""
                
                file = open( str(cwd) +"/" + str(df2)+'/prop2.txt', 'w')
                file.write(prop)
                file.close()
                myCmd = 'java -jar stanford-ner.jar -mx4g -prop' " "  + str(df2) + '/prop2.txt'
                os.system(myCmd)   
    
                return 'Recurrent Training on Completed Successfully'
            else:
                return 'No Data to be trained on NULL'
    else:
        return 'Unsuccessful Auth'

#########################################################################
###############blank Trained#############################################       
#########################################################################
#You can train the model in a blank file or delete the object        
    
@app.route('/nlp/reset')
@cross_origin(supports_credentials=True) 


def blank_trained(): 
    headers_post = request.headers 
    appid = headers_post['appId']
    tenant_id = headers_post['X-TenantID']
    object_id = headers_post['X-Object']
    Authorization = headers_post['Authorization']  
     
    URL = os.environ.get("properties_url_review")
    URL = str(URL)+"/property/platform_url"
    response1 = requests.get(URL,headers={"Content-Type":"application/json","X-TenantID" : tenant_id})
    ENV_URL=response1.json()
    ENV_URL=ENV_URL["propertyValue"]
    vf_url = str(ENV_URL) +"/cac-security/api/userinfo"
    response = requests.get(vf_url,headers={"Authorization":Authorization})


    if response.status_code == 200:    
        ROOT_PATH = os.environ.get("path_root_url")
        os.chdir(ROOT_PATH)
        df2 = str(tenant_id)+"/"+str(appid)+"/"+str(object_id)
        cwd = os.getcwd()
        cwd = pathlib.PureWindowsPath(cwd)
        cwd = cwd.as_posix()
        if not os.path.exists(str(cwd) +"/" + str(df2)):
            os.makedirs(str(cwd) +"/" + str(df2))
            pa2 = pd.DataFrame(index=range(1))
            pa2.to_csv(str(cwd) +"/" +str(df2) +'/dummy-corpus3.tsv',header=False, index=False)
        prop = "trainFile = "+ str(cwd) +"/" + str(df2) + """/dummy-corpus3.tsv
        serializeTo ="""+ str(cwd) +"/" + str(df2) +"""/corpus-tagging.ser.gz
        map = word=0,answer=1
        
        useClassFeature=true
        useWord=true
        useNGrams=true
        noMidNGrams=true
        maxNGramLeng=6
        usePrev=true
        useNext=true
        useSequences=true
        usePrevSequences=true
        maxLeft=1
        useTypeSeqs=true
        useTypeSeqs2=true
        useTypeySequences=true
        wordShape=chris2useLC
        useDisjunctive=true"""
        
        file = open( str(cwd) +"/" + str(df2)+'/prop3.txt', 'w')
        file.write(prop)
        file.close()
        myCmd = 'java -jar stanford-ner.jar -mx4g -prop' " "  + str(df2) + '/prop3.txt'
        os.system(myCmd)  
        if os.system(myCmd)==0:
            return 'Recurrent Training on blank for Completed Successfully'
        else:
            
            return 'Recurrent training Failed check Header'
    else:
        return 'Unsuccessful Auth'


#########################################################################
###############Raw Trained###############################################       
#########################################################################
@app.route('/raw')
@cross_origin(supports_credentials=True)

def raw():
    headers_post = request.headers 
    appid = headers_post['appId']
    tenant_id = headers_post['X-TenantID']
    object_id = headers_post['X-Object']
    Authorization = headers_post['Authorization'] 
    
    URL = os.environ.get("properties_url_review")
    URL = str(URL)+"/property/platform_url"
    response1 = requests.get(URL,headers={"Content-Type":"application/json","X-TenantID" : tenant_id})
    ENV_URL=response1.json()
    ENV_URL=ENV_URL["propertyValue"]
    vf_url = str(ENV_URL) +"/cac-security/api/userinfo"
    response = requests.get(vf_url,headers={"Authorization":Authorization})
    if response.status_code == 200: 
        ROOT_PATH = os.environ.get("path_root_url")
        os.chdir(ROOT_PATH)
        df2 = str(tenant_id)+"/"+str(appid)+"/"+str(object_id)
        cwd = os.getcwd()
        cwd = pathlib.PureWindowsPath(cwd)
        cwd = cwd.as_posix()
        if not os.path.exists(str(cwd) +"/" + str(df2)):
            os.makedirs(str(cwd) +"/" + str(df2))
            pa2 = pd.DataFrame(index=range(1))
            pa2.to_csv(str(cwd) +"/" +str(df2) +'/dummy-corpus1.tsv',header=False, index=False)
            prop = "trainFile = "+ str(cwd) +"/" + str(df2) + """/dummy-corpus1.tsv
            serializeTo ="""+ str(cwd) +"/" + str(df2) +"""/corpus-tagging.ser.gz
            map = word=0,answer=1
            
            useClassFeature=true
            useWord=true
            useNGrams=true
            noMidNGrams=true
            maxNGramLeng=6
            usePrev=true
            useNext=true
            useSequences=true
            usePrevSequences=true
            maxLeft=1
            useTypeSeqs=true
            useTypeSeqs2=true
            useTypeySequences=true
            wordShape=chris2useLC
            useDisjunctive=true"""
            
            file = open( str(cwd) +"/" + str(df2)+'/prop1.txt', 'w')
            file.write(prop)
            file.close()
            myCmd = 'java -jar stanford-ner.jar -mx4g -prop' " "  + str(df2) + '/prop1.txt'
            os.system(myCmd)
        else:         
            prop = "trainFile = "+ str(cwd) +"/" + str(df2) + """/dummy-corpus1.tsv
            serializeTo ="""+ str(cwd) +"/" + str(df2) +"""/corpus-tagging.ser.gz
            map = word=0,answer=1
            
            useClassFeature=true
            useWord=true
            useNGrams=true
            noMidNGrams=true
            maxNGramLeng=6
            usePrev=true
            useNext=true
            useSequences=true
            usePrevSequences=true
            maxLeft=1
            useTypeSeqs=true
            useTypeSeqs2=true
            useTypeySequences=true
            wordShape=chris2useLC
            useDisjunctive=true"""
            
            file = open( str(cwd) +"/" + str(df2)+'/prop1.txt', 'w')
            file.write(prop)
            file.close()
            myCmd = 'java -jar stanford-ner.jar -mx4g -prop' " "  + str(df2) + '/prop1.txt'
            os.system(myCmd)  
        if os.system(myCmd)==0:
            return 'Raw Training on blank Completed Successfully'
        else:
            
            return 'Recurrent training Failed check Header or existance of input File'        
    else:
        return 'Unsuccessful Auth'


#########################################################################
###############Bulk Training#############################################        
#########################################################################
#Bulk training and Initial training  are the subsets of recurrent training codes are same except few changes        
    
@app.route('/nlp/bulk_tags',methods=['GET', 'POST']) 
@cross_origin(supports_credentials=True)


def upload_bulk():
    headers_post = request.headers 
    appid = headers_post['appId']
    tenant_id = headers_post['X-TenantID']
    object_id = headers_post['X-Object']
    Authorization = headers_post['Authorization'] 
    
    URL = os.environ.get("properties_url_review")
    URL = str(URL)+"/property/platform_url"
    response1 = requests.get(URL,headers={"Content-Type":"application/json","X-TenantID" : tenant_id})
    ENV_URL=response1.json()
    ENV_URL=ENV_URL["propertyValue"]
    vf_url = str(ENV_URL) +"/cac-security/api/userinfo"
    response = requests.get(vf_url,headers={"Authorization":Authorization})#    df1=pd.read_csv("C:/Users/kartik.patnaik/Desktop/mobileapp/new_test/stanford-ner-2018-10-16/train2/Book1.csv")
    if response.status_code == 200:
        ROOT_PATH = os.environ.get("path_root_url")
        os.chdir(ROOT_PATH)
        df2 = str(tenant_id)+"/"+str(appid)+"/"+str(object_id)
        cwd = os.getcwd()
        cwd = pathlib.PureWindowsPath(cwd)
        cwd = cwd.as_posix()
        if not os.path.exists(str(cwd) +"/" + str(df2)):
            os.makedirs(str(cwd) +"/" + str(df2))
        user_input = request.get_json()
        if user_input != []:
            for i in range(len(user_input)):        
                user_input_1 = user_input[i]
                wanted_keys = ['sentence']
                wanted_keys1 = ['Tags']
                sentence = {k: user_input_1[k] for k in set(wanted_keys) & set(user_input_1.keys())}
                sentence = list( sentence.values() )[0]
            
                if sentence != None and sentence != '':
                    sentence = sentence.lower()  
                    insensitive_hippo = re.compile(re.escape('buy'), re.IGNORECASE)
                    sentence = insensitive_hippo.sub('purchase', sentence)
                    insensitive_hippo = re.compile(re.escape('sell'), re.IGNORECASE)
                    sentence = insensitive_hippo.sub('sale', sentence) 
                    article = sentence[:]
                    def find_match(sentence,df):
                        for i in range(df.shape[0]):
                            if sentence.find(df['rpl'][i]) !=-1:
                                sentence = sentence[:sentence.find(df['rpl'][i])] +  df['rpl1'][i] +  sentence[sentence.find(df['rpl'][i])+ len(df['rpl'][i]):]
                        return sentence
                   
                    sentencek = sentence[:]
                    stopwords=[' between ',' of ',' to ']
                    for word in stopwords:
                        if word in sentencek:
                            sentencek=sentencek.replace(word," ")   
                    
                    ls3 = search_dates(sentencek)
                    if ls3 == None:
                        ls3 = []
                    else:
                        ls3 = [t[::-1] for t in ls3]
        
                    if ls3!=[]:
                        ls4 = pd.DataFrame(ls3)
                        ls4 = ls4.drop_duplicates()
                        ls4.columns = ["rpl1","rpl"]
                        ls4["rpl1"] = pd.to_datetime(ls4["rpl1"], errors='coerce',utc=True)
                        ls4 = ls4.query('rpl1 != "NaT"')
                        ls4["rpl1"] = ls4["rpl1"].dt.strftime('%Y-%m-%d')
                        ls4 = ls4[pd.to_numeric(ls4['rpl'], errors='coerce').isna()]
                        ls4["rpl2"] = pd.to_datetime(ls4["rpl"], errors='coerce',utc = True)
                        ls4 = ls4.query('rpl2 != "NaT"')
                        ls4 = ls4.drop(columns=['rpl2'])
                        ls4 = ls4.reset_index(drop = True)
                        ls4.index = ls4['rpl'].str.len()
                        ls4 = ls4.sort_index(ascending=True).reset_index(drop=True)
                        ls4["rpl1"] = ls4["rpl1"].map(str)+ ' '
                        sentence = find_match(sentencek,ls4)                    
        
        
                    tags = {k: user_input_1[k] for k in set(wanted_keys1) & set(user_input_1.keys())}
                    tags = list( tags.values() )[0]
                    tags = {k:str(v) for k, v in tags.items()}
                    def lower_dict(d):
                        new_dict = dict((k, v.lower()) for k, v in d.items())
                        return new_dict
                    tags = lower_dict(tags)
                    new_list = [] 
                    for key, value in tags.items():
                        new_list.append([key, value])
                    ui1 = pd.DataFrame(new_list)
                    ui1.columns = ['action','sentence']
                    ui1["sentence1"] = ""
                   
                    for label, content in ui1["sentence"].items():
                        if search_dates(ui1["sentence"][label]) != None:
                            ui1["sentence1"][label] = "Found"
                        else:
                            ui1["sentence1"][label] = "Not Found"
                    
                    uik = ui1[ui1["sentence1"]=="Found"]
                    uik["sentence"] = uik["sentence"].astype(str).str[:-6] #Strip time zone        
                    uik["sentence"] = pd.to_datetime(uik["sentence"], errors='coerce')
                    uik["sentence"] = uik["sentence"].dt.strftime('%Y-%m-%d')            
                    uik = uik.query('sentence != "NaT"')
                    uik = uik.drop(['sentence1'], axis=1)
                    ui1 = ui1.drop(['sentence1'], axis=1)
                    ui1 = ui1.append(uik, ignore_index=True) 
        
        
                    k = ui1.apply(lambda row: nltk.word_tokenize(row['sentence']), axis=1)
                    k = pd.DataFrame(k)
                    k.columns = ["sentence"]
                    new = k.sentence.apply(pd.Series)
                    new["action"]=ui1["action"]
                    df_new = pd.DataFrame()
                    for label, content in new.items():
                        df_new1 = pd.DataFrame()
                        df_new1[0] = new["action"]
                        df_new1[1] = new[label]
                        df_new = df_new.append(df_new1, ignore_index=True)
                        df_new = df_new[df_new[0] != df_new[1]]
                        df_new = df_new.dropna()
                    lst_ip1 = nltk.word_tokenize(sentence)
                    lst_ip3 = pd.DataFrame(lst_ip1)
                    lst_ip3.columns = ['sentence']
                    df_new.columns = ['action','sentence']
                    #################################################join
                    result = pd.merge(lst_ip3,
                                     df_new,
                                     on='sentence', 
                                     how='left')
                    
                    result['action'] = result['action'].fillna('o')
                    result['key'] = (result['sentence'] != result['sentence'].shift(1)).astype(int).cumsum()
                    result =result.groupby(['key', 'sentence'])['action'].apply('#$#'.join).to_frame()
                    result = result.reset_index()
                    result['sentence'] = result['sentence'].map(str) + " " + result["action"]
                    user_input3 = result['sentence']
                    user_input3.to_csv(str(df2) +'/user_input3.tsv',header=False, index=False)
                    user_input3 = pd.read_csv(str(df2) +'/user_input3.tsv', sep='\t',header = None)
                    exists = os.path.isfile(str(df2) +'/dummy-corpus1.tsv')
                    exists1 = os.path.isfile(str(df2) +'/dummy-corpus2.tsv')
                    if exists and not exists1:
                        pa1 = pd.read_csv(str(df2) +'/dummy-corpus1.tsv', sep='\t',header = None)
                        pa2 = pa1.append(user_input3,ignore_index=True)
                        pa2 = pa2.append([". o"])
                    elif exists1 and exists:
                        pa1 = pd.read_csv(str(df2) +'/dummy-corpus2.tsv', sep='\t',header = None)
                        pa2 = pa1.append(user_input3,ignore_index=True)
                        pa2 = pa2.append([". o"])  
                    else:
                        pa2 = user_input3
                        pa2 = pa2.append([". o"])
                        
                    pa2.to_csv(str(df2) +'/dummy-corpus1.tsv',header=False, index=False)
                
            cwd = os.getcwd()
            cwd = pathlib.PureWindowsPath(cwd)
            cwd = cwd.as_posix()
            prop = "trainFile = "+ str(cwd) +"/" + str(df2) + """/dummy-corpus1.tsv
            serializeTo ="""+ str(cwd) +"/" + str(df2) +"""/corpus-tagging.ser.gz
            map = word=0,answer=1
            
            useClassFeature=true
            useWord=true
            useNGrams=true
            noMidNGrams=true
            maxNGramLeng=6
            usePrev=true
            useNext=true
            useSequences=true
            usePrevSequences=true
            maxLeft=1
            useTypeSeqs=true
            useTypeSeqs2=true
            useTypeySequences=true
            wordShape=chris2useLC
            useDisjunctive=true"""
            
            file = open( str(cwd) +"/" + str(df2)+'/prop2.txt', 'w')
            file.write(prop)
            file.close()
            myCmd = 'java -jar stanford-ner.jar -mx4g -prop' " "  + str(df2) + '/prop2.txt'
            os.system(myCmd)   
        
            return 'Recurrent Training on Completed Successfully'
        
        else:
                return 'No Data to be trained on NULL'
    else:
        return 'Unsuccessful Auth'
        

#########################################################################
###############Initial Training##########################################        
#########################################################################
@app.route('/nlp/initial_training',methods=['GET', 'POST']) 
@cross_origin(supports_credentials=True)


def initial_bulk_load():
    headers_post = request.headers 
    appid = headers_post['appId']
    tenant_id = headers_post['X-TenantID']
    object_id = headers_post['X-Object']
    Authorization = headers_post['Authorization'] 
    
    URL = os.environ.get("properties_url_review")
    URL = str(URL)+"/property/platform_url"
    response1 = requests.get(URL,headers={"Content-Type":"application/json","X-TenantID" : tenant_id})
    ENV_URL=response1.json()
    ENV_URL=ENV_URL["propertyValue"]
    vf_url = str(ENV_URL) +"/cac-security/api/userinfo"
    response = requests.get(vf_url,headers={"Authorization":Authorization})#    df1=pd.read_csv("C:/Users/kartik.patnaik/Desktop/mobileapp/new_test/stanford-ner-2018-10-16/train2/Book1.csv")
    if response.status_code == 200:
        ROOT_PATH = os.environ.get("path_root_url")
        os.chdir(ROOT_PATH)
        df2 = str(tenant_id)+"/"+str(appid)+"/"+str(object_id)
        cwd = os.getcwd()
        cwd = pathlib.PureWindowsPath(cwd)
        cwd = cwd.as_posix()
        if not os.path.exists(str(cwd) +"/" + str(df2)):
            os.makedirs(str(cwd) +"/" + str(df2))
        file = open('pre_load.txt', 'r')
        if file.mode == 'r':
            contents =file.read()
        df = pd.DataFrame([x.split('::') for x in contents.split('\n')])
        df = df.rename(columns=df.iloc[0]).drop(df.index[0])
        
        if (len(df['appid'].str.contains(appid))>0):
            df = df[df['appid'].str.contains(appid)]
            if (len(df['objectid'].str.contains(object_id))>0):
                df = df[df['objectid'].str.contains(object_id)]
                df = df[:1]
                JSON_NAME = df["JSON_name"]
                JSON_NAME.reset_index(drop=True, inplace=True)
                JSON_NAME = JSON_NAME[0]
            else:
                JSON_NAME = ""
        
        if JSON_NAME !="":
            with open(JSON_NAME+".json") as json_file:
                user_input = json.load(json_file)    
        else:
            user_input = []
        
        if user_input != []:
            for i in range(len(user_input)):        
                user_input_1 = user_input[i]
                wanted_keys = ['sentence']
                wanted_keys1 = ['Tags']
                sentence = {k: user_input_1[k] for k in set(wanted_keys) & set(user_input_1.keys())}
                sentence = list( sentence.values() )[0]
            
                if sentence != None and sentence != '':
                    sentence = sentence.lower()  
                    insensitive_hippo = re.compile(re.escape('buy'), re.IGNORECASE)
                    sentence = insensitive_hippo.sub('purchase', sentence)
                    insensitive_hippo = re.compile(re.escape('sell'), re.IGNORECASE)
                    sentence = insensitive_hippo.sub('sale', sentence) 
                    article = sentence[:]
                    def find_match(sentence,df):
                        for i in range(df.shape[0]):
                            if sentence.find(df['rpl'][i]) !=-1:
                                sentence = sentence[:sentence.find(df['rpl'][i])] +  df['rpl1'][i] +  sentence[sentence.find(df['rpl'][i])+ len(df['rpl'][i]):]
                        return sentence
                   
                    sentencek = sentence[:]
                    stopwords=[' between ',' of ']
                    for word in stopwords:
                        if word in sentencek:
                            sentencek=sentencek.replace(word," ")   
                    
                    ls3 = search_dates(sentencek)
                    if ls3 == None:
                        ls3 = []
                    else:
                        ls3 = [t[::-1] for t in ls3]
        
                    if ls3!=[]:
                        ls4 = pd.DataFrame(ls3)
                        ls4 = ls4.drop_duplicates()
                        ls4.columns = ["rpl1","rpl"]
                        ls4["rpl1"] = pd.to_datetime(ls4["rpl1"], errors='coerce')
                        ls4 = ls4.query('rpl1 != "NaT"')
                        ls4["rpl1"] = ls4["rpl1"].dt.strftime('%Y-%m-%d')
                        ls4 = ls4[pd.to_numeric(ls4['rpl'], errors='coerce').isna()]
                        ls4["rpl2"] = pd.to_datetime(ls4["rpl"], errors='coerce')
                        ls4 = ls4.query('rpl2 != "NaT"')
                        ls4 = ls4.drop(columns=['rpl2'])
                        ls4 = ls4.reset_index(drop = True)
                        ls4.index = ls4['rpl'].str.len()
                        ls4 = ls4.sort_index(ascending=True).reset_index(drop=True)
                        ls4["rpl1"] = ls4["rpl1"].map(str)+ ' '
                        sentence = find_match(sentencek,ls4)                    
        
        
                    tags = {k: user_input_1[k] for k in set(wanted_keys1) & set(user_input_1.keys())}
                    tags = list( tags.values() )[0]
                    tags = {k:str(v) for k, v in tags.items()}
                    def lower_dict(d):
                        new_dict = dict((k, v.lower()) for k, v in d.items())
                        return new_dict
                    tags = lower_dict(tags)
                    new_list = [] 
                    for key, value in tags.items():
                        new_list.append([key, value])
                    ui1 = pd.DataFrame(new_list)
                    ui1.columns = ['action','sentence']
                    ui1["sentence1"] = ""
                   
                    for label, content in ui1["sentence"].items():
                        if search_dates(ui1["sentence"][label]) != None:
                            ui1["sentence1"][label] = "Found"
                        else:
                            ui1["sentence1"][label] = "Not Found"
                    
                    uik = ui1[ui1["sentence1"]=="Found"]
                    uik["sentence"] = uik["sentence"].astype(str).str[:-6] #Strip time zone        
                    uik["sentence"] = pd.to_datetime(uik["sentence"], errors='coerce')
                    uik["sentence"] = uik["sentence"].dt.strftime('%Y-%m-%d')            
                    uik = uik.query('sentence != "NaT"')
                    uik = uik.drop(['sentence1'], axis=1)
                    ui1 = ui1.drop(['sentence1'], axis=1)
                    ui1 = ui1.append(uik, ignore_index=True) 
        
        
                    k = ui1.apply(lambda row: nltk.word_tokenize(row['sentence']), axis=1)
                    k = pd.DataFrame(k)
                    k.columns = ["sentence"]
                    new = k.sentence.apply(pd.Series)
                    new["action"]=ui1["action"]
                    df_new = pd.DataFrame()
                    for label, content in new.items():
                        df_new1 = pd.DataFrame()
                        df_new1[0] = new["action"]
                        df_new1[1] = new[label]
                        df_new = df_new.append(df_new1, ignore_index=True)
                        df_new = df_new[df_new[0] != df_new[1]]
                        df_new = df_new.dropna()
                    lst_ip1 = nltk.word_tokenize(sentence)
                    lst_ip3 = pd.DataFrame(lst_ip1)
                    lst_ip3.columns = ['sentence']
                    df_new.columns = ['action','sentence']
                    #################################################join
                    result = pd.merge(lst_ip3,
                                     df_new,
                                     on='sentence', 
                                     how='left')
                    
                    result['action'] = result['action'].fillna('o')
                    result['key'] = (result['sentence'] != result['sentence'].shift(1)).astype(int).cumsum()
                    result =result.groupby(['key', 'sentence'])['action'].apply('#$#'.join).to_frame()
                    result = result.reset_index()
                    result['sentence'] = result['sentence'].map(str) + " " + result["action"]
                    user_input3 = result['sentence']
                    user_input3.to_csv(str(df2) +'/user_input3.tsv',header=False, index=False)
                    user_input3 = pd.read_csv(str(df2) +'/user_input3.tsv', sep='\t',header = None)
                    exists = os.path.isfile(str(df2) +'/dummy-corpus1.tsv')
                    exists1 = os.path.isfile(str(df2) +'/dummy-corpus2.tsv')
                    if exists and not exists1:
                        pa1 = pd.read_csv(str(df2) +'/dummy-corpus1.tsv', sep='\t',header = None)
                        pa2 = pa1.append(user_input3,ignore_index=True)
                        pa2 = pa2.append([". o"])
                    elif exists1 and exists:
                        pa1 = pd.read_csv(str(df2) +'/dummy-corpus2.tsv', sep='\t',header = None)
                        pa2 = pa1.append(user_input3,ignore_index=True)
                        pa2 = pa2.append([". o"])  
                    else:
                        pa2 = user_input3
                        pa2 = pa2.append([". o"])
                        
                    pa2.to_csv(str(df2) +'/dummy-corpus1.tsv',header=False, index=False)
                
            cwd = os.getcwd()
            cwd = pathlib.PureWindowsPath(cwd)
            cwd = cwd.as_posix()
            prop = "trainFile = "+ str(cwd) +"/" + str(df2) + """/dummy-corpus1.tsv
            serializeTo ="""+ str(cwd) +"/" + str(df2) +"""/corpus-tagging.ser.gz
            map = word=0,answer=1
            
            useClassFeature=true
            useWord=true
            useNGrams=true
            noMidNGrams=true
            maxNGramLeng=6
            usePrev=true
            useNext=true
            useSequences=true
            usePrevSequences=true
            maxLeft=1
            useTypeSeqs=true
            useTypeSeqs2=true
            useTypeySequences=true
            wordShape=chris2useLC
            useDisjunctive=true"""
            
            file = open( str(cwd) +"/" + str(df2)+'/prop2.txt', 'w')
            file.write(prop)
            file.close()
            myCmd = 'java -jar stanford-ner.jar -mx4g -prop' " "  + str(df2) + '/prop2.txt'
            os.system(myCmd)   
        
            return 'Recurrent Training on Completed Successfully'
        
        else:
                return 'No Data to be trained on NULL'
    else:
        return 'Unsuccessful Auth'
    
if __name__ == '__main__': 
    app.debug = True
    app.run(host = '0.0.0.0',port = 3131)