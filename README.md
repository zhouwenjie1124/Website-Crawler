# Selenium Website Crawler

This project demonstrates how to use Selenium to crawl website information. It consists of three parts: automatically logging in and bypassing captcha, collecting product prices and names from the website, and code for timed purchasing of flash sale items.

## Part 1: Automatically logging in and bypassing captcha

This part demonstrates how to use Selenium to automatically log in to a website and bypass captcha. The key steps are as follows:

1. Use Selenium to open the target website.
2. Locate and fill in the username and password fields of the login form.
3. Locate the captcha image element and save it locally.
4. Use a third-party library (such as Tesseract OCR) to recognize the saved captcha image.
5. Fill the recognized captcha into the captcha input field.
6. Submit the login form and wait for successful login.

## Part 2: Collecting product prices and names from the website

This part shows how to use Selenium to collect product prices and names from a website. The key steps are as follows:

1. Use Selenium to open the target website.
2. Locate the elements containing product information and extract their prices and names.
3. Save the extracted data into an appropriate data structure (such as a list or dictionary) for further processing and analysis.

## Part 3: Timed purchasing of flash sale items

This part demonstrates how to use Selenium to implement timed purchasing of flash sale items. The key steps are as follows:

1. Use Selenium to open the flash sale website and log in to the account.
2. Locate the page of the target item and retrieve its purchase link.
3. Set a timer to wait for the start of the flash sale.
4. When the flash sale starts, click the purchase link to complete the purchase operation.

Please note that this example project is for demonstration and learning purposes only. In actual usage, please comply with the terms and regulations of the website, and respect the limitations and privacy policies of the website.

## Installation Requirements

- Python 3.x
- Selenium library: `pip install selenium`
- Tesseract OCR (if captcha bypass is required): Refer to the relevant documentation for detailed installation steps

## Usage

1. Clone or download this project to your local machine.
2. Modify the relevant configurations in the code (such as login information, website URL, etc.) according to your needs.
3. Run the corresponding Python script file to start crawling website information or perform timed purchasing.

## Notes

- When crawling website information, please ensure compliance with the terms and regulations of the respective website and applicable laws and regulations.
- Exercise caution and comply with the website's rules when performing timed purchasing or similar operations to avoid legal violations or adverse consequences.

## Additional Resources

- [Selenium Official Documentation](https://www.selenium.dev/documentation/)
- [Tesseract OCR Official Documentation](https://github.com/tesseract-ocr/tesseract/wiki)
