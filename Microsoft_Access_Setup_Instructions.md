# Microsoft Access Database Setup Instructions

## 🎯 **How to Set Up the Library Database in Microsoft Access**

### **Step 1: Create a New Database**
1. Open Microsoft Access
2. Click "Blank database"
3. Choose a location and name it "LibraryDatabase"
4. Click "Create"

### **Step 2: Create Tables (Run Each File Separately)**

**⚠️ IMPORTANT: Run each SQL file separately in this exact order!**

1. **Open Query Design**
   - Click "Create" tab
   - Click "Query Design"
   - Click "Close" when prompted to add tables
   - Click "SQL View" in the ribbon

2. **Run Each File in Order:**

   **File 1:** `01_Create_Students_Table.sql`
   - Copy and paste the content
   - Click "Run" (red exclamation mark)
   - Click "Yes" to confirm

   **File 2:** `02_Create_Books_Table.sql`
   - Copy and paste the content
   - Click "Run"
   - Click "Yes" to confirm

   **File 3:** `03_Create_Categories_Table.sql`
   - Copy and paste the content
   - Click "Run"
   - Click "Yes" to confirm

   **File 4:** `04_Create_Borrowings_Table.sql`
   - Copy and paste the content
   - Click "Run"
   - Click "Yes" to confirm

   **File 5:** `05_Create_BookCategories_Table.sql`
   - Copy and paste the content
   - Click "Run"
   - Click "Yes" to confirm

### **Step 3: Set Up Primary Keys (Important!)**

After creating all tables, you need to set up primary keys manually:

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

### **Step 4: Insert Data (Run Each File Separately)**

   **File 6:** `06_Insert_Students_Data.sql`
   - Copy and paste the content
   - Click "Run"
   - Click "Yes" to confirm

   **File 7:** `07_Insert_Categories_Data.sql`
   - Copy and paste the content
   - Click "Run"
   - Click "Yes" to confirm

   **File 8:** `08_Insert_Books_Data.sql`
   - Copy and paste the content
   - Click "Run"
   - Click "Yes" to confirm

   **File 9:** `09_Insert_BookCategories_Data.sql`
   - Copy and paste the content
   - Click "Run"
   - Click "Yes" to confirm

   **File 10:** `10_Insert_Borrowings_Data.sql`
   - Copy and paste the content
   - Click "Run"
   - Click "Yes" to confirm

### **Step 5: Verify Setup**
1. Go to "All Access Objects" in the left panel
2. Click "Tables"
3. You should see 5 tables:
   - Students
   - Books
   - Categories
   - Borrowings
   - BookCategories

### **Step 6: Test Queries**
1. Open Query Design
2. Click "SQL View"
3. Copy and paste any query from the sample queries file
4. Click "Run" to see results

## 📋 **Sample Queries to Test**

### **Query 1: List All Students**
```sql
SELECT StudentID, FirstName, LastName, Grade, Email
FROM Students
WHERE IsActive = Yes
ORDER BY LastName, FirstName;
```

### **Query 2: List All Books**
```sql
SELECT Title, Author, Genre, Price
FROM Books
ORDER BY Title;
```

### **Query 3: Overdue Books**
```sql
SELECT s.FirstName, s.LastName, b.Title, br.DueDate, Date() - br.DueDate AS DaysOverdue
FROM Students s
INNER JOIN Borrowings br ON s.StudentID = br.StudentID
INNER JOIN Books b ON br.BookID = b.BookID
WHERE br.DueDate < Date() AND br.Status = 'Borrowed'
ORDER BY DaysOverdue DESC;
```

## ⚠️ **Important Notes**

- **Run files in order:** Tables must be created before inserting data
- **One file at a time:** Microsoft Access doesn't support multiple statements
- **Set primary keys:** Must be done manually in Design View
- **Save queries:** Save useful queries for future use
- **Backup:** Always backup your database before making changes

## 🎓 **For Students**

This database includes:
- ✅ 8 sample students (Grade 11)
- ✅ 10 popular books across different genres
- ✅ 8 book categories
- ✅ 10 sample borrowing records
- ✅ 18 different query examples

Perfect for practicing Microsoft Access database concepts! 📚✨
