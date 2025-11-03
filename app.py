from flask import Flask, render_template,request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

df = pd.read_csv('Global finance data.csv')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Email and password are required')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('login'))

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST': 
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists')
        else:
            # hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html')  

@app.before_request
def create_tables():
    db.create_all()



# graphs functions

# Graph 1: Stock Market Index Values Over Time
def Stock_Market_Index_Values_Over_Time():
    fig = px.line(df, x='Date', y='Index_Value', color='Stock_Index', markers=True, title='Stock Market Index Value Over Time')
    graph1_html = fig.to_html(full_html=False)   
    return graph1_html 

# Graph 2 : Average Daily Change Percentage by Country
def Average_Daily_Change_Percentage_By_Country():
    df['Daily_Change'] = df['Index_Value'].pct_change()
    fig = px.bar(df, x='Country', y='Daily_Change_Percent',
       title='Average Daily Change Percentage by Country',
       color='Country',
       text='Daily_Change_Percent',
       template='plotly_white')
    graph2_html = fig.to_html(full_html=False)
    return graph2_html

# Graph 3 : GDP Growth Rate by Country
def GDP_Growth_Rate_By_Country():
    fig = px.bar(df, x='Country', y='GDP_Growth_Rate_Percent',
        title='GDP Growth Rate by Country',
        color='Country',
        text='GDP_Growth_Rate_Percent',
        template='plotly_white')
    graph3_html = fig.to_html(full_html=False)
    return graph3_html

# Graph 4 :GDP Growth Rate vs Unemployment Rate
def GDP_Growth_Rate_vs_Unemployment_Rate():
    fig = px.scatter(df,x='GDP_Growth_Rate_Percent', y='Unemployment_Rate_Percent',  
        title='GDP Growth Rate vs Unemployment Rate',color='Country',hover_name='Country',
        size='Market_Cap_Trillion_USD',  # optional: show market cap as marker size
        labels={'GDP_Growth_Rate_Percent': 'GDP Growth (%)', 'Unemployment_Rate_Percent': 'Unemployment Rate (%)'},
    template='plotly_white')
    graph4_html = fig.to_html(full_html=False)
    return graph4_html

# Graph 5 : Correlation Heatmap
def Correlation_Heatmap():
    fig = px.imshow(
        df[['Index_Value', 'Market_Cap_Trillion_USD', 'GDP_Growth_Rate_Percent']].corr(),
        title='Correlation Heatmap',
        color_continuous_scale='RdBu',
        zmin=-1, zmax=1,
        aspect='auto'
    )
    graph5_html = fig.to_html(full_html=False)
    return graph5_html

# Graph 6 : Inflation Rate vs Interest Rate Over Time
def Inflation_Rate_vs_Interest_Rate_Over_Time():
    fig = px.line(df, x='Date', y=['Inflation_Rate_Percent', 'Interest_Rate_Percent'],
        title='Inflation Rate vs Interest Rate Over Time',
        labels={'value': 'Percentage', 'variable': 'Economic Indicators'},
        markers=True)
    graph6_html = fig.to_html(full_html=False)
    return graph6_html

# Graph 7 : Inflation Rate vs Interest Rate
def Inflation_Rate_vs_Interest_Rate():
    fig = px.scatter(df, x='Inflation_Rate_Percent', y='Interest_Rate_Percent',
            title='Inflation Rate vs Interest Rate',
            color='Country', 
            trendline='ols',
            template='plotly_white')
    graph7_html = fig.to_html(full_html=False)
    return graph7_html

# Graph 8 : Exchange Rate vs USD Over Time
def Exchange_Rate_vs_USD_Over_Time():
    fig = px.line(df, x='Date', y='Exchange_Rate_USD',
        title='Exchange Rate vs USD Over Time',
        color='Country',
        markers=True)
    graph8_html = fig.to_html(full_html=False)
    return graph8_html

# Graph 9 : Currency Change Year-to-Date Percentage by Country
def Currency_Change_Year_to_Date_Percentage_By_Country():
    df['Currency_Change_YTD'] = df['Exchange_Rate_USD'].pct_change()
    fig = px.bar(df, x='Country', y='Currency_Change_YTD_Percent',
        title='Currency Change Year-to-Date Percentage by Country',
        color='Currency_Change_YTD_Percent',
        labels={'Currency_Change_YTD_Percent': 'YTD Change (%)'},
        template='plotly_white')
    graph9_html = fig.to_html(full_html=False)
    return graph9_html

# Graph 10 : Exchange Rate vs Inflation with Market Cap and GDP Growth
def Exchange_Rate_vs_Inflation_with_Market_Cap_and_GDP_Growth():
    fig =  px.scatter(
    df,
    x='Exchange_Rate_USD',
    y='Inflation_Rate_Percent',
    size='Market_Cap_Trillion_USD',
    color='GDP_Growth_Rate_Percent',
    hover_name='Country',
    title='Exchange Rate vs Inflation with Market Cap and GDP Growth',
    color_continuous_scale='Viridis',
    labels={
        'GDP_Growth_Rate_Percent': 'GDP Growth (%)',
        'Exchange_Rate_USD': 'Exchange Rate (vs USD)',
        'Inflation_Rate_Percent': 'Inflation Rate (%)'
    },
    template='plotly_white'
)
    graph10_html = fig.to_html(full_html=False)
    return graph10_html

# Graph 11 : Government Debt as Percentage of GDP by Country
def Government_Debt_as_Percentage_of_GDP_by_Country():
    fig =  px.bar(df, x='Country', y='Government_Debt_GDP_Percent',
       title='Government Debt as Percentage of GDP by Country',
       labels={'Government_Debt_GDP_Percent': 'Government Debt (% of GDP)'},
       template='plotly_white'
)
    graph11_html = fig.to_html(full_html=False)
    return graph11_html

# Graph 12 : Government Debt vs Credit Rating
def Government_Debt_vs_Credit_Rating():
     fig =  px.scatter(
    df,
    x='Government_Debt_GDP_Percent',
    y='Credit_Rating',
    title='Government Debt vs Credit Rating',
    color='Country',
    hover_name='Country',
    size='Market_Cap_Trillion_USD',
    color_continuous_scale='Viridis',
    labels={'Credit_Rating': 'Credit Rating (Numeric)', 'Government_Debt_GDP_Percent': 'Government Debt (% of GDP)'},
    template='plotly_white'
)
     graph12_html = fig.to_html(full_html=False)
     return graph12_html

# Graph 13 : Political Risk Score by Country
def Political_Risk_Score_by_Country():
    fig = px.bar(df, x='Country', y='Political_Risk_Score',
        title='Political Risk Score by Country',
       template='plotly_white')
    graph13_html = fig.to_html(full_html=False)
    return graph13_html

# Graph 14 : Banking Sector Health Score by Country
def Banking_Sector_Health_Score_by_Country():
    fig =  px.bar(df, x='Country', y='Banking_Sector_Health',
        title='Banking Sector Health Score by Country',
        labels={'Banking_Sector_Health': 'Banking Sector Health Score'}
)
    graph14_html = fig.to_html(full_html=False)
    return graph14_html

# Graph 15 : Correlation Heatmap (numeric variables)
def Correlation_Heatmap_Numeric_Variables():
    numeric_df = df.select_dtypes(include=[np.number])
    if numeric_df.shape[1] == 0:
        print("No numeric columns available to compute correlation.")
        return ""
    corr = numeric_df.corr()
    fig15 = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale='RdYlGn_r',
        labels={'color': 'Correlation Coefficient'},
        x=corr.columns,
        y=corr.index,
        aspect='auto'
    )
    fig15.update_layout(title='Correlation Heatmap (numeric variables)')
    graph15_html = fig15.to_html(full_html=False)
    return graph15_html

# Graph 16 : Gold_Price_USD_Ounce Price Over Time
def Gold_Price_USD_Ounce_Price_Over_Time():
    fig = px.line(df, x='Date', y='Gold_Price_USD_Ounce',
        title='Gold Price (USD per Ounce) Over Time',
        labels={'Gold_Price_USD_Ounce': 'Gold Price (USD/Ounce)'},
        markers=True)
    graph16_html = fig.to_html(full_html=False)
    return graph16_html

# Graph 17 : 10-Year Bond Yield Comparison
def Bond_Yield_Comparison():
    fig = px.line(df, x='Date', y='Bond_Yield_10Y_Percent', color='Country',
        title='10-Year Bond Yield Comparison',
        labels={'value': 'Yield (%)', 'variable': 'Country'},
        template='plotly_white',
        markers=True)
    graph17_html = fig.to_html(full_html=False)
    return graph17_html

# Graph 18 : Bond Yield vs Inflation Rate
def Bond_Yield_vs_Inflation_Rate():
    fig = px.scatter(df, x='Bond_Yield_10Y_Percent', y='Inflation_Rate_Percent',
           title='Bond Yield vs Inflation Rate',                                                                                                                    
           labels={'Bond_Yield_10Y_Percent': 'Bond Yield (%)', 'Inflation_Rate_Percent': 'Inflation Rate (%)'},
           template='plotly_white',
           color='Country',
           hover_name='Country',
           size_max=10
)       
    graph18_html = fig.to_html(full_html=False)
    return graph18_html

# Graph 19 : Export vs Import Growth by Country
def Export_vs_Import_Growth_by_Country():
    fig = px.bar(df, x='Country', y=['Export_Growth_Percent', 'Import_Growth_Percent'],
       title='Export vs Import Growth by Country',
       labels={'value': 'Growth Rate (%)', 'variable': 'Trade Type'},
       template='plotly_white',
       barmode='group'
)
    graph19_html = fig.to_html(full_html=False)
    return graph19_html

# Group 20 : Current Account Balance with Export and Import Growth
def Current_Account_Balance_with_Export_and_Import_Growth():
    fig = px.scatter(df, x='Export_Growth_Percent', y='Import_Growth_Percent',
           color='Country',
           title='Current Account Balance with Export and Import Growth',
           labels={'Current_Account_Balance_USD_Billion': 'Current Account Balance (USD Billion)'}
           )
    graph20_html = fig.to_html(full_html=False)
    return graph20_html

# graphs Route
@app.route("/overview")
def overview():
    graph1_html = Stock_Market_Index_Values_Over_Time()
    graph2_html = Average_Daily_Change_Percentage_By_Country()
    graph3_html = GDP_Growth_Rate_By_Country()
    graph4_html = GDP_Growth_Rate_vs_Unemployment_Rate()
    graph5_html = Correlation_Heatmap()
    return render_template('overview.html', graph1_html=graph1_html, graph2_html=graph2_html, graph3_html=graph3_html, graph4_html=graph4_html, graph5_html=graph5_html)    

@app.route("/Inflation")
def inflation ():
    graph6_html = Inflation_Rate_vs_Interest_Rate_Over_Time()
    graph7_html = Inflation_Rate_vs_Interest_Rate()
    graph8_html = Exchange_Rate_vs_USD_Over_Time()
    graph9_html = Currency_Change_Year_to_Date_Percentage_By_Country()
    graph10_html = Exchange_Rate_vs_Inflation_with_Market_Cap_and_GDP_Growth()
    return render_template('Inflation.html', graph6_html=graph6_html, graph7_html=graph7_html, graph8_html=graph8_html, graph9_html=graph9_html, graph10_html=graph10_html)

@app.route("/Risk")
def risk():
    graph11_html = Government_Debt_as_Percentage_of_GDP_by_Country()
    graph12_html = Government_Debt_vs_Credit_Rating()
    graph13_html = Political_Risk_Score_by_Country()
    graph14_html = Banking_Sector_Health_Score_by_Country()
    graph15_html = Correlation_Heatmap_Numeric_Variables()
    return render_template('Risk.html', graph11_html=graph11_html,graph12_html=graph12_html, graph13_html=graph13_html, graph14_html=graph14_html, graph15_html=graph15_html)

@app.route("/Commodities")  
def commodities():
    graph16_html = Gold_Price_USD_Ounce_Price_Over_Time()
    graph17_html = Bond_Yield_Comparison()
    graph18_html = Bond_Yield_vs_Inflation_Rate()
    graph19_html = Export_vs_Import_Growth_by_Country()
    graph20_html = Current_Account_Balance_with_Export_and_Import_Growth()
    return render_template('Commodities.html', graph16_html=graph16_html, graph17_html=graph17_html, graph18_html=graph18_html, graph19_html=graph19_html, graph20_html=graph20_html)

if __name__ == "__main__":
    app.run(debug=True)