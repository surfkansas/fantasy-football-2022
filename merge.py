from turtle import pos
import pandas as pd
import os

df_full = None

os.makedirs('data/merged_csv', exist_ok=True)
os.makedirs('data/merged_feather', exist_ok=True)


for position in ['QB', 'RB', 'WR', 'TE', 'DST', 'K']:
    for root, dirs, files in os.walk('data/raw'):
        for file in files:
            if file.split('-')[1] == position:
                full_path = os.path.join(root,file)
                print(full_path)
                df = pd.read_csv(full_path)
                if df_full is None:
                    df_full = df
                else:
                    df_full = pd.concat([df_full, df])

df_full = df_full.sort_values(by=['year', 'week', 'fantasy_points', 'position', 'player_name'], ascending=False)

df_full = df_full.reset_index()

df_full.to_csv('data/merged_csv/ff.csv')

df_full.to_feather('data/merged_feather/ff.feather')
