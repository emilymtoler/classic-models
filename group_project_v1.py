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


# In[ ]:





# In[67]:


print(cm_df['salesRepEmployeeNumber'].unique)


# In[20]:


cm_df = cm_df.T.drop_duplicates().T
print(cm_df.columns)


# In[52]:


cm_df["profit"] = (cm_df["amount"]-cm_df["buyPrice"]*cm_df["quantityOrdered"])/(cm_df['amount'].sum())
cm_df["expectedProfit"] = cm_df["MSRP"]-cm_df["buyPrice"]
#print(cm_df.columns)
#print(cm_df[["profit","productName"]].groupby("productName").head[:5])


# In[53]:


fig = plt.figure(figsize=(9,7))
sns.boxplot(x="productLine", y="MSRP", data=cm_df)


# In[54]:


st.title('Classic Models Business Data')


# In[56]:


#Product Line Performance
st.subheader('Product Line Performance')

plot1 = st.columns(1)
with plot1[0]:
# Display numerical plot
    st.write('Comparing')
    dropbox1 = st.selectbox('Select what you would like to compare', ['MSRP', 'buyPrice', 'priceEach','profit'], key="products")
    dropbox1_names = ['MSRP', 'Buy Price', 'Price Each', 'Profit']
    
    fig = sns.catplot(data=cm_df, x="productLine", y=dropbox1, kind="box")
    #fig.set(xlabel="Product Line", ylabel=dropbox1_names)
    plt.xlabel("Product Line")
    plt.ylabel(dropbox1)
    plt.xticks(rotation=45)

    st.pyplot(fig)
    

st.subheader('Vendor Performance')
plot2 = st.columns(1)
with plot2[0]:
# Display numerical plot
    st.write('Comparing')
    dropbox1 = st.selectbox('Select what you would like to compare', ['profit', 'quantityOrdered', 'amount'], key='vendors')
    
    fig = sns.catplot(data=cm_df, x="productVendor", y=dropbox1, kind="box")
    #fig.set(xlabel="Product Line", ylabel=dropbox1_names)
    plt.xlabel("Vendor")
    plt.ylabel(dropbox1)
    plt.xticks(rotation=45,fontsize=3)

    st.pyplot(fig)
    
    
    
st.subheader('Office Country Performance')
plot3 = st.columns(1)
with plot3[0]:
    # Display numerical plot
    st.write('Performance by office country')
    dropbox1 = st.selectbox('Select what you would like to compare', ['profit', 'quantityOrdered', 'amount'], key='country')
    dropbox1_names = ['Profit', 'Amount', 'Quantity Ordered']
    
    fig = sns.catplot(data=cm_df, x="country", y=dropbox1, kind="box")
    #fig.set(xlabel="Product Line", ylabel=dropbox1_names)
    plt.xlabel("Country")
    plt.ylabel(dropbox1)
    plt.xticks(rotation=45)

    st.pyplot(fig)

st.subheader('Customer Country performance')
plot4 = st.columns(1)
with plot4[0]:
    # Display numerical plot
    st.write('Performance by Customer Country')
    dropbox1 = st.selectbox('Select what you would like to compare', ['profit', 'quantityOrdered', 'amount'],key='customer')
    dropbox1_names = ['Profit', 'Amount', 'Quantity Ordered']
    
    fig = sns.catplot(data=cm_df, x="customerCountry", y=dropbox1, kind="box")
    #fig.set(xlabel="Product Line", ylabel=dropbox1_names)
    plt.xlabel("Country")
    plt.ylabel(dropbox1)
    plt.xticks(rotation=45, fontsize=3)

    st.pyplot(fig)

