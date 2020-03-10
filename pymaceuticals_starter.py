#!/usr/bin/env python
# coding: utf-8

# ## Observations and Insights

# 

# ## Dependencies and starter code

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
import numpy as np
from scipy.stats import sem

# Study data files
mouse_metadata = "data/Mouse_metadata.csv"
study_results = "data/Study_results.csv"

# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata)
study_results = pd.read_csv(study_results)


# In[2]:


# Combine the data into a single dataset
combined_df = pd.merge(study_results, mouse_metadata, how="left", on="Mouse ID")


# In[3]:


#show dataframe
pd.DataFrame(combined_df)


# ## Summary statistics

# In[4]:


# Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor volume for each regimen
mean = combined_df['Tumor Volume (mm3)'].mean()
median = combined_df['Tumor Volume (mm3)'].median()
variance = np.var(combined_df['Tumor Volume (mm3)'],ddof = 0)
std_dev = np.std(combined_df['Tumor Volume (mm3)'],ddof = 0)
SEM = combined_df['Tumor Volume (mm3)'].sem(axis=None, ddof=0)

print(f'The mean is {mean}.')
print(f'The median is {median}.')
print(f'The variance is {variance}.')
print(f'The standard deviance is {std_dev}.')
print(f'The standard error is {SEM}.')


# ## Bar plots

# In[5]:


# Generate a bar plot showing number of data points for each treatment regimen using pandas
treatment_group = combined_df.groupby(['Drug Regimen']).count()
panda_bar = treatment_group['Mouse ID'].plot(kind='bar', title ="V comp", figsize=(15, 10), legend=True, fontsize=12)

panda_bar


# In[6]:


# Generate a bar plot showing number of data points for each treatment regimen using pyplot
treatment_group_count = combined_df.groupby(['Drug Regimen']).count()
treatment_group = combined_df.groupby('Drug Regimen')

y_axis = treatment_group_count["Mouse ID"]
x_axis = combined_df['Drug Regimen'].unique()
plt.bar(x_axis, y_axis)
plt.xlabel('Drug Regimen')
plt.ylabel('Data Points')
plt.xticks(rotation="vertical")


# ## Pie plots

# In[7]:


# Generate a pie plot showing the distribution of female versus male mice using pandas
mouse_sex = combined_df.groupby(['Sex']).count()
plot = mouse_sex.plot.pie(y='Mouse ID', figsize=(5, 5))


# In[8]:


# Generate a pie plot showing the distribution of female versus male mice using pyplot
mouse_sex = combined_df.groupby(['Sex']).count()
sizes = mouse_sex['Mouse ID']
labels = ['Male','Female']
colors = ["red","blue"]
explode = (0,0)

plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct="%1.1f%%", shadow=True, startangle=140)


# ## Quartiles, outliers and boxplots

# In[45]:


# Calculate the final tumor volume of each mouse across four of the most promising treatment regimens. Calculate the IQR and quantitatively determine if there are any potential outliers.

#find top treatments regimens
top_check = combined_df.groupby(['Drug Regimen']).mean()
top_four = top_check.nsmallest(4,['Tumor Volume (mm3)'])
top_four

#separate each drug regimen
ramicane = combined_df.loc[combined_df['Drug Regimen'] == 'Ramicane']
capomulin = combined_df.loc[combined_df['Drug Regimen'] == 'Capomulin']
propriva = combined_df.loc[combined_df['Drug Regimen'] == 'Propriva']
ceftamin = combined_df.loc[combined_df['Drug Regimen'] == 'Ceftamin']


quartiles = top_four['Tumor Volume (mm3)'].quantile([.25,.5,.75])
lowerq = quartiles[0.25]
upperq = quartiles[0.75]
iqr = upperq-lowerq

iqr
print(f"The interquartile range of temperatures is: {iqr}")


# In[50]:


# Generate a box plot of the final tumor volume of each mouse across four regimens of interest

boxplot = ramicane.boxplot(column=['Tumor Volume (mm3)'])


# In[51]:


boxplot2 = capomulin.boxplot(column=['Tumor Volume (mm3)'])


# In[52]:


boxplot3 = propriva.boxplot(column=['Tumor Volume (mm3)'])


# In[53]:


boxplot4 = ceftamin.boxplot(column=['Tumor Volume (mm3)'])


# ## Line and scatter plots

# In[54]:


# Generate a line plot of time point versus tumor volume for a mouse treated with Capomulin
capomulin = combined_df.loc[combined_df['Drug Regimen'] == 'Capomulin']
time_point = capomulin['Timepoint']
tumor_vol = capomulin['Tumor Volume (mm3)']

#plt.plot(time_point, tumor_vol)
capomulin.groupby('Timepoint')['Tumor Volume (mm3)'].plot(legend=True)


# In[55]:


# Generate a scatter plot of mouse weight versus average tumor volume for the Capomulin regimen

capomulin = combined_df.loc[combined_df['Drug Regimen'] == 'Capomulin']
weight = capomulin['Weight (g)']
tumor_vol = capomulin['Tumor Volume (mm3)']

scatter = plt.scatter(weight, tumor_vol, marker="o", facecolors="red", edgecolors="black")                                                                                     
scatter


# In[56]:


# Calculate the correlation coefficient and linear regression model for mouse weight and average tumor volume for the Capomulin regimen
x_values = weight
y_values = tumor_vol
vc_slope, vc_int, vc_r, vc_p, vc_std_err = st.linregress(weight, tumor_vol)
vc_fit = vc_slope * weight + vc_int
regress_values = x_values * vc_slope + vc_int
plt.scatter(x_values, y_values)
plt.plot(x_values,regress_values,"r-")
plt.show()


# In[ ]:




