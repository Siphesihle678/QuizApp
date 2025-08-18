CREATE TABLE Books (
    BookID COUNTER,
    ISBN TEXT(13),
    Title TEXT(200) NOT NULL,
    Author TEXT(100) NOT NULL,
    Publisher TEXT(100),
    PublicationYear NUMBER,
    Genre TEXT(50),
    Price CURRENCY,
    CopiesAvailable NUMBER DEFAULT 1,
    DateAdded DATE DEFAULT Date(),
    IsAvailable YESNO DEFAULT Yes
);
