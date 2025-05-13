import tkinter as tk
from tkinter import messagebox, filedialog  # added filedialog
from PIL import Image, ImageTk
import threading
import time
import tracemalloc
import pygame
from algorithms import trie_based
from PIL import ImageFont, ImageDraw

def load_dictionary(filepath):
    with open(filepath, 'r') as file:
        return set(word.strip().lower() for word in file)

dictionary = load_dictionary('./data/english_words.txt')

class TrieBasedImageGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Unravel Me - Trie-based Solver")
        self.root.geometry("800x600")

        # Initialize pygame mixer
        pygame.mixer.init()

        # Load images
        self.bg_image = ImageTk.PhotoImage(Image.open('SCREEN_BG.png').resize((800, 600)))
        self.logo_image = ImageTk.PhotoImage(Image.open('LOGO.png'))
        self.button_image = ImageTk.PhotoImage(Image.open('BUTTON.png').resize((180, 40)))
        self.textfield_image = ImageTk.PhotoImage(Image.open('TEXT_FIELD.png').resize((400, 40)))
        self.outputbox_image = ImageTk.PhotoImage(Image.open('OUTPUT_BOX.png').resize((600, 200)))

        # Canvas setup
        self.canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # Logo
        self.canvas.create_image(400, 70, image=self.logo_image, anchor="center")

        # Load the custom font
        try:
            custom_font = ImageFont.truetype("MouldyCheeseRegular.ttf", 22)
        except IOError:
            print("MouldyCheeseRegular.ttf not found. Falling back to default font.")
            custom_font = ImageFont.load_default()

        # Create a transparent image
        text_img = Image.new("RGBA", (800, 50), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_img)
        text = "Enter Random or Jumbled Letters"

        # Use textbbox for Pillow 10+
        bbox = draw.textbbox((0, 0), text, font=custom_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Draw centered text
        draw.text(((800 - text_width) / 2, 0), text, font=custom_font, fill="#24624C")

        # Convert to Tkinter image
        self.text_image = ImageTk.PhotoImage(text_img)

        # Display on canvas
        self.canvas.create_image(400, 160, image=self.text_image, anchor="center")


        # Entry background + field
        self.canvas.create_image(400, 200, image=self.textfield_image, anchor="center")
        self.entry = tk.Entry(root, font=("Helvetica", 14), bd=0, justify="center")
        self.canvas.create_window(400, 200, window=self.entry, width=380, height=30)

        # Create Run Trie-based button text as image
        run_text_img = Image.new("RGBA", (170, 20), (0, 0, 0, 0))
        run_draw = ImageDraw.Draw(run_text_img)
        run_text = "Run Trie-based"
        bbox = run_draw.textbbox((0, 0), run_text, font=custom_font)
        text_width = bbox[2] - bbox[0]
        run_draw.text(((200 - text_width) / 2, 0), run_text, font=ImageFont.truetype("MouldyCheeseRegular.ttf", 18), fill="#24624C")
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

        # Results background + text box
        self.canvas.create_image(400, 450, image=self.outputbox_image, anchor="center")
        self.result_text = tk.Text(root, height=10, width=70, bd=0, font=("Helvetica", 10), bg="#ffffff")
        self.canvas.create_window(400, 450, window=self.result_text, width=580, height=180)

        # Export button
        export_text_img = Image.new("RGBA", (170, 20), (0, 0, 0, 0))
        export_draw = ImageDraw.Draw(export_text_img)
        export_text = "Export to txt"
        bbox = export_draw.textbbox((0, 0), export_text, font=custom_font)
        text_width = bbox[2] - bbox[0]
        export_draw.text(((200 - text_width) / 2, 0), export_text, font=ImageFont.truetype("MouldyCheeseRegular.ttf", 18), fill="#24624C")
        self.export_text_image = ImageTk.PhotoImage(export_text_img)
        export_item = self.canvas.create_image(400, 560, image=self.button_image, anchor="center")
        export_text = self.canvas.create_image(400, 560, image=self.export_text_image, anchor="center")
        self.canvas.tag_bind(export_item, "<Button-1>", self.export_to_txt)
        self.canvas.tag_bind(export_text, "<Button-1>", self.export_to_txt)

        # Completion badge (✔ Completed!)
        self.completion_label = tk.Label(root, text="✔ Completed!", bg="#fefecb", fg="#4CAF50", font=("Helvetica", 14, "bold"))

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
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_memory_mb = peak / (1024 * 1024)

        if not words:
            result = "No valid words found.\n"
        else:
            grouped_words = {}
            for word in words:
                grouped_words.setdefault(len(word), []).append(word)

            result = f"Total Words Found: {sum(len(w) for w in grouped_words.values())}\n"
            for length in sorted(grouped_words):
                result += f"\n{length}-Letter Words ({len(grouped_words[length])}):\n"
                result += ', '.join(sorted(grouped_words[length])) + '\n'

        result += f"\nTime: {elapsed:.4f} seconds"
        result += f"\nPeak Memory Used: {peak_memory_mb:.4f} MB"

        self.result_text.after(0, self._update_result_text, result)
        self.status_label.after(0, self._update_status, f"Completed Trie-based in {elapsed:.4f} seconds.")

        # Play sound + show badge
        threading.Thread(target=self._play_completion_sound).start()
        self.root.after(0, self._show_completion_badge)

    def _update_result_text(self, text):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)

    def _update_status(self, message):
        self.status_label.config(text=message, font=("", 12), fg= "#8B9E4D")

    def _play_completion_sound(self):
        try:
            pygame.mixer.music.load('ding.mp3')
            pygame.mixer.music.play()
        except Exception as e:
            print("Error playing sound:", e)

    def _show_completion_badge(self):
        self.completion_label.place(x=350, y=330)
        self.root.after(2000, lambda: self.completion_label.place_forget())

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
