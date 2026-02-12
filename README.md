
# Fancy Coffee Machine ☕

A sophisticated Python-based coffee machine simulator that combines strict resource management with a modern, animated Graphical User Interface.

## 🚀 Features

- **Animated GUI (Fancy Brew 3000):** - Real-time steam animations and cup-filling visuals.
  - Dynamic status bar and LED indicator.
  - Live resource tracking (Water, Milk, Coffee, and Profit).
- **Core Logic:**
  - **Resource Validation:** Checks if enough ingredients exist before starting an order.
  - **Coin Processing:** Handles Quarters, Dimes, Nickels, and Pennies.
  - **Transaction Management:** Calculates change and manages machine profit.
- **Maintenance Mode:** Generate reports to check current resource levels or safely turn off the machine.

## 📸 Interface Preview

![Fancy Coffee Machine GUI](coffeemachineUI.png)

## 🛠️ Project Structure

- `solution.py`: The core logic engine containing the `CoffeeMachine` class.
- `Display.py`: The Tkinter-based GUI implementation with custom animations.
- `main.py`: The terminal-based entry point for classic console play.
- `Coffee+Machine+Program+Requirements.pdf`: The official logic and business requirements for the build.

## 📥 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/fancy-coffee-machine.git](https://github.com/YOUR_USERNAME/fancy-coffee-machine.git)
   cd fancy-coffee-machine

🎮 How it Works
Select a Drink: Choose between Espresso, Latte, or Cappuccino.

Insert Coins: A dialog will appear for you to input the number of coins.

Enjoy: Watch the "Fancy Brew 3000" animate your drink preparation!

Maintenance: Use the Report button to see remaining ingredients or Turn Off to end the session.

📜 Requirements
Python 3.x

Tkinter (standard with most Python installations)


