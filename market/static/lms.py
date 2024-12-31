import pandas as pd
import os
from zipfile import ZipFile
from market import app

def valueCheck(record2,truFlag,values, parameter):
    if isinstance(record2[parameter], bool) or isinstance(values,bool):  
        val1 = record2[parameter]
        val2 = values
        if record2[parameter] in (1,True,'True','TRUE','true'):
            val1 = True
        elif record2[parameter] in (0,False,'False','FALSE','false'):
            val1 = False

        if values in (1,True,'True','TRUE','true'):
            val2 = True
        elif values in (0,False,'False','FALSE','false'):
            val2 = False

        result = val2 != val1
        truFlag = 1 if result else 0

    elif pd.isna(record2[parameter]) and pd.isna(values):
        val1 = record2[parameter]
        val2 = values
        result = False

    elif pd.isna(record2[parameter]):                      
        if isinstance(values, str) and values.replace(' ','').replace('\n','').upper() == 'BLANK':
            val1 = record2[parameter]
            val2 = values
            result = False
        else:
            val1 = record2[parameter]
            val2 = values
            result = True

    elif isinstance(values, str) and values.replace(' ','').replace('\n','').upper() == 'BLANK' and not pd.isna(record2[parameter]):
        result = False
        val1 = record2[parameter]
        val2 = values
    
    elif isinstance(record2[parameter], int) or isinstance(record2[parameter], float):
        val1 = int(record2[parameter])
        try:
            val2 = int(values)
        except:
            val2 = values
        result = val1 != val2

    elif isinstance(record2[parameter], str) and ('MANAGEDELEMENT' in str(record2[parameter]).upper() or 'GNBDUFUNCTION' in str(record2[parameter]).upper()):
        val1 = set(str(record2[parameter]).split(','))
        val2 = set(str(values).split(','))

        result = not val2.issubset(val1)
        val1 = record2[parameter]
        val2 = values

    
    else:
        val1 = str(record2[parameter]).replace(' ','').replace('\n','').upper()
        val2 = str(values).replace(' ','').replace('\n','').upper()
        result = val2 != val1

    return result, truFlag, val1, val2

def conditionCheck(condition, mo):
    val1 = set(str(condition).split(','))
    val2 = set(str(mo).split(','))
    return val1.issubset(val2)

def moParamterCombo(moName, parameter, condition):

    if moName == 'EUtranFreqRelation':
        return False
    elif moName in ('GUtranFreqRelation', 'NRFreqRelation'):
        return False
    elif moName in ('NRCellCU', 'NRCellDU'):
        return False
    elif moName in ('McpcPCellProfileUeCfg', 'IntraFreqMCCellProfileUeCfg', 'McfbCellProfileUeCfg', 'McpcPSCellProfileUeCfg', 'TrStSaCellProfileUeCfg'):
        return False
    elif moName == 'TrStSaCellProfile':
        return False

def resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name):
    flag = 1
    shhetFlag = 1
    if moName == 'FeatureState':
        newCol = "GPL_"+'featureState'
    else:
        newCol = "GPL_"+parameter

    if truFlag:
        if newCol not in df2.keys():
            if moName == 'FeatureState':                
                df2.insert(df2.columns.get_loc('featureState'), newCol, None)
            else:
                df2.insert(df2.columns.get_loc(parameter), newCol, None)
        df2.at[key2, newCol] = val2
        all_sheets[moName] = df2
        
        results.append({"MO Name":moName,"MO": record2['MO'],"Parameter":parameter,"Row":key2+2,"Base-Line Value":val2,"Export Value":val1,"Layer Name":layer_name,"Comments":f"Value must be: {val2} instead of {val1}"})
        print("\nSheet:",moName)
        print("Error found at Column: ",parameter)
        print("Layer Name",layer_name)
        print("Row: ",key2+2)
        print("Value must be: ",val2," instead of ",val1)
        truFlag = 0
    else:
        if newCol not in df2.keys():
            if moName == 'FeatureState':     
                df2.insert(df2.columns.get_loc('featureState'), newCol, None)
            else:
                df2.insert(df2.columns.get_loc(parameter), newCol, None)
        df2.at[key2, newCol] = values
        all_sheets[moName] = df2
        
        if moName == 'FeatureState':  
            results.append({"MO Name":moName,"MO": record2['MO'],"Parameter":parameter,"Row":key2+2,"Base-Line Value":values,"Export Value":record2['featureState'],"Layer Name":layer_name,"Comments":f"Value must be: {values} instead of {record2['featureState']}"})
        else:
            results.append({"MO Name":moName,"MO": record2['MO'],"Parameter":parameter,"Row":key2+2,"Base-Line Value":values,"Export Value":record2[parameter],"Layer Name":layer_name,"Comments":f"Value must be: {values} instead of {record2[parameter]}"})
        print("\nSheet:",moName)
        print("Error found at Column: ",parameter)
        print("Layer Name",layer_name)
        print("Row: ",key2+2)
        if moName == 'FeatureState': 
            print("Value must be: ",values," instead of ",record2['featureState'])
        else:
            print("Value must be: ",values," instead of ",record2[parameter])

    return flag, shhetFlag, truFlag

def find_mecontext_value(mo_string, letter):
    # Split the string by commas to get individual key-value pairs
    if letter == None:
        return False
    
    key_value_pairs = mo_string.split(',')
    
    # Iterate through each key-value pair
    for pair in key_value_pairs:
        # Split the pair by '=' to separate key and value
        key, value = pair.split('=')
        
        # Check if the key is 'MeContext'
        if key == 'MeContext':
            # Check if the value ends with 'H', '1', or '2'
            if value.endswith(letter):
                return True
            else:
                return False
    return False

def check_mecontext_ends_with_3(df2):
    letter = None
    found = False
    for key ,record2 in df2.iterrows():
        mo_string = record2['MO']
        key_value_pairs = mo_string.split(',')
        for pair in key_value_pairs:
            key, value = pair.split('=')
            if key == 'MeContext' and value.endswith('3'):
                # return False
                found = True
            if key == 'MeContext' and value[-1].isalpha():
                letter = value[-1]

    return found,letter

def EUtranFreqRelation(condition, record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[0]+','+conditionSplit[-1]
    if '*' in condition:
        return GUtranFreqRelation(condition, record2)
    else:
        if conditionCheck(moCondition, record2['MO']):
            exportCondition = record2['MO'].split(',')[-2].split('=')[1][0]
            if conditionSplit[1].split('=')[1][0] == exportCondition:
                return True
        return False

def GUtranFreqRelation(condition, record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[0]+','+conditionSplit[-1]
    if conditionCheck(moCondition, record2['MO']):
        exportCondition = record2['MO'].split(',')[-3].split('=')[1]
        starCondition = conditionSplit[1].split('=')[1]
        if starCondition[0] == exportCondition[0] and starCondition[-2:] == exportCondition[-2:]:
            return True
    return False

def McpcPCellProfileUeCfg(condition, record2, parameter):
    if '*' in condition:
        conditionSplit = condition.split(',')
        moCondition = conditionSplit[0]+','+conditionSplit[1]+','+conditionSplit[-1]
        if conditionCheck(moCondition, record2['MO']):
            exportCondition = record2['MO'].split(',')[-2].split('=')[1]
            starCondition = conditionSplit[2].split('=')[1]
            if starCondition[0] == exportCondition[0] and starCondition[-2:] == exportCondition[-2:]:
                return True
        return False
    else:
        return conditionCheck(condition, record2[parameter])
    
def NRFreqRelation(condition, record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[0]+','+conditionSplit[1] if len(conditionSplit) == 3 else conditionSplit[0]
    if conditionCheck(moCondition, record2['MO']):
        exportCondition = record2['MO'].split(',')[-1].split('=')[1]
        starCondition = conditionSplit[2].split('=')[1]
        if starCondition[0] == exportCondition[0] and starCondition[-2:] == exportCondition[-2:]:
            return True
    return False

def TrStSaCellProfile(condition, record2):
    if '*' in condition:
        conditionSplit = condition.split(',')
        moCondition = conditionSplit[0]+','+conditionSplit[1]
        if conditionCheck(moCondition, record2['MO']):
            exportCondition = record2['MO'].split(',')[-1].split('=')[1]
            starCondition = conditionSplit[2].split('=')[1]
            if starCondition[0] == exportCondition[0] and starCondition[-2:] == exportCondition[-2:]:
                return True
        return False
    else:
        return conditionCheck(condition, record2[parameter])

def NRCellCU(condition, record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[0]
    if conditionCheck(moCondition, record2['MO']):
        exportCondition = record2['MO'].split(',')[-1].split('=')[1]
        starCondition = conditionSplit[1].split('=')[1]
        if starCondition[0] == exportCondition[0] and starCondition[-2:] == exportCondition[-2:]:
            return True
    return False

def lmsFile(file):
    print(f"Starting process_file with {file}")
    if file:
        all_sheets = pd.read_excel(file, sheet_name=None)
        flag = 0
        shhetFlag = 0
        truFlag = 0
        results = []
        for layer_name in 'LowBand', 'MidBand', 'N41Band':
            # df = pd.read_excel('LMS Input.xlsx', sheet_name=layer_name)
            df = pd.read_excel('market/static/lms_input.xlsx', sheet_name=layer_name)
            # df = pd.read_excel('modified_file.xlsx', sheet_name=layer_name)

            for key, record in df.iterrows():
                moName = record['MO Class Name']
                condition = record['MO_Bifurcation']
                parameter = record['Parameter']
                values = record['NodeValues']

                if not isinstance(moName, str):
                    continue

                if moName in all_sheets.keys():
                    df2 = all_sheets[moName]
                    layer_Pair_Exist, letterID = check_mecontext_ends_with_3(df2)

                    if parameter in df2.keys() or moName == 'FeatureState':
                        for key2, record2 in df2.iterrows():
                            if layer_name == 'LowBand':
                                if find_mecontext_value(record2['MO'],letterID):
                                    pass
                                else:
                                    continue
                            elif layer_name == 'N41Band':
                                if find_mecontext_value(record2['MO'],'2'):
                                    pass
                                else:
                                    continue
                            else:
                                if find_mecontext_value(record2['MO'],letterID if not layer_Pair_Exist else '3'):
                                    pass
                                else:
                                    continue
                                
                            if moParamterCombo(moName,parameter,condition):                       
                                if conditionCheck(condition, record2['MO']):                                
                                    result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                    if result:
                                        flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                            else:
                                if moName == 'EUtranFreqRelation':
                                    if EUtranFreqRelation(condition, record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName in ('GUtranFreqRelation'):
                                    if GUtranFreqRelation(condition, record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName in ('NRCellCU', 'NRCellDU'):
                                    if NRCellCU(condition, record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName in ('McpcPCellProfileUeCfg', 'IntraFreqMCCellProfileUeCfg', 'McfbCellProfileUeCfg', 'McpcPSCellProfileUeCfg', 'TrStSaCellProfileUeCfg'):
                                    if McpcPCellProfileUeCfg(condition, record2, parameter):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'NRFreqRelation':
                                    if NRFreqRelation(condition, record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)

                else:
                    results.append({"MO Name":moName,"Parameter":None,"Row":None,"Base-Line Value":None,"Export Value":None,"Layer Name":layer_name,"Comments":f"Sheet: {moName} not found"})
                    print(moName,", ",parameter," sheet name not found..")
        
        with pd.ExcelWriter(os.path.join(app.config['UPLOAD_FOLDER'], 'New_Sheet.xlsx'), engine='openpyxl') as writer:
            for sheet_name, dfnew in all_sheets.items():
                dfnew.to_excel(writer, sheet_name=sheet_name, index=False)

        if flag == 0:
            print('\nNo Errors Found..')
            return False
        else:
            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(results)

            # Specify the Excel file name
            excel_file_name = os.path.join(app.config['UPLOAD_FOLDER'], "output.xlsx")

            # Save the DataFrame to Excel
            df.to_excel(excel_file_name, index=False)
        if flag == True:
            output1 = os.path.join(app.config['UPLOAD_FOLDER'], 'New_Sheet.xlsx')
            output2 = os.path.join(app.config['UPLOAD_FOLDER'], 'output.xlsx')

            zip_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'files.zip')
            with ZipFile(zip_filename, 'w') as zipf:
                zipf.write(output1, os.path.basename(output1))
                zipf.write(output2, os.path.basename(output2))

        return True    
    else:
        return False