import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Сначала загружаем данные из базы (это должно быть выше)
df_2024 = pd.read_sql_query("SELECT * FROM Season_2024_Analysis", conn)

# 2. И только ПОТОМ чиним левую ось (конвертируем в числа)
df_2024['points'] = pd.to_numeric(df_2024['points'], errors='coerce').fillna(0)

try:
    # 2. ПОДКЛЮЧЕНИЕ
    conn = sqlite3.connect(db_path)

    # 3. ЗАГРУЗКА ДАННЫХ (создаем ту самую переменную df_2024)
    query = "SELECT * FROM Season_2024_Analysis"
    df_2024 = pd.read_sql_query(query, conn)
    conn.close()

    if not df_2024.empty:
        print("✅ Данные загружены. Начинаю строить график...")

        # 4. ПОДГОТОВКА ДАННЫХ ДЛЯ ГРАФИКА
        # Считаем сумму очков каждой команды в каждом раунде
        team_progress = df_2024.groupby(['round', 'team'])['points'].sum().unstack().fillna(0)

        # Считаем накопительную сумму (Cumulative Sum)
        cumulative_points = team_progress.cumsum()

        # 5. ВИЗУАЛИЗАЦИЯ
        plt.figure(figsize=(12, 7))

        # Выбираем топ-4 команды 2024 года
        top_teams = ['Red Bull', 'McLaren', 'Ferrari', 'Mercedes']

        for team in top_teams:
            if team in cumulative_points.columns:
                plt.plot(cumulative_points.index, cumulative_points[team], label=team, marker='o', linewidth=2)

        plt.title('Битва конструкторов 2024: Накопительные очки', fontsize=16)
        plt.xlabel('Раунд чемпионата', fontsize=12)
        plt.ylabel('Сумма очков', fontsize=12)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)

        # Сохраняем результат
        plt.savefig('f1_2024_battle.png')
        print("💾 График сохранен как f1_2024_battle.png")
        plt.show()

    else:
        print("⚠️ Таблица Season_2024_Analysis пуста.")

except Exception as e:
    print(f"❌ Произошла ошибка: {e}")