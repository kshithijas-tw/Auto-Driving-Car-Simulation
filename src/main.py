from cli.run import read_field, read_car, print_cars, run_simulation
from direct.showbase.ShowBase import ShowBase

def main():
    field = read_field()
    print(f"\nYou have created a field of {field.width} x {field.height}.\n")

    cars = []

    while True:
        print("Please choose from the following options:")
        print("[1] Add a car to field")
        print("[2] Run simulation")

        choice = input().strip()

        if choice == "1":
            try:
                car = read_car({c.name for c in cars})
                cars.append(car)
                print_cars(cars)
            except ValueError as e:
                print(f"Error: {e}\n")

        elif choice == "2":
            run_simulation(field, cars)
            print("Please choose from the following options:")
            print("[1] Start over")
            print("[2] Exit")

            end_choice = input().strip()
            if end_choice == "1":
                main()
                return
            else:
                print("Thank you for running the simulation. Goodbye!")
                return

        else:
            print("Invalid choice.\n")

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)



if __name__ == "__main__":
    app = MyApp()
    app.run()
