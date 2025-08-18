CREATE TABLE Borrowings (
    BorrowingID COUNTER,
    StudentID NUMBER,
    BookID NUMBER,
    BorrowDate DATE,
    DueDate DATE,
    ReturnDate DATE,
    FineAmount CURRENCY,
    Status TEXT(20)
);
