import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageFont, ImageDraw
import threading
import time
import tracemalloc
import pygame
import os
import sys
from algorithms import trie_based

# Load packaged or local resource (for PyInstaller)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # folder for temporary unpacked resources
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load dictionary words
def load_dictionary(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return set(word.strip().lower() for word in file)

dictionary = load_dictionary(resource_path('data/english_words.txt'))

class TrieBasedImageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Unravel Me - Trie-based Solver")
        self.root.geometry("800x600")

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load images
        self.bg_image = ImageTk.PhotoImage(Image.open(resource_path('assets/SCREEN_BG.png')).resize((800, 600)))
        self.logo_image = ImageTk.PhotoImage(Image.open(resource_path('assets/LOGO.png')))
        self.button_image = ImageTk.PhotoImage(Image.open(resource_path('assets/BUTTON.png')).resize((180, 40)))
        self.textfield_image = ImageTk.PhotoImage(Image.open(resource_path('assets/TEXT_FIELD.png')).resize((400, 40)))
        self.outputbox_image = ImageTk.PhotoImage(Image.open(resource_path('assets/OUTPUT_BOX.png')).resize((600, 200)))
        self.completed_image = ImageTk.PhotoImage(Image.open(resource_path('assets/like.png')).resize((250, 250)))

        # Load custom font
        try:
            self.custom_font = ImageFont.truetype(resource_path("assets/MouldyCheeseRegular.ttf"), 22)
        except IOError:
            print("Custom font not found. Using default.")
            self.custom_font = ImageFont.load_default()

        # Set up canvas
        self.canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        self.canvas.create_image(400, 70, image=self.logo_image, anchor="center")

        # Instruction text (drawn using custom font)
        text_img = Image.new("RGBA", (800, 50), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)
        instruction_text = "Enter Random or Jumbled Letters"
        bbox = draw.textbbox((0, 0), instruction_text, font=self.custom_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((800 - text_width) / 2, 0), instruction_text, font=self.custom_font, fill="#24624C")
        self.text_image = ImageTk.PhotoImage(text_img)
        self.canvas.create_image(400, 160, image=self.text_image, anchor="center")

        # Entry box
        self.canvas.create_image(400, 200, image=self.textfield_image, anchor="center")
        self.entry = tk.Entry(root, font=("Helvetica", 14), bd=0, justify="center")
        self.canvas.create_window(400, 200, window=self.entry, width=380, height=30)

        # Run button
        run_text_img = Image.new("RGBA", (170, 20), (0, 0, 0, 0))
        run_draw = ImageDraw.Draw(run_text_img)
        run_draw.text((10, 0), "Run Trie-based", font=ImageFont.truetype(resource_path("assets/MouldyCheeseRegular.ttf"), 18), fill="#24624C")
        self.run_text_image = ImageTk.PhotoImage(run_text_img)
        button_item = self.canvas.create_image(400, 260, image=self.button_image, anchor="center")
        button_text = self.canvas.create_image(400, 260, image=self.run_text_image, anchor="center")
        self.canvas.tag_bind(button_item, "<Button-1>", self.run_trie)
        self.canvas.tag_bind(button_text, "<Button-1>", self.run_trie)

        # Status label
        self.status_label = tk.Label(root, text="", bg="#fefecb", fg="#8B9E4D", font=("MouldyCheeseRegular", 10))
        self.canvas.create_window(400, 310, window=self.status_label)

        # Results label
        self.canvas.create_text(400, 340, text="Results:", font=("Helvetica", 14, "bold"), fill="#4b4b2f")

        # Results display
        self.canvas.create_image(400, 450, image=self.outputbox_image, anchor="center")
        self.result_text = tk.Text(root, height=10, width=70, bd=0, font=("Helvetica", 10), bg="#ffffff")
        self.canvas.create_window(400, 450, window=self.result_text, width=580, height=180)

        # Export button
        export_text_img = Image.new("RGBA", (170, 20), (0, 0, 0, 0))
        export_draw = ImageDraw.Draw(export_text_img)
        export_draw.text((10, 0), "Export to txt", font=ImageFont.truetype(resource_path("assets/MouldyCheeseRegular.ttf"), 18), fill="#24624C")
        self.export_text_image = ImageTk.PhotoImage(export_text_img)
        export_item = self.canvas.create_image(400, 560, image=self.button_image, anchor="center")
        export_text = self.canvas.create_image(400, 560, image=self.export_text_image, anchor="center")
        self.canvas.tag_bind(export_item, "<Button-1>", self.export_to_txt)
        self.canvas.tag_bind(export_text, "<Button-1>", self.export_to_txt)

    def run_trie(self, event=None):
        letters = self.entry.get().lower()
        if not letters.isalpha():
            messagebox.showerror("Invalid Input", "Enter letters only!")
            return
        if len(letters) > 12:
            messagebox.showerror("Input Too Long", "Trie-based supports up to 12 letters.")
            return
        self._update_status("Running Trie-based...")
        threading.Thread(target=self._execute_trie, args=(letters,)).start()

    def _execute_trie(self, letters):
        tracemalloc.start()
        start = time.time()
        words = trie_based.solve(letters, dictionary)
        elapsed = time.time() - start
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_memory_mb = peak / (1024 * 1024)

        result = "No valid words found.\n" if not words else ""
        if words:
            grouped = {}
            for word in words:
                grouped.setdefault(len(word), []).append(word)
            result += f"Total Words Found: {sum(len(g) for g in grouped.values())}\n"
            for length in sorted(grouped):
                result += f"\n{length}-Letter Words ({len(grouped[length])}):\n"
                result += ', '.join(sorted(grouped[length])) + '\n'

        result += f"\nTime: {elapsed:.4f} seconds"
        result += f"\nPeak Memory Used: {peak_memory_mb:.4f} MB"

        self.result_text.after(0, self._update_result_text, result)
        self.status_label.after(0, self._update_status, f"Completed Trie-based in {elapsed:.4f} seconds.")
        threading.Thread(target=self._play_completion_sound).start()
        self.root.after(0, self._show_completion_badge)

    def _update_result_text(self, text):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)

    def _update_status(self, message):
        self.status_label.config(text=message, font=("", 12), fg="#8B9E4D")

    def _play_completion_sound(self):
        try:
            pygame.mixer.music.load(resource_path('assets/sound.mp3'))
            pygame.mixer.music.play()
        except Exception as e:
            print("Error playing sound:", e)

    def _show_completion_badge(self):
        self.root.update_idletasks()
        img_width = self.completed_image.width()
        img_height = self.completed_image.height()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - img_width) // 2
        y = self.root.winfo_rooty() + 180
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.geometry(f"{img_width}x{img_height}+{x}+{y}")
        popup.lift()
        popup.wm_attributes("-topmost", True)
        popup.configure(bg="black")
        popup.wm_attributes("-transparentcolor", "pink")
        label = tk.Label(popup, image=self.completed_image, bg="pink", bd=0, highlightthickness=0)
        label.pack()
        self.root.after(3000, popup.destroy)

    def export_to_txt(self, event=None):
        content = self.result_text.get("1.0", tk.END).strip()
        input_letters = self.entry.get().strip()
        if not input_letters:
            messagebox.showwarning("Missing Input", "Please enter scrambled letters before exporting.")
            return
        if not content:
            messagebox.showwarning("Export Warning", "There is no content to export!")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt")],
                                                 title="Save Results As")
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(f"Input Letters: {input_letters}\n\n")
                    file.write(content)
                messagebox.showinfo("Export Successful", f"Results saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"An error occurred:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrieBasedImageGUI(root)
    root.mainloop()
