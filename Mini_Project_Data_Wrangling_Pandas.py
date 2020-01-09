#!/usr/bin/env python
# coding: utf-8

# # Mini-Project: Data Wrangling and Transformation with Pandas
# 
# Working with tabular data is a necessity for anyone with enterprises having a majority of their data in relational databases and flat files. This mini-project is adopted from the excellent tutorial on pandas by Brandon Rhodes which you have watched earlier in the Data Wrangling Unit. In this mini-project, we will be looking at some interesting data based on movie data from the IMDB.
# 
# This assignment should help you reinforce the concepts you learnt in the curriculum for Data Wrangling and sharpen your skills in using Pandas. Good Luck!

# ### Please make sure you have one of the more recent versions of Pandas

# In[1]:


from platform import python_version

print(python_version())


# In[2]:


import pandas as pd
import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


pd.__version__


# In[4]:


import os
os.chdir('C:/Users/BNi/Documents/ML Track/projects/Mni_pandas')


# ## Taking a look at the Movies dataset
# This data shows the movies based on their title and the year of release

# In[5]:


movies = pd.read_csv('titles.csv.bz2', compression='bz2')
movies.info()


# In[6]:


movies.head(3)


# ## Taking a look at the Cast dataset
# 
# This data shows the cast (actors, actresses, supporting roles) for each movie
# 
# - The attribute `n` basically tells the importance of the cast role, lower the number, more important the role.
# - Supporting cast usually don't have any value for `n`

# In[7]:


cast = pd.read_csv('cast.csv.bz2', compression='bz2')
cast.info()


# In[8]:


cast.head(10)


# ## Taking a look at the Release dataset
# 
# This data shows details of when each movie was release in each country with the release date

# In[9]:


release_dates = pd.read_csv('release_dates.csv.bz2', compression='bz2', parse_dates=['date'], infer_datetime_format=True)
release_dates.info()


# In[10]:


release_dates.head()


# # Section I - Basic Querying, Filtering and Transformations

# ### What is the total number of movies?

# In[11]:


len(movies)


# ### List all Batman movies ever made

# In[12]:


batman_df = movies[movies.title == 'Batman']
print('Total Batman Movies:', len(batman_df))
batman_df


# ### List all Batman movies ever made - the right approach

# In[13]:


batman_df = movies[movies.title.str.contains('Batman', case=False)]
print('Total Batman Movies:', len(batman_df))
batman_df.head(10)


# ### Display the top 15 Batman movies in the order they were released

# In[14]:


batman_df.sort_values(by=['year'], ascending=True).iloc[:15]


# ### Section I - Q1 : List all the 'Harry Potter' movies from the most recent to the earliest

# In[15]:


Harry_Potter_df = movies[movies.title.str.contains('Harry Potter', case=False)]
print('Total Harry Potter:', len(Harry_Potter_df))
Harry_Potter_df.sort_values(by=['year'], ascending=False)


# ### How many movies were made in the year 2017?

# In[16]:


len(movies[movies.year == 2017])


# ### Section I - Q2 : How many movies were made in the year 2015?

# In[17]:


len(movies[movies.year == 2015])


# ### Section I - Q3 : How many movies were made from 2000 till 2018?
# - You can chain multiple conditions using OR (`|`) as well as AND (`&`) depending on the condition

# In[18]:


len(movies[(movies.year >= 2000) & (movies.year <= 2018)])


# ### Section I - Q4: How many movies are titled "Hamlet"?

# In[19]:


Hamlet_df = movies[movies.title == 'Hamlet']
print('Total Hamlet:', len(Hamlet_df))
#Hamlet_df.sort_values(by=['year'], ascending=False)


# ### Section I - Q5: List all movies titled "Hamlet" 
# - The movies should only have been released on or after the year 2000
# - Display the movies based on the year they were released (earliest to most recent)

# In[20]:


Hamlet_df = movies[(movies.title == 'Hamlet') & (movies.year >= 2000)]
Hamlet_df.sort_values(by=['year'], ascending=False)


# ### Section I - Q6: How many roles in the movie "Inception" are of the supporting cast (extra credits)
# - supporting cast are NOT ranked by an "n" value (NaN)
# - check for how to filter based on nulls

# In[21]:


num_supp = cast[cast.title == 'Inception'].n.isna().sum()
print('Number of supporting cast: ', num_supp)


# ### Section I - Q7: How many roles in the movie "Inception" are of the main cast
# - main cast always have an 'n' value

# In[22]:


num_main = cast[cast.title == 'Inception'].n.notnull().sum()
print('Number of main cast: ', num_main)


# ### Section I - Q8: Show the top ten cast (actors\actresses) in the movie "Inception" 
# - support cast always have an 'n' value
# - remember to sort!

# In[23]:


cast[cast.title == 'Inception'].sort_values('n').head(10)


# ### Section I - Q9:
# 
# (A) List all movies where there was a character 'Albus Dumbledore' 
# 
# (B) Now modify the above to show only the actors who played the character 'Albus Dumbledore'
# - For Part (B) remember the same actor might play the same role in multiple movies

# In[24]:


A = cast[cast.character == 'Albus Dumbledore']
A


# In[25]:


B = A.drop_duplicates(subset=['name'],keep = 'first')
B.name


# ### Section I - Q10:
# 
# (A) How many roles has 'Keanu Reeves' played throughout his career?
# 
# (B) List the leading roles that 'Keanu Reeves' played on or after 1999 in order by year.

# In[26]:


cast.head(3)


# In[27]:


A = cast[cast.name == 'Keanu Reeves'].drop_duplicates(subset=['character'],keep = 'first')
print('Number of roles Keanu Reeves played: ', A.character.count())


# In[28]:


B = A[(A.year >=1999) & (A.n == 1)].sort_values(['n','year'])
B.loc[:,['year','character']]


# ### Section I - Q11: 
# 
# (A) List the total number of actor and actress roles available from 1950 - 1960
# 
# (B) List the total number of actor and actress roles available from 2007 - 2017

# In[29]:


A = cast[(cast.year >= 1950) & (cast.year <= 1960)].drop_duplicates(subset = 'character').character.count()
print('total number of actor and actress roles available from 1950 - 1960: ', A)


# In[30]:


B = cast[(cast.year >= 2007) & (cast.year <= 2017)].drop_duplicates(subset = 'character').character.count()
print('total number of actor and actress roles available from 2007 - 2017: ', B)


# ### Section I - Q12: 
# 
# (A) List the total number of leading roles available from 2000 to present
# 
# (B) List the total number of non-leading roles available from 2000 - present (exclude support cast)
# 
# (C) List the total number of support\extra-credit roles available from 2000 - present

# In[31]:


cast[(cast.year >= 2000) & (cast.year <= 2020) & (cast.n == 1)]. drop_duplicates(subset = 'character').character.count()


# In[32]:


cast[(cast.year >= 2000) & (cast.year <= 2020) & (cast.n != 1) & (cast.n.notnull())]. drop_duplicates(subset = 'character').character.count()


# In[33]:


cast[(cast.year >= 2000) & (cast.year <= 2020) & (cast.n.isna())]. drop_duplicates(subset = 'character').character.count()


# # Section II - Aggregations, Transformations and Visualizations

# ## What are the top ten most common movie names of all time?
# 

# In[34]:


movies.head()


# In[35]:


top_ten = movies.title.value_counts()[:10]
top_ten


# ### Plot the top ten common movie names of all time

# In[36]:


top_ten.plot(kind='barh')


# ### Section II - Q1:  Which years in the 2000s saw the most movies released? (Show top 3)

# In[37]:


year_count = release_dates[(release_dates.year >=2000) & (release_dates.year < 2010)].year.value_counts()[:3]
year_count


# ### Section II - Q2: # Plot the total number of films released per-decade (1890, 1900, 1910,....)
# - Hint: Dividing the year and multiplying with a number might give you the decade the year falls into!
# - You might need to sort before plotting

# In[38]:


release_dates['decade'] = release_dates.year//10 * 10
release_dates.sort_values('decade', inplace = True)
decade_count = release_dates.decade.value_counts().sort_index()
decade_count.plot(kind='barh')


# ### Section II - Q3: 
# 
# (A) What are the top 10 most common character names in movie history?
# 
# (B) Who are the top 10 people most often credited as "Herself" in movie history?
# 
# (C) Who are the top 10 people most often credited as "Himself" in movie history?

# In[39]:


cast.character.value_counts()[:10]


# In[40]:


cast[cast.character == 'Herself'].name.value_counts()[:10]


# In[41]:


cast[cast.character == 'Himself'].name.value_counts()[:10]


# ### Section II - Q4: 
# 
# (A) What are the top 10 most frequent roles that start with the word "Zombie"?
# 
# (B) What are the top 10 most frequent roles that start with the word "Police"?
# 
# - Hint: The `startswith()` function might be useful

# In[42]:


cast[cast.character.str.startswith('Zombie')].character.value_counts()[:10]


# In[43]:


cast[cast.character.str.startswith('Police')].character.value_counts()[:10]


# ### Section II - Q5: Plot how many roles 'Keanu Reeves' has played in each year of his career.

# In[44]:


num_roles = cast[cast.name == 'Keanu Reeves'].year.value_counts().sort_index()
num_roles.plot(kind='barh')


# ### Section II - Q6: Plot the cast positions (n-values) of Keanu Reeve's roles through his career over the years.
# 

# In[45]:


cast_pos = cast[(cast.name == 'Keanu Reeves') & (cast.n.notnull())].groupby('year').n.mean().sort_index()
cast_pos.plot()


# ### Section II - Q7: Plot the number of "Hamlet" films made by each decade

# In[46]:


cast['decade'] = cast.year // 10 * 10
num_ham = cast[cast.title.str.contains('Hamlet')].sort_values('decade').decade.value_counts().sort_index()
num_ham.plot()


# ### Section II - Q8: 
# 
# (A) How many leading roles were available to both actors and actresses, in the 1960s (1960-1969)?
# 
# (B) How many leading roles were available to both actors and actresses, in the 2000s (2000-2009)?
# 
# - Hint: A specific value of n might indicate a leading role

# In[47]:


A = cast[(cast.decade == 1960) & (cast.n == 1)].drop_duplicates('character').character.count()
print(' roles were available: ', A)


# In[48]:


B = cast[(cast.decade == 2000) & (cast.n == 1)].drop_duplicates('character').character.count()
print(' roles were available: ', B)


# ### Section II - Q9: List, in order by year, each of the films in which Frank Oz has played more than 1 role.

# In[49]:


cast_film = cast[cast.name == 'Frank Oz'].drop_duplicates(subset='title').set_index('title')

cast_film[cast[cast.name == 'Frank Oz'].groupby('title').character.count() > 1].year.sort_values()


# ### Section II - Q10: List each of the characters that Frank Oz has portrayed at least twice

# In[50]:


cast_role = cast[cast.name == 'Frank Oz'].drop_duplicates(subset='character').set_index('character')
print(cast_role[cast[cast.name == 'Frank Oz'].groupby('character').character.count() > 1 ].index.tolist())


# # Section III - Advanced Merging, Querying and Visualizations

# ## Make a bar plot with the following conditions
# - Frequency of the number of movies with "Christmas" in their title 
# - Movies should be such that they are released in the USA.
# - Show the frequency plot by month

# In[51]:


christmas = release_dates[(release_dates.title.str.contains('Christmas')) & (release_dates.country == 'USA')]
christmas.date.dt.month.value_counts().sort_index().plot(kind='bar')


# ### Section III - Q1: Make a bar plot with the following conditions
# - Frequency of the number of movies with "Summer" in their title 
# - Movies should be such that they are released in the USA.
# - Show the frequency plot by month

# In[52]:


christmas = release_dates[(release_dates.title.str.contains('Summer')) & (release_dates.country == 'USA')]
christmas.date.dt.month.value_counts().sort_index().plot(kind='bar')


# ### Section III - Q2: Make a bar plot with the following conditions
# - Frequency of the number of movies with "Action" in their title 
# - Movies should be such that they are released in the USA.
# - Show the frequency plot by week

# In[53]:


christmas = release_dates[(release_dates.title.str.contains('Action')) & (release_dates.country == 'USA')]
christmas.date.dt.week.value_counts().sort_index().plot(kind='bar')


# ### Section III - Q3: Show all the movies in which Keanu Reeves has played the lead role along with their   release date in the USA sorted by the date of release
# - Hint: You might need to join or merge two datasets!

# In[54]:


result  = pd.merge(cast,release_dates, on = ['title','year'])
result.head()


# In[55]:


result[(result.name == 'Keanu Reeves') & (result.n == 1) & (result.country == 'USA')].sort_values('date').set_index('date').title


# ### Section III - Q4: Make a bar plot showing the months in which movies with Keanu Reeves tend to be released in the USA?

# In[61]:


result_USA = result[(result.name == 'Keanu Reeves') & (result.country == 'USA')]
result_USA.date.dt.month.value_counts().sort_index().plot(kind='bar')


# ### Section III - Q5: Make a bar plot showing the years in which movies with Ian McKellen tend to be released in the USA?

# In[62]:


result_USA = result[(result.name == 'Ian McKellen') & (result.country == 'USA')]
result_USA.date.dt.year.value_counts().sort_index().plot(kind='bar')

