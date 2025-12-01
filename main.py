import argparse
import time
from getpass import getpass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def parse_args():
    parser = argparse.ArgumentParser(
        description="Python-based browser automation agent for sending Gmail emails."
    )
    parser.add_argument(
        "--email", required=True, help="Gmail address used to log in (sender)."
    )
    parser.add_argument(
        "--to", required=True, help="Recipient email address."
    )
    parser.add_argument(
        "--subject", required=True, help="Subject of the email."
    )
    parser.add_argument(
        "--body", required=True, help="Body/content of the email."
    )
    return parser.parse_args()


def create_driver():
    """Create and return a Chrome WebDriver instance.

    Assumes ChromeDriver is installed and either on PATH or in the same
    directory as this script.
    """
    options = webdriver.ChromeOptions()
    # Optional: keep the browser open after script finishes (for debugging)
    # options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


def login_to_gmail(driver, email, password):
    """Logs in to Gmail using the given credentials."""
    wait = WebDriverWait(driver, 40)

    # Open Gmail
    driver.get("https://mail.google.com/")

    # ----- EMAIL / USERNAME -----
    email_input = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@type='email' or @name='identifier']")
        )
    )
    email_input.click()
    email_input.clear()
    email_input.send_keys(email)

    next_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@id='identifierNext']//button | //button//span[text()='Next']/..")
        )
    )
    next_btn.click()

    # ----- PASSWORD -----
    # Wait for password box to be visible and clickable
    password_input = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@type='password' and @name='Passwd']")
        )
    )

    # ensure it is in view and focused
    driver.execute_script("arguments[0].scrollIntoView(true);", password_input)
    password_input.click()
    # DO NOT call clear() – it can trigger ElementNotInteractable on this field
    password_input.send_keys(password)

    next_btn_pwd = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@id='passwordNext']//button | //button//span[text()='Next']/..")
        )
    )
    next_btn_pwd.click()

    # small wait for inbox to load
    time.sleep(5)


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


def compose_and_send_email(driver, to_email, subject, body):
    """Composes and sends an email in Gmail."""
    wait = WebDriverWait(driver, 40)

    # --- CLICK COMPOSE ---
    # Standard Gmail compose button
    compose_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//div[@role='button' and (@gh='cm' or text()='Compose' or @aria-label='Compose')]",
            )
        )
    )
    compose_button.click()

    # --- WAIT FOR COMPOSE DIALOG / TO FIELD TO EXIST ---
    # Don't interact with it yet, just make sure it's loaded
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[@name='to' or @aria-label='To']")
        )
    )

    # --- TYPE IN TO FIELD VIA ACTIVE ELEMENT ---
    to_input = driver.switch_to.active_element
    to_input.send_keys(to_email)
    to_input.send_keys(Keys.TAB)  # move focus to Subject

    # --- SUBJECT FIELD ---
    subject_input = wait.until(
        EC.element_to_be_clickable((By.NAME, "subjectbox"))
    )
    subject_input.click()
    subject_input.send_keys(subject)

    # --- BODY FIELD ---
    body_div = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//div[@aria-label='Message Body' or @aria-label='Message body']",
            )
        )
    )
    body_div.click()
    body_div.send_keys(body)

    # --- SEND BUTTON ---
    send_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//div[@role='button' and "
                "(starts-with(@data-tooltip, 'Send') or starts-with(@aria-label, 'Send'))]"
            )
        )
    )
    send_button.click()

    time.sleep(5)  # give Gmail time to send




def main():
    args = parse_args()
    email = args.email

    # Ask for password securely (input hidden)
    password = getpass(prompt=f"Enter password for {email}: ")

    driver = create_driver()
    try:
        print("[1/3] Logging in...")
        login_to_gmail(driver, email, password)
        print("[2/3] Composing email...")
        compose_and_send_email(driver, args.to, args.subject, args.body)
        print("[3/3] Email sent (if Gmail did not block automated login).")
    finally:
        # Close browser after a short delay so user can see result
        time.sleep(3)
        driver.quit()


if __name__ == "__main__":
    main()
