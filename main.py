import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import norm
st.title("Black and Scholes Model")
st.write("# Feilds")
col1 ,col2 =st.columns(2)
stock_price=col1.number_input("Underlying spot price",min_value=0.0,max_value=1000000.0,step=0.01)
strike_price=col1.number_input("Strike Price",min_value=0.0,max_value=1000000.0,step=0.01)
c=col1.number_input("Dividend Yeild Of Stock",min_value=0.0,max_value=1000000.0,step=0.01)
days_to_maturity=col2.number_input("Time to Expiry in Years",min_value=0.0003,max_value=10000000.0,step=0.0001)
risk_free_rate=col2.number_input("Risk Free Rate",step=0.01)
volatility=col2.number_input("Voltility",step=0.01)
dstp=col1.number_input("Change in Stock Price",step=0.001)
dsg=col2.number_input("Change in Volatiltiy",step=0.01)
if(volatility!=0):

    d1=(np.log(stock_price/strike_price)+((risk_free_rate+0.5*volatility**2)*days_to_maturity)/(volatility*np.sqrt(days_to_maturity)))
    d2=(np.log(stock_price/strike_price)+((risk_free_rate-0.5*volatility**2)*days_to_maturity)/(volatility*np.sqrt(days_to_maturity)))
    calloption=(stock_price*norm.cdf(d1,0,1.0))-strike_price*np.exp(-risk_free_rate*days_to_maturity)*norm.cdf(d2,0,1.0)
    putoption=strike_price*np.exp(-risk_free_rate*days_to_maturity)*(1-norm.cdf(d2,0,1.0))-(stock_price*(1-norm.cdf(d1,0,1.0)))
    vega=np.exp(-c*days_to_maturity)*stock_price*np.sqrt(days_to_maturity)*norm.pdf(d1)
    delta_call=np.exp(-c*days_to_maturity)*norm.cdf(d1,0,1.0)
    delta_put=delta_call-np.exp(-c*days_to_maturity)
    gama=np.exp(-c*days_to_maturity)*(norm.pdf(d1)/(volatility*stock_price*np.sqrt(days_to_maturity)))
    pnl_call=delta_call*dstp+((gama*(dstp**2))/2)+vega*dsg
    pnl_put=delta_put*dstp+((gama*(dstp**2))/2)+vega*dsg

else:
    calloption=float("Nan")
    putoption=float("Nan")


st.write("#Price Calcualtion")
col1,col2=st.columns(2)
col1.metric(label="Call Option Price", value=f"${calloption:,.2f}")
col2.metric(label="Put Option Price", value=f"${putoption:,.2f}")
col1.metric(label="Call PNL", value=f"${pnl_call:,.2f}")
col2.metric(label="Put PNL", value=f"${pnl_put:,.2f}")

if (pnl_put>0 and pnl_call<0):
    st.write('Excecise Put')
elif(pnl_call>0 and pnl_put<0):
    st.write('Excercise call')
elif(pnl_put<0 and pnl_call<0):
    st.write('Not excercise any')
else:
    st.write('exercise both')


