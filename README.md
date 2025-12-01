# Python Email Browser Automation Agent

This is a simple **Python-based browser automation agent** that logs into Gmail,
composes an email, and sends it.  
All inputs (credentials + email content) are taken from the **command prompt**.

> ⚠️ **Important**
>
> - Use this project only for learning / assignments.
> - Prefer using a **separate test Gmail account** or enable an **App Password**
  and 2FA for safety.
> - Google may block automated logins; that is normal for real accounts.

## 1. Project Structure

```text
email_automation_agent/
├─ main.py           # Command line script (browser agent)
├─ requirements.txt  # Python dependencies
└─ README.md         # This file
```

## 2. Prerequisites

1. **Python 3.9+** installed  
   Check with:
   ```bash
   python --version
   ```
2. **Google Chrome** installed.
3. **ChromeDriver** (for Selenium):
   - Open: https://googlechromelabs.github.io/chrome-for-testing/
   - Download the ChromeDriver that matches your Chrome version.
   - Extract it and put the `chromedriver` / `chromedriver.exe` in:
     - Either this project folder, or
     - Any folder that is already in your system PATH.

## 3. Install Python dependencies

Open a terminal / command prompt inside the project folder (`email_automation_agent`)
and run:

```bash
pip install -r requirements.txt
```

This will install:
- `selenium`
- `python-dotenv` (not strictly required but useful if you want to extend)

## 4. How to Run

In the terminal, inside the project folder:

```bash
python main.py ^
    --email YOUR_EMAIL@gmail.com ^
    --to RECEIVER_EMAIL@example.com ^
    --subject "Project Submission" ^
    --body "This email is automated."
```

On Linux / macOS, the line continuation symbol is `\` instead of `^`:

```bash
python main.py         --email YOUR_EMAIL@gmail.com         --to RECEIVER_EMAIL@example.com         --subject "Test from automation"         --body "Hello, this email was sent by a Selenium browser bot."
```

- After you press Enter, the script will:
  1. Open a Chrome browser.
  2. Ask you **securely** for your email password (input is hidden).
  3. Log in to Gmail with the given email + password.
  4. Click **Compose**, fill **To**, **Subject**, **Body**.
  5. Click **Send**.

## 5. Command Line Arguments

- `--email`   : Your Gmail address (used to log in).
- `--to`      : Recipient email address.
- `--subject` : Subject line of the email.
- `--body`    : Body / content of the email.

The password is **NOT** passed as an argument.  
It is read using a hidden prompt (`getpass`) for basic security.

Example:

```bash
python main.py --email test.assignment@gmail.com --to teacher@example.com --subject "Assignment Bot" --body "This is my automated email."
```

