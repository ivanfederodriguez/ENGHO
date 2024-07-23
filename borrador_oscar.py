import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from statsmodels.stats.weightstats import DescrStatsW
def filtro1(data,i,region=False, percapita=False):
  if region:
    n_data=data[data['region']==i]
  else:
    n_data=data[data['provincia']==i]
  fn_data= n_data.drop(['region','provincia','id','hacina','jcomed','cantmiem'],axis=1)
  if percapita:
    fn_data.drop(['gastot','ingtoth'],axis=1,inplace=True)
  else:
    fn_data.drop(['gastotpc','ingpch'],axis=1,inplace=True)  
    #proprauto
   g3= fn_data[['gc09_01','gc09_02','gc09_03']].mean(axis=1)
  g6= fn_data[['gc09_01','gc09_02','gc09_03','gc09_04','gc09_05','gc09_06']].mean(axis=1)
  g9= fn_data[['gc09_01','gc09_02','gc09_03','gc09_04','gc09_05','gc09_06','gc09_07','gc09_08','gc09_09']].mean(axis=1)
  fn_data['gasto']=(fn_data[['gc09_01','gc09_02','gc09_03','gc09_04','gc09_05','gc09_06','gc09_07','gc09_08','gc09_09']].apply(lambda x: (x.iloc[0:2].sum()>g3)+(x.iloc[3:5].sum()>g6)+(x.iloc[6:8].sum()>g9),axis=1)).mean(axis=1)
  fn_data['propauto'] =  fn_data['propauto'].apply(lambda x: 1 if x in [2, 3] else 0)


  #regten regimen de tenencia
  fn_data['regten']=  fn_data['regten'].apply(lambda x: 1 if x==1 else 0)

  #jniveled
  fn_data['prim']=  fn_data['jniveled'].apply(lambda x: 1 if x in[2,3] else 0)
  fn_data['sec']=  fn_data['jniveled'].apply(lambda x: 1 if x in [4,5] else 0)
  fn_data['univ']=  fn_data['jniveled'].apply(lambda x: 1 if x==6 else 0)
  #//////////////////////////////////////////
  fn_data= fn_data.drop(['jniveled'],axis=1)


  fn_data['jsexo']= fn_data['jsexo']-1



  fn_data['edad_25/34']= fn_data['jedad_agrup'].apply(lambda x: 1 if x==3 else 0)
  fn_data['edad_35/49']= fn_data['jedad_agrup'].apply(lambda x: 1 if x in[4,5] else 0)
  fn_data['edad65_mas']= fn_data['jedad_agrup'].apply(lambda x: 1 if x==6 else 0)

  fn_data= fn_data.drop(['jedad_agrup'],axis=1)


  fn_data['casado']= fn_data['jsitconyugal'].apply(lambda x: 1 if x in [1, 2] else 0) #no se que tanto afectaran pensiones y esas cosas, habria que reconsiderar


  fn_data['jestado']= fn_data['jestado'].apply(lambda x: 1 if x==1 else 0)#resumen



  fn_data['asalariado']= fn_data['jocupengh'].apply(lambda x: 1 if x==1 else 0)
  fn_data['propia_soc_jur']= fn_data['jocupengh'].apply(lambda x: 1 if x==2 else 0)
  fn_data['propia_soc_no_jur']= fn_data['jocupengh'].apply(lambda x: 1 if x==3 else 0)
  fn_data['socio_soc_jur']= fn_data['jocupengh'].apply(lambda x: 1 if x==4 else 0)
  fn_data['socio_soc_no_jur']= fn_data['jocupengh'].apply(lambda x: 1 if x==5 else 0)

  fn_data= fn_data.drop(['jocupengh'],axis=1)



  fn_data['jpercept']= fn_data['jpercept']-1


  fn_data['clima_educativo']= fn_data['clima_educativo'].apply(lambda x: 0 if x==99 else x)
  fn_data['clima_educativo']= fn_data['clima_educativo'].apply(lambda x: round( fn_data['clima_educativo'].mean()) if x==0 else x)
  return fn_data
#muchas muchas variables

# Cargar los datos
data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/diplo/engho2018_hogares_diplo.txt')
# Explorar los datos
#por ahora sigue siendo el modelo mas simple que agarra la menor cantidad variables posibles*********************************** no olvidar borrar cuando se creen modelos mas complejos
#filtrado
#mayor_tamaño_provincia=data['provincia'].value_counts().keys()[index(max(data['provincia'].value_counts().values()))]
fdata_nea=filtro1(data,4,region=True,percapita=True)

#/////////////////////////////////////////////

#calculos/////////////////////////////////////////
m_propauto= (fdata_nea['propauto']*fdata_nea['pondera']).mean()
dvp1=DescrStatsW(fdata_nea['propauto'], weights=fdata_nea['pondera'])


mreg1= (fdata_nea['propietario']*fdata_nea['pondera']).mean()
mreg2= (fdata_nea['inquilino']*fdata_nea['pondera']).mean()
mreg3= (fdata_nea['ocupante']*fdata_nea['pondera']).mean()
dvp1= DescrStatsW(fdata_nea['propietario'], weights=fdata_nea['pondera'])
dvp2= DescrStatsW(fdata_nea['inquilino'], weights=fdata_nea['pondera'])
dvp3= DescrStatsW(fdata_nea['ocupante'], weights=fdata_nea['pondera'])


mprim= (fdata_nea['prim']*fdata_nea['pondera']).mean()
msec= (fdata_nea['sec']*fdata_nea['pondera']).mean()
muniv= (fdata_nea['univ']*fdata_nea['pondera']).mean()
dvprim= DescrStatsW(fdata_nea['prim'], weights=fdata_nea['pondera'])
dvsec= DescrStatsW(fdata_nea['sec'], weights=fdata_nea['pondera'])
dvuniv= DescrStatsW(fdata_nea['univ'], weights=fdata_nea['pondera'])


mjedad_agrup= (fdata_nea['jedad_agrup']*fdata_nea['pondera']).mean()
dvpjedad_agrup= DescrStatsW(fdata_nea['jedad_agrup'], weights=fdata_nea['pondera'])


mcasado= (fdata_nea['casado']*fdata_nea['pondera']).mean()
dvcasado= DescrStatsW(fdata_nea['casado'], weights=fdata_nea['pondera'])



mjestado= (fdata_nea['jestado']*fdata_nea['pondera']).mean()
dvpjestado= DescrStatsW(fdata_nea['jestado'], weights=fdata_nea['pondera'])



mas= (fdata_nea['as']*fdata_nea['pondera']).mean()
dvas= DescrStatsW(fdata_nea['as'], weights=fdata_nea['pondera'])



msoc_jur= (fdata_nea['soc_jur']*fdata_nea['pondera']).mean()
dvsoc_jur= DescrStatsW(fdata_nea['soc_jur'], weights=fdata_nea['pondera'])



mjpercept=(fdata_nea['jpercept']*fdata_nea['pondera']).mean()
dvpjpercept= DescrStatsW(fdata_nea['jpercept'], weights=fdata_nea['pondera'])



mclima_educativo= (fdata_nea['clima_educativo']*fdata_nea['pondera']).mean()
dvclima_educativo= DescrStatsW(fdata_nea['clima_educativo'], weights=fdata_nea['pondera'])


'''
corr_datos1 = fdn1[['gastot','ingtoth','clima_educativo','as','jestado','casado','jedad_agrup','univ','prim','regten2','regten1','propauto','cantmiem']].corr()
corr_datos2 = fdn2[['gastot','ingtoth','clima_educativo','as','jestado','casado','jedad_agrup','univ','prim','regten2','regten1','propauto','menor18','menor14','mayor65']].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(corr_datos1, annot=True)
#sns.heatmap(corr_datos2, annot=True)

plt.show()
'''
'''

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
'''

'''#
X = fdn2['ingtoth']
X = sm.add_constant(X)
y = fdn2[['gastot']]

reg1 = sm.OLS(y,X).fit()
print(reg1.summary())


X = fdn2[['ingtoth','clima_educativo','as','jestado','casado','jedad_agrup','univ','sec','prim','regten2','regten1','propauto','menor18','menor14','mayor65']]
X = sm.add_constant(X)
y = fdn2[['gastot']]

reg2 = sm.OLS(y,X).fit()
print(reg2.summary())
'''
'''
plt.scatter(['tamanio_motor'], base['emisiones_co2'])
plt.title('Tamaño del motor vs emisiones CO2')
plt.xlabel('Litros')
plt.ylabel('g/km')
plt.show()
#print(fdata_nea.describe())
'''
