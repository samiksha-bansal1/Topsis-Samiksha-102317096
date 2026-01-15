from flask import Flask, render_template, request, redirect, url_for, session
import os
from topsis_samiksha_102317096 import validate_input, apply_topsis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Optional email imports
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def send_email(receiver_email, attachment_path):
    """
    Send email with TOPSIS result attached
    Uses environment variables for credentials
    """
    try:
        sender_email = os.getenv('SENDER_EMAIL')
        app_password = os.getenv('APP_PASSWORD')
        
        if not sender_email or not app_password:
            print("Error: Email credentials not found in .env file")
            return False
        
        msg = EmailMessage()
        msg['Subject'] = 'TOPSIS Analysis Result'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content('Dear User,\n\nYour TOPSIS analysis has been completed successfully.\nPlease find the result file attached.\n\nBest regards,\nTOPSIS Web Service')
        
        # Attach the result file
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        
        msg.add_attachment(file_data, maintype='application', subtype='csv', filename=file_name)
        
        # Send email via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    # Get flash messages if any
    toast = session.pop('toast', False)
    error = session.pop('error', None)

    if request.method == "POST":
        try:
            # Get form inputs
            file = request.files.get("file")
            weights_raw = request.form.get("weights", "").strip()
            impacts_raw = request.form.get("impacts", "").strip()
            email = request.form.get("email", "").strip()

            # Validation
            if not file or not file.filename:
                raise ValueError("Please upload a CSV file")
            
            if not weights_raw or not impacts_raw or not email:
                raise ValueError("All fields are required")
            
            # Validate email format
            if '@' not in email or '.' not in email.split('@')[-1]:
                raise ValueError("Invalid email format")
            
            # Check file extension
            if not file.filename.endswith('.csv'):
                raise ValueError("Only CSV files are allowed")

            # Save uploaded file
            input_path = os.path.join(UPLOAD_FOLDER, "input.csv")
            output_path = os.path.join(RESULT_FOLDER, "result.csv")
            file.save(input_path)

            # Parse weights and impacts
            try:
                weights = [float(w.strip()) for w in weights_raw.split(",")]
                impacts = [i.strip() for i in impacts_raw.split(",")]
            except ValueError:
                raise ValueError("Weights must be numeric values separated by commas")

            # Validate impacts
            for impact in impacts:
                if impact not in ['+', '-']:
                    raise ValueError("Impacts must be '+' or '-' separated by commas")
            
            # Validate equal length
            if len(weights) != len(impacts):
                raise ValueError(f"Number of weights ({len(weights)}) must equal number of impacts ({len(impacts)})")

            # Validate input and apply TOPSIS using your package
            dataframe, decision_matrix, weights, impacts = validate_input(
                input_path, weights, impacts
            )

            # Apply TOPSIS
            result = apply_topsis(dataframe, decision_matrix, weights, impacts)

            # Save result
            result.to_csv(output_path, index=False)

            # Send email
            email_sent = send_email(email, output_path)
            
            if email_sent:
                # Clean up files after sending email
                if os.path.exists(input_path):
                    os.remove(input_path)
                if os.path.exists(output_path):
                    os.remove(output_path)
                
                # Set success message in session
                session['toast'] = True
                session['error'] = None
                
                # Redirect to prevent form resubmission
                return redirect(url_for('index'))
            else:
                session['toast'] = True
                session['error'] = "Failed to send email. Please check email configuration."
                return redirect(url_for('index'))

        except ValueError as ve:
            session['error'] = str(ve)
            session['toast'] = True
            return redirect(url_for('index'))
        except FileNotFoundError:
            session['error'] = "File not found. Please upload a valid CSV file."
            session['toast'] = True
            return redirect(url_for('index'))
        except Exception as e:
            session['error'] = f"Error: {str(e)}"
            session['toast'] = True
            return redirect(url_for('index'))

    return render_template("index.html", toast=toast, error=error)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

# For Vercel serverless deployment
app = app