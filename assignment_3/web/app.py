import os
import pandas as pd
import smtplib
import re  # For email validation
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from flask import Flask, request, render_template

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- CONFIGURATION (YOU MUST FILL THIS) ---
SENDER_EMAIL = "your_email@gmail.com"      # <--- PUT YOUR GMAIL HERE
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"    # <--- PUT APP PASSWORD HERE (See Step 4)

# --- 1. VALIDATION & TOPSIS LOGIC ---
def validate_and_run_topsis(file_path, weights_str, impacts_str, output_path):
    try:
        # Check 1: Read CSV
        try:
            df = pd.read_csv(file_path)
        except:
            return False, "Could not read file. Ensure it is a valid CSV."

        if df.shape[1] < 3:
            return False, "Input file must have 3 or more columns."

        # Check 2: Filter numeric columns
        df_numeric = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
        df_numeric.dropna(inplace=True)
        
        if df_numeric.empty:
            return False, "File must contain numeric values from 2nd column onwards."

        # Check 3: Comma Separation
        if ',' not in weights_str or ',' not in impacts_str:
            return False, "Weights and Impacts must be separated by commas (e.g., 1,1,1)."

        try:
            weights = [float(w) for w in weights_str.split(',')]
            impacts = impacts_str.split(',')
        except ValueError:
            return False, "Weights must be numeric."

        # Check 4: Count Mismatch
        if len(weights) != len(impacts) or len(weights) != df_numeric.shape[1]:
            return False, "Count Mismatch: Number of weights, impacts, and columns must be equal."
        
        # Check 5: Impacts Validity (+ or -)
        if not all(i.strip() in ['+', '-'] for i in impacts):
            return False, "Impacts must be either '+' or '-'."

        # --- TOPSIS CALCULATION ---
        rss = (df_numeric ** 2).sum() ** 0.5
        norm_df = df_numeric / rss
        weighted_df = norm_df * weights

        ideal_best = []
        ideal_worst = []
        
        for i, col in enumerate(weighted_df.columns):
            if impacts[i].strip() == '+':
                ideal_best.append(weighted_df[col].max())
                ideal_worst.append(weighted_df[col].min())
            else:
                ideal_best.append(weighted_df[col].min())
                ideal_worst.append(weighted_df[col].max())

        score_best = ((weighted_df - ideal_best) ** 2).sum(axis=1) ** 0.5
        score_worst = ((weighted_df - ideal_worst) ** 2).sum(axis=1) ** 0.5
        
        # Handle division by zero
        total_score = score_best + score_worst
        topsis_score = score_worst / total_score
        
        df['Topsis Score'] = topsis_score
        df['Rank'] = df['Topsis Score'].rank(ascending=False)
        
        df.to_csv(output_path, index=False)
        return True, "Success"
        
    except Exception as e:
        return False, f"System Error: {str(e)}"

# --- 2. EMAIL LOGIC ---
def send_email(receiver_email, filename):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = "TOPSIS Result File"
    
    body = "Please find attached the result file for your TOPSIS calculation."
    msg.attach(MIMEText(body, 'plain'))

    with open(filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename=result.csv")
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
    server.quit()

# --- 3. WEB ROUTES ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'file' not in request.files:
        return "No file uploaded"
    
    file = request.files['file']
    if file.filename == '':
        return "No file selected"
    
    weights = request.form['weights']
    impacts = request.form['impacts']
    email = request.form['email']

    # Email Format Validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return "<h3>Error: Invalid Email Format</h3>"

    input_path = os.path.join(UPLOAD_FOLDER, "input.csv")
    output_path = os.path.join(UPLOAD_FOLDER, "result.csv")
    file.save(input_path)

    success, message = validate_and_run_topsis(input_path, weights, impacts, output_path)

    if success:
        try:
            send_email(email, output_path)
            return f"<h3 style='color:green'>Success!</h3><p>Result sent to {email}</p>"
        except Exception as e:
            return f"<h3 style='color:orange'>Calculation Done, but Email Failed.</h3><p>{e}</p><p>Did you set up the App Password?</p>"
    else:
        return f"<h3 style='color:red'>Input Error</h3><p>{message}</p>"

if __name__ == '__main__':
    app.run(debug=True)