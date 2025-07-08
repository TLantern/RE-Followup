"""
Flask webhook for incoming SMS and serve dashboard.
"""
import os, logging
from flask import Flask, request, render_template
from .agent_notifier import notify_agent
from .lead_collector import load_leads_from_csv

app = Flask(__name__, static_folder='static', template_folder='templates')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/sms', methods=['POST'])
def sms_reply():
    frm = request.form.get('From'); body = request.form.get('Body')
    logger.info(f"Reply from {frm}: {body}")
    notify_agent(frm, body)
    return '', 200

@app.route('/')
def dashboard():
    leads = load_leads_from_csv()
    for lead in leads: lead['status'] = 'Sent'
    demo = os.getenv('DEMO_VIDEO_URL', '')
    return render_template('index.html', leads=leads, demo_video=demo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT',5000)))