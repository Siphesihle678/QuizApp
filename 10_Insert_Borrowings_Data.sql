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
