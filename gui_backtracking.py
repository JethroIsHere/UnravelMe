import tkinter as tk
from tkinter import messagebox
import time
import threading
from algorithms import backtracking

def load_dictionary(filepath):
    with open(filepath, 'r') as file:
        return set(word.strip().lower() for word in file)

dictionary = load_dictionary('./data/english_words.txt')

class BacktrackingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Unravel Anagram: Backtracking")
        self.root.geometry("600x500")
        
        tk.Label(root, text="Enter scrambled letters:").pack(pady=10)
        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)
        
        tk.Button(root, text="Run Backtracking", command=self.run_backtracking).pack(pady=10)
        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.pack(pady=10)

        tk.Label(root, text="Results:").pack(pady=10)
        self.result_text = tk.Text(root, height=20, width=70)
        self.result_text.pack()

    def run_backtracking(self):
        letters = self.entry.get().lower()
        if not letters.isalpha():
            messagebox.showerror("Invalid Input", "Enter letters only!")
            return
        
        # Cap at 9 letters for Backtracking
        if len(letters) > 9:
            messagebox.showerror("Input Too Long", "Backtracking supports up to 9 letters for performance reasons.")
            return
        
        self._update_status("Running Backtracking...")

        # Run Backtracking in a background thread
        threading.Thread(target=self._execute_backtracking, args=(letters,)).start()

    def _execute_backtracking(self, letters):
        start = time.time()
        words = backtracking.solve(letters, dictionary)
        elapsed = time.time() - start

        if not words:
            result = "No valid words found.\n"
        else:
            # Group words by length
            grouped_words = {}
            for word in words:
                grouped_words.setdefault(len(word), []).append(word)
            
            result = f"Total Words Found: {sum(len(w) for w in grouped_words.values())}\n"
            for length in sorted(grouped_words):
                result += f"\n{length}-Letter Words ({len(grouped_words[length])}):\n"
                result += ', '.join(sorted(grouped_words[length])) + '\n'
        
        result += f"\nTime: {elapsed:.4f} seconds"
        
        # Update GUI safely from the main thread
        self.result_text.after(0, self._update_result_text, result)
        self.status_label.after(0, self._update_status, f"Completed Backtracking in {elapsed:.4f} seconds.")

    def _update_result_text(self, text):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)

    def _update_status(self, message):
        self.status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = BacktrackingGUI(root)
    root.mainloop()
