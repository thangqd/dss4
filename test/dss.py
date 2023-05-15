import pandas as pd
from pandas.api.types import is_numeric_dtype

# Calculate DSS1
def dss1 (input, fromdate, todate):
    df = pd.read_csv(input,skiprows=[1]) # based on exisitng dss1.csv file               
    df["Date"] =  pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.date # convert Date field to  
    # wqi = df.loc[fromdate:todate]
    # wqi = df[(df['Date'] >= fromdate) & (df['Date'] < todate)]
    wqi = df
    # added_column = ['WQI_I', 'WQI_II', 'WQI_III', 'WQI_IV', 'WQI_V', 'WQI']
    
    wqi.insert(6, 'WQI_I', None)   
    wqi['WQI_I'] = wqi.apply(dss1_I, axis=1)

    wqi.insert(7, 'WQI_II', None)
    wqi['WQI_II'] = wqi.apply(dss1_II, axis=1)

    wqi.insert(8, 'WQI_III', None)
    wqi['WQI_III'] = wqi.apply(dss1_III, axis=1)

    wqi = wqi.iloc[:,0:11]
    return wqi

params_I = pd.DataFrame(
        {
            "1": [5.5,50],
            "2": [6,100],
            "3": [8.5,100], 
            "4": [9,50]
        }
)

params_II = pd.DataFrame(
        {
            "Aldrin": [0.1],
            "BHC": [0.02],
            "Dieldrin": [0.1], 
            "DDTs": [1],
            "Heptachlor": [0.2],
            "Heptachlorepoxide": [0.2]
        }
)

#Calculate DSS1_I
def dss1_I(row):
    result = -1
    if (row['pH'] < params_I.iloc[0][0]) or (row['pH'] >params_I.iloc[0][-1]): # pH < 5.5 or pH > 9
        result = 10
    elif (row['pH'] >= params_I.iloc[0][0]) &  (row['pH'] <params_I.iloc[0][1]): # 5.5 <= pH < 6
        result = params_I.iloc[1][0]+ (params_I.iloc[1][1] - params_I.iloc[1][0])/(params_I.iloc[0][1]-params_I.iloc[0][0])*(row['pH']-params_I.iloc[0][0])
    elif (row['pH'] >= params_I.iloc[0][1]) &  (row['pH'] <params_I.iloc[0][2]): # 6 <= pH < 8.5
        result = 100
    elif (row['pH'] >= params_I.iloc[0][2]) &  (row['pH'] <params_I.iloc[0][3]):  # 8.5 <= pH <=9
        result = params_I.iloc[1][3]+ (params_I.iloc[1][2]-params_I.iloc[1][3])/(params_I.iloc[0][3]-params_I.iloc[0][2])*(params_I.iloc[0][3]-row['pH'])  
    return result

def dss1_II(row):
    result = -1
    if (row['Aldrin'] <= params_II.iloc[0][0]): # Aldrin <= 0.1
        Aldrin = 100
    else: Aldrin = 10
    if (row['BHC'] <= params_II.iloc[0][1]): # Aldrin <= 0.02
        BHC = 100
    else: BHC = 10
    if (row['Dieldrin'] <= params_II.iloc[0][2]): # Dieldrin <= 0.1
        Dieldrin = 100
    else: Dieldrin = 10
    if (row['DDTs'] <= params_II.iloc[0][3]): # DDTs <= 1
        DDTs = 100
    else: DDTs = 10
    if (row['Heptachlor'] <= params_II.iloc[0][4]): # Heptachlor <= 0.2
        Heptachlor = 100
    else: Heptachlor = 10
    if (row['Heptachlorepoxide'] <= params_II.iloc[0][5]): # Heptachlorepoxide <= 0.2
        Heptachlorepoxide = 100
    else: Heptachlorepoxide = 10
    result = round((Aldrin + BHC + Dieldrin + DDTs + Heptachlor + Heptachlorepoxide)/6,2)
    return result

# As,Cd,Pb,Cr6, Cu, Zn
params_III_As = pd.DataFrame(
        {
            "0.01": [0.01,100],
            "0.02": [0.02,75],
            "0.05": [0.05,50], 
            "0.1": [0.1,25],
            ">0.1": [0.1,10] # > 0.1
        }
)

params_III_Cd = pd.DataFrame(
        {
            "<0.005": [0.005,100],
            "0.005": [0.005,75],
            "0.008": [0.008,50], 
            "0.01": [0.01,25],
            ">=0.1": [0.1,10] # > 0.1
        }
)


params_III_Pb = pd.DataFrame(
        {
            "<0.02": [0.02,100],
            "0.02": [0.02,75],
            "0.04": [0.04,50], 
            "0.005": [0.05,25],
            ">=0.5": [0.5,10] # > 0.1
        }
)

params_III_Cr6 = pd.DataFrame(
        {
            "<0.01": [0.01,100],
            "0.02": [0.02,75],
            "0.04": [0.04,50], 
            "0.005": [0.05,25],
            ">=0.1": [0.1,10] # > 0.1
        }
)

params_III_Cu = pd.DataFrame(
        {
            "<0.1": [0.1,100],
            "0.2": [0.2,75],
            "0.5": [0.5,50], 
            "1.0": [1.0,25],
            ">=2": [2.0,10] # > 0.1
        }
)

params_III_Zn = pd.DataFrame(
        {
            "<0.5": [0.5,100],
            "1": [1.0,75],
            "1.5": [1.5,50], 
            "2.0": [2.0,25],
            ">=3": [3.0,10] # > 0.1
        }
)

params_III_Hg = pd.DataFrame(
        {
            "<0.001": [0.001,100],
            "0.001": [0.001,75],
            "0.0015": [0.0015,50], 
            "0.002": [0.002,25],
            ">=0.01": [3.0,10] # > 0.1
        }
)


def dss1_III(row):
    #As
    result = -1
    As=Cd=Pb=Cr6=Cu=Zn=Hg = 0
    if row['As'] <= params_III_As.iloc[0][0]: # 0.01
        As = params_III_As.iloc[1][0] # 100
    elif row['As'] >  params_III_As.iloc[0][0] and  row['As'] < params_III_As.iloc[0][1]: # 0.01 < As  < 0.02
        As = params_III_As.iloc[1][1]+ (params_III_As.iloc[1][0]-params_III_As.iloc[1][1])/(params_III_As.iloc[0][1]-params_III_As.iloc[0][0])*(params_III_As.iloc[0][1]-row['As'])    
    
    elif row['As'] == params_III_As.iloc[0][1]: # 0.02
        As = params_III_As.iloc[1][1] # 75
    elif row['As'] > params_III_As.iloc[0][1] and row['As'] <  params_III_As.iloc[0][2]: # 0.02 < As  < 0.05
        As = params_III_As.iloc[1][2]+ (params_III_As.iloc[1][1]-params_III_As.iloc[1][2])/(params_III_As.iloc[0][2]-params_III_As.iloc[0][1])*(params_III_As.iloc[0][2]-row['As'])    
    
    elif row['As'] == params_III_As.iloc[0][2]: # 0.05
        As = params_III_As.iloc[1][2] # 50
    elif row['As'] > params_III_As.iloc[0][2] and row['As'] <  params_III_As.iloc[0][3]: # 0.05 < As  < 0.1
        As = params_III_As.iloc[1][3]+ (params_III_As.iloc[1][2]-params_III_As.iloc[1][3])/(params_III_As.iloc[0][3]-params_III_As.iloc[0][2])*(params_III_As.iloc[0][3]-row['As'])    

    elif row['As'] == params_III_As.iloc[0][3]: # = 0.1
        As = params_III_As.iloc[1][3] # 25   
    elif (row['As'] > params_III_As.iloc[0][4]): #> 0.1
        As = params_III_As.iloc[1][4] # =10
    
    #Cd
    if row['Cd'] < params_III_Cd.iloc[0][0]: # < 0.005
        Cd = params_III_Cd.iloc[1][0] # 100 

    elif row['Cd'] == params_III_Cd.iloc[0][1]: # == 0.005
        Cd = params_III_Cd.iloc[1][1] # 75
    elif row['Cd'] > params_III_Cd.iloc[0][1] and row['Cd'] <  params_III_Cd.iloc[0][2]: # 0.005 < Cd  < 0.008
        Cd = params_III_Cd.iloc[1][2]+ (params_III_Cd.iloc[1][1]-params_III_Cd.iloc[1][2])/(params_III_Cd.iloc[0][2]-params_III_Cd.iloc[0][1])*(params_III_Cd.iloc[0][2]-row['Cd'])    
    
    elif row['Cd'] == params_III_As.iloc[0][2]: # 0.008
        Cd = params_III_Cd.iloc[1][2] # 50
    elif row['Cd'] > params_III_Cd.iloc[0][2] and row['Cd'] <  params_III_Cd.iloc[0][3]: # 0.008 < Cd  < 0.01
        Cd = params_III_Cd.iloc[1][3]+ (params_III_As.iloc[1][2]-params_III_Cd.iloc[1][3])/(params_III_Cd.iloc[0][3]-params_III_Cd.iloc[0][2])*(params_III_Cd.iloc[0][3]-row['Cd'])    

    elif row['Cd'] == params_III_Cd.iloc[0][3]: # = 0.01
        Cd = params_III_Cd.iloc[1][3] # 25   
    elif (row['Cd'] > params_III_Cd.iloc[0][4]): #> 0.1
        Cd = params_III_Cd.iloc[1][4] # =10    
    
    #Pb
    if row['Pb'] < params_III_Pb.iloc[0][0]: # < 0.005
        Pb = params_III_Pb.iloc[1][0] # 100 

    elif row['Pb'] == params_III_Pb.iloc[0][1]: # == 0.005
        Pb = params_III_Pb.iloc[1][1] # 75
    elif row['Pb'] > params_III_Pb.iloc[0][1] and row['Pb'] <  params_III_Pb.iloc[0][2]: # 0.005 < Pb  < 0.008
        Pb = params_III_Pb.iloc[1][2]+ (params_III_Pb.iloc[1][1]-params_III_Pb.iloc[1][2])/(params_III_Pb.iloc[0][2]-params_III_Pb.iloc[0][1])*(params_III_Pb.iloc[0][2]-row['Pb'])    
    
    elif row['Pb'] == params_III_As.iloc[0][2]: # 0.008
        Pb = params_III_Pb.iloc[1][2] # 50
    elif row['Pb'] > params_III_Pb.iloc[0][2] and row['Pb'] <  params_III_Pb.iloc[0][3]: # 0.008 < Pb  < 0.01
        Pb = params_III_Pb.iloc[1][3]+ (params_III_As.iloc[1][2]-params_III_Pb.iloc[1][3])/(params_III_Pb.iloc[0][3]-params_III_Pb.iloc[0][2])*(params_III_Pb.iloc[0][3]-row['Pb'])    

    elif row['Pb'] == params_III_Pb.iloc[0][3]: # = 0.01
        Pb = params_III_Pb.iloc[1][3] # 25   
    elif (row['Pb'] > params_III_Pb.iloc[0][4]): #> 0.1
        Pb = params_III_Pb.iloc[1][4] # =10    


    #Cr6
    if row['Cr6'] < params_III_Cr6.iloc[0][0]: # < 0.005
        Cr6 = params_III_Cr6.iloc[1][0] # 100 

    elif row['Cr6'] == params_III_Cr6.iloc[0][1]: # == 0.005
        Cr6 = params_III_Cr6.iloc[1][1] # 75
    elif row['Cr6'] > params_III_Cr6.iloc[0][1] and row['Cr6'] <  params_III_Cr6.iloc[0][2]: # 0.005 < Cr6  < 0.008
        Cr6 = params_III_Cr6.iloc[1][2]+ (params_III_Cr6.iloc[1][1]-params_III_Cr6.iloc[1][2])/(params_III_Cr6.iloc[0][2]-params_III_Cr6.iloc[0][1])*(params_III_Cr6.iloc[0][2]-row['Cr6'])    
    
    elif row['Cr6'] == params_III_As.iloc[0][2]: # 0.008
        Cr6 = params_III_Cr6.iloc[1][2] # 50
    elif row['Cr6'] > params_III_Cr6.iloc[0][2] and row['Cr6'] <  params_III_Cr6.iloc[0][3]: # 0.008 < Cr6  < 0.01
        Cr6 = params_III_Cr6.iloc[1][3]+ (params_III_As.iloc[1][2]-params_III_Cr6.iloc[1][3])/(params_III_Cr6.iloc[0][3]-params_III_Cr6.iloc[0][2])*(params_III_Cr6.iloc[0][3]-row['Cr6'])    

    elif row['Cr6'] == params_III_Cr6.iloc[0][3]: # = 0.01
        Cr6 = params_III_Cr6.iloc[1][3] # 25   
    elif (row['Cr6'] > params_III_Cr6.iloc[0][4]): #> 0.1
        Cr6 = params_III_Cr6.iloc[1][4] # =10    

      #Cu
    if row['Cu'] < params_III_Cu.iloc[0][0]: # < 0.005
        Cu = params_III_Cu.iloc[1][0] # 100 

    elif row['Cu'] == params_III_Cu.iloc[0][1]: # == 0.005
        Cu = params_III_Cu.iloc[1][1] # 75
    elif row['Cu'] > params_III_Cu.iloc[0][1] and row['Cu'] <  params_III_Cu.iloc[0][2]: # 0.005 < Cu  < 0.008
        Cu = params_III_Cu.iloc[1][2]+ (params_III_Cu.iloc[1][1]-params_III_Cu.iloc[1][2])/(params_III_Cu.iloc[0][2]-params_III_Cu.iloc[0][1])*(params_III_Cu.iloc[0][2]-row['Cu'])    
    
    elif row['Cu'] == params_III_As.iloc[0][2]: # 0.008
        Cu = params_III_Cu.iloc[1][2] # 50
    elif row['Cu'] > params_III_Cu.iloc[0][2] and row['Cu'] <  params_III_Cu.iloc[0][3]: # 0.008 < Cu  < 0.01
        Cu = params_III_Cu.iloc[1][3]+ (params_III_As.iloc[1][2]-params_III_Cu.iloc[1][3])/(params_III_Cu.iloc[0][3]-params_III_Cu.iloc[0][2])*(params_III_Cu.iloc[0][3]-row['Cu'])    

    elif row['Cu'] == params_III_Cu.iloc[0][3]: # = 0.01
        Cu = params_III_Cu.iloc[1][3] # 25   
    elif (row['Cu'] > params_III_Cu.iloc[0][4]): #> 0.1
        Cu = params_III_Cu.iloc[1][4] # =10    
    
      #Zn
    if row['Zn'] < params_III_Zn.iloc[0][0]: # < 0.005
        Zn = params_III_Zn.iloc[1][0] # 100 

    elif row['Zn'] == params_III_Zn.iloc[0][1]: # == 0.005
        Zn = params_III_Zn.iloc[1][1] # 75
    elif row['Zn'] > params_III_Zn.iloc[0][1] and row['Zn'] <  params_III_Zn.iloc[0][2]: # 0.005 < Zn  < 0.008
        Zn = params_III_Zn.iloc[1][2]+ (params_III_Zn.iloc[1][1]-params_III_Zn.iloc[1][2])/(params_III_Zn.iloc[0][2]-params_III_Zn.iloc[0][1])*(params_III_Zn.iloc[0][2]-row['Zn'])    
    
    elif row['Zn'] == params_III_As.iloc[0][2]: # 0.008
        Zn = params_III_Zn.iloc[1][2] # 50
    elif row['Zn'] > params_III_Zn.iloc[0][2] and row['Zn'] <  params_III_Zn.iloc[0][3]: # 0.008 < Zn  < 0.01
        Zn = params_III_Zn.iloc[1][3]+ (params_III_As.iloc[1][2]-params_III_Zn.iloc[1][3])/(params_III_Zn.iloc[0][3]-params_III_Zn.iloc[0][2])*(params_III_Zn.iloc[0][3]-row['Zn'])    

    elif row['Zn'] == params_III_Zn.iloc[0][3]: # = 0.01
        Zn = params_III_Zn.iloc[1][3] # 25   
    elif (row['Zn'] > params_III_Zn.iloc[0][4]): #> 0.1
        Zn = params_III_Zn.iloc[1][4] # =10    

    #Hg
    if row['Hg'] < params_III_Hg.iloc[0][0]: # < 0.005
        Hg = params_III_Hg.iloc[1][0] # 100 

    elif row['Hg'] == params_III_Hg.iloc[0][1]: # == 0.005
        Hg = params_III_Hg.iloc[1][1] # 75
    elif row['Hg'] > params_III_Hg.iloc[0][1] and row['Hg'] <  params_III_Hg.iloc[0][2]: # 0.005 < Hg  < 0.008
        Hg = params_III_Hg.iloc[1][2]+ (params_III_Hg.iloc[1][1]-params_III_Hg.iloc[1][2])/(params_III_Hg.iloc[0][2]-params_III_Hg.iloc[0][1])*(params_III_Hg.iloc[0][2]-row['Hg'])    
    
    elif row['Hg'] == params_III_As.iloc[0][2]: # 0.008
        Hg = params_III_Hg.iloc[1][2] # 50
    elif row['Hg'] > params_III_Hg.iloc[0][2] and row['Hg'] <  params_III_Hg.iloc[0][3]: # 0.008 < Hg  < 0.01
        Hg = params_III_Hg.iloc[1][3]+ (params_III_As.iloc[1][2]-params_III_Hg.iloc[1][3])/(params_III_Hg.iloc[0][3]-params_III_Hg.iloc[0][2])*(params_III_Hg.iloc[0][3]-row['Hg'])    

    elif row['Hg'] == params_III_Hg.iloc[0][3]: # = 0.01
        Hg = params_III_Hg.iloc[1][3] # 25   
    elif (row['Hg'] > params_III_Hg.iloc[0][4]): #> 0.1
        Hg = params_III_Hg.iloc[1][4] # =10    

    result = round((As+Cd+Pb+Cr6+Cu+Zn+Hg)/7,2)
    return result

def dss1_IV(row):
    result = -1