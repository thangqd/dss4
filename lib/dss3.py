import pandas as pd
from pandas.api.types import is_numeric_dtype
pd.options.mode.copy_on_write = True
import streamlit as st
import locale
from locale import atof
import numpy as np
    
def dss3_level(risk_value):
        level = ''
        if risk_value is not None:
            if risk_value >= 15 and risk_value <= 25:
                level =  "Rất cao"
            elif risk_value >= 9 and risk_value <= 14:
                level =  "Cao"
            elif risk_value >=3 and risk_value  <= 8:
                level =  "Vừa"
            elif risk_value < 3:
                level =  "Thấp"
        return level    
    
def dss3_color(risk_value):
    color = ''
    if risk_value is not None:
        if risk_value >= 15 and risk_value <= 25:
            color =  'RGB(255,0,0)'
        elif risk_value >= 9 and risk_value <= 14:
            color =  'RGB(255,126,0)'            
        elif risk_value >=3 and risk_value  <= 8:
            color =   'RGB(255,255,0)'
        elif risk_value < 3:
            color = 'RGB(0,228,0)'            
    return color    
    
params_H1 = pd.DataFrame(
        {
            ">=91": [91,1],
            "76 - 90": [76,2],
            "51 - 75": [51,3],
            "26 - 50": [26,4], 
            "<= 25": [25,5],

        }
)

def dss3_H1(row):
    if (row['WQI'] >= params_H1.iloc[0][0]): # ">=91"
        H1 = params_H1.iloc[1][0]*row['Wh1'] # =1    
    
    elif  row['WQI'] >= params_H1.iloc[0][1] and row['WQI']<= params_H1.iloc[0][0]: #"76 - 90"
        H1 = params_H1.iloc[1][1]*row['Wh1'] # =2
    
    elif  row['WQI'] >= params_H1.iloc[0][2] and row['WQI']<= params_H1.iloc[0][1]: #"51 - 75"
        H1 = params_H1.iloc[1][2]*row['Wh1'] # =3

    elif  row['WQI'] >= params_H1.iloc[0][3] and row['WQI']<= params_H1.iloc[0][2]: #"26 - 50"
        H1 = params_H1.iloc[1][3]*row['Wh1'] # =4
    
    elif  row['WQI'] <= params_H1.iloc[0][4]: #"<= 25"
        H1 = params_H1.iloc[1][4]*row['Wh1'] # =5

    return H1

params_H2 = pd.DataFrame(
        {
            ">=2": [2.0,1],
            "1.5 - 2": [1.5,1],
            "0 - 1.5": [0,3],
            "-1.5 - 0": [-1.5, 4], 
            "< -1.5": [-1.5,5],

        }
)
def dss3_H2(row):
    if (row['HH'] >= params_H2.iloc[0][0]): # ">=2"
        H2 = params_H2.iloc[1][0]*row['Wh2'] # =1    
    
    elif  row['HH'] >= params_H2.iloc[0][1] and row['HH']< params_H2.iloc[0][0]: #"1.5 - < 2"
        H2 = params_H2.iloc[1][1]*row['Wh2'] # =2
    
    elif  row['HH'] >= params_H2.iloc[0][2] and row['HH']< params_H2.iloc[0][1]: #"0 - < 1.5"
        H2 = params_H2.iloc[1][2]*row['Wh2'] # =3

    elif  row['HH'] >= params_H2.iloc[0][3] and row['HH']< params_H2.iloc[0][2]: #"-1.5 - <0"
        H2 = params_H2.iloc[1][3]*row['Wh2'] # =4
    
    elif  row['HH'] < params_H2.iloc[0][4]: #"<-1.5"
        H2 = params_H2.iloc[1][4]*row['Wh2'] # =5

    return H2

params_H3 = pd.DataFrame(
        {
            "0 - 0.16": [0,1],
            "0.16 - 0.48": [0.16,2],
            "0.48 - 1.44": [0.48,3],
            "1.44 - 2.56": [1.44, 4], 
            "2.56 - 22.4": [2.56,5]
        }
)

def dss3_H3(row):
    if (row['XNM'] >= params_H3.iloc[0][0] and row['XNM'] < params_H3.iloc[0][1]): # "0 <= XNM < 0.16"
        H3 = params_H3.iloc[1][0]*row['Wh3'] # =1    
    
    elif  row['XNM'] >= params_H3.iloc[0][1] and row['XNM']< params_H3.iloc[0][2]: #"0.16<= XNM < 0.48"
        H3 = params_H3.iloc[1][1]*row['Wh3'] # =2
    
    elif  row['XNM'] >= params_H3.iloc[0][2] and row['XNM']< params_H3.iloc[0][3]: #"0.48 <= XNM <1.44"
        H3 = params_H3.iloc[1][2]*row['Wh3'] # =3

    elif  row['XNM'] >= params_H3.iloc[0][3] and row['XNM']< params_H3.iloc[0][4]: #"1.44 <= XNM < 2.56"
        H3 = params_H3.iloc[1][3]*row['Wh3'] # =4
    
    elif  row['XNM'] >= params_H3.iloc[0][4]: #"2.56 <= XNM"
        H3 = params_H3.iloc[1][4]*row['Wh3'] # =5

    return H3

params_H4 = pd.DataFrame(
        {
            "0 - 0.25": [0,1],
            "0.25 - 0.5": [0.25,2],
            "0.5 - 1": [0.5,3],
            "1 - 1.5": [1, 4], 
            ">= 1.5": [1.5,5]
        }
)

def dss3_H4(row):
    if (row['LL'] >= params_H4.iloc[0][0] and row['LL'] < params_H4.iloc[0][1]): # "0 <= LL < 0.25 --> 1"
        H4 = params_H4.iloc[1][0]*row['Wh4'] # =1    
    
    elif  row['LL'] >= params_H4.iloc[0][1] and row['LL']< params_H4.iloc[0][2]: #"0.25 <= LL < 0.5 --> 2"
        H4 = params_H4.iloc[1][1]*row['Wh4'] # =2
    
    elif  row['LL'] >= params_H4.iloc[0][2] and row['LL']< params_H4.iloc[0][3]: #"0.5 <= LL < 1 --> 3"
        H4 = params_H4.iloc[1][2]*row['Wh4'] # =3

    elif  row['LL'] >= params_H4.iloc[0][3] and row['LL']< params_H4.iloc[0][4]: #"1 <= LL < 1.5 --> 4"
        H4 = params_H4.iloc[1][3]*row['Wh4'] # =4
    
    elif  row['LL'] >= params_H4.iloc[0][4]: #"1.5 <= LL --> 5"
        H4 = params_H4.iloc[1][4]*row['Wh4'] # =5

    return H4

params_H5 = pd.DataFrame(
        {
            "0 - 2": [0,1],
            "2 - 4": [2,2],
            "4 - 6": [4,3],
            "6 - 8": [6, 4], 
            ">= 8": [8,5]
        }
)


def dss3_H5(row):
    if (row['SL'] >= params_H5.iloc[0][0] and row['SL'] < params_H5.iloc[0][1]): # "0 <= SL < 2 --> 1"
        H5 = params_H5.iloc[1][0]*row['Wh5'] # =1    
    
    elif  row['SL'] >= params_H5.iloc[0][1] and row['SL']< params_H5.iloc[0][2]: #"2 <= SL < 4 --> 2"
        H5 = params_H5.iloc[1][1]*row['Wh5'] # =2
    
    elif  row['SL'] >= params_H5.iloc[0][2] and row['SL']< params_H5.iloc[0][3]: #"4 <= SL < 6 --> 3"
        H5 = params_H5.iloc[1][2]*row['Wh5'] # =3

    elif  row['SL'] >= params_H5.iloc[0][3] and row['SL']< params_H5.iloc[0][4]: #"6 <= SL < 8 --> 4"
        H5 = params_H5.iloc[1][3]*row['Wh5'] # =4
    
    elif  row['SL'] >= params_H5.iloc[0][4]: #"8 <= SL --> 5"
        H5 = params_H5.iloc[1][4]*row['Wh5'] # =5

    return H5

def dss3_Hindex(row):
    Hindex = row['H1'] + row['H2'] + row['H3'] + row['H4'] + row['H5']
    return Hindex


params_V1 = pd.DataFrame(
        {
            "0 - 500": [0,1],
            "500 - 1000": [500,2],
            "1000 - 2500": [1000,3],
            "2500 - 5000": [2500, 4], 
            ">= 5000": [5000,5]
        }
)

def dss3_V1(row):
    if (row['Qyc'] >= params_V1.iloc[0][0] and row['Qyc'] < params_V1.iloc[0][1]): # "0 <= Qyc < 500 --> 1"
        V1 = params_V1.iloc[1][0]*row['Wv1'] # =1    
    
    elif  row['Qyc'] >= params_V1.iloc[0][1] and row['Qyc']< params_V1.iloc[0][2]: #"500 <= Qyc < 1000 --> 2"
        V1 = params_V1.iloc[1][1]*row['Wv1'] # =2
    
    elif  row['Qyc'] >= params_V1.iloc[0][2] and row['Qyc']< params_V1.iloc[0][3]: #"1000 <= Qyc < 2500 --> 3"
        V1 = params_V1.iloc[1][2]*row['Wv1'] # =3

    elif  row['Qyc'] >= params_V1.iloc[0][3] and row['Qyc']< params_V1.iloc[0][4]: #"2500 <= Qyc < 5000 --> 4"
        V1 = params_V1.iloc[1][3]*row['Wv1'] # =4
    
    elif  row['Qyc'] >= params_V1.iloc[0][4]: #"5000 <= Qyc --> 5"
        V1 = params_V1.iloc[1][4]*row['Wv1'] # =5

    return V1


params_V2 = pd.DataFrame(
        {
            "0 - 500": [0,1],
            "500 - 1200": [500,2],
            "1200 - 1400": [1200,3],
            "1400 - 1800": [1400, 4], 
            ">= 1800": [1800,5]
        }
)


def dss3_V2(row):
    if (row['PD'] >= params_V2.iloc[0][0] and row['PD'] < params_V2.iloc[0][1]): # "0 <= PD < 500 --> 1"
        V2 = params_V2.iloc[1][0]*row['Wv2'] # =1    
    
    elif  row['PD'] >= params_V2.iloc[0][1] and row['PD']< params_V2.iloc[0][2]: #"500 <= PD < 1200 --> 2"
        V2 = params_V2.iloc[1][1]*row['Wv2'] # =2
    
    elif  row['PD'] >= params_V2.iloc[0][2] and row['PD']< params_V2.iloc[0][3]: #"1200 <= PD < 1400 --> 3"
        V2 = params_V2.iloc[1][2]*row['Wv2'] # =3

    elif  row['PD'] >= params_V2.iloc[0][3] and row['PD']< params_V2.iloc[0][4]: #"1400 <= PD < 1800 --> 4"
        V2 = params_V2.iloc[1][3]*row['Wv2'] # =4
    
    elif  row['PD'] >= params_V2.iloc[0][4]: #"1800 <= PD --> 5"
        V2 = params_V2.iloc[1][4]*row['Wv2'] # =5

    return V2


params_V3 = pd.DataFrame(
        {
            "0 - 0.25": [0,1],
            "0.25 - 0.5": [0.25,2],
            "0.5 - 0.75": [0.5,3],
            "0.75 - 1": [0.75, 4], 
            ">= 1": [1,5]
        }
)

def dss3_V3(row):
    if (row['WSCI'] >= params_V3.iloc[0][0] and row['WSCI'] < params_V3.iloc[0][1]): # "0 <= WSCI < 0.25 --> 1"
        V3 = params_V3.iloc[1][0]*row['Wv3'] # =1    
    
    elif  row['WSCI'] >= params_V3.iloc[0][1] and row['WSCI']< params_V3.iloc[0][2]: #"0.25 <= WSCI < 0.5 --> 2"
        V3 = params_V3.iloc[1][1]*row['Wv3'] # =2
    
    elif  row['WSCI'] >= params_V3.iloc[0][2] and row['WSCI']< params_V3.iloc[0][3]: #"0.5 <= WSCI < 0.75 --> 3"
        V3 = params_V3.iloc[1][2]*row['Wv3'] # =3

    elif  row['WSCI'] >= params_V3.iloc[0][3] and row['WSCI']< params_V3.iloc[0][4]: #"0.75 <= WSCI < 1 --> 4"
        V3 = params_V3.iloc[1][3]*row['Wv3'] # =4
    
    elif  row['WSCI'] >= params_V3.iloc[0][4]: #"1 <= WSCI --> 5"
        V3 = params_V3.iloc[1][4]*row['Wv3'] # =5

    return V3

params_V4 = pd.DataFrame(
        {
            "0 - 500": [0,1],
            "500 - 1000": [500,2],
            "1000 - 2500": [1000,3],
            "2500 - 5000": [2500, 4], 
            ">= 5000": [5000,5]
        }
)

def dss3_V4(row):
    if (row['DTR'] >= params_V4.iloc[0][0] and row['DTR'] < params_V4.iloc[0][1]): # "0 <= DTR < 500 --> 1"
        V4 = params_V4.iloc[1][0]*row['Wv4'] # =1    
    
    elif  row['DTR'] >= params_V4.iloc[0][1] and row['DTR']< params_V4.iloc[0][2]: #"500 <= DTR < 1000 --> 2"
        V4 = params_V4.iloc[1][1]*row['Wv4'] # =2
    
    elif  row['DTR'] >= params_V4.iloc[0][2] and row['DTR']< params_V4.iloc[0][3]: #"1000 <= DTR < 2500 --> 3"
        V4 = params_V4.iloc[1][2]*row['Wv4'] # =3

    elif  row['DTR'] >= params_V4.iloc[0][3] and row['DTR']< params_V4.iloc[0][4]: #"2500 <= DTR < 5000 --> 4"
        V4 = params_V4.iloc[1][3]*row['Wv4'] # =4
    
    elif  row['DTR'] >= params_V4.iloc[0][4]: #"5000 <= DTR --> 5"
        V4 = params_V4.iloc[1][4]*row['Wv4'] # =5

    return V4


params_V5 = pd.DataFrame(
        {
            "0 - 1000": [0,1],
            "1000 - 2500": [1000,2],
            "2500 - 5000": [2500,3],
            "5000 - 10000": [5000, 4], 
            ">= 10000": [10000,5]
        }
) 

def dss3_V5(row):
    if (row['MDK'] >= params_V5.iloc[0][0] and row['MDK'] < params_V5.iloc[0][1]): # "0 <= MDK < 1000 --> 1"
        V5 = params_V5.iloc[1][0]*row['Wv5'] # =1    
    
    elif  row['MDK'] >= params_V5.iloc[0][1] and row['MDK']< params_V5.iloc[0][2]: #"1000 <= MDK < 2500 --> 2"
        V5 = params_V5.iloc[1][1]*row['Wv5'] # =2
    
    elif  row['MDK'] >= params_V5.iloc[0][2] and row['MDK']< params_V5.iloc[0][3]: #"2500 <= MDK < 5000 --> 3"
        V5 = params_V5.iloc[1][2]*row['Wv5'] # =3

    elif  row['MDK'] >= params_V5.iloc[0][3] and row['MDK']< params_V5.iloc[0][4]: #"5000 <= MDK < 10000 --> 4"
        V5 = params_V5.iloc[1][3]*row['Wv5'] # =4
    
    elif  row['MDK'] >= params_V5.iloc[0][4]: #"10000 <= MDK --> 5"
        V5 = params_V5.iloc[1][4]*row['Wv5'] # =5

    return V5

def dss3_Vindex(row):
    Vindex = row['V1'] + row['V2'] + row['V3'] + row['V4'] + row['V5']
    return Vindex

def dss3_Risk(row):
    Risk = round(row['Hindex'] * row['Vindex'],0)
    return Risk


# Calculate dss3
def dss3_final (input, status_callback):
    dss3 = pd.read_csv(input,encoding = "UTF-8") # depend on exisitng dss3.csv file 
    # locale.setlocale(locale.LC_NUMERIC, '') 
    # vulnerability = pd.read_csv(vulnerability,encoding = "UTF-8")
    dss3[['P','Qyc','Qc','WQI','Wh1','HH','Wh2','XNM','Wh3','LL','Wh4','SL','Wh5','Wv1','PD','Wv2','WSCI','Wv3','DTR','Wv4','MDK','Wv5']].apply(pd.to_numeric)
   
    # for i in ['QSH', 'QCN', 'QTM-DV','Qi', 'KS','QSP', 'QT','fT','QAN','fAN','QAQ','fAQ','QRE2',\
    #      'QNN','QRE3','Qs','fs','Ws','Qg','fg','Wg','Qr','fr','Wr','Wru','hazard1','hazard2','WSC3']:
    #     if (not is_numeric_dtype(dss3[i])):
    #         print('Kiểm tra dữ liệu đầu vào!')
    #         exit
            
    # dss3[['QSH', 'QCN', 'QTM-DV','Qi', 'KS']].applymap(atof)
    # dss3['QSH'] = dss3['QSH'].map(atof)

    # st.write(dss3.dtypes)
    # locale.setlocale(locale.LC_NUMERIC, '')
    # dss3.applymap(atof)
    i = 0
    steps =13
    ###################### Calculate Hazards
    if 'H1' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'H1', None)  
    dss3['H1'] = dss3.apply(dss3_H1, axis=1) # axis =1 for row
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate H1'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 

    if 'H2' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'H2', None)  
    dss3['H2'] = dss3.apply(dss3_H2, axis=1) # axis =1 for row
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate H2'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 

    
    if 'H3' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'H3', None)  
    dss3['H3'] = dss3.apply(dss3_H3, axis=1) # axis =1 for row
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate H3'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 
    
    if 'H4' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'H4', None)  
    dss3['H4'] = dss3.apply(dss3_H4, axis=1) # axis =1 for row
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate H4'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 

    if 'H5' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'H5', None)  
    dss3['H5'] = dss3.apply(dss3_H5, axis=1) # axis =1 for row
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate H5'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 

    if 'Hindex' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'Hindex', None)  
    dss3['Hindex'] = dss3.apply(dss3_Hindex, axis=1) # axis =1 for row
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate Hindex'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 
    
    ###################### Calculate Vulnerability
    if 'V1' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'V1', None)  
    dss3['V1'] = dss3.apply(dss3_V1, axis=1) # axis =1 for row
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate V1'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 

    
    if 'V2' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'V2', None)  
    dss3['V2'] = dss3.apply(dss3_V2, axis=1) # axis =1 for row
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate V2'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 
    
    if 'V3' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'V3', None)  
    dss3['V3'] = dss3.apply(dss3_V3, axis=1) # axis =1 for row
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate V3'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 


    if 'V4' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'V4', None)  
    dss3['V4'] = dss3.apply(dss3_V4, axis=1) # axis =1 for row
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate V4'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 
    
    if 'V5' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'V5', None)  
    dss3['V5'] = dss3.apply(dss3_V5, axis=1) # axis =1 for row
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate V5'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 
    
    if 'Vindex' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'Vindex', None)  
    dss3['Vindex'] = dss3.apply(dss3_Vindex, axis=1) # axis =1 for row
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate Vindex'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 
    
    if 'Risk' not in dss3.columns:
        dss3.insert(len(dss3.columns) , 'Risk', None)  
    dss3['Risk'] = dss3.apply(dss3_Risk, axis=1) # axis =1 for row
    if 'Risk_Level' not in dss3.columns:
        dss3.insert(len(dss3.columns), 'Risk_Level', '') 
    dss3['Risk_Level']  = dss3['Risk'].map(dss3_level)
    if 'Risk_Color' not in dss3.columns:
        dss3.insert(len(dss3.columns), 'Risk_Color', '') 
    dss3['Risk_Color']  = dss3['Risk'].map(dss3_color)
    
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate Risk'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 

    

    # st.write(hazard.dtypes)
    return dss3