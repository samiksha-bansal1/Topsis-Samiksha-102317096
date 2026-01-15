# TOPSIS Web Service - Setup Guide

A Flask-based web application for TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) analysis with email notification.

## 📁 Project Structure

```
topsis-web-service/
│
├── app.py                          # Main Flask application
├── templates/
│   └── index.html                  # Frontend HTML
├── uploads/                        # Uploaded CSV files (auto-created)
├── results/                        # Generated result files (auto-created)
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🔧 Installation Steps

### 1. Install Dependencies

```bash
pip install Topsis-Samiksha-102317096
pip install flask
```

Or use requirements.txt:

```bash
# Create requirements.txt with:
Flask==3.0.0
Topsis-Samiksha-102317096==0.1.1
pandas
numpy
```

Then install:
```bash
pip install -r requirements.txt
```

### 2. Configure Email Settings

Open `app.py` and update the email configuration in the `send_email()` function:

```python
sender_email = "your_email@gmail.com"      # Your Gmail address
app_password = "your_app_password"          # Your Gmail App Password
```

#### How to Get Gmail App Password:

1. Go to your Google Account settings
2. Navigate to Security
3. Enable 2-Step Verification
4. Search for "App passwords"
5. Generate a new app password for "Mail"
6. Copy the 16-character password
7. Use this password in the `app_password` variable

**Note:** If you don't want email functionality initially, you can comment out the email sending code and just save the result file.

### 3. Create Required Folders

The application will auto-create these folders, but you can create them manually:

```bash
mkdir uploads results templates
```

### 4. Save Files

- Save the Flask code as `app.py`
- Save the HTML code in `templates/index.html`

## 🚀 Running the Application

### Local Development

```bash
python app.py
```

The application will start at: `http://127.0.0.1:5000`

### Access from Other Devices (Same Network)

Find your local IP address:
- Windows: `ipconfig`
- Mac/Linux: `ifconfig` or `ip addr`

Then access at: `http://YOUR_IP:5000`

## 📝 Usage

1. Open the web application in your browser
2. Upload a CSV file with:
   - First column: Model/Object names
   - Remaining columns: Numeric values only
   - At least 3 columns total

3. Enter weights (comma-separated numbers)
   - Example: `1,1,1,2`

4. Enter impacts (comma-separated +/-)
   - `+` for benefit criteria (higher is better)
   - `-` for cost criteria (lower is better)
   - Example: `+,+,-,+`

5. Enter your email address

6. Click "Run TOPSIS Analysis"

7. Check your email for the result file

## 📊 Sample Input File

**input.csv:**
```csv
Model,Price,Storage,Camera,Looks
M1,250,16,12,5
M2,200,16,8,3
M3,300,32,16,4
M4,275,32,8,4
M5,225,16,16,2
```

**Weights:** `1,1,1,2`  
**Impacts:** `+,+,-,+`

(Price: +, Storage: +, Camera: -, Looks: +)

## 🔍 Error Handling

The application handles:
- Missing or invalid files
- Non-numeric values in data
- Mismatched weights/impacts count
- Invalid impact values (not + or -)
- Email sending errors
- File format errors

## 🌐 Deployment Options

### Option 1: Deploy on Render

1. Create a `requirements.txt` file
2. Push code to GitHub
3. Sign up on [Render.com](https://render.com)
4. Create a new Web Service
5. Connect your GitHub repository
6. Set build command: `pip install -r requirements.txt`
7. Set start command: `python app.py`

### Option 2: Deploy on PythonAnywhere

1. Sign up at [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload your files
3. Create a new web app
4. Configure WSGI file
5. Install dependencies in virtual environment

### Option 3: Deploy on Heroku

1. Create `Procfile`:
   ```
   web: python app.py
   ```
2. Push to Heroku
3. Configure environment variables

## 🔒 Security Considerations

- Never commit email credentials to version control
- Use environment variables for sensitive data:
  ```python
  import os
  sender_email = os.environ.get('SENDER_EMAIL')
  app_password = os.environ.get('APP_PASSWORD')
  ```
- Add `.gitignore`:
  ```
  uploads/
  results/
  __pycache__/
  *.pyc
  .env
  ```

## 🐛 Troubleshooting

### Email Not Sending

- Check Gmail App Password is correct
- Ensure "Less secure app access" is OFF (use App Password instead)
- Check internet connection
- Verify SMTP settings

### Import Error

```bash
pip install --upgrade Topsis-Samiksha-102317096
```

### File Upload Issues

- Check file size (max 16MB by default)
- Ensure file is in CSV format
- Verify file has correct structure

## 📞 Support

For issues with the TOPSIS package, visit:
https://pypi.org/project/Topsis-Samiksha-102317096/

## 📄 License

MIT License - Free to use and modify

---

**Author:** Samiksha (102317096)  
**Package:** [Topsis-Samiksha-102317096](https://pypi.org/project/Topsis-Samiksha-102317096/)