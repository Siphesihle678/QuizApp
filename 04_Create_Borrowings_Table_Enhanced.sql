CREATE TABLE Borrowings (
    BorrowingID COUNTER,
    StudentID NUMBER NOT NULL,
    BookID NUMBER NOT NULL,
    BorrowDate DATE NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    FineAmount CURRENCY,
    Status TEXT(20)
);
