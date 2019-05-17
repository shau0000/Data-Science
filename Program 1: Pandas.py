Assignment 2 - Pandas Introduction
All questions are weighted the same in this assignment.

Part 1
The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on All Time Olympic Games Medals, and does some basic data cleaning.

The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.


import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
    return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero()


Question 1
Which country has won the most gold medals in summer games?

This function should return a single string value.

def answer_one():
    return df.loc[df["Gold"] == max(df["Gold"])].index.format()[0]
answer_one()

Question 2
Which country had the biggest difference between their summer and winter gold medal counts?

This function should return a single string value.

def answer_two():
    return (df['Gold'] - df['Gold.1']).argmax()
    
Question 3
Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count?

Summer Gold−Winter GoldTotal Gold
Summer Gold−Winter GoldTotal Gold
 
Only include countries that have won at least 1 gold in both summer and winter.

This function should return a single string value.

def answer_three():
    only_gold = df[(df['Gold'] > 0) & (df['Gold.1'] > 0 )]
    new=((only_gold['Gold'] - only_gold['Gold.1']).abs()/(only_gold['Gold'] + only_gold['Gold.1'] + only_gold['Gold.2']))
    return new.argmax()
    
    
Question 4
Write a function that creates a Series called "Points" which is a weighted value where each gold medal (Gold.2) counts for 3 points, silver medals (Silver.2) for 2 points, and bronze medals (Bronze.2) for 1 point. The function should return only the column (a Series object) which you created, with the country names as indices.

This function should return a Series named Points of length 146

def answer_four():
    df['points']= (df['Gold.2']*3 +df['Silver.2']*2 + df['Bronze.2']*1 )
    return df['points']
    
    
Part 2
For the next set of questions, we will be using census data from the United States Census Bureau. Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. See this document for a description of the variable names.

The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.

Question 5
Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)

This function should return a single string value.

census_df = pd.read_csv('census.csv')
census_df.head()

def answer_five():
    return census_df[census_df["SUMLEV"] == 50].groupby('STNAME')['CTYNAME'].count().argmax()
    

Question 6
Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use CENSUS2010POP.

This function should return a list of string values.
def answer_six():
    return census_df[census_df["SUMLEV"] == 50].groupby('STNAME')['CENSUS2010POP'].apply(lambda x: x.nlargest(3).sum()).nlargest(3).index.format()


Question 7
Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)

e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.

This function should return a single string value.

def answer_seven():
    census_df["Min"] = census_df.loc[census_df["SUMLEV"] == 50, ["POPESTIMATE2010", "POPESTIMATE2011", "POPESTIMATE2012", "POPESTIMATE2013", "POPESTIMATE2014", "POPESTIMATE2015"]].min(axis=1)
    census_df["Max"] = census_df.loc[census_df["SUMLEV"] == 50, ["POPESTIMATE2010", "POPESTIMATE2011", "POPESTIMATE2012", "POPESTIMATE2013", "POPESTIMATE2014", "POPESTIMATE2015"]].max(axis=1)
    census_df["PopGrowth"] = census_df["Max"] - census_df["Min"]
    return census_df.loc[census_df["PopGrowth"] == census_df["PopGrowth"].max(), "CTYNAME"].max()
    
    
Question 8
In this datafile, the United States is broken up into four regions using the "REGION" column.

Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.

This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).

def answer_eight():
    return census_df.loc[((census_df["REGION"] == 1) | (census_df["REGION"] == 2)) & (census_df["CTYNAME"].str.startswith('Washington')) & (census_df["POPESTIMATE2015"] > census_df["POPESTIMATE2014"]), ['STNAME', 'CTYNAME']]
    
    
   
