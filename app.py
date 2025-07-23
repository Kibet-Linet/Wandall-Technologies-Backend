from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into environment locally

app = Flask(__name__)

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False') == 'True'

mail = Mail(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    try:
        msg = Message(
            subject=f"New Inquiry from {data.get('name')}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[os.getenv('TO_EMAIL')]
        )
        msg.reply_to = data.get('email')
        msg.html = f"""
        <div style="font-family: Arial, sans-serif; color: #333;">
          <h2 style="color: #2E86C1;">New Internet Plan Inquiry</h2>
          <p><strong>Package Type:</strong> {data.get('package')}</p>
          <p><strong>Project Type:</strong> {data.get('projectType')}</p>
          <p><strong>Cable Type:</strong> {data.get('cableType') or 'N/A'}</p>
          <p><strong>Number of Floors:</strong> {data.get('floors') or 'N/A'}</p>
          <p><strong>Number of Units:</strong> {data.get('units') or 'N/A'}</p>
          <hr style="border:none; border-top:1px solid #ddd; margin: 10px 0;">
          <h3>Contact Information</h3>
          <p><strong>Name / Company:</strong> {data.get('name')}</p>
          <p><strong>Email:</strong> {data.get('email')}</p>
          <p><strong>Phone:</strong> {data.get('phone')}</p>
          <p><strong>Location:</strong> {data.get('county')}, {data.get('town')}</p>
          <hr style="border:none; border-top:1px solid #ddd; margin: 10px 0;">
          <p style="font-size: 0.9em; color: #555;">This inquiry was submitted via the Wandall Technologies website.</p>
        </div>
        """
        mail.send(msg)
        return jsonify({'success': True, 'message': 'Email sent successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
