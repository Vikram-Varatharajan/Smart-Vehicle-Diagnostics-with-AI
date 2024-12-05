from flask import Flask, request, jsonify, render_template, url_for
from werkzeug.utils import secure_filename
from groq import Groq
from config import GROQ_API_KEY
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

client = Groq(api_key=GROQ_API_KEY)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

def is_car_related(query):
    car_keywords = ['car', 'engine', 'wheel', 'brake', 'bumper', 'light', 'oil', 'tire', 'vehicle', 'automobile', 
                'transmission', 'clutch', 'suspension', 'steering', 'battery', 'radiator', 'alternator', 'exhaust',
                'fuel', 'gearbox', 'coolant', 'ignition', 'dashboard', 'seatbelt', 'airbag', 'windshield', 'muffler',
                'catalytic converter', 'turbocharger', 'fuel injector', 'axle', 'differential', 'spark plug', 'thermostat','how','to','fix','it','Explain']

    return any(word in query.lower() for word in car_keywords)

@app.route('/troubleshoot', methods=['POST'])
def troubleshoot():
    user_input = request.form.get('message')
    image_file = request.files.get('image')
    filename = None

    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            image_file.save(image_path)
        except Exception as e:
            return jsonify({'error': f'Failed to save image: {e}'}), 500

    if user_input and is_car_related(user_input):
        message_content = user_input + (f" (Image: {filename})" if filename else "")
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": message_content}],
                model="llama3-70b-8192",
            )
            ai_response = chat_completion.choices[0].message.content.strip()
            return jsonify({'response': ai_response})
        except Exception as e:
            return jsonify({'error': 'Failed to get response from GROQ API'}), 500
    else:
        return jsonify({'error': 'The query does not appear to be car-related or is not supported.'}), 400

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
