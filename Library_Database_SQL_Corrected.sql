CREATE TABLE Students (
    StudentID COUNTER PRIMARY KEY,
    FirstName TEXT(50) NOT NULL,
    LastName TEXT(50) NOT NULL,
    Grade TEXT(2) NOT NULL,
    Email TEXT(100),
    PhoneNumber TEXT(15),
    DateOfBirth DATE,
    RegistrationDate DATE DEFAULT Date(),
    IsActive YESNO DEFAULT Yes
);

CREATE TABLE Books (
    BookID COUNTER PRIMARY KEY,
    ISBN TEXT(13) UNIQUE,
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

CREATE TABLE Categories (
    CategoryID COUNTER PRIMARY KEY,
    CategoryName TEXT(50) NOT NULL UNIQUE,
    Description TEXT(200)
);

CREATE TABLE Borrowings (
    BorrowingID COUNTER PRIMARY KEY,
    StudentID NUMBER NOT NULL,
    BookID NUMBER NOT NULL,
    BorrowDate DATE DEFAULT Date() NOT NULL,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    FineAmount CURRENCY DEFAULT 0,
    Status TEXT(20) DEFAULT 'Borrowed'
);

CREATE TABLE BookCategories (
    BookID NUMBER NOT NULL,
    CategoryID NUMBER NOT NULL
);

INSERT INTO Students (FirstName, LastName, Grade, Email, PhoneNumber, DateOfBirth) VALUES
('John', 'Smith', '11', 'john.smith@school.com', '0821234567', #2006-03-15#),
('Sarah', 'Johnson', '11', 'sarah.johnson@school.com', '0822345678', #2006-07-22#),
('Michael', 'Brown', '11', 'michael.brown@school.com', '0823456789', #2006-01-10#),
('Emily', 'Davis', '11', 'emily.davis@school.com', '0824567890', #2006-11-05#),
('David', 'Wilson', '11', 'david.wilson@school.com', '0825678901', #2006-05-18#),
('Lisa', 'Anderson', '11', 'lisa.anderson@school.com', '0826789012', #2006-09-30#),
('James', 'Taylor', '11', 'james.taylor@school.com', '0827890123', #2006-12-12#),
('Amanda', 'Martinez', '11', 'amanda.martinez@school.com', '0828901234', #2006-04-25#);

INSERT INTO Categories (CategoryName, Description) VALUES
('Fiction', 'Imaginative literature and novels'),
('Non-Fiction', 'Factual and educational books'),
('Science', 'Scientific and technical books'),
('History', 'Historical books and references'),
('Mathematics', 'Math textbooks and references'),
('Literature', 'Classic and modern literature'),
('Technology', 'Computer and technology books'),
('Biography', 'Biographical books and memoirs');

INSERT INTO Books (ISBN, Title, Author, Publisher, PublicationYear, Genre, Price, CopiesAvailable) VALUES
('9780140283334', 'To Kill a Mockingbird', 'Harper Lee', 'Penguin Books', 1960, 'Fiction', 150.00, 3),
('9780061120084', '1984', 'George Orwell', 'HarperCollins', 1949, 'Fiction', 120.00, 2),
('9780743273565', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', 1925, 'Fiction', 110.00, 4),
('9780618640157', 'The Lord of the Rings', 'J.R.R. Tolkien', 'Houghton Mifflin', 1954, 'Fiction', 200.00, 2),
('9780141439518', 'Pride and Prejudice', 'Jane Austen', 'Penguin Books', 1813, 'Fiction', 95.00, 3),
('9780743273566', 'A Brief History of Time', 'Stephen Hawking', 'Bantam Books', 1988, 'Science', 180.00, 2),
('9780393609394', 'The Selfish Gene', 'Richard Dawkins', 'W.W. Norton', 1976, 'Science', 160.00, 1),
('9780143111801', 'Sapiens', 'Yuval Noah Harari', 'Harper', 2011, 'Non-Fiction', 190.00, 3),
('9780062301239', 'The Power of Habit', 'Charles Duhigg', 'Random House', 2012, 'Non-Fiction', 140.00, 2),
('9780143127550', 'Thinking, Fast and Slow', 'Daniel Kahneman', 'Farrar, Straus and Giroux', 2011, 'Non-Fiction', 170.00, 1);

INSERT INTO BookCategories (BookID, CategoryID) VALUES
(1, 1), (1, 6),
(2, 1), (2, 6),
(3, 1), (3, 6),
(4, 1),
(5, 1), (5, 6),
(6, 3), (6, 2),
(7, 3), (7, 2),
(8, 2),
(9, 2),
(10, 2);

INSERT INTO Borrowings (StudentID, BookID, BorrowDate, DueDate, Status) VALUES
(1, 1, Date()-30, Date()-15, 'Returned'),
(2, 3, Date()-25, Date()-10, 'Returned'),
(3, 5, Date()-20, Date()-5, 'Borrowed'),
(4, 2, Date()-18, Date()-3, 'Borrowed'),
(5, 6, Date()-15, Date(), 'Borrowed'),
(6, 8, Date()-12, Date()+3, 'Borrowed'),
(7, 4, Date()-10, Date()+5, 'Borrowed'),
(1, 7, Date()-8, Date()+7, 'Borrowed'),
(2, 9, Date()-5, Date()+10, 'Borrowed'),
(3, 10, Date()-3, Date()+12, 'Borrowed');

SELECT StudentID, FirstName, LastName, Grade, Email
FROM Students
WHERE IsActive = Yes
ORDER BY LastName, FirstName;

SELECT FirstName, LastName, Grade, RegistrationDate
FROM Students
WHERE Grade = '11' AND Year(RegistrationDate) = Year(Date())
ORDER BY RegistrationDate;

SELECT Title, Author, Genre
FROM Books
WHERE Genre = 'Fiction' OR Genre = 'Science'
ORDER BY Title;

SELECT Title, Author, Genre
FROM Books
WHERE NOT Genre = 'Fiction'
ORDER BY Genre, Title;

SELECT s.FirstName, s.LastName, b.Title, br.DueDate, Date() - br.DueDate AS DaysOverdue
FROM Students s
INNER JOIN Borrowings br ON s.StudentID = br.StudentID
INNER JOIN Books b ON br.BookID = b.BookID
WHERE s.Grade = '11' AND br.DueDate < Date() AND br.Status = 'Borrowed'
ORDER BY DaysOverdue DESC;

SELECT Genre, COUNT(*) AS NumberOfBooks, AVG(Price) AS AveragePrice
FROM Books
GROUP BY Genre
ORDER BY NumberOfBooks DESC;

SELECT b.Title, b.Author, c.CategoryName
FROM Books b
INNER JOIN BookCategories bc ON b.BookID = bc.BookID
INNER JOIN Categories c ON bc.CategoryID = c.CategoryID
ORDER BY b.Title, c.CategoryName;

SELECT s.FirstName, s.LastName, COUNT(br.BorrowingID) AS BooksBorrowed
FROM Students s
INNER JOIN Borrowings br ON s.StudentID = br.StudentID
GROUP BY s.StudentID, s.FirstName, s.LastName
HAVING COUNT(br.BorrowingID) > (
    SELECT AVG(BookCount)
    FROM (
        SELECT COUNT(*) AS BookCount
        FROM Borrowings
        GROUP BY StudentID
    ) AS AvgCount
)
ORDER BY BooksBorrowed DESC;

SELECT 
    s.StudentID,
    s.FirstName & ' ' & s.LastName AS FullName,
    s.Grade,
    COUNT(br.BorrowingID) AS TotalBorrowings,
    SUM(IIF(br.Status = 'Borrowed', 1, 0)) AS CurrentlyBorrowed,
    SUM(IIF(br.ReturnDate IS NULL AND br.DueDate < Date(), 1, 0)) AS OverdueBooks,
    SUM(br.FineAmount) AS TotalFines
FROM Students s
LEFT JOIN Borrowings br ON s.StudentID = br.StudentID
GROUP BY s.StudentID, s.FirstName, s.LastName, s.Grade
ORDER BY s.LastName, s.FirstName;

SELECT 
    b.Title,
    b.Author,
    b.Genre,
    b.Publisher,
    b.PublicationYear,
    b.Price,
    b.CopiesAvailable,
    b.CopiesAvailable * b.Price AS TotalValue
FROM Books b
ORDER BY b.Genre, b.Title;

SELECT 
    s.FirstName & ' ' & s.LastName AS StudentName,
    s.Grade,
    b.Title,
    br.BorrowDate,
    br.DueDate,
    Date() - br.DueDate AS DaysOverdue,
    (Date() - br.DueDate) * 5 AS FineAmount
FROM Students s
INNER JOIN Borrowings br ON s.StudentID = br.StudentID
INNER JOIN Books b ON br.BookID = b.BookID
WHERE br.Status = 'Borrowed' AND br.DueDate < Date()
ORDER BY DaysOverdue DESC;

SELECT FirstName, LastName, Email, PhoneNumber, Grade
FROM Students
WHERE IsActive = Yes
ORDER BY LastName, FirstName;

SELECT 
    s.FirstName,
    s.LastName,
    s.Email,
    b.Title,
    br.DueDate,
    Date() - br.DueDate AS DaysOverdue,
    (Date() - br.DueDate) * 5 AS FineAmount
FROM Students s
INNER JOIN Borrowings br ON s.StudentID = br.StudentID
INNER JOIN Books b ON br.BookID = b.BookID
WHERE br.Status = 'Borrowed' AND br.DueDate < Date();

SELECT ISBN, Title, Author, Publisher, PublicationYear, Genre, Price, CopiesAvailable
FROM Books
ORDER BY Genre, Title;

SELECT 
    b.Title,
    b.Author,
    COUNT(br.BorrowingID) AS TimesBorrowed,
    b.CopiesAvailable,
    IIF(b.CopiesAvailable > 0, COUNT(br.BorrowingID) / b.CopiesAvailable, 0) AS BorrowsPerCopy
FROM Books b
LEFT JOIN Borrowings br ON b.BookID = br.BookID
GROUP BY b.BookID, b.Title, b.Author, b.CopiesAvailable
ORDER BY TimesBorrowed DESC;

SELECT 
    s.FirstName & ' ' & s.LastName AS StudentName,
    s.Grade,
    SUM(IIF(br.DueDate < Date() AND br.Status = 'Borrowed', 1, 0)) AS OverdueBooks,
    SUM(IIF(br.DueDate < Date() AND br.Status = 'Borrowed', 
        (Date() - br.DueDate) * 5, 0)) AS TotalFinesOwed
FROM Students s
LEFT JOIN Borrowings br ON s.StudentID = br.StudentID
GROUP BY s.StudentID, s.FirstName, s.LastName, s.Grade
HAVING SUM(IIF(br.DueDate < Date() AND br.Status = 'Borrowed', 
    (Date() - br.DueDate) * 5, 0)) > 0
ORDER BY TotalFinesOwed DESC;

SELECT 
    s.FirstName & ' ' & s.LastName AS StudentName,
    s.Grade,
    COUNT(DISTINCT b.Genre) AS GenresRead
FROM Students s
INNER JOIN Borrowings br ON s.StudentID = br.StudentID
INNER JOIN Books b ON br.BookID = b.BookID
GROUP BY s.StudentID, s.FirstName, s.LastName, s.Grade
HAVING COUNT(DISTINCT b.Genre) > 1
ORDER BY GenresRead DESC, StudentName;

SELECT 
    'Student: ' & s.FirstName & ' ' & s.LastName AS StudentInfo,
    'Grade: ' & s.Grade AS GradeInfo,
    'Email: ' & s.Email AS ContactInfo,
    'Books Borrowed: ' & COUNT(br.BorrowingID) AS BorrowingInfo,
    'Overdue: ' & SUM(IIF(br.DueDate < Date() AND br.Status = 'Borrowed', 1, 0)) AS OverdueInfo
FROM Students s
LEFT JOIN Borrowings br ON s.StudentID = br.StudentID
GROUP BY s.StudentID, s.FirstName, s.LastName, s.Grade, s.Email
ORDER BY s.LastName, s.FirstName;
