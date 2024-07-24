def plot_heatmap(df):
    corr_datos = df[['ingpch','ingpch2','clima_educativo', 'asalariado', 'casado','regten', 'propauto', 'edad_25/34', 'edad_35/49', 'edad65_mas']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_datos, annot=True)
    plt.show()
def plot_histogramas(df):
  variables = ['ingpch','ingpch2','clima_educativo', 'asalariado', 'casado','regten', 'propauto', 'edad_25/34', 'edad_35/49', 'edad65_mas']
  titulos = ['ingpch','ingpch2','clima_educativo', 'asalariado', 'casado','regten', 'propauto', 'edad_25/34', 'edad_35/49', 'edad65_mas']
  xs = ['gastot','ingtoth','clima_educativo','as','jestado','casado','jedad_agrup','univ','sec','prim','regten2','regten1','propauto','menor18','menor14','mayor65']
  ys = ['Frecuencia',None,None,'Frecuencia',None,None, 'Frecuencia',None,None,'Frecuencia',None,None,'Frecuencia',None,None]
  fig, ax = plt.subplots(5, 2, figsize=(16,16))

  for i in range(5):
    for j in range(2):
      ax[i,j].hist(df[variables[i*2+j]], edgecolor = "white")
      ax[i,j].set_title(titulos[i*2+j])
      ax[i,j].set_xlabel(xs[i*2+j])
      ax[i,j].set_ylabel(ys[i*2+j])

  plt.subplots_adjust(hspace=0.7)
  plt.show()
