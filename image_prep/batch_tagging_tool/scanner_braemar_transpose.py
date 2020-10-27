import pandas as pd

inputExcelLocation = r"W:\ImageCatalogue_prep\Surveys\2013_01_RVCefasEndeavour_FladenGrounds_CEND0113x\Fladen_Ground_Proforma_Stills_Analysis.xls"
dataSheetPrefix =''
xl = pd.ExcelFile(inputExcelLocation)
inputSheets = [x for x in xl.sheet_names if x.startswith(dataSheetPrefix)]

outXLS  = r"W:\ImageCatalogue_prep\Surveys\2013_01_RVCefasEndeavour_FladenGrounds_CEND0113x\fladen_transposed.xlsx"


pdDict = pd.read_excel(inputExcelLocation,inputSheets,None,None,0)

outputDFlist = []

for key in pdDict:
    outputDFlist.append(pdDict[key].transpose())

megaDF = pd.concat(outputDFlist)
megaDF = megaDF.drop(['Total %'], axis=1)
megaDF.dropna(axis='rows',how='all', inplace=True)
megaDF.to_excel(outXLS)