import tkinter as tk
from tkinter import ttk, messagebox

CIPHERTEXT = "YXOP TXZWT KNGMKTT SUK CMKHFT HZC GMHLKMT HZC UXGKT XY SUK EXMPAZW GKXGOK"

class CryptogramBoxedSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Cryptogram Boxed Solver")

        self.ciphertext = CIPHERTEXT
        self.substitutions = {}
        self.letter_widgets = []

        self.create_widgets()

    def create_widgets(self):
        # Controls
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=5)

        ttk.Label(control_frame, text="Substitute:").pack(side="left")
        self.from_entry = ttk.Entry(control_frame, width=3)
        self.from_entry.pack(side="left")
        self.to_entry = ttk.Entry(control_frame, width=3)
        self.to_entry.pack(side="left")
        ttk.Button(control_frame, text="Apply", command=self.apply_substitution).pack(side="left")

        # Letter bank (A-Z)
        self.letter_bank_label = ttk.Label(self.root, text="", font=("Courier", 11))
        self.letter_bank_label.pack(pady=5)
        self.update_letter_bank()

        # Grid
        self.grid_frame = ttk.Frame(self.root)
        self.grid_frame.pack(padx=10, pady=10)
        self.render_letter_boxes()

    def render_letter_boxes(self):
        words = self.ciphertext.split()
        row = 0
        col = 0
        max_columns = 6
        self.letter_widgets.clear()

        for word in words:
            word_frame = ttk.Frame(self.grid_frame)
            word_frame.grid(row=row, column=col, padx=5, pady=5)

            word_widgets = []
            for letter in word:
                letter_frame = ttk.Frame(word_frame)
                letter_frame.pack(side="left", padx=1)

                solved_label = ttk.Label(letter_frame, text="_", width=2, relief="solid", anchor="center", font=("Courier", 12))
                solved_label.pack()

                cipher_label = ttk.Label(letter_frame, text=letter, width=2, anchor="center", font=("Courier", 9))
                cipher_label.pack()

                word_widgets.append((letter, solved_label))
            self.letter_widgets.append(word_widgets)

            col += 1
            if col >= max_columns:
                row += 1
                col = 0

        self.update_boxes()

    def apply_substitution(self):
        src = self.from_entry.get().upper()
        dst = self.to_entry.get().upper()

        # Validation
        if not (len(src) == 1 and len(dst) == 1 and src.isalpha() and dst.isalpha()):
            return

        # Prevent duplicate substitutions
        if dst in self.substitutions.values():
            messagebox.showwarning("Duplicate Letter", f"'{dst}' is already used for another letter.")
            return

        self.substitutions[src] = dst
        self.update_boxes()
        self.update_letter_bank()

    def update_boxes(self):
        for word in self.letter_widgets:
            for cipher_letter, solved_label in word:
                solved_letter = self.substitutions.get(cipher_letter, "_")
                solved_label.config(text=solved_letter)

    def update_letter_bank(self):
        used = set(self.substitutions.values())
        bank = ""
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            if letter in used:
                bank += f"· "  # Dots show used letters
            else:
                bank += f"{letter} "
        self.letter_bank_label.config(text=bank)

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = CryptogramBoxedSolver(root)
    root.mainloop()
