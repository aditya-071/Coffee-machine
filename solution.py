class CoffeeMachine:
    """A coffee machine that can make different types of coffee."""
    
    # Coffee recipes with ingredients and cost
    MENU = {
        "espresso": {
            "ingredients": {
                "water": 50,
                "coffee": 18,
            },
            "cost": 1.5
        },
        "latte": {
            "ingredients": {
                "water": 200,
                "milk": 150,
                "coffee": 24,
            },
            "cost": 2.5
        },
        "cappuccino": {
            "ingredients": {
                "water": 250,
                "milk": 100,
                "coffee": 24,
            },
            "cost": 3.0
        }
    }
    
    def __init__(self):
        """Initialize the coffee machine with resources."""
        self.resources = {
            "water": 300,
            "milk": 200,
            "coffee": 100,
            "money": 0.0
        }
    
    def check_resources(self, drink):
        """Check if there are enough resources to make the drink."""
        ingredients_needed = self.MENU[drink]["ingredients"]
        
        for ingredient, amount in ingredients_needed.items():
            if self.resources[ingredient] < amount:
                print(f"Sorry, there is not enough {ingredient}.")
                return False
        return True
    
    def process_coins(self):
        """Process coin input from user."""
        print("Please insert coins.")
        total = 0
        
        quarters = int(input("How many quarters?: "))
        dimes = int(input("How many dimes?: "))
        nickels = int(input("How many nickels?: "))
        pennies = 4
        
        total = (quarters * 0.25) + (dimes * 0.10) + (nickels * 0.05) + (pennies * 0.01)
        return total
    
    def is_transaction_successful(self, money_received, drink_cost):
        """Check if the transaction was successful."""
        if money_received < drink_cost:
            print(f"Sorry, that's not enough money. Money refunded.")
            return False
        else:
            change = money_received - drink_cost
            if change > 0:
                print(f"Here is ${change:.2f} dollars in change.")
            self.resources["money"] += drink_cost
            return True
    
    def make_coffee(self, drink):
        """Make the requested coffee drink."""
        if not self.check_resources(drink):
            return
        
        money_received = self.process_coins()
        
        if not self.is_transaction_successful(money_received, self.MENU[drink]["cost"]):
            return
        
        # Deduct ingredients
        ingredients_needed = self.MENU[drink]["ingredients"]
        for ingredient, amount in ingredients_needed.items():
            self.resources[ingredient] -= amount
        
        print(f"Here is your {drink}. Enjoy!")
    
    def report(self):
        """Print a report of all resources."""
        print("\n--- Coffee Machine Resources ---")
        print(f"Water: {self.resources['water']}ml")
        print(f"Milk: {self.resources['milk']}ml")
        print(f"Coffee: {self.resources['coffee']}g")
        print(f"Money: ${self.resources['money']:.2f}")
        print("--------------------------------\n")
