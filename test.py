import soccerdata as sd
import pandas as pd
import os



# def extract_columns_to_new_csv(input_filename, output_filename): # A function to make a final csv table with all required information
#     # Read with multi-index columns
#     df = pd.read_csv(input_filename, header=[0, 1])
#     df.columns = [(str(a).strip(), str(b).strip()) for a, b in df.columns] # Clean up column names by stripping whitespace
#     #print(df.columns.tolist()) # Print all column names for debugging
#     team_col = next((col for col in df.columns if col[0].lower() == 'team'), None) # Ensure case-insensitive match
#     gls_col = next((col for col in df.columns if col[1] == 'Gls'), None) # Match the second level of the multi-index
#     poss_col = next((col for col in df.columns if col[0] == 'Poss'), None) # Match the first level of the multi-index
#     #print(f"team_col: {team_col}, gls_col: {gls_col}, poss_col: {poss_col}") # Debugging output
#     df_selected = pd.DataFrame() # Create an empty DataFrame to store selected columns

#     if team_col: 
#         df_selected['team'] = df[team_col] 

#     if gls_col: 
#         df_selected['Gls'] = df[gls_col]
        
#     if poss_col:
#         df_selected['Poss'] = df[poss_col]

#     # df_selected.to_csv(output_filename, index=False)
#     return df_selected


# output_filename = 'selected_columns.csv'

# df_file1=extract_columns_to_new_csv('ENG-Premier Leaguestandard.csv', output_filename)
# df_file2=extract_columns_to_new_csv('ENG-Premier Leaguestandard.csv', output_filename)
# df_file3=extract_columns_to_new_csv('ENG-Premier Leaguekeeper.csv', output_filename)
# # Print the first few rows of the merged DataFrame for debugging

# # Replace 'Tkl' with the actual column you want from df_file2

# # Merge on 'team'
# merged_df = pd.merge(df_file1, df_file2, on='team', how='inner')

# print(merged_df)

fbref = sd.FBref(leagues="ENG-Premier League", seasons=2425)
df = fbref.read_team_season_stats(stat_type="standard")
df1 = fbref.read_team_season_stats(stat_type="passing")
df2 = fbref.read_team_season_stats(stat_type="keeper")
df3 = fbref.read_team_season_stats(stat_type="defense")
df4 = fbref.read_team_season_stats(stat_type="possession")
df5 = fbref.read_team_season_stats(stat_type="shooting")
df6 = fbref.read_team_season_stats(stat_type="goal_shot_creation")
df7 = fbref.read_team_season_stats(stat_type="misc")
df8 = fbref.read_team_season_stats(stat_type="playing_time")
df = df.reset_index()
df1 = df1.reset_index()
df2 = df2.reset_index()
df3 = df3.reset_index()
df4 = df4.reset_index()
df5 = df5.reset_index()
df6 = df6.reset_index()
df7 = df7.reset_index()
df8 = df8.reset_index()

# Flatten multi-index columns if present for all DataFrames
dfs = [df, df1, df2, df3, df4, df5, df6, df7, df8]
for i, d in enumerate(dfs):
    d.columns = [' '.join(col).strip() if isinstance(col, tuple) else col for col in d.columns]
    print(f"df{i} columns: {d.columns.tolist()}")  # Debug: print columns after flattening

# Use correct column names as per your CSVs and soccerdata
# For standard: 'Performance Gls', for passing: 'Performance Ast', etc.
df = df[['team', 'league', 'season', 'players_used', 'Performance Gls' , "Poss" , "Expected xAG" , "Expected xG" , "Per 90 Minutes G+A"]]
df1 = df1[['team', 'league', 'season', 'players_used', 'Ast']]
df2 = df2[['team', 'league', 'season', 'players_used', 'Performance Save%']]
df3 = df3[['team', 'league', 'season', 'players_used', 'Tackles Tkl']]
df4 = df4[['team', 'league', 'season', 'players_used']]
df5 = df5[['team', 'league', 'season', 'players_used']]
df6 = df6[['team', 'league', 'season', 'players_used']]
df7 = df7[['team', 'league', 'season', 'players_used']]
df8 = df8[['team', 'league', 'season', 'players_used']]


# Merge on the selected columns, always using the key columns to avoid merge errors and duplicates
res = df.copy()
res = res.merge(df1, on=['team', 'league', 'season', 'players_used'], how='outer')
res = res.merge(df2, on=['team', 'league', 'season', 'players_used'], how='outer')
res = res.merge(df3, on=['team', 'league', 'season', 'players_used'], how='outer')
res = res.merge(df4, on=['team', 'league', 'season', 'players_used'], how='outer')
res = res.merge(df5, on=['team', 'league', 'season', 'players_used'], how='outer')
res = res.merge(df6, on=['team', 'league', 'season', 'players_used'], how='outer')
res = res.merge(df7, on=['team', 'league', 'season', 'players_used'], how='outer')
res = res.merge(df8, on=['team', 'league', 'season', 'players_used'], how='outer')

# Display the full DataFrame
print(res)