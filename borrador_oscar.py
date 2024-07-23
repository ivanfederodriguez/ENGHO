import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm
from statsmodels.stats.weightstats import DescrStatsW
def filtro1(data,i,region=False):
  n=data.shape[0]
  if region:
    n_data=data[data['region']==i]
  else:
    n_data=data[data['provincia']==i]
  fn_data= n_data.drop(['region','provincia','id','hacina','jcomed','gastotpc','gastot','ingtoth'],axis=1) 


  #gasto bajo es un gasto por debajo de la media de la suma de los primeros 3 grupos de gasto
  g3= (fn_data['gc09_01']+fn_data['gc09_02']+fn_data['gc09_03']).mean()
  g6= (fn_data['gc09_01']+fn_data['gc09_02']+fn_data['gc09_03']+fn_data['gc09_04']+fn_data['gc09_05']+fn_data['gc09_06']).mean()
  g9= (fn_data['gc09_01']+fn_data['gc09_02']+fn_data['gc09_03']+fn_data['gc09_04']+fn_data['gc09_05']+fn_data['gc09_06']+fn_data['gc09_07']+fn_data['gc09_08']+fn_data['gc09_09']).mean()
  gasto=[]
  l=np.array(fn_data[['gc09_01','gc09_02','gc09_03','gc09_04','gc09_05','gc09_06','gc09_07','gc09_08','gc09_09']].values.tolist())
  for i in range(l.shape[0]):
    gasto.append(int(l[i][0:2].sum()>g3)+int(l[i][0:5].sum()>g6)+int(l[i][0:8].sum()>g9))
  fn_data['gasto']=gasto
  #proprauto
  fn_data['propauto'] =  fn_data['propauto'].apply(lambda x: 1 if x in [2, 3] else 0)

  #regten regimen de tenencia
  fn_data['regten']=  fn_data['regten'].apply(lambda x: 1 if x==1 else 0)

  #jniveled
  fn_data['prim']=  fn_data['jniveled'].apply(lambda x: 1 if x in[2,3] else 0)
  fn_data['sec']=  fn_data['jniveled'].apply(lambda x: 1 if x in [4,5] else 0)
  fn_data['univ']=  fn_data['jniveled'].apply(lambda x: 1 if x==6 else 0)
  #//////////////////////////////////////////
  fn_data= fn_data.drop(['jniveled'],axis=1)


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
fdata_nea=filtro1(data,4,region=True)
n=fdata_nea.shape[0]

X = fdata_nea['ingpch']
X = sm.add_constant(X)
y = fdata_nea[['gasto']]

reg1 = sm.OLS(y,X).fit()
print(reg1.summary())


X = fdata_nea[['ingpch','clima_educativo','asalariado','propia_soc_jur','propia_soc_no_jur','socio_soc_jur','socio_soc_no_jur','jestado','casado','univ','sec','prim','regten','propauto','cantmiem','edad_25/34','edad_35/49','edad65_mas']]
X = sm.add_constant(X)
y = fdata_nea[['gasto']]

reg2 = sm.OLS(y,X).fit()
print(reg2.summary())
plt.hist(np.log(fdata_nea['gasto'][fdata_nea['gasto']>0]))
plt.show()
plt.hist(np.log(fdata_nea['ingpch'][fdata_nea['ingpch']>0]))
plt.show()
