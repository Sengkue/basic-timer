import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pygame
import os
import sys

class OfficeTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Office Timer")
        self.root.geometry("400x200")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Initialize pygame mixer for sound
        pygame.mixer.init()
        
        # Timer variables
        self.timer_running = False
        self.remaining_time = 0
        self.timer_thread = None
        
        # Create GUI elements
        self.create_widgets()
        
        # Flash variables
        self.original_bg = self.root.cget('bg')
        self.flash_count = 0
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (200 // 2)
        self.root.geometry(f"400x200+{x}+{y}")
        
    def create_widgets(self):
        """Create and arrange GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Timer input frame
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Hours input
        ttk.Label(input_frame, text="Hours:").grid(row=0, column=0, padx=(0, 5))
        self.hours_var = tk.StringVar(value="0")
        self.hours_entry = ttk.Entry(input_frame, textvariable=self.hours_var, width=4)
        self.hours_entry.grid(row=0, column=1, padx=(0, 10))
        
        # Minutes input
        ttk.Label(input_frame, text="Minutes:").grid(row=0, column=2, padx=(0, 5))
        self.minutes_var = tk.StringVar(value="25")
        self.minutes_entry = ttk.Entry(input_frame, textvariable=self.minutes_var, width=4)
        self.minutes_entry.grid(row=0, column=3, padx=(0, 10))
        
        # Seconds input
        ttk.Label(input_frame, text="Seconds:").grid(row=0, column=4, padx=(0, 5))
        self.seconds_var = tk.StringVar(value="0")
        self.seconds_entry = ttk.Entry(input_frame, textvariable=self.seconds_var, width=4)
        self.seconds_entry.grid(row=0, column=5)
        
        # Countdown display
        self.countdown_var = tk.StringVar(value="00:00:00")
        countdown_label = ttk.Label(main_frame, textvariable=self.countdown_var, 
                                   font=("Arial", 22, "bold"))
        countdown_label.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_timer, state="disabled")
        self.stop_button.grid(row=0, column=1)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to start timer")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, font=("Arial", 9))
        status_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))
        
    def validate_input(self):
        """Validate timer input"""
        try:
            hours = int(self.hours_var.get() or "0")
            minutes = int(self.minutes_var.get() or "0")
            seconds = int(self.seconds_var.get() or "0")
            
            if hours < 0 or minutes < 0 or seconds < 0:
                raise ValueError("Time cannot be negative")
            
            if hours == 0 and minutes == 0 and seconds == 0:
                raise ValueError("Please set a time greater than 0")
                
            if minutes >= 60:
                raise ValueError("Minutes must be less than 60")
                
            if seconds >= 60:
                raise ValueError("Seconds must be less than 60")
                
            return hours, minutes, seconds
        except ValueError as e:
            if "invalid literal" in str(e):
                messagebox.showerror("Input Error", "Please enter valid numbers")
            else:
                messagebox.showerror("Input Error", str(e))
            return None, None, None
    
    def start_timer(self):
        """Start the countdown timer"""
        hours, minutes, seconds = self.validate_input()
        if hours is None:
            return
            
        self.remaining_time = hours * 3600 + minutes * 60 + seconds
        self.timer_running = True
        
        # Update button states
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.hours_entry.config(state="disabled")
        self.minutes_entry.config(state="disabled")
        self.seconds_entry.config(state="disabled")
        
        # Start timer thread
        self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
        self.timer_thread.start()
        
        self.status_var.set("Timer running...")
    
    def stop_timer(self):
        """Stop the timer"""
        self.timer_running = False
        self.reset_ui()
        self.status_var.set("Timer stopped")
    
    def reset_ui(self):
        """Reset UI to initial state"""
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.hours_entry.config(state="normal")
        self.minutes_entry.config(state="normal")
        self.seconds_entry.config(state="normal")
        self.countdown_var.set("00:00:00")
        
    def run_timer(self):
        """Run the countdown timer in a separate thread"""
        while self.timer_running and self.remaining_time > 0:
            # Update countdown display
            hours = self.remaining_time // 3600
            minutes = (self.remaining_time % 3600) // 60
            seconds = self.remaining_time % 60
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.countdown_var.set(time_str)
            
            time.sleep(1)
            self.remaining_time -= 1
        
        if self.timer_running:  # Timer finished naturally
            self.timer_finished()
    
    def timer_finished(self):
        """Handle timer completion"""
        self.timer_running = False
        self.countdown_var.set("00:00:00")
        self.status_var.set("Time's up!")
        
        # Reset UI
        self.root.after(0, self.reset_ui)
        
        # Play sound and flash screen
        self.play_notification_sound()
        self.flash_screen()
        
        # Show completion message
        self.root.after(0, lambda: messagebox.showinfo("Timer Complete", "Time's up!"))
    
    def play_notification_sound(self):
        """Play the timer.mp3 file looping for 30 seconds when timer finishes"""
        try:
            # Get the directory where the script is located
            if getattr(sys, 'frozen', False):
                # If running as exe, use the exe directory
                app_dir = os.path.dirname(sys.executable)
            else:
                # If running as script, use script directory
                app_dir = os.path.dirname(os.path.abspath(__file__))
                
            sound_file = os.path.join(app_dir, "timer.mp3")
            
            if os.path.exists(sound_file):
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                # Stop the sound after 30 seconds
                threading.Timer(30.0, lambda: pygame.mixer.music.stop()).start()
            else:
                # Fallback to system beep if mp3 not found
                self.root.bell()
                print(f"Sound file not found: {sound_file}")
        except Exception as e:
            # Fallback to system beep if sound fails
            self.root.bell()
            print(f"Error playing sound: {e}")
    
    def flash_screen(self):
        """Flash the screen background red and white"""
        self.flash_count = 0
        self.flash_background()
    
    def flash_background(self):
        """Recursively flash the background"""
        if self.flash_count < 6:  # Flash 3 times (6 changes)
            if self.flash_count % 2 == 0:
                self.root.configure(bg='red')
            else:
                self.root.configure(bg='white')
            
            self.flash_count += 1
            self.root.after(300, self.flash_background)  # Flash every 300ms
        else:
            # Restore original background
            self.root.configure(bg=self.original_bg)

def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = OfficeTimer(root)
    
    # Handle window closing
    def on_closing():
        if app.timer_running:
            if messagebox.askokcancel("Quit", "Timer is running. Do you want to quit?"):
                app.timer_running = False
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()