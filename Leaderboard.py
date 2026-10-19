import csv
import os

FILENAME = "leaderboard.csv"

class Leaderboard:
    def __init__(self, filename):
        self.filename = filename
        self.creating_csv()

    def load_scores(self):
        scores_list = []
        with open(self.filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row:
                    scores_list.append([row[0], float(row[1])])
        scores_list.sort(key=lambda item: item[1], reverse=True)
        return scores_list
        
    
    def creating_csv(self):
        if not os.path.exists(self.filename):
            with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Gamer", "Score"])


    def writing_score(self, new_name=None):
        found = False
        scores_list = []
        if new_name is None:
            new_name = input("Enter Name: ")

        with open(self.filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row:
                    if row[0].strip().lower() == new_name.strip().lower():
                        print(f"The gamer '{new_name}' already exists. Maybe you want to update their score instead?")
                        found = True
                        while True:
                            add_choice = (
                            input(
                                f"Do you want to update the score for '{new_name}'? (yes/no): "
                            )
                            .strip()
                            .lower()
                        )
                            if add_choice == "yes":
                                self.update_score(new_name)
                                return
                            elif add_choice == "no":
                                print("No changes made.")
                                return
                            else:
                                print("Invalid input. Please enter 'yes' or 'no'.")

        if not found:
            while True:
                try:
                    new_score = float(input("Enter Score: "))
                    if new_score < 0:
                        print("Score cannot be negative. Please try again.")
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter a valid score.")

            with open(self.filename, "r") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
                    if row:
                        scores_list.append([row[0], float(row[1])])

            scores_list.append([new_name, new_score])

        def get_score(item):
            return item[1]

        scores_list.sort(key=get_score, reverse=True)

        with open(self.filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Gamer", "Score"])
            for row in scores_list:
                writer.writerow(row)

        print(f"New gamer was added. Name: {new_name}; Score: {new_score}")


    def reading_score(self):
        scores_list = self.load_scores()

        for row in scores_list:
            print(f"Name: {row[0]}; Score: {row[1]}")


    def gamer_search(self):
        search_name = input("Enter the name of the gamer to search their score: ")
        found = False
        with open(self.filename, "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row:
                    if row[0].strip().lower() == search_name.strip().lower():
                        print(f"Match Found! Name: {row[0]}; Score: {row[1]}")
                        found = True
                        while True:
                            add_choice = (
                                input(
                                f"Do you want to update the score for '{search_name}'? (yes/no): "
                            )
                            .strip()
                            .lower()
                        )
                            if add_choice == "yes":
                                self.update_score(search_name)
                                return
                            elif add_choice == "no":
                                print("No changes made.")
                                return
                            else:
                                print("Invalid input. Please enter 'yes' or 'no'.")

        if not found:
            while True:
                add_choice = (
                    input(
                    f"Gamer '{search_name}' not found. Do you want to add this gamer? (yes/no): "
                )
                .strip()
                .lower()
            )
                if add_choice == "yes":
                    self.writing_score(search_name)
                    return
                elif add_choice == "no":
                    print("No changes made.")
                    return
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")


    def update_score(self, search_name=None):
        if search_name is None:
            search_name = input("Enter the name of the gamer to update their score: ")
        scores_list = self.load_scores()
        found = False
        for row in scores_list:
            if row[0].strip().lower() == search_name.strip().lower():
                while True:
                    try:
                        new_score = float(
                            input(f"Enter new score for {row[0]}: ")
                    )
                        if new_score < 0:
                            print(
                            "Score cannot be negative. Please try again."
                        )
                        else:
                            break
                    except ValueError:
                        print("Invalid input. Please enter a valid score.")
                row[1] = new_score
                found = True
                break

        if found:
            scores_list.sort(key=lambda item: item[1], reverse=True)

            with open(self.filename, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Gamer", "Score"])
                writer.writerows(scores_list)
            print(f"Score updated for gamer '{search_name}'.")
        else:
            while True:
                add_choice = (
                input(
                    f"Gamer '{search_name}' not found. Do you want to add this gamer? (yes/no): "
                )
                .strip()
                .lower()
            )
                if add_choice == "yes":
                    self.writing_score(search_name)
                    return
                elif add_choice == "no":
                    print("No changes made.")
                    return
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")


    def menu(self):
        while True:
            print("1. Add Gamer with their score")
            print("2. View Gamers in sorted order from highest score to lowest")
            print("3. Search Gamer")
            print("4. Update Gamer Score")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.writing_score()
            elif choice == "2":
                self.reading_score()
            elif choice == "3":
                self.gamer_search()
            elif choice == "4":
                self.update_score()
            elif choice == "5":
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    lb = Leaderboard(FILENAME)
    lb.menu()