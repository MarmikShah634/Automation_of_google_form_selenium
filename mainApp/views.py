from datetime import datetime
from django.core.mail import EmailMessage
import time
from django.http import HttpResponse
from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from django.conf import settings
import os

# Initialize the driver as None
driver = None

# Function to initialize the driver
def init_driver():
    global driver
    if driver is None:
        # Verify the path to the ChromeDriver
        CHROME_DRIVER_PATH = os.path.join(os.getcwd(), "chromedriver.exe")
        if not os.path.exists(CHROME_DRIVER_PATH):
            print("ChromeDriver not found at path:", CHROME_DRIVER_PATH)
            return

        # Initialize ChromeDriver options
        options = Options()
        options.add_experimental_option("detach", True)

        # Start ChromeDriver service
        service = ChromeService(executable_path=CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)

# Main function to use the driver
def main(request):
    global driver
    try:
        init_driver()

        if driver is None:
            print("Driver initialization failed.")
            return render(request, 'your_template.html')

        # Open the Google Form
        form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdUCd3UWQ3VOgeg0ZzNeT-xzNawU8AJ7Xidml-w1vhfBcvBWQ/viewform"
        print("Opening URL:", form_url)
        driver.get(form_url)

        filling_form()

        screenshot_and_send_mail()

        return HttpResponse("mail sent")

    except Exception as e:
        return HttpResponse("Error in sending mail")

# Optional: Function to close the driver
def close_driver():
    global driver
    if driver is not None:
        driver.close()
        driver = None

def filling_form():
    time.sleep(3)

    full_name = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    full_name.clear()
    full_name.send_keys("Marmik Shah")


    contact_number = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    contact_number.clear()
    contact_number.send_keys("9426465173")


    email = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
    email.clear()
    email.send_keys("mnshah632004@gmail.com")


    full_address = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div[2]/textarea")
    full_address.clear()
    full_address.send_keys("Ahmedabad, Gujarat, India")


    pincode = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input")
    pincode.clear()
    pincode.send_keys("380013")


    date = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input")
    date.clear()
    date.send_keys("03-06-2004")
    

    gender = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input")
    gender.clear()
    gender.send_keys("Male")

    code = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[8]/div/div/div[1]/div/div[1]/span[1]/b").text.strip()

    verify_human_code = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input")
    verify_human_code.clear()
    verify_human_code.send_keys(code)


    submit_button = driver.find_element(By.XPATH, value="/html/body/div/div[2]/form/div[2]/div/div[3]/div[1]/div[1]/div").click()
    time.sleep(5)
    
def screenshot_and_send_mail():
    time.sleep(2)
    now = datetime.now()
    datetime_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    fpath = os.path.join(os.getcwd(), "screenshots", "{}.png".format(datetime_str))
    driver.get_screenshot_as_file(fpath)
    
    # Prepare email parameters
    subject = 'Python (Selenium) Assignment - Marmik Shah'
    message = '''
    ### Project Overview: Google Form Automation and Email Notification

    #### Objective
    The goal of this project is to automate the process of filling out a Google Form using Selenium WebDriver, capturing a screenshot of the filled form, and sending this screenshot via email using Django's email backend.

    #### Key Components
    1. **Django Web Application**: Manages the entire process including initializing Selenium WebDriver, handling form automation, capturing screenshots, and sending emails.
    2. **Selenium WebDriver**: Automates browser interactions to fill out the Google Form.

    #### Setup and Configuration

    1. **Django Project Setup**:
        - Create a Django project and app.
        - Configure email settings in `settings.py` using Mailtrap's SMTP settings.

    2. **Install Dependencies**:
        - Install necessary packages like Django and Selenium.
        - Download and set up ChromeDriver.

    #### Workflow

    1. **Initializing the WebDriver**:
        - The `init_driver()` function initializes the Selenium WebDriver using ChromeDriver, ensuring proper setup before interacting with the Google Form.

    2. **Filling the Google Form**:
        - The `filling_form()` function automates the process of entering data into the Google Form fields using Selenium WebDriver. This includes filling out personal details and submitting the form.

    3. **Capturing and Sending Email with Screenshot**:
        - The `screenshot_and_send_mail()` function captures a screenshot of the browser window after form submission and sends it as an email attachment using Django's email capabilities.

    ---

    This documentation provides a high-level overview of the project's objectives, key components, setup instructions, and workflow for automating Google Form interactions and sending email notifications with screenshots.'''

    from_email = settings.EMAIL_HOST_USER
    to_emails = ['tech@themedius.ai',]
    cc_emails = ['hr@themedius.ai']
    
    # Send email with attached screenshot
    email = EmailMessage(subject, message, from_email, to_emails, cc=cc_emails)
    email.attach_file(fpath)  # Attach screenshot
    try:
        email.send()
        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred while sending email:", e)