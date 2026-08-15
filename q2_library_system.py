def add_book(catalog, book_id, title, author, year):
    catalog[book_id] = (title, author, year)

def borrow_book(catalog, borrowed_books, book_id):
    if book_id in catalog:
        if book_id not in borrowed_books:
            borrowed_books.append(book_id)
            print(f"Book {book_id} borrowed successfully.")
        else:
            print(f"Book {book_id} is already borrowed.")
    else:
        print(f"Book {book_id} does not exist in the catalog.")


def return_book(borrowed_books, book_id):
    if book_id in borrowed_books:
        borrowed_books.remove(book_id)
        print(f"Book {book_id} returned successfully.")
    else:
        print(f"Book {book_id} is not currently borrowed.")


def register_member(members, member_id):
    # Set automatically ignores duplicate values
    members.add(member_id)


def show_available(catalog, borrowed_books):
    print("\nAvailable Books:")

    for book_id, details in catalog.items():
        if book_id not in borrowed_books:
            title, author, year = details
            print(f"ID: {book_id}, Title: {title}, Author: {author}, Year: {year}")


def main():
    catalog = {}
    borrowed_books = []
    members = set()

    add_book(catalog, 101, "Python Basics", "John Smith", 2022)
    add_book(catalog, 102, "Data Structures", "Robert Brown", 2021)
    add_book(catalog, 103, "Cyber Security", "Alice Johnson", 2023)
    add_book(catalog, 104, "Machine Learning", "David Wilson", 2024)

    register_member(members, 1001)
    register_member(members, 1002)
    register_member(members, 1003)

    register_member(members, 1002)

    print("Members:", members)

    borrow_book(catalog, borrowed_books, 101)
    borrow_book(catalog, borrowed_books, 103)

    print("Borrowed Books:", borrowed_books)

    return_book(borrowed_books, 101)

    print("Borrowed Books after return:", borrowed_books)

    show_available(catalog, borrowed_books)

if __name__ == "__main__":
    main()