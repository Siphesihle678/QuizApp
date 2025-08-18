CREATE TABLE Students (
    StudentID COUNTER,
    FirstName TEXT(50) NOT NULL,
    LastName TEXT(50) NOT NULL,
    Grade TEXT(2) NOT NULL,
    Email TEXT(100),
    PhoneNumber TEXT(15),
    DateOfBirth DATE,
    RegistrationDate DATE DEFAULT Date(),
    IsActive YESNO DEFAULT Yes
);
