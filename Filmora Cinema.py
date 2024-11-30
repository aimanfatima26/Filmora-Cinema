import tkinter as tk
from tkinter import messagebox, font
from collections import deque
import os
import json

# File paths for saving data
BOOKING_FILE = "booking_history.txt"
SHOWS_FILE = "shows_data.txt"

# Initialize global variables
booking_queue = deque()  # Queue to store booking requests in order
booking_history = []  # List to keep track of all bookings

# Default shows data
shows = {
    "Show1": {"seats": 10, "ticket_prices": {"Silver": 50, "Gold": 100, "Platinum": 150}},
    "Show2": {"seats": 8, "ticket_prices": {"Silver": 60, "Gold": 120, "Platinum": 180}},
}

# Load previous data if available
def load_data():
    global shows, booking_history
    try:
        if os.path.exists(SHOWS_FILE):
            with open(SHOWS_FILE, 'r') as file:
                shows = json.load(file)
        if os.path.exists(BOOKING_FILE):
            with open(BOOKING_FILE, 'r') as file:
                booking_history.extend(json.load(file))
    except (IOError, json.JSONDecodeError) as e:
        messagebox.showerror("Error", f"Error loading data: {e}")

# Save shows data to file
def save_shows_data():
    try:
        with open(SHOWS_FILE, 'w') as file:
            json.dump(shows, file)
    except IOError as e:
        messagebox.showerror("Error", f"Error saving show data: {e}")

# Save booking history to file
def save_booking_history():
    try:
        with open(BOOKING_FILE, 'w') as file:
            json.dump(booking_history, file)
    except IOError as e:
        messagebox.showerror("Error", f"Error saving booking history: {e}")

# Main Application class
class TicketBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Filmora Cinema")
        self.root.geometry("900x500")
        self.root.configure(bg="#fce4ec")  # Light pink background
        
        # Fonts
        self.title_font = font.Font(size=20, weight="bold")
        self.label_font = font.Font(size=14)
        
        # Cinema Name Screen
        self.show_cinema_name()

    def show_cinema_name(self):
        """First screen displaying the cinema name and welcome message"""
        self.clear_screen()

        tk.Label(self.root, text="Filmora Cinema", font=self.title_font, bg="#fce4ec", fg="#880e4f").pack(pady=30)
        tk.Label(self.root, text="Welcome to Filmora Cinema", font=self.label_font, bg="#fce4ec", fg="#880e4f").pack(pady=20)
        
        tk.Button(self.root, text="For Booking", command=self.create_welcome_screen, font=self.label_font,
                  bg="#f48fb1", fg="white", activebackground="#880e4f", activeforeground="white").pack(pady=10)

    def create_welcome_screen(self):
        """Welcome screen with options for booking, canceling or viewing history"""
        self.clear_screen()

        tk.Label(self.root, text="Welcome to Movie Ticket Booking", font=self.title_font, bg="#fce4ec", fg="#880e4f").pack(pady=20)
        
        tk.Button(self.root, text="Book a Ticket", command=self.book_ticket, font=self.label_font,
                  bg="#ff80ab", fg="white", activebackground="#880e4f", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Cancel a Booking", command=self.cancel_booking, font=self.label_font,
                  bg="#ec407a", fg="white", activebackground="#880e4f", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="View Booking History", command=self.show_booking_history, font=self.label_font,
                  bg="#ec407a", fg="white", activebackground="#880e4f", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="View Available Shows", command=self.view_available_shows, font=self.label_font,
                  bg="#d81b60", fg="white", activebackground="#880e4f", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Quit", command=self.quit_app, font=self.label_font,
                  bg="#ad1457", fg="white", activebackground="#880e4f", activeforeground="white").pack(pady=10)

    def book_ticket(self):
        """Booking screen with options for selecting shows and ticket types"""
        self.clear_screen()
        
        tk.Label(self.root, text="Book Your Ticket", font=self.title_font, bg="#fce4ec", fg="#880e4f").pack(pady=20)
        
        tk.Label(self.root, text="Enter your name:", font=self.label_font, bg="#fce4ec", fg="#880e4f").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        tk.Label(self.root, text="Select Show:", font=self.label_font, bg="#fce4ec", fg="#880e4f").pack()
        self.show_var = tk.StringVar(value=list(shows.keys())[0])
        tk.OptionMenu(self.root, self.show_var, *shows.keys()).pack(pady=5)

        tk.Label(self.root, text="Select Ticket Category:", font=self.label_font, bg="#fce4ec", fg="#880e4f").pack()
        self.category_var = tk.StringVar(value="Silver")
        tk.OptionMenu(self.root, self.category_var, "Silver", "Gold", "Platinum").pack(pady=5)
        
        tk.Button(self.root, text="Confirm Booking", command=self.confirm_booking, font=self.label_font,
                  bg="#e91e63", fg="white", activebackground="#880e4f", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_welcome_screen, font=self.label_font,
                  bg="#c2185b", fg="white", activebackground="#880e4f", activeforeground="white").pack()

    def confirm_booking(self):
        """Handle ticket booking and seat availability"""
        try:
            name = self.name_entry.get()
            show_name = self.show_var.get()
            ticket_type = self.category_var.get()
            
            if not name:
                messagebox.showerror("Error", "Please enter your name.")
                return
            
            show_info = shows[show_name]
            available_seats = show_info["seats"]
            
            if available_seats > 0:
                # Process the booking
                show_info["seats"] -= 1
                price = show_info["ticket_prices"][ticket_type]
                booking_queue.append((name, show_name, ticket_type, price))
                booking_history.append((name, show_name, ticket_type, price))
                
                # Save data to files
                save_booking_history()
                save_shows_data()
                
                messagebox.showinfo("Booking Confirmed", f"Booking confirmed for {name}.\nShow: {show_name}\nTicket: {ticket_type}\nPrice: ${price}")
            else:
                # Add to waiting list if no seats are available
                messagebox.showinfo("Waiting List", f"No seats available for {show_name}. {name} has been added to the waiting list.")
        except KeyError as e:
            messagebox.showerror("Error", f"Invalid data selection: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        finally:
            self.create_welcome_screen()

    def cancel_booking(self):
        """Allow the user to cancel a booking by searching their name"""
        self.clear_screen()

        tk.Label(self.root, text="Cancel Booking", font=self.title_font, bg="#fce4ec", fg="#880e4f").pack(pady=20)
        
        tk.Label(self.root, text="Enter your name to cancel the booking:", font=self.label_font, bg="#fce4ec", fg="#880e4f").pack()
        self.cancel_name_entry = tk.Entry(self.root)
        self.cancel_name_entry.pack(pady=5)

        tk.Button(self.root, text="Search Booking", command=self.search_booking, font=self.label_font,
                  bg="#ff80ab", fg="white", activebackground="#880e4f", activeforeground="white").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_welcome_screen, font=self.label_font,
                  bg="#c2185b", fg="white", activebackground="#880e4f", activeforeground="white").pack()

    def search_booking(self):
        """Search for a booking by name and cancel it"""
        name = self.cancel_name_entry.get()
        if not name:
            messagebox.showerror("Error", "Please enter your name to search.")
            return
        
        found = False
        for booking in booking_history:
            if booking[0].lower() == name.lower():
                show_name = booking[1]
                ticket_type = booking[2]
                price = booking[3]
                # Remove from history and re-add the seat
                booking_history.remove(booking)
                shows[show_name]["seats"] += 1
                save_booking_history()
                save_shows_data()

                messagebox.showinfo("Booking Canceled", f"Your booking for {show_name} ({ticket_type}) has been canceled.\nRefund: ${price}")
                found = True
                break
        
        if not found:
            messagebox.showerror("Error", "Booking not found.")

        self.create_welcome_screen()

    def view_available_shows(self):
        """Display available shows and their seat availability"""
        self.clear_screen()

        tk.Label(self.root, text="Available Shows", font=self.title_font, bg="#fce4ec", fg="#880e4f").pack(pady=20)

        shows_text = "\n".join(
            [f"{show}: {info['seats']} seats available" for show, info in shows.items()]
        )

        tk.Label(self.root, text=shows_text, font=self.label_font, bg="#fce4ec", fg="#880e4f", justify="left").pack(pady=10)

        tk.Button(self.root, text="Back", command=self.create_welcome_screen, font=self.label_font,
                  bg="#c2185b", fg="white", activebackground="#880e4f", activeforeground="white").pack()

    def show_booking_history(self):
        """Display all past bookings in a new window"""
        try:
            self.clear_screen()
            
            tk.Label(self.root, text="Booking History", font=self.title_font, bg="#fce4ec", fg="#880e4f").pack(pady=20)
            
            history_text = "\n".join(
                [f"Name: {name}, Show: {show}, Ticket: {ticket}, Price: ${price}" for name, show, ticket, price in booking_history]
            ) or "No bookings yet."
            
            history_label = tk.Label(self.root, text=history_text, font=self.label_font, bg="#fce4ec", fg="#880e4f", justify="left")
            history_label.pack(pady=10)
            
            tk.Button(self.root, text="Back", command=self.create_welcome_screen, font=self.label_font,
                      bg="#c2185b", fg="white", activebackground="#880e4f", activeforeground="white").pack()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load booking history: {e}")

    def quit_app(self):
        """Quit the application after saving data"""
        try:
            save_shows_data()
            save_booking_history()
        except Exception as e:
            messagebox.showerror("Error", f"Error while quitting: {e}")
        finally:
            self.root.quit()

    def clear_screen(self):
        """Clear all widgets from the screen"""
        for widget in self.root.winfo_children():
            widget.destroy()

# Load data and run the application
load_data()
root = tk.Tk()
app = TicketBookingApp(root)
root.mainloop()
