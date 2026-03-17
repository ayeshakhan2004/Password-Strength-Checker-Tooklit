# Password Strength Checker (GUI)

This is a beginner cybersecurity project I built to learn about password security, hashing, and working with APIs. It's a Python desktop application that evaluates how secure a password actually is.

The tool checks the password's complexity, estimates how long it would take a hacker to crack it, and securely checks if it has been exposed in any known data breaches.


## What it does
* **Single Password Check:** You can type a password directly into the app to get instant feedback on its strength and breach history.
* **Batch Scanner:** You can upload a `.txt` file containing a list of passwords. The script will scan all of them and generate a `.csv` spreadsheet report.
* **Secure API Integration:** To check for data breaches, the app uses the Have I Been Pwned (HIBP) API. It uses the k-Anonymity model—meaning it hashes the password locally using SHA-1 and only sends the first 5 characters of the hash over the internet. Your actual password never leaves your machine.

## Technologies I Used
* **Python** * **Tkinter:** Built-in Python library used to create the graphical user interface (GUI).
* **Hashlib:** Used for SHA-1 cryptography/hashing.
* **Requests:** Used to handle the web requests to the HIBP API.
* **Zxcvbn:** A library developed by Dropbox that estimates realistic password cracking times based on offline fast hashing.

## How to run it


### Option 1: Download the App (Easiest - Windows Only)
You don't need Python installed to use this tool! 
1. Go to the **Releases** section on the right side of this GitHub page.
2. Download the latest `.exe` file.
3. Double-click to run it directly on your Windows PC. *(Note: Windows Defender might flag it since it's an unsigned indie app. Just click "More info" -> "Run anyway").*
   
### Option 2: Run the Python Code (For Developers)
If you want to look at the code or run it on Mac/Linux, you will need Python installed.

1. Download or clone this repository to your machine.
2. Open your terminal or command prompt and install the required external libraries:
   ```bash
   pip install requests zxcvbn
   ```
3. Run the application:
   ```bash
   python password_checker.py
   ```
Note: If you use the batch scanner, the app will generate .csv files in your folder. If you are pushing your own updates to GitHub, be careful not to accidentally commit those report files or any .txt files containing real passwords!
