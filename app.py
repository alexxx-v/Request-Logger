from flask import Flask, request, render_template_string, redirect, url_for, session, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Замените на ваш собственный секретный ключ

# Список для хранения запросов
requests_log = []
count_requests = 0

# Словарь для хранения пользователей
users = {
    "admin": "password"  # Замените на ваши собственные учетные данные
}

# HTML-шаблон для отображения запросов с использованием Bootstrap и формы входа
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Request Logger</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <style>
        pre {
            white-space: pre-wrap; /* Позволяет переносить длинные строки */
            word-wrap: break-word; /* Переносит слова, если они слишком длинные */
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        {% if 'username' in session %}
            <div class="container">
                <div class="row">
                    <div class="col">
                        <form action="{{ url_for('clear_log') }}" method="post">
                            <button type="submit" class="btn btn-danger">Clear list</button>
                        </form>
                    </div>
                    <div class="col">
                    </div>
                    <div class="col float-right">
                        <form class="float-right" method="post" action="{{ url_for('logout') }}">
                            User: {{ session['username'] }}
                            <button type="submit" class="btn btn-secondary">Logout</button>
                        </form>
                    </div>
                </div>
            </div>
            <div class="mb-3">
                
            </div>
            
            <div class="table-responsive">
                <table class="table table-bordered w-100">
                    <thead class="thead-light">
                        <tr>
                            <th>ID</th>
                            <th>Date and Time</th>
                            <th>Method</th>
                            <th>IP Address</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for req in requests %}
                        <tr data-toggle="modal" data-target="#modal-{{ loop.index }}">
                            <td>{{ req.id }}</td>
                            <td>{{ req.timestamp }}</td>
                            <td>{{ req.method }}</td>
                            <td>{{ req.ip }}</td>
                        </tr>

                        <!-- Модальное окно для отображения заголовков и тела запроса -->
                        <div class="modal fade" id="modal-{{ loop.index }}" tabindex="-1" role="dialog" aria-labelledby="modalLabel-{{ loop.index }}" aria-hidden="true">
                            <div class="modal-dialog" role="document">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="modalLabel-{{ loop.index }}">Request Details</h5>
                                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div class="modal-body">
                                        <strong>Headers:</strong>
                                        <pre>{{ req.headers }}</pre>
                                        <strong>Body:</strong>
                                        <pre>{{ req.body }}</pre>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        {% else %}
            <h2>Login</h2>
            <form method="post" action="{{ url_for('login') }}">
                <label for="username">Username:</label>
                <input type="text" name="username" required>
                <br>
                <label for="password">Password:</label>
                <input type="password" name="password" required>
                <br>
                <button type="submit">Login</button>
            </form>
            {% if error %}
                <p style="color: red;">{{ error }}</p>
            {% endif %}
        {% endif %}
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr .net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
"""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username  # Сохраняем имя пользователя в сессии
            return redirect(url_for('index'))  # Перенаправляем на главную страницу
        else:
            return render_template_string(HTML_TEMPLATE, requests=requests_log, error="Invalid credentials")  # Отображаем ошибку
    return render_template_string(HTML_TEMPLATE, requests=requests_log)  # Отображаем форму входа

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Удаляем имя пользователя из сессии
    return redirect(url_for('index'))  # Перенаправляем на главную страницу

@app.route('/log', methods=['POST'])
def log_request():
    global count_requests
    # Сохраняем запрос
    now = datetime.now()
    count_requests += 1
    req_data = {
        'id': count_requests,
        'timestamp': now.strftime('%Y-%m-%d %H:%M:%S') + f".{now.microsecond // 1000:03d}",  # Сохраняем дату и время запроса с миллисекундами
        'method': request.method,
        'ip': request.headers.get('X-Real-Ip', request.remote_addr),  # Сохраняем IP-адрес из заголовка X-Real-Ip или используем remote_addr
        'headers': dict(request.headers),
        'body': request.get_data(as_text=True)
    }
    if count_requests >500:
        return jsonify({"error": "Too many requests"}), 429  # Возвращаем статус 429 и сообщение об ошибке
    else:
        requests_log.append(req_data)
        return '', 204  # Возвращаем статус 204 No Content

@app.route('/clear', methods=['POST'])
def clear_log():
    global count_requests
    # Очищаем лог запросов
    requests_log.clear()
    count_requests = 0
    return redirect(url_for('index'))  # Перенаправляем на главную страницу

@app.route('/')
def index():
    # Отображаем все сохраненные запросы
    return render_template_string(HTML_TEMPLATE, requests=requests_log)

if __name__ == '__main__':
    app.run(debug=True)