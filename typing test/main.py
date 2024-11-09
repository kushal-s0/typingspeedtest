import tkinter as tk
import time
import random
import threading

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("600x400")  # Set a fixed size for the window
        
        # Sample list of words for random text generation
        self.word_list = [
            "algorithm", "performance", "python", "efficiency", "programming", "development", 
            "computer", "machine", "science", "technology", "data", "analytics", "artificial", "intelligence", 
            "networks", "automation", "security", "innovation", "database", "system"
        ]
        
        # Initialize the start and end time variables
        self.start_time = None
        self.end_time = None
        self.time_limit = 60  # 60 seconds time limit
        self.timer_thread = None  # To hold the timer thread reference
        
        # Instructions Label
        self.instructions_label = tk.Label(root, text="Welcome to the Typing Speed Test!\nType the passage below as quickly as possible.", font=("Helvetica", 14))
        self.instructions_label.pack(pady=10)
        
        # Display Passage
        self.passage_label = tk.Label(root, text="", font=("Arial", 16), width=50, height=4, bg="lightgray", wraplength=550)
        self.passage_label.pack(pady=20)
        
        # Entry widget to type the passage
        self.typing_entry = tk.Entry(root, font=("Arial", 16), width=50, bd=2)
        self.typing_entry.pack(pady=10)
        
        # Start Button
        self.start_button = tk.Button(root, text="Start Test", font=("Arial", 14), command=self.start_test, bg="#4CAF50", fg="white")
        self.start_button.pack(pady=10)
        
        # Result Labels
        self.result_label = tk.Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)
        
        # A Progress Bar (Optional for visual feedback)
        self.progress = tk.Label(root, text="", font=("Arial", 12), fg="gray")
        self.progress.pack(pady=10)
    
    def generate_random_text(self):
        """Generate a random passage by selecting words from the list."""
        num_words = random.randint(10, 20)  # Generate a random number of words for the passage
        random_words = random.sample(self.word_list, num_words)
        return " ".join(random_words)

    def start_test(self):
        self.start_button.config(state="disabled")  # Disable the start button once the test starts
        self.typing_entry.delete(0, tk.END)  # Clear the entry widget
        
        # Generate a random passage and display it
        self.passage = self.generate_random_text()
        self.passage_label.config(text=self.passage)
        
        self.start_time = time.time()  # Record the start time
        self.result_label.config(text="Start typing the passage above...")  # Instruction to start typing
        
        self.typing_entry.bind("<KeyRelease>", self.check_typing)  # Bind key release event to check typing
        
        # Start the 60-second timer in a separate thread
        self.timer_thread = threading.Timer(self.time_limit, self.time_up)
        self.timer_thread.start()

    def time_up(self):
        """This function will be called when the 60 seconds are up."""
        self.end_time = time.time()  # Record the end time after the time limit is reached
        self.typing_entry.config(state="disabled")  # Disable further typing
        self.result_label.config(text="Time's up! The test has ended.")
        self.calculate_results()

    def check_typing(self, event):
        user_input = self.typing_entry.get()
        
        # Update progress as the user types
        progress_text = f"Typing Progress: {len(user_input)}/{len(self.passage)} characters"
        self.progress.config(text=progress_text)

        if user_input == self.passage:
            self.end_time = time.time()  # Record the end time when the passage is correctly typed
            self.typing_entry.config(state="disabled")  # Disable further typing
            self.timer_thread.cancel()  # Cancel the timer if the user finishes before the time limit
            self.result_label.config(text="Congratulations! You've completed the test!")
            self.calculate_results()

    def calculate_results(self):
        """Calculate and display the typing speed, accuracy, and time taken."""
        time_taken = self.end_time - self.start_time  # Time taken in seconds
        user_input = self.typing_entry.get()
        
        # Number of words typed
        words_typed = len(user_input.split())
        
        # Calculate words per minute (WPM)
        wpm = (words_typed / time_taken) * 60 if time_taken > 0 else 0
        
        # Accuracy (compared to the original passage)
        accuracy = sum(1 for a, b in zip(user_input, self.passage) if a == b) / len(self.passage) * 100
        
        # Display the results
        result_text = (f"Test Complete!\n"
                       f"Time Taken: {time_taken:.2f} seconds\n"
                       f"Words Typed: {words_typed}\n"
                       f"Typing Speed: {wpm:.2f} words per minute\n"
                       f"Accuracy: {accuracy:.2f}%")
        self.result_label.config(text=result_text)
        self.start_button.config(state="normal")  # Re-enable the start button for a new test

# Main loop
root = tk.Tk()
typing_test = TypingSpeedTest(root)
root.mainloop()
