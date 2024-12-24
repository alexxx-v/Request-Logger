from flask import Flask, request, render_template_string, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from datetime import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()

# Список для хранения запросов
requests_log = []

# Словарь для хранения пользователей
users = {
    "admin": "password"  # Замените на ваши собственные учетные данные
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

# HTML-шаблон для отображения запросов с использованием Bootstrap
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
        <h1>Request Logger</h1>
        <h2>Received POST Requests</h2>
        <div class="mb-3">
            <form action="{{ url_for('clear_log') }}" method="post">
                <button type="submit" class="btn btn-danger">Clear Log</button>
            </form>
        </div>
        <div class="table-responsive">
            <table class="table table-bordered w-100">
                <thead class="thead-light">
                    <tr>
                        <th>Date and Time</th>
                        <th>Method</th>
                        <th>URL</th>
                    </tr>
                </thead>
                <tbody>
                    {% for req in requests %}
                    <tr data-toggle="modal" data-target="#modal-{{ loop.index }}">
                        <td>{{ req.timestamp }}</td>
                        <td>{{ req.method }}</td>
                        <td>{{ req.referer }}</td>
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
    </div>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
"""

@app.route('/log', methods=['POST'])
@auth.login_required
def log_request():
    # Сохраняем запрос
    now = datetime.now()
    req_data = {
        'timestamp': now.strftime('%Y-%m-%d %H:%M:%S') + f".{now.microsecond // 1000:03d}",  # Сохраняем дату и время запроса с миллисекундами
        'method': request.method,
        'referer': request.referrer or request.url,  # Сохраняем URL, с которого был запрос
        'headers': dict(request.headers),
        'body': request.get_data(as_text=True)
    }
    requests_log.append(req_data)
    return '', 204  # Возвращаем статус 204 No Content

@app.route('/clear', methods=['POST'])
@auth.login_required
def clear_log():
    # Очищаем лог запросов
    requests_log.clear()
    return redirect(url_for('index'))  # Перенаправляем на главную страницу

@app.route('/')
def index():
    # Отображаем все сохраненные запросы
    return render_template_string(HTML_TEMPLATE, requests=requests_log)

if __name__ == '__main__':
    app.run(debug=True)