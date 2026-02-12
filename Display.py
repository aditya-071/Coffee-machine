import tkinter as tk
from tkinter import ttk, messagebox
from solution import CoffeeMachine


class CoffeeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fancy Coffee Machine")
        self.geometry("760x520")
        self.resizable(False, False)
        self.configure(bg="#222")

        self.coffee_machine = CoffeeMachine()

        self._build_ui()
        self._draw_machine_art()
        self._animate_steam()

    def _build_ui(self):
        # Left panel: machine art
        self.canvas = tk.Canvas(self, width=480, height=480, bg="#111", highlightthickness=0)
        self.canvas.place(x=10, y=10)

        # Right panel: controls
        right = tk.Frame(self, width=240, height=480, bg="#1c1c1c")
        right.place(x=500, y=10)

        title = tk.Label(right, text="Order", font=("Segoe UI", 16, "bold"), bg="#1c1c1c", fg="#ffd07f")
        title.pack(pady=(12, 6))

        # Drink buttons
        btn_frame = tk.Frame(right, bg="#1c1c1c")
        btn_frame.pack(pady=6)

        for drink in ("espresso", "latte", "cappuccino"):
            cost = self.coffee_machine.MENU[drink]["cost"]
            b = ttk.Button(btn_frame, text=f"{drink.title()} — ${cost:.2f}", width=22,
                           command=lambda d=drink: self._on_order(d))
            b.pack(pady=6)

        # Report
        rep_btn = ttk.Button(right, text="Report", width=22, command=self._show_report)
        rep_btn.pack(pady=(14, 6))

        off_btn = ttk.Button(right, text="Turn Off", width=22, command=self._turn_off)
        off_btn.pack(pady=6)

        # Resource display
        self.resources_frame = tk.Frame(right, bg="#121212")
        self.resources_frame.pack(pady=(18, 6), fill="x", padx=10)

        lbl = tk.Label(self.resources_frame, text="Resources", bg="#121212", fg="#ffd07f", font=("Segoe UI", 11, "bold"))
        lbl.pack(anchor="w", padx=6, pady=(6, 2))

        self.water_var = tk.StringVar()
        self.milk_var = tk.StringVar()
        self.coffee_var = tk.StringVar()
        self.money_var = tk.StringVar()

        for name, var in (("Water", self.water_var), ("Milk", self.milk_var), ("Coffee", self.coffee_var), ("Money", self.money_var)):
            f = tk.Frame(self.resources_frame, bg="#121212")
            f.pack(fill="x", padx=6, pady=2)
            tk.Label(f, text=f"{name}:", bg="#121212", fg="#ddd").pack(side="left")
            tk.Label(f, textvariable=var, bg="#121212", fg="#9ae6b4").pack(side="right")

        self._update_resource_vars()

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status = tk.Label(self, textvariable=self.status_var, bg="#111", fg="#ccc")
        status.place(x=10, y=500, width=740, height=18)

    def _draw_machine_art(self):
        c = self.canvas
        c.delete("all")

        # Machine body
        c.create_rectangle(40, 30, 440, 420, fill="#2b2b2b", outline="#333", width=3)

        # Display area
        c.create_rectangle(60, 50, 420, 120, fill="#0f0f0f", outline="#444")
        c.create_text(240, 85, text="Fancy Brew 3000", fill="#ffd07f", font=("Segoe UI", 16, "bold"))

        # Cup area
        self.cup_base = c.create_oval(170, 240, 310, 360, fill="#ffffff", outline="#d9d9d9")
        self.cup_liquid = c.create_rectangle(180, 260, 300, 260, fill="#6b3f2d", outline="")

        # Buttons (fake) on machine
        for i, x in enumerate((100, 170, 240, 310)):
            c.create_oval(x, 150, x+28, 178, fill="#353535", outline="#222")

        # Coffee beans decorative
        for i in range(10):
            x = 70 + i * 34
            c.create_oval(x, 390, x+16, 404, fill="#6b4f2f", outline="#4a341f")

        # LED lights
        self.led = c.create_oval(380, 60, 398, 78, fill="#3b3b3b")

        # Steam group
        self.steam_items = []

    def _update_resource_vars(self):
        r = self.coffee_machine.resources
        self.water_var.set(f"{r.get('water',0)} ml")
        self.milk_var.set(f"{r.get('milk',0)} ml")
        self.coffee_var.set(f"{r.get('coffee',0)} g")
        self.money_var.set(f"${r.get('money',0.0):.2f}")

    def _on_order(self, drink):
        # Check resources
        if not self.coffee_machine.check_resources(drink):
            messagebox.showwarning("Insufficient", f"Sorry, not enough resources for {drink}.")
            return

        # Open coin dialog
        self._coin_dialog(drink)

    def _coin_dialog(self, drink):
        d = tk.Toplevel(self)
        d.title(f"Insert Coins — {drink.title()}")
        d.geometry("320x220")
        d.resizable(False, False)

        cost = self.coffee_machine.MENU[drink]["cost"]
        tk.Label(d, text=f"Cost: ${cost:.2f}", font=("Segoe UI", 12, "bold")).pack(pady=8)

        frame = tk.Frame(d)
        frame.pack(pady=6)

        entries = {}
        for i, (lbl, val) in enumerate((("Quarters (0.25)", 0.25), ("Dimes (0.10)", 0.10), ("Nickels (0.05)", 0.05), ("Pennies (0.01)", 0.01))):
            row = tk.Frame(frame)
            row.grid(row=i, column=0, pady=4)
            tk.Label(row, text=lbl, width=18, anchor="w").grid(row=0, column=0)
            ent = tk.Entry(row, width=6)
            ent.insert(0, "0")
            ent.grid(row=0, column=1, padx=6)
            entries[val] = ent

        def submit_coins():
            try:
                total = 0.0
                for val, ent in entries.items():
                    n = int(ent.get())
                    total += n * val
            except Exception:
                messagebox.showerror("Input error", "Please enter integer counts for coins.")
                return

            if total < cost:
                messagebox.showinfo("Not enough", f"Inserted ${total:.2f}. Money refunded.")
                d.destroy()
                return

            change = total - cost
            if change > 0:
                messagebox.showinfo("Change", f"Here is ${change:.2f} in change.")

            # Update machine resources and animate
            self.coffee_machine.resources['money'] += cost
            for ingr, amt in self.coffee_machine.MENU[drink]["ingredients"].items():
                self.coffee_machine.resources[ingr] -= amt

            self._update_resource_vars()
            self.status_var.set(f"Preparing your {drink}...")
            d.destroy()
            self._flash_led()
            self._fill_cup_animation(drink)

        submit = ttk.Button(d, text="Insert", command=submit_coins)
        submit.pack(pady=12)

    def _fill_cup_animation(self, drink):
        c = self.canvas
        # Cup top y positions
        top = 260
        bottom = 300
        fill_color = "#6b3f2d" if drink != 'latte' else '#b5734a'

        # animate increasing rectangle height
        steps = 18

        def step(i=0):
            if i > steps:
                self.status_var.set(f"Here is your {drink}. Enjoy!")
                self.after(1200, lambda: self.status_var.set("Ready"))
                return
            y = top + (bottom - top) * (1 - i / steps)
            c.coords(self.cup_liquid, 180, y, 300, 300)
            c.itemconfig(self.cup_liquid, fill=fill_color)
            self.after(60, lambda: step(i + 1))

        step()

    def _flash_led(self):
        c = self.canvas
        def flash(n=0):
            if n % 2 == 0:
                c.itemconfig(self.led, fill="#5effa1")
            else:
                c.itemconfig(self.led, fill="#3b3b3b")
            if n < 6:
                self.after(150, lambda: flash(n + 1))
        flash()

    def _animate_steam(self):
        c = self.canvas
        # create steam items and animate upward fade
        def new_puff():
            x = 235
            y = 230
            r = 8
            item = c.create_oval(x - r, y - r, x + r, y + r, fill="#ffffff", outline="", stipple="gray50")
            self.steam_items.append((item, 0))
            self.after(700, new_puff)

        def animate():
            for i, (item, age) in enumerate(list(self.steam_items)):
                if age > 28:
                    c.delete(item)
                    self.steam_items.remove((item, age))
                    continue
                c.move(item, 0, -1.6 - age * 0.02)
                alpha = max(0, 1 - age / 28)
                # simulate fade by adjusting fill color brightness
                col = f"#{int(255*alpha):02x}{int(255*alpha):02x}{int(255*alpha):02x}"
                try:
                    c.itemconfig(item, fill=col)
                except Exception:
                    pass
                # update age tuple
                idx = self.steam_items.index((item, age))
                self.steam_items[idx] = (item, age + 1)
            self.after(90, animate)

        new_puff()
        animate()

    def _show_report(self):
        r = self.coffee_machine.resources
        txt = f"Water: {r.get('water',0)}ml\nMilk: {r.get('milk',0)}ml\nCoffee: {r.get('coffee',0)}g\nMoney: ${r.get('money',0.0):.2f}"
        messagebox.showinfo("Report", txt)

    def _turn_off(self):
        if messagebox.askyesno("Confirm", "Turn off the coffee machine?"):
            self.destroy()


if __name__ == '__main__':
    app = CoffeeGUI()
    app.mainloop()
