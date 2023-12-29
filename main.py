from flask import Flask, render_template
from flask.ext.navigation import Navigation
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
#from sklearn.preprocessing import PolynomialFeatures
#from sklearn.pipeline import Pipeline
#from sklearn.linear_model import Ridge
#from sklearn.kernel_ridge import KernelRidge
#from sklearn.model_selection import GridSearchCV
import matplotlib.pyplot as plt
import io
import base64
app = Flask(__name__)
nav = Navigation(app)

nav.Bar('top', [
    nav.Item('Home','show_table'),
    nav.Item('Grafici', 'plot')
])

# Metodo che importa i dati da un foglio di formato excel.Per come � strutturato questo file, il modo corretto per caricare i dati �:
def get_data(filename, sheetname):
  dataset = pd.read_excel(
    filename,
    sheet_name=sheetname,
    index_col=3,
    usecols=5,
    skiprows=8,
  ).dropna(axis=1)
  return dataset

# Metodo che mostra il grafico del nostro dataset.
def show_plot(dataset):
  dataset.plot(title="Grafico dell'andamento del prezzo dell'oro dal 1979 al giorno d'oggi", figsize=(12, 4))
    
# Metodo che mostra il grafico del nostro dataset in un lasso di tempo specifico. 
def show_period_plot(i_date, f_date, dataset):
  dataset[i_date: f_date].plot(style="o-", figsize=(12, 4))
    
    
@app.route("/")
@app.route("/home")
def show_table():
  # Importo i dati nella variabile gold_daily ed elimino la colonna relativa ai dollari.
  gold = get_data("gold_price.xls", "Weekly_EndofPeriod")
  show_gold = gold.drop("US dollar",1)
  length = len(gold)
  # Creo un nuovo dataset composta dalla differenza del prezzo da una settimana all'altra.
  show_gold_diff = show_gold.diff().dropna()
  gold_diff = gold["Euro"].diff
  return render_template('home.html', tables=[show_gold.head().to_html(),show_gold.tail().to_html()], length = length,
  gold_diff = show_gold_diff.head().to_html())
  
@app.route("/plot")
def plot():
  # Visualizzo alcuni grafici
  gold = get_data("gold_price.xls", "Weekly_EndofPeriod")
  img = io.BytesIO()
  show_plot(gold.drop("US dollar",1))
#   show_period_plot("2018-01-01", "2018-06-29", gold.drop("US dollar",1))
  plt.savefig(img, format='png')
  img.seek(0)
  plot_url = base64.b64encode(img.getvalue()).decode()
  return render_template('plot.html', plot_url = plot_url)
  

if __name__ == '__main__':
  app.run(debug=True)