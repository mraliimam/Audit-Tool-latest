import pandas as pd
from zipfile import ZipFile
import os, time

def valueCheck(record2,truFlag,values, parameter):
    if isinstance(record2[parameter], bool) or isinstance(values,bool):  
        # val1 = True if record2[parameter] in (1,True,'True','TRUE','true') else False
        # val2 = True if values in (1,True,'True','TRUE','true') else False
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
    if moName == 'DU5qi' and parameter in ('drbRlcRef', 'srHandlingRef'):
        return False
    # elif moName == 'EUtranCellFDD' and parameter in ('additionalPlmnReservedList', 'prioAdditionalFreqBandList', 'primaryUpperLayerInd', 'mfbiFreqBandIndPrio','frameStartOffset','extGUtranCellRef', 'loopingEndcProtectionEnabled', 'mappingInfoSIB24', 'additionalPlmnList','endcAllowedPlmnList ', 'upperLayerAutoConfEnabled', 'additionalUpperLayerIndList', 'siPeriodicity.siPeriodicitySI8', 'systemInformationBlock24.tReselectionNR', 'systemInformationBlock24.tReselectionNRSfHigh', 'sCellPriority','systemInformationBlock24__tReselectionNRSfMedium','caPrioThreshold','endcAllowedPlmnList__mnc','endcAllowedPlmnList__mncLength','additionalSpectrumEmissionValues','endcDistrProfileRef','frameStartOffset__subFrameOffset', 'mappingInfo__mappingInfoSIB24','endcAllowedPlmnList__mcc', 'siPeriodicity__siPeriodicitySI8'):
    elif moName == 'EUtranCellFDD':
        return False
    elif moName in ('FeatureState','NRCellCU','NRCellDU'):
        return False
    elif moName == 'FieldReplaceableUnit' and parameter == 'isSharedWithExternalMe':
        return False
    elif moName == 'GNBCUUPFunction' and parameter == 'dcDlAggActTime' and len(condition.split(',')) > 1:
        return False
    elif moName == 'GtpuSupervision' and parameter == 'gtpuErrorIndDscp':
        return False
    elif moName == 'ENodeBFunction' and parameter == 's1GtpuEchoDscp':
        return False
    elif moName == 'GUtranSyncSignalFrequency' and parameter == 'band':
        return False
    elif moName == 'NRFrequency' and parameter in ('smtcDuration', 'smtcOffset'):
        return False
    elif moName == 'QciProfileOperatorPredefined' and parameter == 'endcProfileRef':
        return False
    elif moName == 'ReportConfigSearch' and parameter == 'a1a2SearchThresholdRsrp':
        return False
    # elif moName == 'TermPointToENodeB' and parameter == 'administrativeState':
    #     return False
    elif moName == 'TimerProfile' and parameter == 'tRrcConnectionReconfiguration':
        return False
    elif moName == 'UaiProfileUeCfg' and parameter == 'overheatingAssistanceConfig':
        return False
    elif moName == 'UeBbProfileUeCfg' and parameter == 'powerControlUeCfgRef':
        return False
    elif moName == 'UeMeasControl' and parameter in ('waitForStartNRMeas', 'waitForResumeNRMeas','maxMeasNR','maxMeasB1Endc','endcMeasTime','nrB1MeasAtEndcEnabled','rwrToNRAllowed'):
        return False
    elif moName == 'PartitionMapping' and parameter == 'resourceAllocationPolicyR':
        return False
    # elif moName == 'GUtranFreqRelation' and parameter in ('threshXHigh', 'qQualMin', 'threshXHighQ', 'b1ThrRsrpFreqOffset', 'anrMeasOn', 'cellReselectionSubPriority', 'allowedPlmnList__mnc', 'qRxLevMin', 'deriveSsbIndexFromCell', 'pMaxNR', 'threshXLowQ', 'allowedPlmnList__mncLength', 'cellReselectionPriority', 'b1ThrRsrqFreqOffset ', 'connectedModeMobilityPrio', 'qOffsetFreq', 'endcB1MeasPriority', 'threshXLow', 'allowedPlmnList__mcc'):
    #     return False
    # elif moName == 'NRFreqRelation' and parameter in ('pMax', 'qQualMin', 'sIntraSearchQ', 'threshXHighQ', 'qOffsetFreq', 'sIntraSearchP', 'threshXHighP', 'threshXLowP', 'tReselectionNR', 'threshXLowQ', 'cellReselectionSubPriority', 'qRxLevMin', 'cellReselectionPriority'):
    #     return False
    # elif moName == 'EUtranFreqRelation' and parameter in ('qQualMin', 'threshXHighQ', 'presenceAntennaPort1', 'voicePrio', 'tReselectionEUtra', 'threshXLowP', 'threshXHighP', 'allowedMeasBandwidth', 'threshXLowQ', 'anrMeasOn', 'qRxLevMin', 'cellReselectionPriority', 'eUtranFallbackPrioEc', 'pMaxEUtra'):
    #     return False
    elif moName == 'UeGroupSelectionProfile' and parameter in ('ueGroupPriority', 'selectionProbability', 'selectionCriteria', 'ueGroupId'):
        return False
    elif moName == 'McpcPCellProfileUeCfg' and parameter in ('rsrpCandidateA5__threshold1', 'rsrpCritical__hysteresis', 'rsrpCandidateA5__threshold2', 'rsrpCritical__timeToTriggerA1', 'rsrpSearchZonePcOffset__powerClass', 'rsrpCandidateB2__timeToTrigger', 'rsrpCriticalPcOffset__thresholdOffset', 'rsrpCritical__timeToTrigger', 'rsrpCritical__threshold', 'mcpcQuantityList', 'rsrpCandidateB2__hysteresis', 'rsrpSearchZone__threshold', 'rsrpCandidateB2__threshold2EUtra', 'rsrpCandidateA5__timeToTrigger', 'rsrpCandidateB2PcOffset__powerClass', 'rsrpCandidateA5PcOffset__threshold2Offset', 'rsrpSearchTimeRestriction', 'rsrpCandidateB2__threshold1', 'rsrpCandidateA5PcOffset__powerClass', 'rsrpCriticalPcOffset__powerClass', 'rsrpCriticalEnabled', 'lowHighFreqPrioClassification', 'rsrpSearchZone__hysteresis', 'rsrpSearchZonePcOffset__thresholdOffset', 'rsrpSearchZone__timeToTrigger', 'rsrpCandidateA5PcOffset__threshold1Offset', 'rsrpCandidateA5__hysteresis', 'rsrpCandidateB2PcOffset__threshold1Offset', 'rsrpSearchZone__timeToTriggerA1'):
        return False
    elif moName == 'IntraFreqMCCellProfileUeCfg':
        return False
    elif moName == 'McpcPCellNrFreqRelProfileUeCfg' and parameter in ('rsrpCandidateA5Offsets__threshold2Offset', 'ueGroupList', 'inhibitMeasForCellCandidate', 'rsrpCandidateA5Offsets__threshold1Offset'):
        return False
    elif moName == 'UeMCNrFreqRelProfileUeCfg' and parameter in ('ueGroupList', 'connModeAllowedPCell', 'connModePrioPSCell', 'connModeAllowedPSCell', 'connModePrioPCell'):
        return False
    elif moName == 'UeMCEUtranFreqRelProfileUeCfg' and parameter in ('connModeAllowedPCell', 'blindRwrAllowed', 'connModePrioPCell', 'ueGroupList'):
        return False
    elif moName == 'McpcPCellEUtranFreqRelProfileUeCfg':
        return False
    elif moName == 'McfbCellProfileUeCfg':
        return False
    elif moName == 'McpcPSCellNrFreqRelProfileUeCfg':
        return False
    elif moName == 'CgSwitchCfg' and parameter in ('dlCgSwitchMode','dlScgLowQualThresh','dlScgLowQualHyst'):
        return False
    elif moName == 'GNBDUFunction' and parameter in ('caVlanPortRef'):
        return False
    elif moName in ('MimoSleepFunction','DESManagementFunction','DlOuterLoop'):
        return False
    elif moName in ('ReportConfigB1GUtra'):
        return False
    elif moName == 'CellSleepFunction':
        return False
    elif moName == 'ReportConfigB1NR':
        return False
    else:
        return True
    
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
        #print("\nSheet:",moName)
        #print("Error found at Column: ",parameter)
        #print("Layer Name",layer_name)
        #print("Row: ",key2+2)
        #print("Value must be: ",val2," instead of ",val1)
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
        #print("\nSheet:",moName)
        #print("Error found at Column: ",parameter)
        #print("Layer Name",layer_name)
        #print("Row: ",key2+2)
        # if moName == 'FeatureState': 
        #     #print("Value must be: ",values," instead of ",record2['featureState'])
        # else:
        #     #print("Value must be: ",values," instead of ",record2[parameter])

    return flag, shhetFlag, truFlag
    
def DU5qi(condition, parameter, values, record2):
    if conditionCheck(condition, record2['MO']):
        if conditionCheck(values,record2[parameter]):
            return True
        else:
            return False
    return True
        
def NRCELLS(condition, record2):
    conditionSplit = condition.split(',')
    if conditionCheck(conditionSplit[0], record2['MO']):
        exportCondition = record2['MO'].split(',')[-1].split('=')[1][0]
        if conditionSplit[1].split('=')[1][0] == exportCondition:                        
            return True
    return False       
# 8144254000000008002
def EUtranCellFDD(condition,record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[0]
    if conditionCheck(moCondition, record2['MO']):
        exportCondition = record2['MO'].split(',')[-1].split('=')[1]
        starCondition = conditionSplit[1].split('=')[1]
        if starCondition[0] == exportCondition[0] and starCondition[-2:] == exportCondition[-2:]:
            return True
    return False


def CgSwitchCfg(condition,record2): 
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[0]+','+conditionSplit[1]
    if conditionCheck(moCondition, record2['MO']):
        exportCondition = record2['MO'].split(',')[-1].split('=')[1][0]
        if conditionSplit[-1].split('=')[1][0] == exportCondition:                        
            return True
    return False 

def FieldReplaceableUnit(condition,record2):
    conditionSplit = condition.split(',')
    if conditionCheck(conditionSplit[0], record2['MO']):
        exportCondition = record2['MO'].split(',')[-1].split('=')[1].split('-')[0]
        if conditionSplit[1].split('=')[1] == exportCondition:
            return True
    return False

def GNBCUUPFunction(condition,record2):
    conditionSplit = condition.split(',')
    if conditionCheck(conditionSplit[1], record2['MO']):
        exportCondition = record2['MO'].split(',')[-2].split('=')[1][0]
        if conditionSplit[0].split('=')[1][0] == exportCondition:                        
            return True
    return False   

def GUtranSyncSignalFrequency(condition, record2):
    # conditionSplit = condition.split(',')
    # if conditionCheck(conditionSplit[0], record2['MO']):
    exportCondition = record2['MO'].split(',')[-1].split('=')[1].split('-')[0]
    if condition.split('=')[1] == exportCondition:
        return True
    return False    

def NRFrequency(condition,record2):
    exportCondition = record2['MO'].split(',')[-1].split('=')[1].split('-')[0]
    if condition.split('=')[1] == exportCondition:
        return True
    return False    

def ReportConfigSearch(condition,record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[1]+','+conditionSplit[2]
    if conditionCheck(moCondition, record2['MO']):
        exportCondition = record2['MO'].split(',')[-3].split('=')[1][0]
        if conditionSplit[0].split('=')[1][0] == exportCondition:
            return True
    return False

def MimoSleepFunction(condition, record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[0]+','+conditionSplit[-1]
    if conditionCheck(moCondition, record2['MO']):
        exportCondition = record2['MO'].split(',')[-2].split('=')[1]
        starCondition = conditionSplit[1].split('=')[1]
        if starCondition[0] == exportCondition[0] and starCondition[-2:] == exportCondition[-2:]:
            return True
    return False

def ReportConfigB1GUtra(condition, record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[0]+','+conditionSplit[-1]
    if conditionCheck(moCondition, record2['MO']):
        exportCondition = record2['MO'].split(',')[-3].split('=')[1]
        starCondition = conditionSplit[1].split('=')[1]
        if starCondition[0] == exportCondition[0] and starCondition[-2:] == exportCondition[-2:]:
            return True
    return False

def ReportConfigB1NR(condition, record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[1]+','+conditionSplit[2]
    if conditionCheck(moCondition, record2['MO']):
        exportCondition = record2['MO'].split(',')[-3].split('=')[1]
        starCondition = conditionSplit[0].split('=')[1]
        if starCondition[0] == exportCondition[0]:
            return True
    return False


def TimerProfile(condition,record2):
    conditionSplit = condition.split(',')
    if conditionCheck(conditionSplit[0], record2['MO']):
        exportCondition = record2['MO'].split(',')[-1]
        if conditionSplit[1] == exportCondition:
            return True
    return False

def UaiProfileUeCfg(condition,record2):
    if conditionCheck(condition, record2['MO']):
        return True
    return False

def UeMeasControl(condition, record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[0]+','+conditionSplit[2]
    if conditionCheck(moCondition, record2['MO']):
        exportCondition = record2['MO'].split(',')[-2].split('=')[1][0]
        if conditionSplit[1].split('=')[1][0] == exportCondition:
            return True
    return False

def CellSleepFunction(condition,record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[0]+','+conditionSplit[2]
    if conditionCheck(moCondition, record2['MO']) and conditionSplit[1].split('=')[1][0] == record2['MO'].split(',')[-2].split('=')[1][0]:
        return True
    return False


def IntraFreqMCCellProfileUeCfg(condition, record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[1]
    if conditionCheck(moCondition, record2['MO']):
        exportCondition = record2['MO'].split(',')[-2].split('=')[1][0]
        if conditionSplit[0].split('=')[1][0] == exportCondition:
            return True
    return False

def McfbCellProfileUeCfg(condition, record2):
    conditionSplit = condition.split(',')
    moCondition = conditionSplit[1]
    if conditionCheck(moCondition, record2['MO']):
        exportCondition = record2['MO'].split(',')[-2].split('=')[1][0]
        if conditionSplit[0].split('=')[1][0] == exportCondition:
            return True
    return False

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


def process_file(file):
    if file:
        # try:
        # yield f'data: 5\n\n'
        all_sheets = pd.read_excel(file, sheet_name=None)  
        # yield f'data: 10\n\n'

        # all_sheets = logic_sheet
        
        # flag = scripting_main(df, logic_sheet)
        # #print(flag)
        flag = 0
        shhetFlag = 0
        truFlag = 0
        # try:
            # all_sheets = pd.read_excel('ExportXLS_04Apr1007.xlsx', sheet_name=None)

            # df = pd.read_excel('Final Input Sheet (Scripting)_New_V150424.xlsx', sheet_name='Sheet1')

        # keys_list = list(all_sheets.keys())

        # # Convert dictionary keys to a list
        # keys_list = list(all_sheets.keys())

        # # Calculate the indices for 0.3, 0.5, and 0.7 of the length
        # index_03 = int(len(keys_list) * 0.3)
        # index_05 = int(len(keys_list) * 0.5)
        # index_07 = int(len(keys_list) * 0.7)

        # # Ensure indices are within the bounds of the list
        # index_03 = min(max(index_03, 0), len(keys_list) - 1)
        # index_05 = min(max(index_05, 0), len(keys_list) - 1)
        # index_07 = min(max(index_07, 0), len(keys_list) - 1)

        # # Get the keys at these indices
        # key_03 = keys_list[index_03]
        # key_05 = keys_list[index_05]
        # key_07 = keys_list[index_07]

        results = []

        for layer_name in 'LowBand', 'MidBand', 'N41Band':
            df = pd.read_excel('market/static/input_golden_parameter.xlsx', sheet_name=layer_name)

            for key, record in df.iterrows():
                moName = record['MO Class Name']
                condition = record['MO_Bifurcation']
                parameter = record['Parameter']
                values = record['NodeValues']

                
                if moName in all_sheets.keys():
                    # if int(key) <= int(index_03) and int(key) > 50:
                    #     yield f'data: 30\n\n'
                    # elif int(key) >= int(index_03) and int(key) <= int(index_05):
                    #     yield f'data: 55\n\n'
                    # elif int(key) >= int(index_05) and int(key) >= int(index_07):
                    #     yield f'data: 75\n\n'

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
                                if moName in ('DU5qi','GNBDUFunction', 'PartitionMapping'):
                                    if not DU5qi(condition, parameter, values, record2):
                                        flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName in ('NRCellDU', 'NRCellCU'):
                                    if NRCELLS(condition, record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'EUtranCellFDD':
                                    if EUtranCellFDD(condition, record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'FeatureState':
                                    if conditionCheck(condition, record2['MO']):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, 'featureState')
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName,parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'FieldReplaceableUnit':
                                    if FieldReplaceableUnit(condition,record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'GNBCUUPFunction':
                                    if GNBCUUPFunction(condition,record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'GtpuSupervision':
                                    if conditionCheck(condition, record2['MO']):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'ENodeBFunction':
                                    if conditionCheck(condition, record2['MO']):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'GUtranSyncSignalFrequency':
                                    if GUtranSyncSignalFrequency(condition, record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'NRFrequency':
                                    if NRFrequency(condition,record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'QciProfileOperatorPredefined':
                                    if conditionCheck(condition,record2):
                                        if not conditionCheck(values,record2[parameter]):
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'ReportConfigSearch':
                                    if ReportConfigSearch(condition,record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'TimerProfile':
                                    if TimerProfile(condition,record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'UaiProfileUeCfg':
                                    if UaiProfileUeCfg(condition,record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'UeBbProfileUeCfg':
                                    if conditionCheck(condition, record2['MO']):
                                        if not conditionCheck(values, record2[parameter]):
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'UeMeasControl':
                                    if UeMeasControl(condition,record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                # elif moName == 'GUtranFreqRelation':
                                #     if GUtranFreqRelation(condition, record2):
                                #         result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                #         if result:
                                #             flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                # elif moName == 'NRFreqRelation':
                                #     if NRFreqRelation(condition, record2):
                                #         result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                #         if result:
                                #             flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                # elif moName == 'EUtranFreqRelation':
                                #     if EUtranFreqRelation(condition, record2):
                                #         result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                #         if result:
                                #             flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'UeGroupSelectionProfile':
                                    if conditionCheck(condition, record2['MO']):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'McpcPCellProfileUeCfg':
                                    if conditionCheck(condition, record2['MO']):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'IntraFreqMCCellProfileUeCfg':
                                    if parameter in ('betterSpCellTriggerQuantity','endcActionEvalFail','rsrpBetterSCell__hysteresis','rsrpBetterSCell__offset','rsrpBetterSCell__timeToTrigger','rsrpBetterSpCell__hysteresis','rsrpBetterSpCell__offset','rsrpBetterSpCell__timeToTrigger','rsrpSCellCoverage__hysteresis','rsrpSCellCoverage__threshold','rsrpSCellCoverage__timeToTrigger','rsrpSCellCoverage__timeToTriggerA1','sCellCoverageTriggerQuantity','rsrqBetterSpCell__hysteresis','rsrqBetterSpCell__offset','rsrqBetterSpCell__timeToTrigger'):
                                        if conditionCheck(condition, record2['MO']):
                                            result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                            if result:
                                                flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                    else:
                                        if IntraFreqMCCellProfileUeCfg(condition, record2):
                                            result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                            if result:
                                                flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'McpcPCellNrFreqRelProfileUeCfg':
                                    if conditionCheck(condition, record2['MO']):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'UeMCNrFreqRelProfileUeCfg':
                                    if conditionCheck(condition, record2['MO']):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'UeMCEUtranFreqRelProfileUeCfg':
                                    if conditionCheck(condition, record2['MO']):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'McpcPCellEUtranFreqRelProfileUeCfg':
                                    if conditionCheck(condition, record2['MO']):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'McfbCellProfileUeCfg':
                                    if parameter in ('epsFallbackOperation','epsFallbackOperationEm','rsrpCellCandidate__hysteresis','rsrpCellCandidate__threshold','rsrpCellCandidate__timeToTrigger','epsFbAtSessionSetup','epsFbTargetSearchTimer','rejectVoiceIncHoAtEpsFb','rsrpCriticalCoverage__threshold','rsrpCriticalCoverage__hysteresis','rsrpCriticalCoverage__timeToTrigger','rsrpCriticalCoverage__timeToTriggerA1','triggerQuantity'):
                                        if conditionCheck(condition, record2['MO']):
                                            result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                            if result:
                                                flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                    else:
                                        if McfbCellProfileUeCfg(condition, record2):
                                            result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                            if result:
                                                flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                elif moName == 'McpcPSCellNrFreqRelProfileUeCfg':
                                    if conditionCheck(condition, record2['MO']):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)

                                elif moName == 'CgSwitchCfg':
                                    if CgSwitchCfg(condition, record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                
                                elif moName in ('MimoSleepFunction','DESManagementFunction','DlOuterLoop'):
                                    if MimoSleepFunction(condition, record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)

                                elif moName in ('ReportConfigB1GUtra'):
                                    if ReportConfigB1GUtra(condition, record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)

                                elif moName == 'ReportConfigB1NR':
                                    if ReportConfigB1NR(condition, record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                                
                                elif moName == 'CellSleepFunction':
                                    if CellSleepFunction(condition,record2):
                                        result, truFlag, val1, val2 = valueCheck(record2,truFlag,values, parameter)
                                        if result:
                                            flag, shhetFlag, truFlag = resultFunction(all_sheets,truFlag, moName, parameter, values, record2,results,key2,val1,val2,df2, layer_name)
                        
                else:
                    results.append({"MO Name":moName,"Parameter":None,"Row":None,"Base-Line Value":None,"Export Value":None,"Layer Name":layer_name,"Comments":f"Sheet: {moName} not found"})
                    #print(key," sheet name not found..")
            
        with pd.ExcelWriter('New_Sheet.xlsx', engine='openpyxl') as writer:
            # yield f'data: 80\n\n'
            for sheet_name, dfnew in all_sheets.items():
                dfnew.to_excel(writer, sheet_name=sheet_name, index=False)
            # yield f'data: 90\n\n'
            # shhetFlag = 0
        # except Exception as e:
        #     #print(moName,parameter,values)
        #     #print('Exception',e)
        #     return 'Fail'

        if flag == 0:
            #print('\nNo Errors Found..')
            # return False
            yield f'data: 147'
            # raise Exception("An error occurred")
        else:
            # Convert the list of dictionaries to a DataFrame
            df = pd.DataFrame(results)

            # Specify the Excel file name
            excel_file_name = "output.xlsx"

            # Save the DataFrame to Excel
            df.to_excel(excel_file_name, index=False)
            # yield f'data: 90\n\n'
            # return True

            #print(f"\nData has been successfully written to {excel_file_name}.")
        if flag == True:
            output1 = os.path.join(os.getcwd(), 'New_Sheet.xlsx')
            output2 = os.path.join(os.getcwd(), 'output.xlsx')

            zip_filename = 'files.zip'
            with ZipFile(zip_filename, 'w') as zipf:
                zipf.write(output1, os.path.basename(output1))
                zipf.write(output2, os.path.basename(output2))

        return True    
            # yield 'data: 100\n\n'
            # time.sleep(2)
            # yield 'data: 110\n\n'
            # Send the zip file as an attachment
            # return send_file(os.path.join(os.getcwd(), zip_filename), as_attachment=True)
        # else:                
        #     yield f'data: 147'
                # raise Exception("An error occurred")
            # return redirect(url_for('upload_file'))
            
    # except Exception as e:
    #     #print(e)
    #     yield f'data: 147'
    #     # raise Exception(f"An error occurred {e}")