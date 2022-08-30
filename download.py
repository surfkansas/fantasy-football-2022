import os
import requests
from bs4 import BeautifulSoup
import csv

key = '48ca46aa7d721af4d58dccc0c249a1c4'

csv_headers = {
    'QB': [
        'year', 'week', 'position', 'player_code', 'player_name', 
        'team', 'opponent', 'home_away', 'fantasy_points',
        'pass_attempts', 'pass_completions', 'pass_yards', 'pass_touchdowns', 'pass_interceptions', 'pass_2points', 
        'rush_attempts', 'rush_yards', 'rush_touchdowns', 'rush_2points', 
        'receptions', 'reception_yards', 'reception_touchdowns', 'reception_2points',
        'fumbles_lost', 'fumble_recovery_touchdowns',
    ],
    'K': [
        'year', 'week', 'position', 'player_code', 'player_name', 
        'team', 'opponent', 'home_away', 'fantasy_points',
        'pat_attempts', 'pat_made', 'field_goal_att', 'field_goal_made', 'field_goal_made_50_yards'
    ],
    'DST': [
        'year', 'week', 'position', 'player_code', 'player_name', 
        'team', 'opponent', 'home_away', 'fantasy_points',
        'sacks', 'interceptions', 'safeties', 'fumble_recoveries', 
        'blocked_kicks', 'defensive_touchdowns', 'points_against',
        'passing_yards_allowed', 'rushing_yards_allowed', 'total_yards_allowed'
    ]
}

csv_headers['RB'] = csv_headers['QB']
csv_headers['WR'] = csv_headers['QB']
csv_headers['TE'] = csv_headers['QB']

os.makedirs('data/raw', exist_ok=True)

for position in csv_headers:
    for year in range(2012,2022):
        for week in range(1, 19):

            path = f'data/raw/{year}-{position}-WK{week}.csv'

            if os.path.exists(path):
                continue
            
            url = f'https://www.footballdb.com/fantasy-football/index.html?pos={position}&yr={year}&wk={week}&key={key}'
            print(url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
            }
            resp = requests.get(url, headers=headers)
            soup = BeautifulSoup(resp.text, 'html.parser')

            table = soup.find('table', {'class':'statistics scrollable'})

            rows = []
            for tr in table.find('tbody').find_all('tr'):
                cell_num = 0
                row = [year,week,position]
                for td in tr.find_all('td'):
                    if cell_num == 0:
                        row.append(td.find('a')['href'].split('/')[2])
                        row.append(td.find('a').text)
                    elif cell_num == 1:
                        lh_team = td.contents[0].text
                        rh_team = td.contents[1].text
                        if '@' in lh_team:
                            row.append(rh_team)
                            row.append(lh_team.replace('@', ''))
                            row.append('home')
                        else:
                            row.append(lh_team)
                            row.append(rh_team.replace('@', ''))
                            row.append('away')
                    else:
                        row.append(td.text)
                        pass
                    cell_num += 1

                rows.append(row)

            with open(path, 'w') as f:
                writer = csv.writer(f)
                writer.writerow(csv_headers[position])
                writer.writerows(rows)