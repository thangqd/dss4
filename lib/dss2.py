import pandas as pd
from pandas.api.types import is_numeric_dtype
pd.options.mode.copy_on_write = True
import streamlit as st
import locale
from locale import atof

# Calculate dss2
def dss2_final (input, status_callback):
    wqi = pd.read_csv(input) # depend on exisitng dss2.csv file 
    # locale.setlocale(locale.LC_NUMERIC, '') 

    wqi[['QSH', 'QCN', 'QTM-DV','Qi', 'KS','QSP', 'QT','fT','QAN','fAN','QAQ','fAQ','QRE2',\
         'QNN','QRE3','Qs','fs','Ws','Qg','fg','Wg','Qr','fr','Wr','Wru','WSCI1','WSCI2','WSC3']].apply(pd.to_numeric,errors='coerce')
    wqi.replace('NaN',0)
    wqi.replace('',0)


    # wqi[['QSH', 'QCN', 'QTM-DV','Qi', 'KS']].applymap(atof)
    # wqi['QSH'] = wqi['QSH'].map(atof)

    st.write(wqi.dtypes)
    # locale.setlocale(locale.LC_NUMERIC, '')
    # wqi.applymap(atof)
    i = 0
    steps =4 
    if 'Q_RE1' not in wqi.columns:
        wqi.insert(10, 'Q_RE1', None)  
    wqi['Q_RE1']  = round(sum([wqi['QSH'], wqi['QCN'],wqi['QTM-DV']]),0)
    wqi['Q_RE1'] = wqi['Q_RE1'].astype(float)
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate Q_RE1'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 

    if 'Q_SP' not in wqi.columns:
        wqi.insert(11, 'Q_SP', None)  
    wqi['Q_SP']  = wqi['Qi']*wqi['KS']
    wqi['Q_SP'] = wqi['Q_SP'].astype(float)

    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate Q_SP'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 

    if 'Q_RE2' not in wqi.columns:
        wqi.insert(12, 'Q_RE2', None)  
    wqi['Q_RE2']  = round((wqi['Q_RE1']+ (wqi['QT']*wqi['fT']) + (wqi['QAN']*wqi['fAN'])+(wqi['QAQ']*wqi['fAQ'])),0)
    # wqi['Q_RE2']  = round(sum([wqi['QT'],wqi['fT'],wqi['fAN'],wqi['QAQ'],wqi['fAQ']]),0)
    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate Q_RE2'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label) 


    # i+=1
    # percent = int((i/steps)*100)
    # label = str(i)+ '/'+ str(steps)+ '. Calculate WQI_I'    
    # if status_callback:
    #     status_callback(percent,label)
    # else:
    #     print(label) 

    # if 'WQI_II' not in wqi.columns:
    #     wqi.insert(7, 'WQI_II', None)  
    # wqi['WQI_II'] = wqi.apply(dss2_II, axis=1)
    # i+=1
    # percent = int((i/steps)*100)
    # label = str(i)+ '/'+ str(steps)+ '. Calculate WQI_II'    
    # if status_callback:
    #     status_callback(percent,label)
    # else:
    #     print(label) 

    # if 'WQI_III' not in df.columns:
    #     wqi.insert(8, 'WQI_III', None)  
    # wqi['WQI_III'] = wqi.apply(dss2_III, axis=1)
    # i+=1
    # percent = int((i/steps)*100)
    # label = str(i)+ '/'+ str(steps)+ '. Calculate WQI_III'    
    # if status_callback:
    #     status_callback(percent,label)
    # else:
    #     print(label) 
    
    # if 'WQI_IV' not in df.columns:
    #     wqi.insert(9, 'WQI_IV', None)  
    # wqi['WQI_IV'] = wqi.apply(dss2_IV, axis=1)
    # i+=1
    # percent = int((i/steps)*100)
    # label = str(i)+ '/'+ str(steps)+ '. Calculate WQI_IV'    
    # if status_callback:
    #     status_callback(percent,label)
    # else:
    #     print(label) 
    
    # if 'WQI_V' not in df.columns:
    #     wqi.insert(10, 'WQI_V', None)  
    # wqi['WQI_V'] = wqi.apply(dss2_V, axis=1)
    # i+=1
    # percent = int((i/steps)*100)
    # label = str(i)+ '/'+ str(steps)+ '. Calculate WQI_V'    
    # if status_callback:
    #     status_callback(percent,label)
    # else:
    #     print(label) 
    
    # if 'WQI' not in df.columns:
    #     wqi.insert(11, 'WQI', None)     
    # wqi['WQI'] = round((wqi['WQI_I']/100)*(wqi['WQI_II']/100)*(wqi['WQI_III']/100)*wqi['WQI_IV'],0)

    # if 'WQI_Desc' not in df.columns:
    #     wqi.insert(12, 'WQI_Desc', '') 
    # wqi['WQI_Desc']  = wqi['WQI'].map(dss2_desc)

    # if 'WQI_Color' not in df.columns:
    #     wqi.insert(13, 'WQI_Color', '') 
    # wqi['WQI_Color']  = wqi['WQI'].map(dss2_color)

    # if 'WQI_Weight' not in df.columns:
    #     wqi.insert(14, 'WQI_Weight', None) 
    # wqi['WQI_Weight'] = round((wqi['WQI_I']/100)*(wqi['WQI_II']/100)*(wqi['WQI_III']/100)*(pow((wqi['WQI_IV']**2)*wqi['WQI_V'],1/3)),0)

    # if 'WQI_no_V' not in df.columns:
    #     wqi.insert(15, 'WQI_no_V', None)  
    # wqi['WQI_no_V'] = round((wqi['WQI_I']/100)*(wqi['WQI_II']/100)*(wqi['WQI_III']/100)*(pow(wqi['WQI_IV']*wqi['WQI_V'],1/2)),0)

    i+=1
    percent = int((i/steps)*100)
    label = str(i)+ '/'+ str(steps)+ '. Calculate WSCI'    
    if status_callback:
        status_callback(percent,label)
    else:
        print(label)     

    # wqi = wqi.iloc[:,0:11]
    return wqi