CREATE TABLE Books (
    BookID COUNTER,
    ISBN TEXT(13),
    Title TEXT(200) NOT NULL,
    Author TEXT(100) NOT NULL,
    Publisher TEXT(100),
    PublicationYear NUMBER,
    Genre TEXT(50),
    Price CURRENCY,
    CopiesAvailable NUMBER,
    DateAdded DATE,
    IsAvailable YESNO
);
