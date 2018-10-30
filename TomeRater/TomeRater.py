#!/usr/bin/env python
#title           :TomeRater.py
#description     :Allows users to read and rate books.
#author          :Brad Stubbe(bstubbe4@gmail.com)
#date            :2018-10-29
#version         :0.1
#usage           :python3.7 -i populate.py
#notes           :requires populate.py
#python_version  :3.7.0
#==============================================================================


class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def __repr__(self):
        return "User: {} " \
               "Email: {} " \
               "Books read: {} " \
               .format(self.name, self.email, len(self.books))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email

    def get_email(self):
        return self.email


    def change_email(self, new_email):
        self.email = new_email
        return "Email updated to {}".format(new_email)

    def read_book(self, book, rating=None):
        self.books[book] = rating


    def get_average_rating(self):
        return sum([rating for rating in self.books.values() if rating != None]) / len(self.books)



class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        return "ISBN updated to {}".format(new_isbn)

    def add_rating(self, rating):
        if rating is not None:
            if rating >= 0 and rating <= 4:
                return self.ratings.append(rating)
            else:
                print("Invalid rating!")
        else:
            pass

    def get_average_rating(self):
        return sum([rating for rating in self.ratings]) / len(self.ratings)


    def __hash__(self):
        return hash((self.title, self.isbn))

    def __repr__(self):
        return "Title: {title} \n" \
               "ISBN: {isbn} \n" \
               .format(title=self.title, isbn=self.isbn)

class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)


class TomeRater(object):
    def __init__(self):
        self.users = {}
        self.books = {}

    def __repr__(self):
        user_list = []
        book_list = []
        for user in self.users:
            user_list.append(user)
        for book in self.books:
            book_list.append(book)
        return "Users: \n*********\n{} \n\nBooks: \n*********\n{} "\
        .format(str(user_list)\
        .strip('[]')\
        .replace("'", '')\
        .replace(',', '')\
        .replace(' ', '\n'), str(book_list)\
        .strip('[]')\
        .replace(', ', '\n'))



    def create_book(self, title, isbn):
        return Book(title, isbn)


    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)


    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)

    def add_book_to_user(self, book, email, rating=None):
        user = self.users.get(email, "No user with email {email}".format(email=email))

        if user:
            user.read_book(book, rating)
            self.books[book] = self.books.get(book, 0) + 1
            if rating is not None:
                book.add_rating(rating)

    def add_user(self, name, email, user_books=None):
        if email not in self.users:
            self.users[email] = User(name, email)
            if user_books is not None:
                for book in user_books:
                    self.add_book_to_user(book, email)
        else:
            print("Unable to add user")
            print("The email {} is already in use".format(email))

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        max_book = None
        max_val = None

        for book, val in self.books.items():

            if max_val is None or val > max_val:
                max_val = val
                max_book = book


        return "Most read book: {} Read count: {}".format(max_book, max_val)


    def highest_rated_book(self):
        all_avg_ratings = {}
        max_book = None
        max_rating = None

        for book in self.books.keys():
            avg_rating = book.get_average_rating()
            all_avg_ratings.update({book:avg_rating})

        for book, avg_rating in all_avg_ratings.items():
            if max_rating is None or avg_rating > max_rating:
                max_rating = avg_rating
                max_book = book

        return "Highest rated book: {} Rating: {}" \
               .format(str(max_book), str(max_rating))

    def most_positive_user(self):
        top_rated = max(rating.get_average_rating() for rating in self.users.values())
        return str([user for user in self.users.values() if user.get_average_rating() == top_rated]).strip('[]')

    def __eq__(self, other):
        return self.users == other.users and self.books == other.books
