import pandas as pd
import numpy as np
#este filtro, se aplica a cualquier i provincia de datasert y devuelve uno nuevo con la inforamción modificada de esa provincia
#ignora los posibles efectos de 'region','provincia','id','gastotpc','gc09_01','gc09_02','gc09_03','gc09_04','gc09_05','gc09_06','gc09_07','gc09_08','gc09_09','ingpch','hacina','jcomed','menor18','menor14','mayor65'
#por favor mejorar porque esta construido en base casi nada de información sobre la correlacion
def filtro1(data,i,percapita=False):
  n_data=data[data['provincia']==i]
  fn_data= n_data.drop(['region','provincia','id','gc09_01','gc09_02','gc09_03','gc09_04','gc09_05','gc09_06','gc09_07','gc09_08','gc09_09','hacina','jcomed','cantmiem'],axis=1)
  if percapita:
    fn_data.drop(['gastot','ingtoth'],inplace=True)
  else:
    fn_data.drop(['gastotpc','ingpch'],inplace=True)  
    #proprauto
  fn_data['propauto'] =  fn_data['propauto'].apply(lambda x: 1 if x in [2, 3] else 0)


  #regten regimen de tenencia
  fn_data['propietario']=  fn_data['regten'].apply(lambda x: 1 if x==1 else 0)
  fn_data['inquilino']=  fn_data['regten'].apply(lambda x: 1 if x==2 else 0)
  fn_data['ocupante']=  fn_data['regten'].apply(lambda x: 1 if x==3 else 0)

  fn_data= fn_data.drop(['regten'],axis=1)

  #jniveled
  fn_data['prim']=  fn_data['jniveled'].apply(lambda x: 1 if x==1 else 0)
  fn_data['sec']=  fn_data['jniveled'].apply(lambda x: 1 if x==3 else 0)
  fn_data['univ']=  fn_data['jniveled'].apply(lambda x: 1 if x==5 else 0)
  fn_data['noed/noans']=  fn_data['jniveled'].apply(lambda x: 1 if x==7 else 0)
  #//////////////////////////////////////////
  fn_data= fn_data.drop(['jniveled'],axis=1)


  fn_data['jsexo']= fn_data['jsexo']-1



  fn_data['jedad_agrup']= fn_data['jedad_agrup']-1 #resumen



  fn_data['casado']= fn_data['jsitconyugal'].apply(lambda x: 1 if x in [1, 2] else 0) #no se que tanto afectaran pensiones y esas cosas, habria que reconsiderar



  fn_data['jestado']= fn_data['jestado'].apply(lambda x: 1 if x==1 else 0)#resumen



  fn_data['as']= fn_data['jocupengh'].apply(lambda x: 1 if x==1 else 0)



  fn_data['soc_jur']= fn_data['jocupengh'].apply(lambda x: 1 if x in [2,5] else 0)



  fn_data['jpercept']= fn_data['jpercept']-1


  fn_data['clima_educativo']= fn_data['clima_educativo'].apply(lambda x: 0 if x==99 else x)
  fn_data['clima_educativo']= fn_data['clima_educativo'].apply(lambda x: round( fn_data['clima_educativo'].mean()) if x==0 else x)
  return fn_data
#muchas muchas variables
def filtro2(data,i,percapita=False):
  n_data=data[data['provincia']==i]
  fn_data= n_data.drop(['region','provincia','id','gc09_01','gc09_02','gc09_03','gc09_04','gc09_05','gc09_06','gc09_07','gc09_08','gc09_09','hacina','jcomed','menor18','menor14','mayor65'],axis=1)
  if percapita:
    fn_data.drop(['gastot','ingtoth'],inplace=True)
  else:
    fn_data.drop(['gastotpc','ingpch'],inplace=True)
  #proprauto
  fn_data['propauto'] =  fn_data['propauto']-1


  #regten regimen de tenencia
  fn_data['propietario']=  fn_data['regten'].apply(lambda x: 1 if x==1 else 0)
  fn_data['inquilino']=  fn_data['regten'].apply(lambda x: 1 if x==2 else 0)
  fn_data['ocupante']=  fn_data['regten'].apply(lambda x: 1 if x==3 else 0)

  fn_data= fn_data.drop(['regten'],axis=1)

  #jniveled
  fn_data['prim']=  fn_data['jniveled'].apply(lambda x: 1 if x==1 else 0)
  fn_data['sec']=  fn_data['jniveled'].apply(lambda x: 1 if x==3 else 0)
  fn_data['univ']=  fn_data['jniveled'].apply(lambda x: 1 if x==5 else 0)
  fn_data['noed/noans']=  fn_data['jniveled'].apply(lambda x: 1 if x==7 else 0)
  #//////////////////////////////////////////
  fn_data= fn_data.drop(['jniveled'],axis=1)


  fn_data['varon']= fn_data['jsexo'].apply(lambda x: 1 if x==1 else 0)
  fn_data['mujer']= fn_data['jsexo'].apply(lambda x: 1 if x==2 else 0)

  fn_data= fn_data.drop(['jsexo'],axis=1)


  fn_data['hasta24']= fn_data['jedad_agrup'].apply(lambda x: 1 if x==2 else 0)
  fn_data['25-34']= fn_data['jedad_agrup'].apply(lambda x: 1 if x==3 else 0)
  fn_data['35-49']= fn_data['jedad_agrup'].apply(lambda x: 1 if x==4 else 0)
  fn_data['50-64']= fn_data['jedad_agrup'].apply(lambda x: 1 if x==5 else 0)
  fn_data['65_mas']= fn_data['jedad_agrup'].apply(lambda x: 1 if x==6 else 0)

  fn_data= fn_data.drop(['jedad_agrup'],axis=1)


  fn_data['unido']= fn_data['jsitconyugal'].apply(lambda x: 1 if x==1 else 0) #no se que tanto afectaran pensiones y esas cosas, habria que reconsiderar
  fn_data['casado']= fn_data['jsitconyugal'].apply(lambda x: 1 if x==2 else 0)
  fn_data['separado']= fn_data['jsitconyugal'].apply(lambda x: 1 if x==3 else 0)
  fn_data['viudo']= fn_data['jsitconyugal'].apply(lambda x: 1 if x==4 else 0)
  fn_data['soltera']= fn_data['jsitconyugal'].apply(lambda x: 1 if x==5 else 0)

  fn_data= fn_data.drop(['jsitconyugal'],axis=1)


  fn_data['ocupado']= fn_data['jestado'].apply(lambda x: 1 if x==1 else 0)#resumen
  fn_data['desocupado']= fn_data['jestado'].apply(lambda x: 1 if x==2 else 0)
  fn_data['inactivo']= fn_data['jestado'].apply(lambda x: 1 if x==3 else 0)
  fn_data['menores10']= fn_data['jestado'].apply(lambda x: 1 if x==4 else 0)
  fn_data= fn_data.drop(['jestado'],axis=1)


  fn_data['asalariado']= fn_data['jocupengh'].apply(lambda x: 1 if x==1 else 0)
  fn_data['propia_soc_jur']= fn_data['jocupengh'].apply(lambda x: 1 if x in [2,3] else 0)
  fn_data['socio_soc_jur']= fn_data['jocupengh'].apply(lambda x: 1 if x in [4,5] else 0)
  fn_data['empleado']= fn_data['jocupengh'].apply(lambda x: 1 if x==6 else 0)

  fn_data= fn_data.drop(['jocupengh'],axis=1)


  fn_data['jcomed']= fn_data['jcomed'].apply(lambda x: 0 if x==99 else x)
  fn_data['jcomed']= fn_data['jcomed'].apply(lambda x: round( fn_data['jcomed'].mean()) if x==0 else x)


  fn_data['jpercept']= fn_data['jpercept']-1


  fn_data['clima_educativo']= fn_data['clima_educativo'].apply(lambda x: 0 if x==99 else x)
  fn_data['clima_educativo']= fn_data['clima_educativo'].apply(lambda x: round( fn_data['clima_educativo'].mean()) if x==0 else x)
  return fn_data
