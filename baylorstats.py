from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go

url = "https://cfbstats.com/2024/team/51/index.html"  # Replace with the actual URL for other teams

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
req = Request(url, headers=headers)
response = urlopen(req)
soup = BeautifulSoup(response, 'html.parser')

#table = soup.find('table', {'class': 'team_stats_table'})

rows = soup.find_all('tr')
  

data = []

for row in rows[1:]:  # Skip header
    columns = row.find_all('td')

    if len(columns) >= 6: 
        year = columns[0].text.strip()
        scoring_points = columns[1].text.strip()
        passing_yards = columns[2].text.strip()
        third_down_conversion = columns[3].text.strip()
        field_goal_success = columns[4].text.strip()
        attendance = columns[5].text.strip()
    
        data.append([year, scoring_points, passing_yards, third_down_conversion, field_goal_success, attendance])

df = pd.DataFrame(data, columns=['Year', 'Scoring Points', 'Passing Yards', '3rd Down Conversion %', 'Field Goals Success %', 'Attendance'])

df['Scoring Points'] = pd.to_numeric(df['Scoring Points'], errors='coerce')
df['Passing Yards'] = pd.to_numeric(df['Passing Yards'], errors='coerce')
df['3rd Down Conversion %'] = pd.to_numeric(df['3rd Down Conversion %'], errors='coerce')
df['Field Goals Success %'] = pd.to_numeric(df['Field Goals Success %'], errors='coerce')
df['Attendance'] = pd.to_numeric(df['Attendance'], errors='coerce')

best_worst = {
    'Best Year for Scoring Points': df['Scoring Points'].idxmax(),
    'Worst Year for Scoring Points': df['Scoring Points'].idxmin(),
    'Best Year for Passing Yards': df['Passing Yards'].idxmax(),
    'Worst Year for Passing Yards': df['Passing Yards'].idxmin(),
    'Best Year for 3rd Down Conversion %': df['3rd Down Conversion %'].idxmax(),
    'Worst Year for 3rd Down Conversion %': df['3rd Down Conversion %'].idxmin(),
    'Best Year for Field Goals Success %': df['Field Goals Success %'].idxmax(),
    'Worst Year for Field Goals Success %': df['Field Goals Success %'].idxmin(),
}

total_attendance = df.groupby('Year')['Attendance'].sum().sort_values(ascending=False).head(5)

fig = go.bar(total_attendance, x=total_attendance.index, y=total_attendance.values, 
             labels={'x': 'Teams', 'y': 'Attendance'},
             title='Biggest Rivalry based on Attendance')



fig.show()