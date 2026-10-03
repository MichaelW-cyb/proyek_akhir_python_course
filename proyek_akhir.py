library_items = []


class LibraryItem:
    def __init__(self, item_id, title, category, publication_year, is_borrowed=False):
        self.item_id = item_id
        self.title = title
        self.category = category
        self.publication_year = publication_year
        self.is_borrowed = is_borrowed

    def calculate_late_fee(self, days_late):
        return 0


class Book(LibraryItem):
    def __init__(self, item_id, title, category, publication_year, author):
        super().__init__(item_id, title, category, publication_year)
        self.author = author

    def calculate_late_fee(self, days_late):
        fee = days_late * 2000

        if days_late > 7:
            fee += 10000

        return fee


class Magazine(LibraryItem):
    def __init__(self, item_id, title, category, publication_year, issue_number):
        super().__init__(item_id, title, category, publication_year)
        self.issue_number = issue_number

    def calculate_late_fee(self, days_late):
        fee = days_late * 3000

        if days_late > 5:
            fee += 15000

        return fee


def find_item(item_id):
    for item in library_items:
        if item.item_id == item_id:
            return item

    return None


def add_item():
    print("\n===== ADD LIBRARY ITEM =====")

    while True:
        item_type = input("Type (Book/Magazine): ").strip().lower()

        if item_type == "book" or item_type == "magazine":
            break

        print("Invalid type. Choose Book or Magazine.")

    while True:
        item_id = input("Item ID : ").strip()

        if item_id == "":
            print("Item ID cannot be empty.")
        elif find_item(item_id) is not None:
            print("Item ID already exists.")
        else:
            break

    title = input("Title : ")
    category = input("Category : ")

    while True:
        try:
            publication_year = int(input("Publication Year : "))

            if publication_year > 0:
                break

            print("Publication Year must be greater than 0.")
        except ValueError:
            print("Publication Year must be a number.")

    if item_type == "book":
        author = input("Author : ")
        item = Book(
            item_id,
            title,
            category,
            publication_year,
            author
        )
        library_items.append(item)
        print("Book successfully added.")

    else:
        while True:
            try:
                issue_number = int(input("Issue Number : "))

                if issue_number > 0:
                    break

                print("Issue Number must be greater than 0.")
            except ValueError:
                print("Issue Number must be a number.")

        item = Magazine(
            item_id,
            title,
            category,
            publication_year,
            issue_number
        )
        library_items.append(item)
        print("Magazine successfully added.")


def show_all_items():
    print("\n===== LIBRARY ITEMS =====")

    if len(library_items) == 0:
        print("No library items.")
        return

    number = 1

    for item in library_items:
        print(f"Item #{number}")
        print(f"ID : {item.item_id}")

        if isinstance(item, Book):
            print("Type : Book")
        else:
            print("Type : Magazine")

        print(f"Title : {item.title}")
        print(f"Category : {item.category}")
        print(f"Publication Year : {item.publication_year}")

        if isinstance(item, Book):
            print(f"Author : {item.author}")
        else:
            print(f"Issue Number : {item.issue_number}")

        if item.is_borrowed:
            print("Status : Borrowed")
        else:
            print("Status : Available")

        print("----------------------------------------")
        number += 1

    print(f"Total Items : {len(library_items)}")


def borrow_item():
    print("\n===== BORROW ITEM =====")
    item_id = input("Enter Item ID to borrow : ")

    item = find_item(item_id)

    if item is None:
        print("Item not found.")
        return

    if item.is_borrowed:
        print("Item is not available.")
    else:
        item.is_borrowed = True
        print(f"{item.title} successfully borrowed.")


def return_item():
    print("\n===== RETURN ITEM =====")
    item_id = input("Enter Item ID to return : ")

    item = find_item(item_id)

    if item is None:
        print("Item not found.")
        return

    if not item.is_borrowed:
        print("Item is not currently borrowed.")
        return

    while True:
        try:
            days_late = int(input("Days late : "))

            if days_late >= 0:
                break

            print("Days late cannot be negative.")
        except ValueError:
            print("Days late must be a number.")

    fee = item.calculate_late_fee(days_late)

    if isinstance(item, Book):
        item_type = "Book"
    else:
        item_type = "Magazine"

    print(f"Item Type : {item_type}")
    print(f"Days Late : {days_late}")
    print(f"Late Fee : Rp{fee:,}".replace(",", "."))

    item.is_borrowed = False
    print("Item successfully returned.")


def category_summary():
    summary = {}

    for item in library_items:
        if item.category not in summary:
            summary[item.category] = {
                "total_items": 0,
                "borrowed_items": 0
            }

        summary[item.category]["total_items"] += 1

        if item.is_borrowed:
            summary[item.category]["borrowed_items"] += 1

    print("\n===== CATEGORY SUMMARY =====")

    if len(summary) == 0:
        print("No library items.")
        return

    for category in summary:
        print(f"Category : {category}")
        print(f"Total Items : {summary[category]['total_items']}")
        print(f"Borrowed Items : {summary[category]['borrowed_items']}")
        print("----------------------------------------")


def library_summary():
    total_items = len(library_items)
    total_books = 0
    total_magazines = 0
    borrowed_items = 0

    newest_item = None
    oldest_item = None

    for item in library_items:
        if isinstance(item, Book):
            total_books += 1
        elif isinstance(item, Magazine):
            total_magazines += 1

        if item.is_borrowed:
            borrowed_items += 1

        if newest_item is None:
            newest_item = item
            oldest_item = item
        else:
            if item.publication_year > newest_item.publication_year:
                newest_item = item

            if item.publication_year < oldest_item.publication_year:
                oldest_item = item

    available_items = total_items - borrowed_items

    print("\n===== LIBRARY SUMMARY =====")
    print(f"Total Items : {total_items}")
    print(f"Total Books : {total_books}")
    print(f"Total Magazines : {total_magazines}")
    print(f"Borrowed Items : {borrowed_items}")
    print(f"Available Items : {available_items}")

    if newest_item is not None:
        print(f"Newest Item : {newest_item.title}")
        print(f"Oldest Item : {oldest_item.title}")

    category_summary()


def save_report():
    with open("library_report.txt", "w") as file:
        file.write("===== LIBRARY REPORT =====\n")

        for item in library_items:
            file.write(f"ID : {item.item_id}\n")
            file.write(f"Title : {item.title}\n")

            if isinstance(item, Book):
                file.write("Type : Book\n")
            else:
                file.write("Type : Magazine\n")

            file.write(f"Category : {item.category}\n")
            file.write(f"Publication Year : {item.publication_year}\n")

            if isinstance(item, Book):
                file.write(f"Author : {item.author}\n")
            else:
                file.write(f"Issue Number : {item.issue_number}\n")

            if item.is_borrowed:
                file.write("Status : Borrowed\n")
            else:
                file.write("Status : Available\n")

            file.write("----------------------------------------\n")

        total_items = len(library_items)
        total_books = 0
        total_magazines = 0
        borrowed_items = 0
        newest_item = None
        oldest_item = None

        for item in library_items:
            if isinstance(item, Book):
                total_books += 1
            else:
                total_magazines += 1

            if item.is_borrowed:
                borrowed_items += 1

            if newest_item is None:
                newest_item = item
                oldest_item = item
            else:
                if item.publication_year > newest_item.publication_year:
                    newest_item = item

                if item.publication_year < oldest_item.publication_year:
                    oldest_item = item

        file.write("========================================\n")
        file.write("LIBRARY SUMMARY\n")
        file.write("========================================\n")
        file.write(f"Total Items : {total_items}\n")
        file.write(f"Total Books : {total_books}\n")
        file.write(f"Total Magazines : {total_magazines}\n")
        file.write(f"Borrowed Items : {borrowed_items}\n")
        file.write(f"Available Items : {total_items - borrowed_items}\n")

        if newest_item is not None:
            file.write(f"Newest Item : {newest_item.title}\n")
            file.write(f"Oldest Item : {oldest_item.title}\n")

    print("Report successfully saved to library_report.txt.")


def read_report():
    print("\n===== LIBRARY REPORT =====")

    try:
        with open("library_report.txt", "r") as file:
            report = file.read()

        print(report)

    except FileNotFoundError:
        print("Report file not found.")


status = True

while status == True:
    print("\n===== LIBRARY BORROWING MANAGEMENT SYSTEM =====")
    print("1. Add Library Item")
    print("2. Show All Items")
    print("3. Find Item")
    print("4. Borrow Item")
    print("5. Return Item")
    print("6. Category Summary")
    print("7. Library Summary")
    print("8. Save Report")
    print("9. Read Report")
    print("10. Exit")

    choice = input("Choose menu: ")

    if choice == "1":
        add_item()

    elif choice == "2":
        show_all_items()

    elif choice == "3":
        item_id = input("Enter Item ID to find : ")
        item = find_item(item_id)

        if item is None:
            print("Item not found.")
        else:
            print(f"ID : {item.item_id}")
            print(f"Title : {item.title}")

            if isinstance(item, Book):
                print("Type : Book")
            else:
                print("Type : Magazine")

            print(f"Category : {item.category}")
            print(f"Publication Year : {item.publication_year}")

    elif choice == "4":
        borrow_item()

    elif choice == "5":
        return_item()

    elif choice == "6":
        category_summary()

    elif choice == "7":
        library_summary()

    elif choice == "8":
        save_report()

    elif choice == "9":
        read_report()

    elif choice == "10":
        status = False
        print("Program ended.")

    else:
        print("Invalid menu choice.")
