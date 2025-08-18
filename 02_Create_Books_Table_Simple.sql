CREATE TABLE Books (
    BookID COUNTER,
    ISBN TEXT(13),
    Title TEXT(200),
    Author TEXT(100),
    Publisher TEXT(100),
    PublicationYear NUMBER,
    Genre TEXT(50),
    Price CURRENCY,
    CopiesAvailable NUMBER,
    DateAdded DATE,
    IsAvailable YESNO
);
