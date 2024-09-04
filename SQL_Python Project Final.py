import pandas as pd
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib_inline
import seaborn as sns
import scipy.sparse as sp

# Database connection details
server = 'DESKTOP-E9FRPJF\SQLEXPRESS01'
database = 'Baseball'
username = 'Test'
password = '0772'

# Create the connection string
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=Yes'
conn = pyodbc.connect(conn_str)

#2. Query Data from Each Table
#Query All Data from Each Table:
# Query to retrieve data from the Batting table
query_batting = "SELECT * FROM dbo.Batting"
df_batting = pd.read_sql(query_batting, conn)
print("Batting Table:")
print(df_batting.head())
df_batting.info()
 ##############################################################################   
# Q1 Calculation the total number of triples per year.
# Q1.1. Query to retrieve triples (3B) per year
query_triples = """
SELECT yearID, SUM(CAST([3B] AS INT)) AS total_triples
FROM dbo.Batting
GROUP BY yearID
ORDER BY yearID
"""

df_triples = pd.read_sql(query_triples, conn)
print(df_triples)
print(df_triples.head())

# Plotting the histogram
df_triples = pd.read_sql(query_triples, conn)

# Plotting the histogram
plt.figure(figsize=(14, 7))  # Increase figure size
plt.bar(df_triples['yearID'].astype(str), df_triples['total_triples'], color='skyblue')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Total Triples', fontsize=14)
plt.title('Histogram of Triples (3B) per Year', fontsize=16)

# Reduce number of x-axis ticks
plt.xticks(ticks=df_triples['yearID'][::5].astype(str), rotation=45, ha='right', fontsize=12)

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

"""
.1.2 Top 20 Years for Triples: 
The plot highlights the top 20 years with the highest total number of triples in Major League Baseball. 
By focusing on these years, we can identify periods when teams had exceptional performance in hitting triples.
"""

# Sample DataFrame 'df_triples'
# df_triples = pd.read_sql(query_triples, conn)  # Assuming you've already done this

# Step 1: Aggregate data by year and sort to get the top 20 years
top_years = df_triples.groupby('yearID')['total_triples'].sum().nlargest(20).index

# Filter the DataFrame to include only top 20 years
filtered_df = df_triples[df_triples['yearID'].isin(top_years)]

# Sort the filtered DataFrame by year
filtered_df = filtered_df.sort_values('yearID')

print(filtered_df)
print(filtered_df.head())

# Step 2: Plot the data
plt.figure(figsize=(14, 7))
plt.bar(filtered_df['yearID'].astype(str), filtered_df['total_triples'], color='skyblue')
plt.xlabel('Year')
plt.ylabel('Total Triples')
plt.title('Histogram of Triples (3B) per Year')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#Or cleared trend 

#Or can display based on range of the years based on the years Range

years = df_triples['yearID']
n = len(years)
chunk_size = 10  # Number of years per plot

for i in range(0, n, chunk_size):
    plt.figure(figsize=(14, 7))
    df_chunk = df_triples.iloc[i:i+chunk_size]
    plt.bar(df_chunk['yearID'].astype(str), df_chunk['total_triples'], color='skyblue')
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Total Triples', fontsize=14)
    plt.title(f'Histogram of Triples (3B) per Year ({df_chunk["yearID"].iloc[0]}-{df_chunk["yearID"].iloc[-1]})', fontsize=16)
    plt.xticks(rotation=45, ha='right', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


################################################################
# Q2. To calculate the player age per years 
# Define the SQL query
query_ppl = """SELECT * FROM dbo.People"""

# Execute the query and fetch the data into a DataFrame
df_ppl = pd.read_sql(query_ppl, conn)

# Print the entire DataFrame
print(df_ppl)

print(df_ppl.head())

# # Close the database connection
# conn.close()

# Query to calculate player's age
query_age = """
SELECT p.playerID, p.nameFirst, p.nameLast, 
       (YEAR(GETDATE()) - p.birthYear) - 
       CASE 
           WHEN MONTH(GETDATE()) < p.birthMonth 
                OR (MONTH(GETDATE()) = p.birthMonth AND DAY(GETDATE()) < p.birthDay)
           THEN 1 
           ELSE 0 
       END AS Age
FROM dbo.People p
"""

# Execute the query and fetch the data into a DataFrame
df_age = pd.read_sql(query_age, conn)



print(df_age)
# Define age bins
bins = [0, 20, 30, 40, 50, 60, 70, 80]
labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80']
df_age['Age Group'] = pd.cut(df_age['Age'], bins=bins, labels=labels, right=False)

# Count the number of players in each age group
age_group_counts = df_age['Age Group'].value_counts()

print(age_group_counts)

# Plotting the pie chart
plt.figure(figsize=(8, 8))
plt.pie(age_group_counts, labels=age_group_counts.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired(range(len(age_group_counts))))
plt.title('Age Distribution of Players')
plt.show()

##################################################################
# Q3. Top 50 Players with Most RBI from 2015-2018
# Shows players with the most RBIs over this period.

# Query to find the player with the most RBI from 2015-2018
# Create the connection string
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=Yes'
conn = pyodbc.connect(conn_str)

query_rbi = """
SELECT Top (50) playerID, SUM(CAST(RBI AS INT)) AS Total_RBI 
FROM dbo.Batting
WHERE yearID BETWEEN 2015 AND 2018
GROUP BY playerID
ORDER BY Total_RBI DESC
"""

df_rbi = pd.read_sql(query_rbi, conn)

print(df_rbi)

print(df_rbi.head())
# Plotting the bar plot
plt.figure(figsize=(12, 6))
sns.barplot(x='playerID', y='Total_RBI', data=df_rbi, palette='viridis')
plt.xlabel('Player ID')
plt.ylabel('Total RBI')
plt.title('Top 3 Players with Most RBI (2015-2018)')
plt.xticks(rotation=45)
plt.show()


#############################################################################
#Q4 Total Games Played by Each Team
# Shows the total games played by each team.

# Query to find total games played by each team
query_total_games = """
SELECT Top (20)teamID, SUM(CAST(G AS INT)) AS total_games
FROM dbo.Teams
GROUP BY teamID
ORDER BY total_games DESC
"""

df_total_games = pd.read_sql(query_total_games, conn)

print(df_total_games)

# Plotting the bar plot
plt.figure(figsize=(12, 6))
sns.barplot(x='teamID', y='total_games', data=df_total_games, palette='coolwarm')
plt.xlabel('Team ID')
plt.ylabel('Total Games Played')
plt.title('Total Games Played by Each Team')
plt.xticks(rotation=45)
plt.show()

#Or # Plotting the pie chart to find total games played


plt.figure(figsize=(10, 8))
plt.pie(df_total_games['total_games'], labels=df_total_games['teamID'], autopct='%1.1f%%', colors=plt.cm.Paired(range(len(df_total_games))))
plt.title('Proportion of Total Games Played by Each Team (Top 50)')
plt.show()


###################################################
# Q5. Total Double Plays (GIDP) for Albert Pujols in 2016
# Shows the total double plays for a specific player in a specific year.

# Query to find the total GIDP for Albert Pujols in 2016
query_gidp = """
SELECT SUM(CAST(GIDP AS INT)) AS Total_GIDP
FROM dbo.Batting
WHERE playerID = 'pujolal01' 
  AND yearID = 2016
"""
print(df_gidp)
#######################################################
# Q6. Top 50 Teams with Most Home Runs in a Single Season
# Displays the team with the highest number of home runs in a season.

# Query to retrieve the maximum home runs per year and team
query_home_runs = """
SELECT TOP(50) yearID, teamID, MAX(HR) AS max_HR
FROM dbo.Teams
GROUP BY yearID, teamID
ORDER BY yearID, teamID
"""

df_home_runs = pd.read_sql(query_home_runs, conn)
print(df_home_runs)

# Convert max_HR to numeric
df_home_runs['max_HR'] = pd.to_numeric(df_home_runs['max_HR'], errors='coerce')

# Verify the data types and values
print("Data Types:")
print(df_home_runs.dtypes)
print("\nFirst 10 Rows:")
print(df_home_runs.head(10))

# Check for unique values in max_HR
print("\nUnique max_HR values:")
print(df_home_runs['max_HR'].unique())

# Plotting
plt.figure(figsize=(14, 7))
plt.bar(df_home_runs['yearID'].astype(str) + '-' + df_home_runs['teamID'], df_home_runs['max_HR'], color='skyblue')
plt.xlabel('Year-Team')
plt.ylabel('Max Home Runs')
plt.title('Maximum Home Runs (HR) by Team per Year')
plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()
#######################################################################

# Q7. Active Players Who Played at Least 50 Games
# Displays active players who have played at least 50 games.
# # Query to find active players who played at least 50 games

query_active_players = """
SELECT TOP(100) playerID, SUM(CAST(G AS INT)) AS total_games
FROM dbo.Batting
GROUP BY playerID
HAVING SUM(CAST(G AS INT)) >= 50
ORDER BY total_games DESC
"""

# Fetch the data into a DataFrame
df_active_players = pd.read_sql(query_active_players, conn)

# Print the DataFrame to check the data
print(df_active_players)
print(df_active_players.head())


# Plotting the total games played by active players
plt.figure(figsize=(14, 8))
sns.barplot(x='playerID', y='total_games', data=df_active_players, palette='coolwarm')
plt.xlabel('Player ID')
plt.ylabel('Total Games Played')
plt.title('Total Games Played by Active Players (50+ Games)')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
################################################################################################################
# Q8. Line Plot of Team Wins Over Time
# Shows the trend of wins for each team over the years.

# Query to retrieve total wins per team over the years
query_team_wins = """
SELECT Top(100) yearID, teamID, SUM(CAST(W AS INT)) AS total_wins
FROM dbo.Teams
GROUP BY yearID, teamID
ORDER BY yearID, teamID
"""

df_team_wins = pd.read_sql(query_team_wins, conn)

print(df_team_wins)

# # Plotting the line plot
# plt.figure(figsize=(14, 8))
# sns.lineplot(x='yearID', y='total_wins', hue='teamID', data=df_team_wins, marker='o')
# plt.xlabel('Year')
# plt.ylabel('Total Wins')
# plt.title('Total Wins per Team Over Time')
# plt.legend(title='Team ID', bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# Plotting the line plot
plt.figure(figsize=(15, 8))
sns.lineplot(x='yearID', y='total_wins', hue='teamID', data=df_team_wins, marker='o')

# Add annotations for each point
for _, row in df_team_wins.iterrows():
    plt.text(row['yearID'], row['total_wins'], row['teamID'], 
             ha='center', va='bottom', fontsize=8, color='black')

plt.xlabel('Year')
plt.ylabel('Total Wins')
plt.title('Total Wins per Team Over Time')
plt.legend(title='Team ID', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#################################################################################################
# 2. Box Plot of Home Runs (HR) by League (lgID)
# Displays the distribution of home runs by league, showing variability and outliers.

# Query to retrieve home runs (HR) by league
query_hr_by_league = """
SELECT lgID, HR
FROM dbo.Teams
"""

df_hr_by_league = pd.read_sql(query_hr_by_league, conn)

print(df_hr_by_league)

# Convert HR to numeric
df_hr_by_league['HR'] = pd.to_numeric(df_hr_by_league['HR'], errors='coerce')
# Plotting the box plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='lgID', y='HR', data=df_hr_by_league, palette='pastel')
plt.xlabel('League ID')
plt.ylabel('Home Runs')
plt.title('Distribution of Home Runs by League')
plt.show()
#########################################################################################################################
# 3. Heatmap of Batting Statistics by Year and Team
# Visualizes batting statistics such as total runs (R) by year and team using a heatmap

# Query to retrieve total runs (R) by year and team
query_batting_stats = """
SELECT TOP(100) yearID, teamID, SUM(CAST(R AS INT)) AS total_runs
FROM dbo.Batting
GROUP BY yearID, teamID
ORDER BY yearID, teamID
"""

df_batting_stats = pd.read_sql(query_batting_stats, conn)

print(df_batting_stats)

# Convert total_runs to numeric if necessary
df_batting_stats['total_runs'] = pd.to_numeric(df_batting_stats['total_runs'], errors='coerce')

# Pivot the DataFrame for heatmap
pivot_table = df_batting_stats.pivot(index='yearID', columns='teamID', values='total_runs')

# Plotting the heatmap

plt.figure(figsize=(16, 12))
sns.heatmap(pivot_table, cmap='YlGnBu', annot=True, fmt='.0f', linewidths=.5, annot_kws={"size": 10})  # Increase or decrease size as needed
plt.xlabel('Team ID', fontsize=14)
plt.ylabel('Year', fontsize=14)
plt.title('Heatmap of Total Runs by Year and Team', fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.show()