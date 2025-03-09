#!/usr/bin/env python
# coding: utf-8

# In[4]:


get_ipython().system('pip install pandas')
get_ipython().system('pip install numpy ')
get_ipython().system('pip install matplotlib ')
get_ipython().system('pip install seaborn ')
get_ipython().system('pip install folium')


# In[9]:



# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap


# In[10]:


# Define important columns to load (for memory efficiency)
use_cols = ['ID', 'Start_Time', 'End_Time', 'Severity', 'State', 'City',
            'Weather_Condition', 'Visibility(mi)', 'Temperature(F)', 'Humidity(%)', 
            'Start_Lat', 'Start_Lng']

# Load dataset in chunks to handle large file
chunk_size = 100000  # Adjust based on system memory
chunks = pd.read_csv("US_Accidents_March23.csv", usecols=use_cols, chunksize=chunk_size, low_memory=False)

# Concatenate all chunks into a single DataFrame
df = pd.concat(chunks, ignore_index=True)

# Display dataset information
df.info()


# In[11]:


# Convert date columns to datetime format
df['Start_Time'] = pd.to_datetime(df['Start_Time'])
df['End_Time'] = pd.to_datetime(df['End_Time'])

# Calculate accident duration (in minutes)
df['Duration'] = (df['End_Time'] - df['Start_Time']).dt.total_seconds() / 60

# Drop rows with missing values for accurate analysis
df.dropna(inplace=True)

# Display first 5 rows after preprocessing
df.head()


# In[12]:


plt.figure(figsize=(6, 4))
sns.countplot(x='Severity', data=df, palette='coolwarm')
plt.title("Accident Severity Distribution")
plt.xlabel("Severity Level")
plt.ylabel("Count")
plt.show()


# In[13]:


plt.figure(figsize=(12, 5))
df['State'].value_counts().head(15).plot(kind='bar', color='blue')
plt.title("Top 15 States with Most Accidents")
plt.xlabel("State")
plt.ylabel("Number of Accidents")
plt.show()


# In[14]:


# Extract latitude and longitude for heatmap
heatmap_data = df[['Start_Lat', 'Start_Lng']].dropna()

# Define map center
map_center = [heatmap_data['Start_Lat'].mean(), heatmap_data['Start_Lng'].mean()]
m = folium.Map(location=map_center, zoom_start=4)

# Add heatmap layer
HeatMap(data=heatmap_data, radius=8).add_to(m)

# Save and display the map
m.save("accident_hotspots.html")
m  


# In[ ]:




