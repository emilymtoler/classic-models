#!/usr/bin/env python
# coding: utf-8

# In[6]:


import mysql.connector as mysqlcon
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


# In[7]:


#create connection to mysql server on your computer
mysqlConnection = mysqlcon.connect(user='test1',
                                 password = 'Test1234#',
                                 host='3.16.213.2')
print("Connection succeeded.")


# In[8]:


#use connection you just created
mysqlCursor = mysqlConnection.cursor()
print("Cursor connected again!")


# In[9]:


new_query = "SELECT * FROM classicmodels.products AS p \
    JOIN classicmodels.orderdetails AS o \
    ON o.productCode = p.productCode;"
mysqlCursor.execute(new_query, params=None, multi=True)
print("Query executed!!")


# In[10]:


#fetch remaining results if any
mysqlCursor.fetchall()


# In[12]:


import pymysql
from sqlalchemy import create_engine
import sqlalchemy
sqlEngineStr = "mysql+pymysql://test1:Test1234#@3.16.213.2:3306/classicmodels"
sqlEngine = create_engine(sqlEngineStr)
print("Engine created!")


# In[13]:


cm_sql = pd.read_sql_query(new_query, mysqlConnection)
print("Dataframe created. :)))))")
print(cm_sql)


# In[14]:


q = '''ALTER TABLE classicmodels.customers
RENAME COLUMN country to customerCountry;'''


#mysqlCursor.execute(q)
print("Exe")


# In[15]:


query2 = "SELECT * from classicmodels.products AS p \
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
mysqlCursor.execute(query2, params=None, multi=True)
print("2nd Done!")


# In[16]:


mysqlCursor.fetchall()


# In[17]:


cm_df = pd.read_sql_query(query2, mysqlConnection)
print("Dataframe 2 created.")
print(cm_df)


# In[18]:


cm_df.drop(columns = ["productDescription","phone","addressLine1","addressLine2","postalCode","checkNumber","comments", "requiredDate","status", "email", "extension","creditLimit", "customerNumber","orderNumber"], inplace = True)


# In[67]:


print(cm_df['salesRepEmployeeNumber'].unique)


# In[20]:


cm_df = cm_df.T.drop_duplicates().T
print(cm_df.columns)


# In[52]:


cm_df["profit"] = (cm_df["priceEach"]-cm_df["buyPrice"])*cm_df["quantityOrdered"]
cm_df["expectedProfit"] = (cm_df["MSRP"]-cm_df["buyPrice"])*cm_df['quantityOrdered']
cm_df['percentProfit'] = (cm_df['amount'] - cm_df['buyPrice']*cm_df['quantityOrdered'])/(cm_df['amount'].sum())
cm_df['priceDifference'] = cm_df['MSRP'] - cm_df['priceEach']
#print(cm_df[["profit","productName"]].groupby("productName").head[:5])


# In[54]:


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


# In[56]:


#Product Line Performance
st.title('Classic Models Business Data')
st.subheader('Product Line Performance')

plot1 = st.columns(1)
with plot1[0]:
# Display numerical plot
    st.write('How are different product lines performing?')
    dropbox1 = st.selectbox('Select what you would like to compare', ['quantityOrdered', 'priceDifference', 'expectedProfit', 'profit', 'percentProfit'], key="products")
    dropbox1_names = ['Quantity Ordered', 'Price Difference', 'Expected Profit', 'Profit', 'Percent Profit']
    
    fig = sns.catplot(data=cm_df, x="productLine", y=dropbox1, kind="box")
    plt.xlabel("Product Line")
    plt.ylabel(dropbox1)
    plt.xticks(rotation=45)

    st.pyplot(fig)
    

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

