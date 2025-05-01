from flask import Flask, render_template, request

app = Flask(__name__)

checklist_items = [
    "Есть политика информационной безопасности",
    "Назначен ответственный за ИБ",
    "Регулярно проводится анализ рисков",
    "Внедрена система управления доступом",
    "Ведется аудит доступа к информации",
    "Проводится резервное копирование",
    "Обновления безопасности устанавливаются регулярно",
    "Пользователи проходят обучение по ИБ",
    "Инциденты безопасности регистрируются",
    "Доступ к ИТ-системам разделяется по ролям"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        answers = request.form.getlist('check')
        total = len(checklist_items)
        checked = len(answers)
        percent = round((checked / total) * 100)
        return render_template('index.html', checklist=checklist_items, result=percent)
    return render_template('index.html', checklist=checklist_items)

if __name__ == '__main__':
    app.run(debug=True)
