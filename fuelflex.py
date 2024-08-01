from tkinter import messagebox, simpledialog
import tkinter as tk
import re
import datetime

# Constants for the application
# Regular expressions for phone numbers of Lesotho, Eswatini, Botswana, South Africa, and India
PHONE_PATTERNS = {
    'Lesotho': r'^(?:\+266)?[256]\d{7}$',
    'Eswatini': r'^(?:\+268)?[67]\d{7}$',
    'Botswana': r'^(?:\+267)?[7]\d{7}$',
    'South Africa': r'^(?:\+27)?[6-8]\d{8}$',
    'India': r'^(?:\+91)?[6-9]\d{9}$'
}

# Utility function to verify phone numbers
def verify_phone_number(phone_number):
    return any(re.match(pattern, phone_number) for pattern in PHONE_PATTERNS.values())

# Main App Class
class FuelFlexApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FuelFlex - Smart Fuel Management")
        self.geometry("600x400")
        self.configure(bg='black')

        # Initialize user data
        self.name = None
        self.phone_number = None
        self.pin = None
        self.balance = 0
        self.monthly_fuel_purchased = 0
        self.transactions = []  # List to store transactions

        # Welcome Frame
        self.welcome_frame = tk.Frame(self, bg='black')
        self.welcome_label = tk.Label(self.welcome_frame, text="Welcome to FuelFlex", font=("Helvetica", 24), bg='black', fg='white')
        self.welcome_label.pack(pady=20)
        self.name_entry_label = tk.Label(self.welcome_frame, text="Please enter your name:", bg='black', fg='white')
        self.name_entry_label.pack(pady=10)
        self.name_entry = tk.Entry(self.welcome_frame)
        self.name_entry.pack()
        self.name_submit_button = tk.Button(self.welcome_frame, text="Submit", command=self.submit_name)
        self.name_submit_button.pack(pady=10)
        self.welcome_frame.pack(expand=True)

    def submit_name(self):
        name = self.name_entry.get().strip()
        if name:
            self.name = name
            self.welcome_label.config(text=f"Welcome {name} to FuelFlex")
            self.name_entry.config(state='disabled')
            self.name_submit_button.config(state='disabled')
            self.prompt_phone_number()
        else:
            messagebox.showerror("Error", "Please enter your name.")

    def prompt_phone_number(self):
        self.phone_entry_label = tk.Label(self.welcome_frame, text="Please enter your phone number:", bg='black', fg='white')
        self.phone_entry_label.pack(pady=10)
        self.phone_entry = tk.Entry(self.welcome_frame)
        self.phone_entry.pack()
        self.phone_submit_button = tk.Button(self.welcome_frame, text="Submit", command=self.submit_phone)
        self.phone_submit_button.pack(pady=10)

    def submit_phone(self):
        phone_number = self.phone_entry.get()
        if verify_phone_number(phone_number):
            self.phone_number = phone_number
            # Simulate OTP sent to the user's phone number
            dummy_otp = "123456"  # Hardcoded dummy OTP
            otp = simpledialog.askstring("OTP Verification", "Enter the OTP sent to your phone:")
            if otp == dummy_otp:
                # Dummy OTP verification successful
                # Prompt user to set a PIN
                self.set_pin()
            else:
                messagebox.showerror("OTP Verification Failed", "Invalid OTP. Please try again.")
        else:
            messagebox.showerror("Error", "Invalid phone number. Please try again.")

    def set_pin(self):
        # Remove previous widgets
        self.phone_entry_label.pack_forget()
        self.phone_entry.pack_forget()
        self.phone_submit_button.pack_forget()

        # Prompt the user to set a PIN
        self.pin_entry_label = tk.Label(self.welcome_frame, text="Set a 5-digit PIN for your account:", bg='black', fg='white')
        self.pin_entry_label.pack(pady=10)
        self.pin_entry = tk.Entry(self.welcome_frame, show='*')
        self.pin_entry.pack()
        self.pin_submit_button = tk.Button(self.welcome_frame, text="Submit", command=self.submit_pin)
        self.pin_submit_button.pack(pady=10)

    def submit_pin(self):
        pin = self.pin_entry.get()
        if pin and len(pin) == 5 and pin.isdigit():
            self.pin = pin
            messagebox.showinfo("PIN Set", "Your PIN has been set successfully.")
            self.welcome_frame.pack_forget()
            self.initialize_main_window()
        else:
            messagebox.showerror("Error", "Invalid PIN. Please try again.")

    def initialize_main_window(self):
        # Clear the window
        for widget in self.winfo_children():
            widget.destroy()

        # Navigation bar
        navbar = tk.Frame(self, bg='deep sky blue', height=40)
        navbar.pack(fill='x', side='top')
        self.custom_logo = tk.Canvas(navbar, width=100, height=100, bg='deep sky blue', highlightthickness=0)
        self.custom_logo.create_oval(10, 10, 90, 90, fill='deep sky blue')
        self.custom_logo.create_text(50, 50, text="FF", fill="white", font=("Helvetica", 24))
        self.custom_logo.pack(side='left', padx=10)
        tk.Label(navbar, text=f"Welcome {self.name}", bg='deep sky blue', fg='white', font=('Helvetica', 12)).pack(side='left')

        # Main frame
        self.main_frame = tk.Frame(self, bg='black')
        tk.Label(self.main_frame, text="Introducing FuelFlex - Your Convenient Fuel Payment Solution", font=("Helvetica", 18), bg='black', fg='white').pack(pady=20)

        # Add buttons and functionalities for the main window here
        purchase_button = tk.Button(self.main_frame, text="Purchase Fuel", command=self.open_purchase_window)
        purchase_button.pack(pady=10)

        view_receipts_button = tk.Button(self.main_frame, text="View Receipts", command=self.open_view_receipts_window)
        view_receipts_button.pack(pady=10)

        download_receipts_button = tk.Button(self.main_frame, text="Download Receipts", command=self.open_download_receipts_window)
        download_receipts_button.pack(pady=10)

        view_statements_button = tk.Button(self.main_frame, text="View Yearly Statements", command=self.view_yearly_statements)
        view_statements_button.pack(pady=10)

        description_label = tk.Label(self.main_frame, text="With FuelFlex, you'll have access to a virtual card that allows you to purchase fuel up to a limit of 3000R per month. If you exceed this limit, the card will no longer work until the next billing cycle.\n\nAt the end of each month, you'll receive a bill for the amount of fuel you consumed, plus an 11.5% interest charge. For example, if you used 500R worth of fuel, you'll be charged an additional R57.50 in interest (11.5% of 500R), bringing your total bill to R557.50. This includes a return charge of R17 and a profit of R40.50.\n\nThe FuelFlex app allows you to easily track your balances, view receipts, and find nearby petrol stations.", bg='black', fg='white')
        description_label.pack(pady=20)

        self.main_frame.pack(expand=True)

    def open_purchase_window(self):
        # Clear the window
        for widget in self.winfo_children():
            widget.destroy()

        # Navigation bar
        navbar = tk.Frame(self, bg='deep sky blue', height=40)
        navbar.pack(fill='x', side='top')
        self.custom_logo = tk.Canvas(navbar, width=100, height=100, bg='deep sky blue', highlightthickness=0)
        self.custom_logo.create_oval(10, 10, 90, 90, fill='deep sky blue')
        self.custom_logo.create_text(50, 50, text="FF", fill="white", font=("Helvetica", 24))
        self.custom_logo.pack(side='left', padx=10)
        back_button = tk.Button(navbar, text="←", command=self.initialize_main_window)
        back_button.pack(side='right', padx=10)
        tk.Label(navbar, text="Purchase Fuel", bg='deep sky blue', fg='white', font=('Helvetica', 12)).pack(side='left')

        # Purchase window frame
        purchase_frame = tk.Frame(self, bg='black')
        tk.Label(purchase_frame, text="Purchase Fuel Window", font=("Helvetica", 16), bg='black', fg='white').pack(pady=20)
        tk.Label(purchase_frame, text="Enter the amount of fuel you want to purchase:", bg='black', fg='white').pack(pady=10)
        fuel_amount_entry = tk.Entry(purchase_frame)
        fuel_amount_entry.pack(pady=10)

        def calculate_monthly_bill(fuel_amount):
            interest = fuel_amount * INTEREST_RATE
            total_amount = fuel_amount + interest + 17 + 40.5
            return total_amount

        def purchase_fuel():
            fuel_amount = float(fuel_amount_entry.get())
            monthly_bill = calculate_monthly_bill(fuel_amount)
            if self.monthly_fuel_purchased + fuel_amount <= MONTHLY_LIMIT:
                self.monthly_fuel_purchased += fuel_amount
                self.transactions.append((datetime.datetime.now(), "Fuel Purchase", monthly_bill))  # Record transaction
                messagebox.showinfo("Purchase Successful", f"Your total bill for this month is: R{monthly_bill:.2f}")
                # Now prompt the user to choose the payment method
                choose_payment_method(monthly_bill)
            else:
                remaining_amount = MONTHLY_LIMIT - self.monthly_fuel_purchased
                messagebox.showerror("Error", f"You have reached your monthly limit for fuel purchase. Amount remaining: R{remaining_amount:.2f}")
            fuel_amount_entry.delete(0, tk.END)

        def choose_payment_method(amount):
            payment_frame = tk.Frame(purchase_frame, bg='black')
            tk.Label(payment_frame, text="Choose Payment Method:", bg='black', fg='white', font=('Helvetica', 12)).pack(pady=10)

            def pay_with_visa():
                messagebox.showinfo("Payment Method", f"Payment of R{amount:.2f} with Visa is successful.")
                payment_frame.destroy()

            def pay_with_mastercard():
                messagebox.showinfo("Payment Method", f"Payment of R{amount:.2f} with Mastercard is successful.")
                payment_frame.destroy()

            def pay_with_mpesa():
                messagebox.showinfo("Payment Method", f"Payment of R{amount:.2f} with M-Pesa is successful.")
                payment_frame.destroy()

            def pay_with_ecocash():
                messagebox.showinfo("Payment Method", f"Payment of R{amount:.2f} with EcoCash is successful.")
                payment_frame.destroy()

            visa_button = tk.Button(payment_frame, text="Visa", command=pay_with_visa)
            visa_button.pack(pady=5)
            mastercard_button = tk.Button(payment_frame, text="Mastercard", command=pay_with_mastercard)
            mastercard_button.pack(pady=5)
            mpesa_button = tk.Button(payment_frame, text="M-Pesa", command=pay_with_mpesa)
            mpesa_button.pack(pady=5)
            ecocash_button = tk.Button(payment_frame, text="EcoCash", command=pay_with_ecocash)
            ecocash_button.pack(pady=5)

            payment_frame.pack()

        purchase_button = tk.Button(purchase_frame, text="Purchase", command=purchase_fuel)
        purchase_button.pack(pady=10)

        purchase_frame.pack(expand=True)

    def open_view_receipts_window(self):
        # Clear the window
        for widget in self.winfo_children():
            widget.destroy()

        # Navigation bar
        navbar = tk.Frame(self, bg='deep sky blue', height=40)
        navbar.pack(fill='x', side='top')
        self.custom_logo = tk.Canvas(navbar, width=100, height=100, bg='deep sky blue', highlightthickness=0)
        self.custom_logo.create_oval(10, 10, 90, 90, fill='deep sky blue')
        self.custom_logo.create_text(50, 50, text="FF", fill="white", font=("Helvetica", 24))
        self.custom_logo.pack(side='left', padx=10)
        back_button = tk.Button(navbar, text="←", command=self.initialize_main_window)
        back_button.pack(side='right', padx=10)
        tk.Label(navbar, text="View Receipts", bg='deep sky blue', fg='white', font=('Helvetica', 12)).pack(side='left')

        # View receipts window frame
        view_receipts_frame = tk.Frame(self, bg='black')
        tk.Label(view_receipts_frame, text="View Receipts Window", font=("Helvetica", 16), bg='black', fg='white').pack(pady=20)

        receipt_text = ""
        for transaction in self.transactions:
            receipt_text += f"{transaction[0].strftime('%Y-%m-%d')}   {transaction[1]}   R{transaction[2]:.2f}\n"

        receipt_label = tk.Label(view_receipts_frame, text=receipt_text, bg='black', fg='white')
        receipt_label.pack(pady=20)

        view_receipts_frame.pack(expand=True)

    def open_download_receipts_window(self):
        # Clear the window
        for widget in self.winfo_children():
            widget.destroy()

        # Navigation bar
        navbar = tk.Frame(self, bg='deep sky blue', height=40)
        navbar.pack(fill='x', side='top')
        self.custom_logo = tk.Canvas(navbar, width=100, height=100, bg='deep sky blue', highlightthickness=0)
        self.custom_logo.create_oval(10, 10, 90, 90, fill='deep sky blue')
        self.custom_logo.create_text(50, 50, text="FF", fill="white", font=("Helvetica", 24))
        self.custom_logo.pack(side='left', padx=10)
        back_button = tk.Button(navbar, text="←", command=self.initialize_main_window)
        back_button.pack(side='right', padx=10)
        tk.Label(navbar, text="Download Receipts", bg='deep sky blue', fg='white', font=('Helvetica', 12)).pack(side='left')

        # Download receipts window frame
        download_receipts_frame = tk.Frame(self, bg='black')
        tk.Label(download_receipts_frame, text="Download Receipts Window", font=("Helvetica", 16), bg='black', fg='white').pack(pady=20)

        receipt_text = ""
        for transaction in self.transactions:
            receipt_text += f"{transaction[0].strftime('%Y-%m-%d')}   {transaction[1]}   R{transaction[2]:.2f}\n"

        with open("transactions_receipts.txt", "w") as file:
            file.write(receipt_text)

        download_label = tk.Label(download_receipts_frame, text="Receipts downloaded as transactions_receipts.txt", bg='black', fg='white')
        download_label.pack(pady=20)

        download_receipts_frame.pack(expand=True)

    def view_yearly_statements(self):
        # Generate yearly statement PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="FuelFlex - Yearly Statement", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Name: {self.name}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Phone Number: {self.phone_number}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Date: {datetime.datetime.now().strftime('%Y-%m-%d')}", ln=True, align="L")
        pdf.cell(200, 10, txt="\n", ln=True)  # Add empty line
        pdf.cell(200, 10, txt="Yearly Statement:", ln=True, align="L")
        # Add yearly statement data here
        pdf.output("yearly_statement.pdf")

# Run the application
if __name__ == "__main__":
    app = FuelFlexApp()
    app.mainloop()
