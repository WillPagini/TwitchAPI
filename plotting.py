import numpy as np 
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('darkgrid')
import query

df = query.return_query()

# Get the average viewes per streamer
df2 = df.groupby(['user_name'], as_index=False).mean().groupby('user_name')['max_views'].mean().reset_index()

df2 = df2.sort_values(['max_views'], ascending=False).head(10)
print(type(df2))

#df.sort_values(['user_name', 'max_views'], ascending=False).groupby('item').head(10)

plt.figure(figsize=(25,6))
sns.barplot(x=df2['user_name'] , y=df2['max_views'], palette="Set2")
plt.show()