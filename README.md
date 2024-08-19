# Expense Tracker 1.0

## Description
This Expense Tracker is a web-based application built with Flask that helps users manage their personal finances. It allows users to track their income and expenses, categorize transactions, and view their spending habits over time.

## Features
- User registration and authentication
- Add and delete transactions
- Categorize transactions
- View transaction history

## Technologies Used
- Python
- Flask
- MySQL
- HTML/CSS
- JavaScript

## Setup and Installation
1. Clone the repository:
   ```
   git clone https://github.com/saxcrawford/expense-tracker.git
   cd expense-tracker
   ```

2. Create a virtual environment and activate it:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip3 install -r requirements.txt
   ```

4. Set up your MySQL database and update the connection details in `app.py`.
   I am currently in the process of hosting the website so you don't have to make the database tables yourself. However, if you want to, these are the tables:
   #### Categories
   ```
    CREATE TABLE Categories (
      category_id INT AUTO_INCREMENT PRIMARY KEY,
      category_name VARCHAR(50) UNIQUE NOT NULL
    );
   ```
   #### Transactions
   ```
    CREATE TABLE Transactions (
      transaction_id INT AUTO_INCREMENT PRIMARY KEY,
      transaction_amount DECIMAL(10,2),
      transaction_desc VARCHAR(100) NOT NULL,
      transaction_date DATE,
      category_id INT,
      transaction_type ENUM('Income', 'Expense'),
      user_id INT,
      FOREIGN KEY (category_id) REFERENCES Categories(category_id) ON DELETE CASCADE,
      FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );
   ```
   #### Users
   ```
    CREATE TABLE Users (
      user_id INT AUTO_INCREMENT PRIMARY KEY,
      user_username VARCHAR(50) UNIQUE NOT NULL,
      user_password VARCHAR(255) NOT NULL,
    );
   ```

6. Run the application:
   ```
   python3 app.py 
   ```

8. Open a web browser and navigate to `http://localhost:5000`.

## Contact
Saxon Crawford - saxon.crawford@icloud.com
