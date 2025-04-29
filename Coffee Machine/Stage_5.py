water = 400
milk = 540
beans = 120
cups = 9
money = 550


def buy():
    global water, milk, beans, cups, money
    print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:")
    coffee_option = input()

    if coffee_option == "1":
        if water >= 250 and beans >= 16 and cups >= 1:
            print("I have enough resources, making you a coffee!")
            water -= 250
            beans -= 16
            cups -= 1
            money += 4
        else:
            if water < 250:
                print("Sorry, not enough water!")
            elif beans < 16:
                print("Sorry, not enough beans!")
            elif cups < 1:
                print("Sorry, not enough cups!")
    elif coffee_option == "2":
        if water >= 350 and milk >= 75 and beans >= 20 and cups >= 1:
            print("I have enough resources, making you a coffee!")
            water -= 350
            milk -= 75
            beans -= 20
            cups -= 1
            money += 7
        else:
            if water < 350:
                print("Sorry, not enough water!")
            elif milk < 75:
                print("Sorry, not enough milk!")
            elif beans < 20:
                print("Sorry, not enough beans!")
            elif cups < 1:
                print("Sorry, not enough cups!")
    elif coffee_option == "3":
        if water >= 200 and milk >= 100 and beans >= 12 and cups >= 1:
            print("I have enough resources, making you a coffee!")
            water -= 200
            milk -= 100
            beans -= 12
            cups -= 1
            money += 6
        else:
            if water < 200:
                print("Sorry, not enough water!")
            elif milk < 100:
                print("Sorry, not enough milk!")
            elif beans < 12:
                print("Sorry, not enough beans!")
            elif cups < 1:
                print("Sorry, not enough cups!")
    elif coffee_option == "back":
        pass
    else:
        print("Invalid input")


def fill():
    global water, milk, beans, cups
    print("Write how many ml of water you want to add:")
    water += int(input())
    print("Write how many ml of milk you want to add:")
    milk += int(input())
    print("Write how many grams of coffee beans you want to add:")
    beans += int(input())
    print("Write how many disposable cups you want to add:")
    cups += int(input())


def take():
    global money
    print(f"I gave you ${money}")
    money = 0


def main_display():
    print("The coffee machine has:")
    print(f"{water} ml of water")
    print(f"{milk} ml of milk")
    print(f"{beans} g of coffee beans")
    print(f"{cups} disposable cups")
    print(f"${money} of money")


while True:
    print("Write action (buy, fill, take, remaining, exit):")
    action = input()
    if action == "buy":
        buy()
    elif action == "fill":
        fill()
    elif action == "take":
        take()
    elif action == "remaining":
        main_display()
    elif action == "exit":
        break
    else:
        print("Invalid action")
