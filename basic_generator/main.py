# main.py
import person
from gedcom_export import export_to_gedcom
from print_basic_family_info import print_basic_family_info

def main():
    print("Welcome to the CK3 Family Generator")
    start_date = int(input("Enter the simulation start year (e.g., 1200): "))
    end_date   = int(input("Enter the simulation end year (e.g., 1450): "))
    first_name = input("Enter the first name of the patriarch: ")
    last_name  = input("Enter the surname of the patriarch (or leave blank to use first name): ")
    name = first_name + (f"_{last_name}" if last_name else "")

    while True:
        # Generate a new tree
        patriarch = person.MalePerson(
            parent_name=first_name,
            birth_position=1,
            birth_year=start_date,
            END_YEAR=end_date
        )

        print(f"\nGenerated family tree for patriarch: {patriarch.name}")
        print_basic_family_info(patriarch)

        choice = input("\nDo you wish to save or regenerate? (y = save, n = regenerate): ").strip().lower()
        if choice == 'y':
            filepath = f"test_family_ged_exports/{name}_tree.ged"
            export_to_gedcom(patriarch, filepath, root_surname=last_name, end_year=end_date)
            print(f"\nGEDCOM written to: {filepath}")
            break
        elif choice == 'n':
            print("\nRegenerating...\n")
            continue
        else:
            print("Invalid input. Please type 'y' or 'n'.\n")

if __name__ == "__main__":
    main()
