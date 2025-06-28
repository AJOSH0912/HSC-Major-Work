import pandas as pd
import soccerdata as sd

mh = sd.MatchHistory(leagues="ENG-Premier League", seasons=2000)
mh1 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2001)
mh2 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2002)
mh3 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2003)
mh4 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2004)
mh5 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2005)
mh6 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2006)
mh7 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2007)
mh8 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2008)
mh9 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2009)
mh10 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2010)
mh11 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2011)
mh12 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2012)
mh13 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2013)
mh14 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2014)
mh15 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2015)
mh16 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2016)
mh17 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2017)
mh18 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2018)
mh19 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2019)
mh20 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2020)
mh21 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2021)
mh22 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2022)
mh23 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2023)
mh24 = sd.MatchHistory(leagues="ENG-Premier League", seasons=2024)

hist = mh.read_games()
hist.head()
hist1 = mh1.read_games()
hist2 = mh2.read_games()
hist3 = mh3.read_games()
hist4 = mh4.read_games()
hist5 = mh5.read_games()
hist6 = mh6.read_games()
hist7 = mh7.read_games()
hist8 = mh8.read_games()
hist9 = mh9.read_games()
hist10 = mh10.read_games()
hist11 = mh11.read_games()
hist12 = mh12.read_games()
hist13 = mh13.read_games()
hist14 = mh14.read_games()
hist15 = mh15.read_games()
hist16 = mh16.read_games()
hist17 = mh17.read_games()
hist18 = mh18.read_games()
hist19 = mh19.read_games()
hist20 = mh20.read_games()
hist21 = mh21.read_games()
hist22 = mh22.read_games()
hist23 = mh23.read_games()
hist24 = mh24.read_games()

hist.to_csv('data/Premier_League_2000.csv', index=False)
hist1.to_csv('data/Premier_League_2001.csv', index=False)
hist2.to_csv('data/Premier_League_2002.csv', index=False)
hist3.to_csv('data/Premier_League_2003.csv', index=False)
hist4.to_csv('data/Premier_League_2004.csv', index=False)
hist5.to_csv('data/Premier_League_2005.csv', index=False)
hist6.to_csv('data/Premier_League_2006.csv', index=False)
hist7.to_csv('data/Premier_League_2007.csv', index=False)
hist8.to_csv('data/Premier_League_2008.csv', index=False)
hist9.to_csv('data/Premier_League_2009.csv', index=False)
hist10.to_csv('data/Premier_League_2010.csv', index=False)
hist11.to_csv('data/Premier_League_2011.csv', index=False)
hist12.to_csv('data/Premier_League_2012.csv', index=False)
hist13.to_csv('data/Premier_League_2013.csv', index=False)
hist14.to_csv('data/Premier_League_2014.csv', index=False)
hist15.to_csv('data/Premier_League_2015.csv', index=False)
hist16.to_csv('data/Premier_League_2016.csv', index=False)
hist17.to_csv('data/Premier_League_2017.csv', index=False)
hist18.to_csv('data/Premier_League_2018.csv', index=False)
hist19.to_csv('data/Premier_League_2019.csv', index=False)
hist20.to_csv('data/Premier_League_2020.csv', index=False)
hist21.to_csv('data/Premier_League_2021.csv', index=False)
hist22.to_csv('data/Premier_League_2022.csv', index=False)
hist23.to_csv('data/Premier_League_2023.csv', index=False)
hist24.to_csv('data/Premier_League_2024.csv', index=False)



# function to load the raw csv data into data frame

def load_selected_columns(csv_path):



    use_cols=['date','home_team','away_team','FTHG','FTAG','FTR','HTHG','HTAG','HTR','referee','HS','AS','HST','AST','HF','AF','HC','AC','HY','AY','HR','AR','B365H','B365D','B365A','BWH','BWD','BWA','WHH','WHD','WHA']

    return pd.read_csv(csv_path,usecols=use_cols)



# union of all data frame into one for storing in a text file.

def union_all(dfs):



    return pd.concat(dfs, ignore_index=True)




df_2004 = load_selected_columns("data/Premier_League_2004.csv")

df_2005 = load_selected_columns("data/Premier_League_2005.csv")

df_2006 = load_selected_columns("data/Premier_League_2006.csv")

df_2007 = load_selected_columns("data/Premier_League_2007.csv")

df_2008 = load_selected_columns("data/Premier_League_2008.csv")

df_2009 = load_selected_columns("data/Premier_League_2009.csv")

df_2010 = load_selected_columns("data/Premier_League_2010.csv")

df_2011 = load_selected_columns("data/Premier_League_2011.csv")

df_2012 = load_selected_columns("data/Premier_League_2012.csv")

df_2013 = load_selected_columns("data/Premier_League_2013.csv")

df_2014 = load_selected_columns("data/Premier_League_2014.csv")

df_2015 = load_selected_columns("data/Premier_League_2015.csv")

df_2016 = load_selected_columns("data/Premier_League_2016.csv")

df_2017 = load_selected_columns("data/Premier_League_2017.csv")

df_2018 = load_selected_columns("data/Premier_League_2018.csv")

df_2019 = load_selected_columns("data/Premier_League_2019.csv")

df_2020 = load_selected_columns("data/Premier_League_2020.csv")

df_2021 = load_selected_columns("data/Premier_League_2021.csv")

df_2022 = load_selected_columns("data/Premier_League_2022.csv")

df_2023 = load_selected_columns("data/Premier_League_2023.csv")

df_2024 = load_selected_columns("data/Premier_League_2024.csv")



merge_df = union_all([df_2004,df_2005,df_2006, df_2007,df_2008, df_2009, df_2010,df_2011,df_2012,df_2013,df_2014,df_2015,df_2016,df_2017,df_2018,df_2019,df_2020,df_2021,df_2022,df_2023,df_2024])

merge_df.to_csv('data/merged_data2.csv',index=False)

print("Data Merged Successfully!")
