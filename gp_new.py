#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import statements
import mysql.connector as mysqlcon
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


#create connection to mysql server on your computer
#this was done in class as a group
mysqlConnection = mysqlcon.connect(user='test1',
                                 password = 'Test1234#',
                                 host='3.16.213.2')


# In[3]:


#use connection you just created
#this was done in class as a group
mysqlCursor = mysqlConnection.cursor()


# In[4]:


#create engine - this ended up not being usd but leaving for our process
#this was done in class as a group
import pymysql
from sqlalchemy import create_engine
import sqlalchemy
sqlEngineStr = "mysql+pymysql://test1:Test1234#@3.16.213.2:3306/classicmodels"
sqlEngine = create_engine(sqlEngineStr)


# In[5]:


#change one of the 'country' column names so there are not 2 columns named the same thing
#this was done in class as a group
q = '''ALTER TABLE classicmodels.customers
RENAME COLUMN country to customerCountry;'''

#mysqlCursor.execute(q)


# In[6]:


#create the query - this was done in class as a group
query = "SELECT * from classicmodels.products AS p \
    JOIN classicmodels.orderdetails AS od \
    ON od.productCode = p.productCode \
    JOIN classicmodels.orders AS o \
    ON o.orderNumber = od.orderNumber \
    JOIN classicmodels.customers AS c \
    ON o.customerNumber = c.customerNumber \
    JOIN classicmodels.employees AS e \
    ON e.employeeNumber = c.salesRepEmployeeNumber \
    JOIN classicmodels.offices AS off \
    ON off.officeCode = e.officeCode \
    JOIN classicmodels.payments AS pay \
    ON c.customerNumber = pay.customerNumber;"
mysqlCursor.execute(query, params=None, multi=True)


# In[7]:


mysqlCursor.fetchall()


# In[8]:


cm_df = pd.read_sql_query(query, mysqlConnection)
print("Dataframe created.")


# In[9]:


#drop irrelevant columns
#this was done as a group in a group meeting
cm_df.drop(columns = ["productDescription","phone","addressLine1","addressLine2","postalCode","checkNumber","comments", "requiredDate","status", "email", "extension","creditLimit", "customerNumber","orderNumber"], inplace = True)


# In[10]:


#drop duplicate columns
#this was done as a group in a group meeting
cm_df = cm_df.T.drop_duplicates().T


# In[11]:


#NEW
#Kyle did this
#Set data types for columns
cm_df["quantityInStock"] = cm_df["quantityInStock"].astype('int32')
cm_df["buyPrice"] = pd.to_numeric(cm_df["buyPrice"])
cm_df["MSRP"] = pd.to_numeric(cm_df["MSRP"])
cm_df["quantityOrdered"] = cm_df["quantityOrdered"].astype('int32')
cm_df["priceEach"] = pd.to_numeric(cm_df["priceEach"])
cm_df["orderLineNumber"] = cm_df["orderLineNumber"].astype('int32')
cm_df["orderDate"] = pd.to_datetime(cm_df["orderDate"], yearfirst=True)
cm_df["shippedDate"] = pd.to_datetime(cm_df["shippedDate"])
cm_df["paymentDate"] = pd.to_datetime(cm_df["paymentDate"])
cm_df["salesRepEmployeeNumber"] = cm_df["salesRepEmployeeNumber"].astype("int32")
cm_df["officeCode"] = cm_df["officeCode"].astype('int32')
#NEW END


# In[12]:


#add new columns for easier analysis
#Emily and Hannah did this
cm_df["profit"] = (cm_df["priceEach"]-cm_df["buyPrice"])*cm_df["quantityOrdered"]
cm_df["expectedProfit"] = (cm_df["MSRP"]-cm_df["buyPrice"])*cm_df['quantityOrdered']
cm_df['percentProfit'] = (cm_df['amount'] - cm_df['buyPrice']*cm_df['quantityOrdered'])/(cm_df['amount'].sum())
cm_df['priceDifference'] = cm_df['MSRP'] - cm_df['priceEach']


# In[13]:


#setup the dashboard
#Emily and Sami did this
st.title('Group 4 Final Project')
st.write('Kyle Kendall, Hannah Palmer, Sami Saliba, and Emily Toler')
st.subheader('Problem Identification')
st.write('Businesses must make operating decisions based on reliable data in order to be efficient. For example, \
         if a component of the business, such as a store, is found to not be profitable, the business will take \
         action to maximize profit. In this project, the team seeks to improve the business outcomes of a company \
         that is an intermediary between companies that produce models of classic vehicles and stores that carry \
         models of classic vehicles for purchase by customers.')
st.subheader('Details of the Data Pipeline Design and Development')
st.write('The team will use Jupyter Notebook to extract the data from the classicmodels database, \
         transform the data into a unified table, and access this data in order to create an interactive \
         dashboard that displays in a URL outside of Jupyter Notebook.')


# In[19]:


#NEW
#Kyle did this code
#set new dataframes by each product line
PLvc = cm_df.loc[lambda df: df["productLine"]=="Vintage Cars"]
PLcc = cm_df.loc[lambda df: df["productLine"]=="Classic Cars"]
PLtb = cm_df.loc[lambda df: df["productLine"]=="Trucks and Buses"]
PLt = cm_df.loc[lambda df: df["productLine"]=="Trains"]
PLs = cm_df.loc[lambda df: df["productLine"]=="Ships"]
PLp = cm_df.loc[lambda df: df["productLine"]=="Planes"]
PLm = cm_df.loc[lambda df: df["productLine"]=="Motorcycles"]
cm_df_PL = cm_df[["productLine",'quantityInStock', 'buyPrice', 'quantityOrdered', 'profit', 'expectedProfit', 'priceDifference']].groupby(by=cm_df["productLine"]).sum()
#NEW END
cm_df_PL


# In[22]:


#Product Line Performance
st.title('Classic Models Business Data')
st.subheader('Product Line Performance')

#Kyle did this code
plot1 = st.columns(1)
with plot1[0]:
# Display numerical plot
    st.write('How are different product lines performing?')
    dropbox1 = st.selectbox('Select what you would like to compare', ['quantityOrdered', 'priceDifference', 'expectedProfit', 'profit', 'percentProfit'], key="classic")
    dropbox1_names = ['Quantity Ordered', 'Price Difference', 'Expected Profit', 'Profit', 'Percent Profit']
    fig = sns.catplot(data=cm_df, x="productLine", y=dropbox1, kind="box")
    plt.xlabel("Product Line")
    plt.ylabel(dropbox1)
    plt.xticks(rotation=45)
    
    st.pyplot(fig)
    
#NEW
plot11 = st.columns(1)
with plot11[0]:
    dropbox11 = st.selectbox('Select what you would like to compare', ['quantityOrdered', 'priceDifference', 'expectedProfit', 'profit', 'percentProfit'], key = 'models')
    dropbox11_names = ["Quantity Ordered", "Price Difference", "Expected Profit", "Profit", "Percent Profit"]
    fig, axes = plt.subplots(2,4, sharey=True)
    sns.histplot(ax=axes[0,0], data=PLvc, x=dropbox11)
    plt.xlabel(dropbox11)
    plt.ylabel("Count")
    sns.histplot(ax=axes[0,1], data=PLcc, x=dropbox11)
    sns.histplot(ax=axes[0,2], data=PLtb, x=dropbox11)
    sns.histplot(ax=axes[0,3], data=PLt, x=dropbox11)
    sns.histplot(ax=axes[1,0], data=PLs, x=dropbox11)
    sns.histplot(ax=axes[1,1], data=PLp, x=dropbox11)
    sns.histplot(ax=axes[1,2], data=PLm, x=dropbox11)
    st.pyplot(fig)
    
plot12 = st.columns(1)
with plot12[0]:
    dropbox12 = st.selectbox('Select what you would like to compare', ['quantityOrdered', 'priceDifference', 'expectedProfit', 'profit', 'percentProfit'], key = 'corvette')
    dropbox12_names = ["Quantity Ordered", "Price Difference", "Expected Profit", "Profit", "Percent Profit"]
    dropbox22 = st.selectbox('Select what you would like to compare', ['orderDate', 'shippedDate', 'paymentDate'], key='products')
    dropbox22_names = ['Order Date', 'Shipped Date', 'Payment Date']
    fig, axes = plt.subplots(2,4, sharey=True)
    sns.histplot(ax=axes[0,0], data=PLvc, x=dropbox22, y=dropbox12)
    plt.xlabel(dropbox22)
    plt.ylabel(dropbox12)
    axes[0, 0].axis('off')
    axes[0, 1].axis('off')
    axes[0, 2].axis('off')
    axes[0, 3].axis('off')
    axes[1, 0].axis('off')
    axes[1, 1].axis('off')
    axes[1, 2].axis('off')
    axes[1, 3].axis('off')
    sns.histplot(ax=axes[0,1], data=PLcc, x=dropbox22, y=dropbox12)
    sns.histplot(ax=axes[0,2], data=PLtb, x=dropbox22, y=dropbox12)
    sns.histplot(ax=axes[0,3], data=PLt, x=dropbox22, y=dropbox12)
    sns.histplot(ax=axes[1,0], data=PLs, x=dropbox22, y=dropbox12)
    sns.histplot(ax=axes[1,1], data=PLp, x=dropbox22, y=dropbox12)
    sns.histplot(ax=axes[1,2], data=PLm, x=dropbox22, y=dropbox12)
    st.pyplot(fig)
    
plot13=st.columns(1)
with plot13[0]:
    dropbox13 = st.selectbox('Select what you would like to compare', ['quantityOrdered', 'priceDifference', 'expectedProfit', 'profit', 'percentProfit'], key = 'camaro')
    dropbox13_names = ["Quantity Ordered", "Price Difference", "Expected Profit", "Profit", "Percent Profit"]
    dropbox23 = st.selectbox('Select what you would like to compare', ['orderDate', 'shippedDate', 'paymentDate'], key='accent')
    dropbox23_names = ['Order Date', 'Shipped Date', 'Payment Date']
    fig, axes = plt.subplots(2,4, sharey=True)
    sns.histplot(ax=axes[0,0], data=PLvc, x=dropbox23, y=dropbox13)
    plt.xlabel(dropbox23)
    plt.ylabel(dropbox13)
    axes[0, 0].axis('off')
    axes[0, 1].axis('off')
    axes[0, 2].axis('off')
    axes[0, 3].axis('off')
    axes[1, 0].axis('off')
    axes[1, 1].axis('off')
    axes[1, 2].axis('off')
    axes[1, 3].axis('off')
    sns.histplot(ax=axes[0,1], data=PLcc, x=dropbox23, y=dropbox13)
    sns.histplot(ax=axes[0,2], data=PLtb, x=dropbox23, y=dropbox13)
    sns.histplot(ax=axes[0,3], data=PLt, x=dropbox23, y=dropbox13)
    sns.histplot(ax=axes[1,0], data=PLs, x=dropbox23, y=dropbox13)
    sns.histplot(ax=axes[1,1], data=PLp, x=dropbox23, y=dropbox13)
    sns.histplot(ax=axes[1,2], data=PLm, x=dropbox23, y=dropbox13)
    
    st.pyplot(fig)

# plot14 = st.columns(1)
# with plot14[0]:
#     dropbox14 = st.selectbox('Select what you would like to compare', ['quantityInStock', 'buyPrice', 'quantityOrdered', 'profit', 'expectedProfit', 'priceDifference'], key='products3')
#     fig = plt.pie(data=cm_df_PL, x=cm_df_PL[dropbox14], labels = dropbox14)
#     st.pyplot(fig)
#NEW END
#Emily did this code
st.subheader('Vendor Performance')
plot2 = st.columns(1)
with plot2[0]:
# Display numerical plot
    st.write('How are different vendors performing?')
    dropbox2 = st.selectbox('Select what you would like to compare', ['quantityOrdered', 'amount', 'priceDifference', 'expectedProfit', 'profit'], key='vendors')
    dropbox2_names = ['Quantity Ordered', 'Revenue', 'Price Difference', 'Expected Profit', 'Profit']
    
    fig = sns.catplot(data=cm_df, x="productVendor", y=dropbox2, kind="box")
    plt.xlabel("Vendor")
    plt.ylabel(dropbox2)
    plt.xticks(rotation=45,fontsize=3)

    st.pyplot(fig)
    
    
#Sami did this code
st.subheader('Country Performance by Offices')
plot3 = st.columns(1)
with plot3[0]:
    # Display numerical plot
    st.write('How are offices in different countries performing?')
    dropbox3 = st.selectbox('Select what you would like to compare', ['quantityOrdered', 'amount', 'profit', 'expectedProfit', 'priceDifference', 'percentProfit'], key='country')
    dropbox3_names = ['Revenue', 'Quantity Ordered', 'Profit per Transaction', 'Expected Profit', 'Price Difference', 'Percent Profit']
    
    fig = sns.catplot(data=cm_df, x="country", y=dropbox3, kind="box")
    plt.xlabel("Country")
    plt.ylabel(dropbox3)
    plt.xticks(rotation=45)

    st.pyplot(fig)

#Hannah did this code
st.subheader('Country performance by Customers')
plot4 = st.columns(1)
with plot4[0]:
    # Display numerical plot
    st.write('How are different countries performing in terms of customer purchases?')
    dropbox4 = st.selectbox('Select what you would like to compare', ['quantityOrdered', 'amount', 'profit'],key='customer')
    dropbox4_names = ['Quantity Ordered', 'Revenue', 'Profit']
    
    fig = sns.catplot(data=cm_df, x="customerCountry", y=dropbox4, kind="box")
    plt.xlabel("Country")
    plt.ylabel(dropbox4)
    plt.xticks(rotation=45, fontsize=3)

    st.pyplot(fig)


# In[ ]:




