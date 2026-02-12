from solution import CoffeeMachine

# Create coffee machine instance
coffee_machine = CoffeeMachine()

# Run the coffee machine
while True:
    user_input = input("What would you like? (espresso/latte/cappuccino/off): ").lower()
    
    if user_input == "off":
        print("Turning off the coffee machine...")
        break
    elif user_input == "report":
        coffee_machine.report()
    elif user_input in ["espresso", "latte", "cappuccino"]:
        coffee_machine.make_coffee(user_input)
    else:
        print("Invalid choice. Please try again.")
