# DUEDC Full Stack Contact Form + API

A responsive full-stack contact form built with **Python, Flask, HTML, CSS, JavaScript, and SQLite**. The application collects contact information, validates submissions, stores records in a database, and provides an API to retrieve saved messages.

## Features

- Responsive contact form interface
- Required fields for full name, company name, email, and phone number
- Email format validation
- Privacy consent validation
- Success and error feedback for submissions
- Flask backend with REST API endpoints
- SQLite database for persistent storage
- JSON responses for API requests
- Parameterized SQL queries for database operations

## Technologies Used

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python, Flask
- **Database:** SQLite
- **Templating:** Jinja2
- **Environment configuration:** python-dotenv, if installed and used

## Project Structure

```
│
├── env/
│   └── ...  (Python virtual environment)
│
├── Static/
│   ├── style.css
│   └── Corporate guy.jpg
│
├── Templates/
│   ├── base.html
│   └── web.html
│
├── .gitignore
├── app.py
└── messages.db
```


## Requirements

- Python 3.10 or later recommended
- pip
- A modern web browser

## Installation and Setup

### 1. Clone the repository

### 2. Create a virtual environment

```powershell
python -m venv env
```
### 3. Activate the environment

**Windows PowerShell:**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\env\Scripts\Activate.ps1
```
### 4. Install dependencies

```powershell
python -m pip install Flask
```

If your application uses `python-dotenv` to load environment variables, install it too:

```powershell
python -m pip install python-dotenv
```

### 5. Run the application

```powershell
python app.py
```
Open the following URL in your browser:

http://127.0.0.1:5000

## API Documentation

### 1. Submit a contact message

**Endpoint:** `/api/messages`

**Method:** `POST`

**Content-Type:** `application/json`

Example request:

```json
{
  "full_name": "Alex Morgan",
  "company_name": "NovaTech Solutions",
  "email": "alex.morgan@example.com",
  "phone": "+1-202-555-0101",
  "consent": true
}
```

Example successful response:

```json
{
  "success": true,
  "message": "Your message has been sent successfully!"
}
```

A successful submission returns HTTP status `201 Created`.

### 2. Retrieve saved messages

**Endpoint:** `/api/messages`

**Method:** `GET`

Open this URL in your browser while the application is running:

http://127.0.0.1:5000/api/messages

The endpoint returns saved contact records in JSON format, ordered from newest to oldest.

## Validation

The backend checks that:

- All required fields are completed.
- The email address has a valid basic format.
- Privacy consent is provided.
- The submitted data is valid JSON.

Invalid submissions receive an appropriate error message and HTTP status.

## Database

The application uses SQLite to store contact submissions in `messages.db`. The database table contains:

- `id`
- `full_name`
- `company_name`
- `email`
- `phone`
- `consent`

The database table is created automatically when the application starts.

## Testing

1. Start the Flask application.
2. Open the contact form in your browser.
3. Submit a contact with valid information.
4. Confirm that the success message appears.
5. Open `/api/messages` and verify that the submission was saved.
6. Test missing fields, an invalid email address, and unchecked consent.
7. Confirm that invalid submissions are rejected.

## Security Notes

- Database operations use parameterized SQL queries.
- Input validation is performed on the backend.
- Do not commit `.env`, virtual environment files, or sensitive information to GitHub.
- This project uses Flask's development server and should be configured with a production-ready server before public deployment.

## Author

**Asma Sadia Sheikh**

## Project

DUEDC Full Stack Contact Form + API — Task 2
