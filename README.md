# DriveSafe - Driver Drowsiness Detection

Flask web application with account registration/login (SQLite), password hashing, live camera frame processing, eye-blink counting and drowsiness alerts.

## Run locally (Windows)

1. Open this folder in VS Code or Cursor.
2. Create and activate a virtual environment (recommended):
   ```powershell
   py -m venv venv
   .\venv\Scripts\activate
   ```
3. Install packages:
   ```powershell
   pip install -r requirements.txt
   ```
4. Start the website:
   ```powershell
   py app.py
   ```
5. Open `http://127.0.0.1:5000` and choose **Create account**.

The SQLite database (`drivesafe.db`) is created automatically on first start.

## Render deployment

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`
- Add an environment variable named `SECRET_KEY` with a long random value.
- Add `COOKIE_SECURE=true` when serving the site over HTTPS.
- The SQLite database is local to the service. On Render, use a persistent disk mounted at the application directory (or switch to a managed database) if user accounts must survive service replacement/redeploys. Do not rely on an ephemeral filesystem for production account storage.

## Important

- Passwords are stored as Werkzeug password hashes, not plain text.
- The camera is accessed by the visitor's browser and requires HTTPS when deployed (localhost is also permitted by modern browsers).
- This is a student prototype, not a certified vehicle safety system.
- Set a strong `SECRET_KEY` before deployment. The fallback key is only for local testing.
