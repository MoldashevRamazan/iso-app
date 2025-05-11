from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from flask import Flask, render_template, request, send_file
from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas

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

selected_checks = []
result_percent = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    global selected_checks, result_percent
    if request.method == 'POST':
        selected_checks = request.form.getlist('check')
        total = len(checklist_items)
        result_percent = int((len(selected_checks) / total) * 100)
        return render_template('index.html', checklist=checklist_items, result=result_percent)
    return render_template('index.html', checklist=checklist_items)

@app.route('/download')
def download_pdf():
    buffer = BytesIO()
    
    # Регистрируем шрифт
    pdfmetrics.registerFont(TTFont('DejaVu', 'DejaVuSans.ttf'))
    
    # Только после регистрации создаём Canvas
    p = canvas.Canvas(buffer)
    p.setFont("DejaVu", 12)

    p.drawString(100, 800, "Отчёт по самооценке соответствия ISO 27001")
    p.drawString(100, 785, f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}")

    y = 750
    for item in selected_checks:
        p.drawString(100, y, f"- {item}")
        y -= 20

    p.drawString(100, y - 20, f"Итоговое соответствие: {result_percent}%")
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="iso27001_report.pdf", mimetype='application/pdf')
