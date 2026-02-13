from flask import Flask, render_template, request, redirect, url_for, session
import os
import tempfile
import time
import pandas as pd
from topsis_samiksha_102317096 import validate_input, apply_topsis

# Email imports
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this-random-string-for-production')

# Use /tmp for serverless (Vercel doesn't allow writing to other directories)
UPLOAD_FOLDER = "/tmp/uploads"
RESULT_FOLDER = "/tmp/results"
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
            print("Error: Email credentials not found in environment variables")
            print("Please set SENDER_EMAIL and APP_PASSWORD in your .env file")
            return False
        
        msg = EmailMessage()
        msg['Subject'] = 'TOPSIS Analysis Result - Your Multi-Criteria Decision Analysis'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        # Email body
        email_body = """Dear User,

Your TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) analysis has been completed successfully!

The attached CSV file contains:
- Original data
- Calculated TOPSIS scores
- Final rankings of alternatives

What's Next?
- Review the TOPSIS Score column (higher is better)
- Check the Rank column for the final ordering
- The alternative with Rank 1 is the best option based on your criteria

Thank you for using TOPSIS Web Service!

Best regards,
TOPSIS Web Service Team

---
Powered by topsis-samiksha-102317096
Visit: https://pypi.org/project/topsis-samiksha-102317096/
"""
        
        msg.set_content(email_body)
        
        # Attach the result file
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
        
        msg.add_attachment(file_data, maintype='application', subtype='csv', filename=file_name)
        
        # Send email via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
        
        print(f"✅ Email sent successfully to {receiver_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Email authentication failed. Please check your SENDER_EMAIL and APP_PASSWORD")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error occurred: {e}")
        return False
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False

def validate_csv_structure(file_path):
    """
    Validate CSV file structure before processing
    Returns: (is_valid, error_message, column_count)
    """
    try:
        # Read CSV
        df = pd.read_csv(file_path)
        
        # Check if file has at least 3 columns
        if len(df.columns) < 3:
            return False, f"CSV file must contain at least 3 columns (1 name + 2 criteria). Found {len(df.columns)} columns.", 0
        
        # Check if file has at least one row
        if len(df) == 0:
            return False, "CSV file is empty. Please provide data rows.", 0
        
        # Number of criteria columns (excluding first column which is name/alternative)
        criteria_count = len(df.columns) - 1
        
        # Check if columns 2 to last contain numeric values
        numeric_columns = df.columns[1:]
        for col in numeric_columns:
            # Try to convert to numeric
            try:
                pd.to_numeric(df[col], errors='raise')
            except (ValueError, TypeError):
                return False, f"Column '{col}' contains non-numeric values. All criteria columns must have numeric values only.", 0
        
        return True, None, criteria_count
        
    except pd.errors.EmptyDataError:
        return False, "CSV file is empty or invalid.", 0
    except pd.errors.ParserError:
        return False, "Unable to parse CSV file. Please check the file format.", 0
    except Exception as e:
        return False, f"Error reading CSV file: {str(e)}", 0

@app.route("/", methods=["GET", "POST"])
def index():
    # Get flash messages if any
    toast = session.pop('toast', False)
    error = session.pop('error', None)
    results = session.pop('results', None)

    if request.method == "POST":
        input_path = None
        output_path = None
        
        try:
            # Get form inputs
            file = request.files.get("file")
            weights_raw = request.form.get("weights", "").strip()
            impacts_raw = request.form.get("impacts", "").strip()
            email = request.form.get("email", "").strip()

            # ===== VALIDATION PHASE 1: Basic Input Validation =====
            
            # Check if file is uploaded
            if not file or not file.filename:
                raise ValueError("❌ Please upload a CSV file")
            
            # Check if all fields are filled
            if not weights_raw:
                raise ValueError("❌ Weights field is required")
            if not impacts_raw:
                raise ValueError("❌ Impacts field is required")
            if not email:
                raise ValueError("❌ Email field is required")
            
            # Validate email format
            if '@' not in email or '.' not in email.split('@')[-1]:
                raise ValueError("❌ Invalid email format. Please enter a valid email address (e.g., user@example.com)")
            
            # Check file extension
            if not file.filename.lower().endswith('.csv'):
                raise ValueError("❌ Only CSV files are allowed. Please upload a file with .csv extension")

            # Save uploaded file with unique name
            timestamp = str(int(time.time()))
            input_filename = f"input_{timestamp}.csv"
            output_filename = f"result_{timestamp}.csv"
            
            input_path = os.path.join(UPLOAD_FOLDER, input_filename)
            output_path = os.path.join(RESULT_FOLDER, output_filename)
            file.save(input_path)

            # ===== VALIDATION PHASE 2: CSV Structure Validation =====
            
            is_valid, csv_error, criteria_count = validate_csv_structure(input_path)
            if not is_valid:
                raise ValueError(csv_error)

            # ===== VALIDATION PHASE 3: Weights and Impacts Validation =====
            
            # Parse weights
            try:
                weights = [w.strip() for w in weights_raw.split(",")]
                weights = [float(w) for w in weights]
                
                # Check for positive weights
                if any(w <= 0 for w in weights):
                    raise ValueError("❌ All weights must be positive numbers greater than 0")
                    
            except ValueError as ve:
                if "could not convert" in str(ve) or "invalid literal" in str(ve):
                    raise ValueError("❌ Weights must be numeric values separated by commas (e.g., 1,2,1,3)")
                raise

            # Parse impacts
            impacts = [i.strip() for i in impacts_raw.split(",")]
            
            # Validate impacts - must be + or -
            invalid_impacts = [i for i in impacts if i not in ['+', '-']]
            if invalid_impacts:
                raise ValueError(f"❌ Invalid impacts: {', '.join(invalid_impacts)}. Impacts must be '+' (benefit) or '-' (cost) separated by commas")
            
            # ===== VALIDATION PHASE 4: Count Matching =====
            
            # Check if counts match
            if len(weights) != len(impacts):
                raise ValueError(
                    f"❌ Count mismatch: You provided {len(weights)} weights and {len(impacts)} impacts. "
                    f"Number of weights must equal number of impacts."
                )
            
            # Check if counts match with CSV criteria columns
            if len(weights) != criteria_count:
                raise ValueError(
                    f"❌ Count mismatch: CSV file has {criteria_count} criteria columns, but you provided "
                    f"{len(weights)} weights and {len(impacts)} impacts. All counts must match."
                )

            # ===== TOPSIS PROCESSING =====
            
            print(f"✅ All validations passed. Processing TOPSIS...")
            print(f"   - Criteria columns: {criteria_count}")
            print(f"   - Weights: {weights}")
            print(f"   - Impacts: {impacts}")
            
            # Validate input and apply TOPSIS using your package
            try:
                dataframe, decision_matrix, validated_weights, validated_impacts = validate_input(
                    input_path, weights, impacts
                )
            except ValueError as ve:
                # Catch errors from your TOPSIS package
                raise ValueError(f"❌ TOPSIS validation error: {str(ve)}")
            except Exception as e:
                raise ValueError(f"❌ Error validating input data: {str(e)}")

            # Apply TOPSIS
            try:
                result = apply_topsis(dataframe, decision_matrix, validated_weights, validated_impacts)
            except Exception as e:
                raise ValueError(f"❌ Error applying TOPSIS algorithm: {str(e)}")

            # Save result
            result.to_csv(output_path, index=False)
            print(f"✅ TOPSIS result saved to {output_path}")

            # ===== EMAIL SENDING =====
            
            print(f"📧 Sending email to {email}...")
            email_sent = send_email(email, output_path)
            
            # Convert results to JSON for display (preserving column order)
            # Convert to dict with 'records' orientation to maintain column order
            results_json = result.to_dict('records')
            
            # Clean up files after processing
            if os.path.exists(input_path):
                os.remove(input_path)
                print(f"🗑️  Cleaned up input file: {input_path}")
            if os.path.exists(output_path):
                os.remove(output_path)
                print(f"🗑️  Cleaned up output file: {output_path}")
            
            if email_sent:
                # Set success message and results in session
                session['toast'] = True
                session['error'] = None
                session['results'] = results_json
                print("✅ Process completed successfully!")
                
                # Redirect to prevent form resubmission
                return redirect(url_for('index'))
            else:
                session['toast'] = True
                session['error'] = (
                    "❌ TOPSIS analysis completed, but failed to send email. "
                    "Please check email configuration (SENDER_EMAIL and APP_PASSWORD environment variables)."
                )
                session['results'] = results_json
                return redirect(url_for('index'))

        except ValueError as ve:
            # Clean up files if they exist
            if input_path and os.path.exists(input_path):
                os.remove(input_path)
            if output_path and os.path.exists(output_path):
                os.remove(output_path)
            
            session['error'] = str(ve)
            session['toast'] = True
            return redirect(url_for('index'))
            
        except FileNotFoundError:
            session['error'] = "❌ File not found. Please upload a valid CSV file."
            session['toast'] = True
            return redirect(url_for('index'))
            
        except Exception as e:
            # Clean up files if they exist
            if input_path and os.path.exists(input_path):
                os.remove(input_path)
            if output_path and os.path.exists(output_path):
                os.remove(output_path)
            
            # Generic error handler
            error_msg = str(e)
            if "No such file or directory" in error_msg:
                session['error'] = "❌ File not found. Please upload a valid CSV file."
            elif "Permission denied" in error_msg:
                session['error'] = "❌ Permission denied. Please try again."
            else:
                session['error'] = f"❌ An error occurred: {error_msg}"
            
            session['toast'] = True
            return redirect(url_for('index'))

    return render_template("index.html", toast=toast, error=error, results=results)

@app.route("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "TOPSIS Web Service"}, 200

@app.route("/samples/<filename>")
def download_sample(filename):
    """Serve sample CSV files"""
    from flask import send_from_directory
    samples_dir = os.path.join(os.path.dirname(__file__), 'samples')
    return send_from_directory(samples_dir, filename)

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    debug_mode = os.getenv('FLASK_ENV', 'production') == 'development'
    
    print("=" * 60)
    print("🚀 Starting TOPSIS Web Service")
    print("=" * 60)
    print(f"Port: {port}")
    print(f"Debug: {debug_mode}")
    print(f"Upload folder: {UPLOAD_FOLDER}")
    print(f"Result folder: {RESULT_FOLDER}")
    print("=" * 60)
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)

# For Vercel serverless deployment
app = app