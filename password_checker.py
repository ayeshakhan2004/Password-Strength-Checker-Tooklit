import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import hashlib
import requests
import csv
from datetime import datetime
import zxcvbn

def check_complexity(password):
    feedback = []
    if len(password) < 12: feedback.append("Less than 12 characters.")
    if not re.search(r"[A-Z]", password): feedback.append("Missing uppercase letters.")
    if not re.search(r"[a-z]", password): feedback.append("Missing lowercase letters.")
    if not re.search(r"[0-9]", password): feedback.append("Missing numbers.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): feedback.append("Missing special characters.")
    return feedback

def check_pwned_api(password):
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1_hash[:5], sha1_hash[5:]
    url = f"https://api.pwnedpasswords.com/range/{first5}"
    headers = {'User-Agent': 'Python-Password-Checker-GUI'}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            hashes = (line.split(':') for line in response.text.splitlines())
            for h, count in hashes:
                if h == tail: return int(count)
        return 0
    except requests.RequestException:
        return "Error"

def analyze_single_password(password):
    feedback = check_complexity(password)
    breaches = check_pwned_api(password)
    crack_time_data = zxcvbn.zxcvbn(password)
    crack_time = crack_time_data['crack_times_display']['offline_fast_hashing_1e10_per_second']
    
    return {
        "password": password,
        "feedback": feedback,
        "breaches": breaches,
        "crack_time": crack_time
    }

class PasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Password Security Toolkit")
        self.root.geometry("550x450")
        self.root.configure(padx=20, pady=20)

        title_label = tk.Label(root, text="🛡️ Password Security Toolkit", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 20))

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.tab_single = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_single, text="Single Password")
        self.setup_single_tab()

        self.tab_batch = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_batch, text="Batch File Scanner")
        self.setup_batch_tab()

    def setup_single_tab(self):
        tk.Label(self.tab_single, text="Enter Password:").pack(pady=(10, 5))
        
        self.pass_entry = tk.Entry(self.tab_single, show="*", width=40, font=("Helvetica", 12))
        self.pass_entry.pack(pady=5)
        
        check_btn = tk.Button(self.tab_single, text="Analyze Password", command=self.run_single_check, bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        check_btn.pack(pady=10)

        self.result_text = tk.Text(self.tab_single, height=10, width=55, state=tk.DISABLED, bg="#f4f4f4")
        self.result_text.pack(pady=10)

    def setup_batch_tab(self):
        tk.Label(self.tab_batch, text="Upload a .txt file containing one password per line.", wraplength=400, justify="center").pack(pady=(30, 10))
        
        upload_btn = tk.Button(self.tab_batch, text="📂 Select File & Generate Report", command=self.run_batch_check, bg="#2196F3", fg="white", font=("Helvetica", 10, "bold"))
        upload_btn.pack(pady=20)
        
        self.batch_status = tk.Label(self.tab_batch, text="", fg="green")
        self.batch_status.pack(pady=10)

    def run_single_check(self):
        password = self.pass_entry.get()
        if not password:
            messagebox.showwarning("Input Error", "Please enter a password.")
            return

        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Analyzing... Please wait...\n")
        self.root.update()

        results = analyze_single_password(password)

        output = f"⏱️ Time to Crack (Estimated): {results['crack_time']}\n\n"
        
        if results['breaches'] == "Error":
            output += "⚠️ API Error: Could not check data breaches.\n\n"
        elif results['breaches'] > 0:
            output += f"🚨 DANGER: Found in {results['breaches']:,} data breaches!\n\n"
        else:
            output += "✅ SAFE: Not found in any known breaches.\n\n"

        if results['feedback']:
            output += "Suggestions for improvement:\n"
            for item in results['feedback']:
                output += f" - {item}\n"
        else:
            output += "👍 Complexity: Excellent.\n"

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, output)
        self.result_text.config(state=tk.DISABLED)

    def run_batch_check(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return
        
        self.batch_status.config(text="Processing file... This may take a moment depending on size.", fg="blue")
        self.root.update()

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                passwords = [line.strip() for line in file if line.strip()]
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"Password_Report_{timestamp}.csv"
            
            with open(report_name, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['Password', 'Time_To_Crack', 'Breach_Count', 'Issues']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for pw in passwords:
                    res = analyze_single_password(pw)
                    writer.writerow({
                        'Password': pw,
                        'Time_To_Crack': res['crack_time'],
                        'Breach_Count': res['breaches'],
                        'Issues': " | ".join(res['feedback']) if res['feedback'] else "None"
                    })
            
            self.batch_status.config(text=f"✅ Success! Report saved as:\n{report_name}", fg="green")
            messagebox.showinfo("Batch Complete", f"Successfully analyzed {len(passwords)} passwords.\nReport saved to your current folder.")
            
        except Exception as e:
            self.batch_status.config(text="❌ Error processing file.", fg="red")
            messagebox.showerror("Error", f"Could not process file:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()