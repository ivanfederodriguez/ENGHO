import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.weightstats import DescrStatsW
# Cargar los datos
import requests
from io import BytesIO
from zipfile import ZipFile

# URL del archivo zip
url = "https://www.indec.gob.ar/ftp/cuadros/menusuperior/engho/engho2018_hogares.zip"

# Descargar el contenido del archivo zip
response = requests.get(url)
zip_file = ZipFile(BytesIO(response.content))

# Obtener la lista de archivos en el zip para encontrar el archivo .txt
files = zip_file.namelist()

# Encontrar el nombre del archivo .txt
txt_file_name = [file for file in files if file.endswith('.txt')][0]

# Leer el contenido del archivo .txt en un DataFrame de pandas
with zip_file.open(txt_file_name) as file:
    data = pd.read_csv(file, delimiter='|')
#filtrado
data_nea=data[data['region']==4]
n=len(data_nea)
#asumo que todos los que están como float 64 son valores continuos y los int64 son categoricos
fdata_nea=data_nea.drop(['region','provincia','id','gastotpc','gc09_01','gc09_02','gc09_03','gc09_04','gc09_05','gc09_06','gc09_07','gc09_08','gc09_09','ingpch','hacina'],axis=1)
#mientras tanto, cuando sean necesarias las sacamos del filtrado a las distintas categorias de gastos
#/////////////////////////////////////////////
#variables aleatorias, distribución
#proprauto
#convierto en binaria tiene auto:1, no:0
fdata_nea['propauto'] = fdata_nea['propauto'].apply(lambda x: 1 if x in [2, 3] else 0)
#calculos/////////////////////////////////////////
m_propauto= (fdata_nea['propauto']*data_nea['pondera']).mean()
dvp1=DescrStatsW(fdata_nea['propauto'], weights=fdata_nea['pondera'])

#regten regimen de tenencia
fdata_nea['regten1']= fdata_nea['regten'].apply(lambda x: 1 if x==1 else 0)
fdata_nea['regten2']= fdata_nea['regten'].apply(lambda x: 1 if x==2 else 0)
fdata_nea['regten3']= fdata_nea['regten'].apply(lambda x: 1 if x==3 else 0)
#calculos/////////////////////////////////////////
mreg1= (fdata_nea['regten1']*data_nea['pondera']).mean()
mreg2= (fdata_nea['regten2']*data_nea['pondera']).mean()
mreg3= (fdata_nea['regten3']*data_nea['pondera']).mean()
dvp1= DescrStatsW(fdata_nea['regten1'], weights=fdata_nea['pondera'])
dvp2= DescrStatsW(fdata_nea['regten2'], weights=fdata_nea['pondera'])
dvp3= DescrStatsW(fdata_nea['regten3'], weights=fdata_nea['pondera'])
#fdata_nea[['regten1','regten2','regten3']]
#como descompuse regten, la deshago, lo mismo p=voy a hacer a partir de ahora
fdata_nea=fdata_nea.drop(['regten'],axis=1)


#jniveled
fdata_nea['prim']= fdata_nea['jniveled'].apply(lambda x: 1 if x==1 else 0)
fdata_nea['sec']= fdata_nea['jniveled'].apply(lambda x: 1 if x==3 else 0)
fdata_nea['univ']= fdata_nea['jniveled'].apply(lambda x: 1 if x==5 else 0)
fdata_nea['noed/noans']= fdata_nea['jniveled'].apply(lambda x: 1 if x==7 else 0)
#calculos/////////////////////////////////////////
mprim= (fdata_nea['prim']*data_nea['pondera']).mean()
msec= (fdata_nea['sec']*data_nea['pondera']).mean()
muniv= (fdata_nea['univ']*data_nea['pondera']).mean()
dvprim= DescrStatsW(fdata_nea['prim'], weights=fdata_nea['pondera'])
dvsec= DescrStatsW(fdata_nea['sec'], weights=fdata_nea['pondera'])
dvuniv= DescrStatsW(fdata_nea['univ'], weights=fdata_nea['pondera'])
#//////////////////////////////////////////
fdata_nea=fdata_nea.drop(['jniveled'],axis=1)


fdata_nea['jsexo']=fdata_nea['jsexo']-1
#calculos////////////////////////////////
mjsexo= (fdata_nea['jsexo']*data_nea['pondera']).mean()
dvpjsexo= DescrStatsW(fdata_nea['jsexo'], weights=fdata_nea['pondera'])


fdata_nea['jedad_agrup']=fdata_nea['jedad_agrup']-1 #resumen
#calculos////////////////////////////////
mjedad_agrup= (fdata_nea['jedad_agrup']*data_nea['pondera']).mean()
dvpjedad_agrup= DescrStatsW(fdata_nea['jedad_agrup'], weights=fdata_nea['pondera'])


fdata_nea['casado']=fdata_nea['jsitconyugal'].apply(lambda x: 1 if x in [1, 2] else 0) #no se que tanto afectaran pensiones y esas cosas, habria que reconsiderar
#calculos////////////////////////////////
mcasado= (fdata_nea['casado']*data_nea['pondera']).mean()
dvcasado= DescrStatsW(fdata_nea['casado'], weights=fdata_nea['pondera'])


fdata_nea['jestado']=fdata_nea['jestado'].apply(lambda x: 1 if x==1 else 0)#resumen
#calculos////////////////////////////////
mjestado= (fdata_nea['jestado']*data_nea['pondera']).mean()
dvpjestado= DescrStatsW(fdata_nea['jestado'], weights=fdata_nea['pondera'])


fdata_nea['as']=fdata_nea['jocupengh'].apply(lambda x: 1 if x==1 else 0)
#calculos/////////////////////////////// 
mas= (fdata_nea['as']*data_nea['pondera']).mean()
dvas= DescrStatsW(fdata_nea['as'], weights=fdata_nea['pondera'])


fdata_nea['soc_jur']=fdata_nea['jocupengh'].apply(lambda x: 1 if x in [2,5] else 0)
#calculos////////////////////////////////
msoc_jur= (fdata_nea['soc_jur']*data_nea['pondera']).mean()
dvsoc_jur= DescrStatsW(fdata_nea['soc_jur'], weights=fdata_nea['pondera'])


''''
fdata_nea['propia_soc_jur']=fdata_nea['jocupengh'].apply(lambda x: 1 if x==2 else 0)
#calculos////////////////////////////////
mpropia_soc_jur= (fdata_nea['propia_soc_jur']*data_nea['pondera']).mean()
dvpropia_soc_jur= DescrStatsW(fdata_nea['propia_soc_jur'], weights=fdata_nea['pondera'])


fdata_nea['socio_soc_jur']=fdata_nea['jocupengh'].apply(lambda x: 1 if x==4 else 0)
#calculos////////////////////////////////
msocio_soc_jur= (fdata_nea['socio_soc_jur']*data_nea['pondera']).mean()
dvsocio_soc_jur= DescrStatsW(fdata_nea['socio_soc_jur'], weights=fdata_nea['pondera'])
#//////////////////////////////////////////
fdata_nea=fdata_nea.drop(['jocupengh'],axis=1)
'''


fdata_nea['jpercept']=fdata_nea['jpercept']-1
#calculos////////////////////////////////
mjpercept=(fdata_nea['jpercept']*data_nea['pondera']).mean()
dvpjpercept= DescrStatsW(fdata_nea['jpercept'], weights=fdata_nea['pondera'])


fdata_nea['clima_educativo']=fdata_nea['clima_educativo'].apply(lambda x: round(fdata_nea['clima_educativo'].mean()) if x==99 else x)#si no existe lo tomo como la media, no se cuanto influye
#calculos////////////////////////////////
mclima_educativo= (fdata_nea['clima_educativo']*data_nea['pondera']).mean()
dvclima_educativo= DescrStatsW(fdata_nea['clima_educativo'], weights=fdata_nea['pondera'])


fdata_nea.drop(['jcomed'],axis=1,inplace=True)#por ahora


#//////////////////////////////////////
#ya tengo hechas 2 bases de datos listas para modelizar con regresión y hacerle descriptiva evitando muy a groso modo la multicolinealidad
#creo 2 grupos para ver como influyen las edades de los miembros
fdn1=fdata_nea.drop(['menor18','menor14','mayor65'],axis=1)
fdn2=fdata_nea.drop(['cantmiem'],axis=1)

'''
#Matriz de correlación
corr_datos1 = fdn1[['gastot','ingtoth','clima_educativo','as','jestado','casado','jedad_agrup','univ','prim','regten2','regten1','propauto','cantmiem']].corr()
corr_datos2 = fdn2[['gastot','ingtoth','clima_educativo','as','jestado','casado','jedad_agrup','univ','prim','regten2','regten1','propauto','menor18','menor14','mayor65']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr_datos1, annot=True)
#sns.heatmap(corr_datos2, annot=True)
'''
plt.show()
print(fdata_nea.describe())

variables = ['gastot','ingtoth','clima_educativo','as','jestado','casado','jedad_agrup','univ','sec','prim','regten2','regten1','propauto','menor18','menor14','mayor65']
titulos = ['gastot','ingtoth','clima_educativo','as','jestado','casado','jedad_agrup','univ','sec','prim','regten2','regten1','propauto','menor18','menor14','mayor65']
xs = ['gastot','ingtoth','clima_educativo','as','jestado','casado','jedad_agrup','univ','sec','prim','regten2','regten1','propauto','menor18','menor14','mayor65']
ys = ['Frecuencia',None,None,'Frecuencia',None,None, 'Frecuencia',None,None,'Frecuencia',None,None]

fig, ax = plt.subplots(4, 4, figsize=(16,16))

for i in range(4):
  for j in range(4):
    ax[i,j].hist(fdn2[variables[i*2+j]], edgecolor = "white")
    ax[i,j].set_title(titulos[i*2+j])
    ax[i,j].set_xlabel(xs[i*2+j])
    ax[i,j].set_ylabel(ys[i*2+j])

plt.subplots_adjust(hspace=0.7)
plt.show()
