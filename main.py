import flask
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import os

GRAPH_FOLDER = os.path.join('static')

app = flask.Flask(__name__) 
app.config.from_object(__name__)
app.config['UPLOAD_FOLDER'] = GRAPH_FOLDER

db = sqlite3.connect('COTDresults.db')
df = pd.read_sql_query("SELECT * FROM Results", db)


@app.route('/')
def home():
    return flask.render_template('home.html')

@app.route('/info')
def info():
    return flask.render_template('info.html')

@app.route('/download')  
def download(): 
    df.to_csv('cotdresults.csv', index=False) 
    return flask.render_template('download.html')

@app.route('/linegraphs')  
def linegraphs():
    df.plot(x='Date', y='Qualifying', kind='line', color='green', label="Kvalifikācija")
    plt.savefig('static/qualiline.png')
    df.plot(x='Date', y='FinalPosition', kind='line', color='green', label="Fināla pozīcija")
    plt.savefig('static/finalline.png')
    df.plot(x='Date', y='Division', kind='line', color='green', label="Divīzija")
    plt.savefig('static/divisionline.png')
    df.plot(x='Date', y='DivPosition', kind='line', color='green', label="Divīzijas pozīcija")
    plt.savefig('static/divposline.png')
    line1 = os.path.join(app.config['UPLOAD_FOLDER'], 'qualiline.png')
    line2 = os.path.join(app.config['UPLOAD_FOLDER'], 'divisionline.png')
    line3 = os.path.join(app.config['UPLOAD_FOLDER'], 'divposline.png')
    line4 = os.path.join(app.config['UPLOAD_FOLDER'], 'finalline.png') 
    return flask.render_template('linegraphs.html', line1=line1, line2=line2, line3=line3, line4=line4) 

@app.route('/histograms')  
def histograms():
    df.hist('Division')
    plt.savefig('static/divhist.png')
    df.hist('DivPosition')
    plt.savefig('static/divposhist.png')
    hist1 = os.path.join(app.config['UPLOAD_FOLDER'], 'divhist.png')
    hist2 = os.path.join(app.config['UPLOAD_FOLDER'], 'divposhist.png')
    return flask.render_template('histograms.html', hist1=hist1, hist2=hist2)

@app.route('/multiline')  
def multiline():
    plt.plot(df['Date'], df['Qualifying'], color='red', label="Kvalifikācija")
    plt.plot(df['Date'], df['FinalPosition'], color='green', label="Fināla pozīcija")
    plt.legend()
    plt.savefig('static/multiline.png')
    multiline = os.path.join(app.config['UPLOAD_FOLDER'], 'multiline.png') 
    return flask.render_template('multiline.html', multiline = multiline)

@app.route('/divisions')  
def divisions():
    division_df = df['Division'].value_counts().reset_index()
    division_df.plot(x ='Division', y ='count', kind ='barh', color='blue')
    plt.title('Divīziju biežums')
    plt.savefig('static/divbar.png')
    divbar = os.path.join(app.config['UPLOAD_FOLDER'], 'divbar.png') 
    return flask.render_template('divisions.html', divbar = divbar)

@app.route('/scatter')  
def scatter():
    plt.scatter(df['Division'], df['DivPosition'], color ='red')
    plt.xlabel('Division')
    plt.ylabel('DivPosition')
    plt.savefig('static/scatter.png')
    scatter = os.path.join(app.config['UPLOAD_FOLDER'], 'scatter.png') 
    return flask.render_template('scatter.html', scatter = scatter)

app.run(debug=True)
