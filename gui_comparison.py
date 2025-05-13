import tkinter as tk
from tkinter import messagebox
import time
import threading
import psutil 
import tracemalloc  
from algorithms import brute_force, backtracking, trie_based
import matplotlib.pyplot as plt

def load_dictionary(filepath):
    with open(filepath, 'r') as file:
        return set(word.strip().lower() for word in file)

dictionary = load_dictionary('./data/english_words.txt')

class ComparisonGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Algorithm Comparison (Anagram Solver)")
        self.root.geometry("600x500")

        tk.Label(root, text="Enter scrambled letters:").pack(pady=10)
        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)

        tk.Button(root, text="Run Comparison", command=self.run_comparison).pack(pady=10)
        self.status_label = tk.Label(root, text="", fg="blue")
        self.status_label.pack(pady=10)

        tk.Label(root, text="System Resource Usage:").pack(pady=5)
        self.resource_text = tk.Text(root, height=10, width=70)
        self.resource_text.pack()

    def run_comparison(self):
        letters = self.entry.get().lower()
        if not letters.isalpha():
            messagebox.showerror("Invalid Input", "Enter letters only!")
            return

        threading.Thread(target=self._execute_comparison, args=(letters,)).start()

    def _execute_comparison(self, letters):
        results = []
        usage_report = ""

        # Brute Force
        if len(letters) <= 7:
            self.root.after(0, self._update_status, "Running Brute Force...")
            start = time.time()
            process = psutil.Process()
            cpu_start = psutil.cpu_percent(interval=None)
            mem_before = process.memory_info().rss / (1024 * 1024)
            bf_words = brute_force.solve(letters, dictionary)
            elapsed = time.time() - start
            mem_after = process.memory_info().rss / (1024 * 1024)
            results.append(("Brute Force", elapsed, len(bf_words)))
            usage_report += f"Brute Force:\nTime: {elapsed:.4f}s | Memory: {mem_after - mem_before:.2f} MB\n\n"
            self.root.after(0, self._update_status, f"Completed Brute Force in {elapsed:.4f} seconds.")
        else:
            results.append(("Brute Force", 0, 0))
            usage_report += "Brute Force: Skipped (input > 7 letters)\n\n"

        # Backtracking
        if len(letters) <= 9:
            self.root.after(0, self._update_status, "Running Backtracking...")
            start = time.time()
            process = psutil.Process()
            mem_before = process.memory_info().rss / (1024 * 1024)
            bt_words = backtracking.solve(letters, dictionary)
            elapsed = time.time() - start
            mem_after = process.memory_info().rss / (1024 * 1024)
            results.append(("Backtracking", elapsed, len(bt_words)))
            usage_report += f"Backtracking:\nTime: {elapsed:.4f}s | Memory: {mem_after - mem_before:.2f} MB\n\n"
            self.root.after(0, self._update_status, f"Completed Backtracking in {elapsed:.4f} seconds.")
        else:
            results.append(("Backtracking", 0, 0))
            usage_report += "Backtracking: Skipped (input > 9 letters)\n\n"

        # Trie-based
        if len(letters) <= 12:
            self.root.after(0, self._update_status, "Running Trie-based...")
            start = time.time()
            process = psutil.Process()
            mem_before = process.memory_info().rss / (1024 * 1024)
            tb_words = trie_based.solve(letters, dictionary)
            elapsed = time.time() - start
            mem_after = process.memory_info().rss / (1024 * 1024)
            results.append(("Trie-based", elapsed, len(tb_words)))
            usage_report += f"Trie-based:\nTime: {elapsed:.4f}s | Memory: {mem_after - mem_before:.2f} MB\n\n"
            self.root.after(0, self._update_status, f"Completed Trie-based in {elapsed:.4f} seconds.")
        else:
            results.append(("Trie-based", 0, 0))
            usage_report += "Trie-based: Skipped (input > 12 letters)\n\n"

        self.root.after(0, self._plot_results, results)
        self.root.after(0, self._update_resource_text, usage_report)

    def _update_status(self, message):
        self.status_label.config(text=message)

    def _update_resource_text(self, text):
        self.resource_text.delete(1.0, tk.END)
        self.resource_text.insert(tk.END, text)

    def _plot_results(self, results):
        names = [r[0] for r in results]
        times = [r[1] for r in results]
        word_counts = [r[2] for r in results]

        print("\n--- Chart Descriptions ---")
        print("1. Execution Time Chart: Shows how long each algorithm takes to find all valid words.")
        print(f"   Times (seconds): {dict(zip(names, times))}")
        print("2. Words Found Chart: Displays how many valid words each algorithm discovered.")
        print(f"   Word counts: {dict(zip(names, word_counts))}\n")

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.bar(names, times, color=['blue', 'green', 'orange'])
        plt.title("Execution Time (Seconds)")
        plt.ylabel("Time (s)")

        plt.subplot(1, 2, 2)
        plt.bar(names, word_counts, color=['blue', 'green', 'orange'])
        plt.title("Words Found")
        plt.ylabel("Word Count")

        plt.tight_layout()
        plt.show(block=False)

    # Inside your class ComparisonGUI:
    def _execute_comparison(self, letters):
        results = []
        usage_report = ""

        # Brute Force (≤7)
        if len(letters) <= 7:
            self.root.after(0, self._update_status, "Running Brute Force...")
            tracemalloc.start()
            start = time.time()
            bf_words = brute_force.solve(letters, dictionary)
            elapsed = time.time() - start
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            results.append(("Brute Force", elapsed, len(bf_words)))
            usage_report += f"Brute Force:\nTime: {elapsed:.4f}s | Peak Memory: {peak / 1024:.2f} KB\n\n"
            self.root.after(0, self._update_status, f"Completed Brute Force in {elapsed:.4f} seconds.")
        else:
            results.append(("Brute Force", 0, 0))
            usage_report += "Brute Force: Skipped (input > 7 letters)\n\n"

        # Backtracking (≤9)
        if len(letters) <= 9:
            self.root.after(0, self._update_status, "Running Backtracking...")
            tracemalloc.start()
            start = time.time()
            bt_words = backtracking.solve(letters, dictionary)
            elapsed = time.time() - start
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            results.append(("Backtracking", elapsed, len(bt_words)))
            usage_report += f"Backtracking:\nTime: {elapsed:.4f}s | Peak Memory: {peak / 1024:.2f} KB\n\n"
            self.root.after(0, self._update_status, f"Completed Backtracking in {elapsed:.4f} seconds.")
        else:
            results.append(("Backtracking", 0, 0))
            usage_report += "Backtracking: Skipped (input > 9 letters)\n\n"

        # Trie-based (≤12)
        if len(letters) <= 12:
            self.root.after(0, self._update_status, "Running Trie-based...")
            tracemalloc.start()
            start = time.time()
            tb_words = trie_based.solve(letters, dictionary)
            elapsed = time.time() - start
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            results.append(("Trie-based", elapsed, len(tb_words)))
            usage_report += f"Trie-based:\nTime: {elapsed:.4f}s | Peak Memory: {peak / 1024:.2f} KB\n\n"
            self.root.after(0, self._update_status, f"Completed Trie-based in {elapsed:.4f} seconds.")
        else:
            results.append(("Trie-based", 0, 0))
            usage_report += "Trie-based: Skipped (input > 12 letters)\n\n"

        self.root.after(0, self._plot_results, results)
        self.root.after(0, self._update_resource_text, usage_report)


if __name__ == "__main__":
    root = tk.Tk()
    app = ComparisonGUI(root)
    root.mainloop()
