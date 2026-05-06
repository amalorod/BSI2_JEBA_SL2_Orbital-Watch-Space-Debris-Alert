import tkinter as tk
from tkinter import scrolledtext, messagebox



from src.challenge1 import run_challenge_1
from src.challenge2 import run_challenge_2
from src.challenge3 import run_challenge_3



class OrbitalWatchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Orbital Watch – Space Debris Alert")
        self.root.geometry("760x520")
        self.root.configure(bg="#101820")

        title = tk.Label(
            root,
            text="Orbital Watch",
            font=("Arial", 26, "bold"),
            bg="#101820",
            fg="#FEE715"
        )
        title.pack(pady=15)

        subtitle = tk.Label(
            root,
            text="Space Debris Alert System",
            font=("Arial", 13),
            bg="#101820",
            fg="white"
        )
        subtitle.pack(pady=5)

        button_frame = tk.Frame(root, bg="#101820")
        button_frame.pack(pady=15)

        self.create_button(button_frame, "Challenge 1", self.run_challenge_1).grid(row=0, column=0, padx=8)
        self.create_button(button_frame, "Challenge 2", self.run_challenge_2).grid(row=0, column=1, padx=8)
        self.create_button(button_frame, "Challenge 3", self.run_challenge_3).grid(row=0, column=2, padx=8)
        self.create_button(button_frame, "Alle ausführen", self.run_all).grid(row=0, column=3, padx=8)

        self.output = scrolledtext.ScrolledText(
            root,
            width=86,
            height=20,
            font=("Consolas", 11),
            bg="#1E1E1E",
            fg="#D4D4D4",
            insertbackground="white"
        )
        self.output.pack(padx=20, pady=15)

    def create_button(self, parent, text, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg="#FEE715",
            fg="#101820",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=8,
            relief=tk.FLAT
        )

    def write(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def clear(self):
        self.output.delete("1.0", tk.END)

    def handle_error(self, error):
        messagebox.showerror("Fehler", str(error))
        self.write(f"ERROR: {error}")

    def run_challenge_1(self):
        try:
            result = run_challenge_1()
            self.write(f"Challenge 1 result: {result}")
            self.write("Expected result: 2436297.459044")
            self.write("")
        except Exception as error:
            self.handle_error(error)

    def run_challenge_2(self):
        try:
            result = run_challenge_2()
            self.write(f"Challenge 2 result: {result}")
            self.write("Expected result: -359776.16973")
            self.write("")
        except Exception as error:
            self.handle_error(error)

    def run_challenge_3(self):
        try:
            risks, total_distance_m = run_challenge_3()

            self.write(f"Challenge 3 collision risks: {len(risks)}")
            self.write(f"Total distance: {total_distance_m} m")
            self.write("Expected: 3 risks and 1500 m")
            self.write("")

            for risk in risks:
                self.write(
                    f"- {risk['satellite']} near {risk['debris']}: "
                    f"{risk['distance_m']} m"
                )

            self.write("")
        except Exception as error:
            self.handle_error(error)

    def run_all(self):
        self.clear()
        self.run_challenge_1()
        self.run_challenge_2()
        self.run_challenge_3()


def main():
    root = tk.Tk()
    app = OrbitalWatchApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()