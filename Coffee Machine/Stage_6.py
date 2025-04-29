class CoffeeMachine:

    def __init__(self):
        self.supplies = {'water': 400, 'milk': 540, 'coffee beans': 120, 'disposable cups': 9, 'money': 550}

    def __repr__(self):
        return f"An object of the {self.__class__.__name__} class."

    def main(self):
        while True:
            action = input('Write action (buy, fill, take, remaining, exit):\n')
            if action == 'exit':
                break
            else:
                self.handle_action(action)

    def handle_action(self, action):
        if action == 'remaining':
            self.print_status()
        elif action == 'buy':
            self.buy_coffee()
        elif action == 'fill':
            self.fill_machine()
        elif action == 'take':
            self.take_money()

    def print_status(self):
        print('The coffee machine has:')
        for item, amount in self.supplies.items():
            print(f"${amount} of {item}" if item == 'money' else f"{amount} of {item}")

    def buy_coffee(self):
        coffee_choices = {
            '1': {'water': 250, 'coffee beans': 16, 'disposable cups': 1, 'money': -4},
            '2': {'water': 350, 'milk': 75, 'coffee beans': 20, 'disposable cups': 1, 'money': -7},
            '3': {'water': 200, 'milk': 100, 'coffee beans': 12, 'disposable cups': 1, 'money': -6},
        }
        user_choice = input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n')
        if user_choice == 'back':
            return
        else:
            for item, amount in coffee_choices[user_choice].items():
                if self.supplies[item] - amount < 0:
                    print(f'Sorry, not enough {item}!')
                    return

            print('I have enough resources, making you a coffee!')
            for item, amount in coffee_choices[user_choice].items():
                self.supplies[item] -= amount

    def fill_machine(self):
        self.supplies['water'] += int(input('Write how many ml of water do you want to add:\n'))
        self.supplies['milk'] += int(input('Write how many ml of milk do you want to add:\n'))
        self.supplies['coffee beans'] += int(input('Write how many grams of coffee beans do you want to add:\n'))
        self.supplies['disposable cups'] += int(input('Write how many disposable cups of coffee do you want to add:\n'))

    def take_money(self):
        print(f"I gave you ${self.supplies['money']}")
        self.supplies['money'] = 0


if __name__ == '__main__':
    CoffeeMachine().main()
