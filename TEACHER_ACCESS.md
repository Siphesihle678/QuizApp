# 👨‍🏫 Teacher Access Information

## Login Credentials

**Username:** `admin`  
**Password:** `password123`

## How to Access the Teacher Dashboard

1. **Go to the main page** of your CAT Quiz System
2. **Click on "👨‍🏫 Teacher Access"** at the bottom of the page
3. **Enter the credentials above**
4. **Click "Login"**
5. **You'll be redirected to the protected teacher dashboard**

## Dashboard Features

- 📊 View all student quiz results
- 📈 Analyze performance statistics
- 🔍 Filter results by grade, score, and student name
- 📋 Export results to CSV
- 👥 View detailed student information
- 📊 Switch between Database and Excel quiz results

## Security Notes

⚠️ **Important:** 
- Change the default password in production
- Update the `app.secret_key` in `app.py` for production use
- Consider using environment variables for sensitive data

## URLs

- **Student Portal:** `/` (main page)
- **Teacher Login:** `/teacher-login`
- **Teacher Dashboard:** `/teacher-dashboard` (requires login)
- **Logout:** `/teacher-logout`

## Default Credentials Location

The credentials are stored in the `app.py` file:

```python
TEACHER_CREDENTIALS = {
    'admin': hashlib.sha256('password123'.encode()).hexdigest()
}
```

To change the password, update the `'password123'` part and regenerate the hash.
