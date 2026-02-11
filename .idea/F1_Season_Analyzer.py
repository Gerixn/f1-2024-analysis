import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

db_path = r'C:\Users\Artem\DataGripProjects\f1_project\identifier.sqlite'

try:
    conn = sqlite3.connect(db_path)
    # Load 2021 data
    df_2021 = pd.read_sql_query("SELECT * FROM Season_2021_Analysis", conn)
    conn.close()

    if not df_2021.empty:
        # Convert points to numeric to fix Y-axis
        df_2021['points'] = pd.to_numeric(df_2021['points'], errors='coerce').fillna(0)

        # Calculating cumulative points for drivers
        driver_progress = df_2021.groupby(['round', 'driver'])['points'].sum().unstack().fillna(0)
        cumulative_points = driver_progress.cumsum()

        # Visualization
        plt.figure(figsize=(12, 7))

        # Focus on the main rivals
        rivals = ['Max Verstappen', 'Lewis Hamilton']
        colors = {'Max Verstappen': '#0600EF', 'Lewis Hamilton': '#00D2BE'} # Red Bull blue vs Mercedes teal

        for driver in rivals:
            if driver in cumulative_points.columns:
                plt.plot(cumulative_points.index, cumulative_points[driver],
                         label=driver, marker='o', color=colors[driver], linewidth=3)

        plt.title('2021 Title Battle: Hamilton vs Verstappen', fontsize=16)
        plt.xlabel('Round (1 to 22)', fontsize=12)
        plt.ylabel('Cumulative Points', fontsize=12)
        plt.xticks(range(1, 23)) # 2021 had 22 rounds
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)

        plt.savefig('f1_2021_title_battle.png')
        df_2021.to_csv('f1_2021_cleaned.csv', index=False)
        print("✅ 2021 Analysis complete. Files saved.")
        plt.show()

except Exception as e:
    print(f"❌ Error: {e}")