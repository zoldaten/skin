from flask import Flask, request, render_template_string, redirect, url_for, flash, session
import os
import base64
import json
import requests

app = Flask(__name__)
app.secret_key = 'your-secret-key' 

HTML_TEMPLATE = '''
<!doctype html>
<title>Загрузка изображения</title>
<h1>Загрузите изображение для анализа</h1>

<form method=post enctype=multipart/form-data>
  <input type=file name=file required>
  <input type=submit value=Загрузить>
</form>

{% if result %}
<h2>Результат:</h2>
<pre>{{ result }}</pre>
{% endif %}

{% with messages = get_flashed_messages() %}
  {% if messages %}
  <ul>
    {% for message in messages %}
      <li>{{ message }}</li>
    {% endfor %}
  </ul>
  {% endif %}
{% endwith %}
'''

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def process_image(image_path, question_text):
    #<<your code here>>
    if response.status_code == 200:
        content = response.json().get("choices")[0].get("message").get('content')
        # сохраняем в файл
        with open('response.json', 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        return content
    else:
        return f"Error {response.status_code}: {response.text}"

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filename)
            question_text = 'Какое кожное заболевание ты видишь на картинке'
            result = process_image(filename, question_text)
            os.remove(filename)

            # Сохраняем результат в сессию для передачи после редиректа
            session['result'] = result
            # Перенаправляем клиента на GET запрос (PRG)
            return redirect(url_for('upload_file'))
        else:
            flash("Ошибка загрузки файла.")
            return redirect(url_for('upload_file'))

    # Метод GET — отображаем форму и, если есть, результат из сессии
    result = session.pop('result', None)  # достаем и удаляем из сессии
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(debug=True)
