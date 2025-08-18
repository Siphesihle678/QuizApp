# Microsoft Access - Correct Table Creation Method

## 🎯 **The Right Way to Create Tables in Microsoft Access**

### **Step 1: Create a New Database**
1. Open Microsoft Access
2. Click "Blank database"
3. Choose a location and name it "LibraryDatabase"
4. Click "Create"

### **Step 2: Create Tables Using Data Definition Query**

**⚠️ IMPORTANT: Use "Data Definition" query type, NOT "Make Table"!**

1. **Open Query Design**
   - Click "Create" tab
   - Click "Query Design"
   - Click "Close" when prompted to add tables

2. **Change to Data Definition Query**
   - In the ribbon, click "Query Type" group
   - Click "Data Definition" (this is crucial!)
   - The query window will change to show SQL view

3. **Now Copy and Paste Each SQL File**

   **File 1:** `01_Create_Students_Table.sql`
   ```sql
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
   ```
   - Copy and paste the above code
   - Click "Run" (red exclamation mark)
   - Click "Yes" to confirm

   **File 2:** `02_Create_Books_Table.sql`
   ```sql
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
   ```
   - Copy and paste the above code
   - Click "Run"
   - Click "Yes" to confirm

   **File 3:** `03_Create_Categories_Table.sql`
   ```sql
   CREATE TABLE Categories (
       CategoryID COUNTER,
       CategoryName TEXT(50) NOT NULL,
       Description TEXT(200)
   );
   ```
   - Copy and paste the above code
   - Click "Run"
   - Click "Yes" to confirm

   **File 4:** `04_Create_Borrowings_Table.sql`
   ```sql
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
   ```
   - Copy and paste the above code
   - Click "Run"
   - Click "Yes" to confirm

   **File 5:** `05_Create_BookCategories_Table.sql`
   ```sql
   CREATE TABLE BookCategories (
       BookID NUMBER NOT NULL,
       CategoryID NUMBER NOT NULL
   );
   ```
   - Copy and paste the above code
   - Click "Run"
   - Click "Yes" to confirm

### **Step 3: Set Up Primary Keys**

After creating all tables, set up primary keys manually:

1. **Go to "All Access Objects" → "Tables"**
2. **For each table, right-click → "Design View"**

   **Students table:**
   - Click on "StudentID" field
   - In "Field Properties" at bottom, set:
     - "Indexed" = "Yes (No Duplicates)"
     - "Required" = "Yes"
   - Save the table

   **Books table:**
   - Set "BookID" as primary key (Indexed = "Yes (No Duplicates)")
   - Set "ISBN" as unique (Indexed = "Yes (No Duplicates)")
   - Save the table

   **Categories table:**
   - Set "CategoryID" as primary key (Indexed = "Yes (No Duplicates)")
   - Set "CategoryName" as unique (Indexed = "Yes (No Duplicates)")
   - Save the table

   **Borrowings table:**
   - Set "BorrowingID" as primary key (Indexed = "Yes (No Duplicates)")
   - Save the table

   **BookCategories table:**
   - Select both "BookID" and "CategoryID" fields
   - Right-click → "Primary Key"
   - Save the table

### **Step 4: Insert Data Using Select Queries**

Now switch back to regular Select queries for inserting data:

1. **Open Query Design**
2. **Click "Query Type" → "Select"** (or just leave as default)
3. **Click "SQL View"**

   **Insert Students:**
   ```sql
   INSERT INTO Students (FirstName, LastName, Grade, Email, PhoneNumber, DateOfBirth) VALUES
   ('John', 'Smith', '11', 'john.smith@school.com', '0821234567', #2006-03-15#),
   ('Sarah', 'Johnson', '11', 'sarah.johnson@school.com', '0822345678', #2006-07-22#),
   ('Michael', 'Brown', '11', 'michael.brown@school.com', '0823456789', #2006-01-10#),
   ('Emily', 'Davis', '11', 'emily.davis@school.com', '0824567890', #2006-11-05#),
   ('David', 'Wilson', '11', 'david.wilson@school.com', '0825678901', #2006-05-18#),
   ('Lisa', 'Anderson', '11', 'lisa.anderson@school.com', '0826789012', #2006-09-30#),
   ('James', 'Taylor', '11', 'james.taylor@school.com', '0827890123', #2006-12-12#),
   ('Amanda', 'Martinez', '11', 'amanda.martinez@school.com', '0828901234', #2006-04-25#);
   ```

   **Insert Categories:**
   ```sql
   INSERT INTO Categories (CategoryName, Description) VALUES
   ('Fiction', 'Imaginative literature and novels'),
   ('Non-Fiction', 'Factual and educational books'),
   ('Science', 'Scientific and technical books'),
   ('History', 'Historical books and references'),
   ('Mathematics', 'Math textbooks and references'),
   ('Literature', 'Classic and modern literature'),
   ('Technology', 'Computer and technology books'),
   ('Biography', 'Biographical books and memoirs');
   ```

   **Insert Books:**
   ```sql
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
   ```

   **Insert BookCategories:**
   ```sql
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
   ```

   **Insert Borrowings:**
   ```sql
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
   ```

## ⚠️ **Key Differences:**

- **"Make Table"** = Creates table from existing data (SELECT...INTO)
- **"Data Definition"** = Creates table structure from scratch (CREATE TABLE)
- **"Select"** = For INSERT, UPDATE, DELETE operations

## 🎯 **The Correct Sequence:**

1. **Data Definition** → Create tables
2. **Design View** → Set primary keys
3. **Select Query** → Insert data
4. **Select Query** → Run queries

This should work perfectly now! 🎉
