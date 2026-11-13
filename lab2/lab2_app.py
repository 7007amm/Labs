import sqlite3
from flask import Flask, request

app = Flask(__name__)

# Создаем базу данных в памяти при запуске
def init_db():
    conn = sqlite3.connect("meme.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS secrets")
    cursor.execute("CREATE TABLE secrets (id INTEGER PRIMARY KEY, password TEXT)")
    cursor.execute("INSERT INTO secrets (password) VALUES ('67676767')")
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username", "Аноним")
        password = request.form.get("password", "")

        conn = sqlite3.connect("meme.db")
        cursor = conn.cursor()

        # УЯЗВИМОСТЬ 1: SQL Injection (A03:2021 - Injection)
        # Данные подставляются напрямую в запрос через f-строку
        query = f"SELECT * FROM secrets WHERE password = '{password}'"
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()

        if result:
            # УЯЗВИМОСТЬ 2: Reflected XSS (A03:2021 - Injection)
            # Имя пользователя выводится в HTML без экранирования
            return f"""
            <div style="text-align: center; font-family: sans-serif; margin-top: 50px;">
                <h2>Привет, {username}! Доступ открыт.</h2>
                <h1 style="font-size: 200px; margin: 0; color: #ff4500;">67</h1>
            </div>
            """
        else:
            return "<h3>Неверный пароль! Подсказка: попробуй 67676767</h3><a href='/'>Назад</a>"

    return """
    <div style="font-family: sans-serif; max-width: 400px; margin: 50px auto;">
        <h2>Секретный портал</h2>
        <form method="POST">
            <label>Скажи, как тебя зовут:</label><br>
            <input type="text" name="username" required style="width: 100%; margin-bottom: 10px;"><br>
            <label>Введи пароль 67676767 для открытия секретной картинки:</label><br>
            <input type="text" name="password" required style="width: 100%; margin-bottom: 10px;"><br>
            <button type="submit">Открыть</button>
        </form>
    </div>
    """

if __name__ == "__main__":
    init_db()
    app.run(debug=False)
