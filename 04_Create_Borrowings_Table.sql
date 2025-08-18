CREATE TABLE Borrowings (
    BorrowingID COUNTER,
    StudentID NUMBER NOT NULL,
    BookID NUMBER NOT NULL,
    BorrowDate DATE DEFAULT Date() NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    FineAmount CURRENCY DEFAULT 0,
    Status TEXT(20) DEFAULT 'Borrowed'
);
