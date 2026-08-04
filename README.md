# FinTrack AI — Intelligent Personal Finance Dashboard

## About the Project

FinTrack AI is an AI-powered Personal Finance Dashboard built using Python and Streamlit that helps users take control of their finances by tracking income, managing expenses, analyzing spending patterns, and planning future savings—all from a single dashboard.

The application provides a centralized platform for recording income and expenses, monitoring financial health, managing budgets, tracking savings goals, and understanding spending behavior through interactive analytics.

FinTrack AI follows a modern fintech dashboard approach with:

* Interactive financial dashboards
* Real-time calculations
* Data visualization
* Automated financial insights
* Financial report generation

The project is built with a lightweight and modular architecture where financial data is stored locally using CSV files, making the application simple to configure and run without requiring an external database.

---

# Problem Statement

Managing personal finances manually using spreadsheets or notes makes it difficult to identify spending patterns, control unnecessary expenses, and maintain consistent savings.

FinTrack AI solves this problem by providing:

* Structured transaction management
* Expense and income tracking
* Financial analytics visualization
* Budget monitoring
* Savings goal tracking
* Automated spending insights
* Exportable financial reports

---

# Project Objectives

The main objectives of FinTrack AI are:

* Build an easy-to-use personal finance management system
* Analyze financial activities using data visualization
* Help users understand spending behavior
* Improve budgeting and saving decisions
* Provide meaningful financial summaries
* Create a scalable foundation for future AI and cloud-based enhancements

---

# Application Workflow

```
User Input
     |
     |
Transaction Management
     |
     |
Local CSV Storage
     |
     |
Financial Data Processing
     |
     |
Analytics Engine
     |
     |
Dashboard Visualization & Insights
```

---

# Key Features

## Financial Dashboard

Provides a complete overview of financial status:

* Total income
* Total expenses
* Current balance
* Savings summary
* Transaction statistics
* Recent activity tracking

---

## Transaction Management

Users can manage financial records:

* Add income transactions
* Add expense transactions
* Edit transactions
* Delete transactions
* Search transactions
* Filter transactions by:

  * Type
  * Category
  * Date range

---

## Financial Analytics

Interactive analytics using Plotly:

* Income vs expense trends
* Expense category analysis
* Income source analysis
* Daily spending patterns
* Monthly financial summaries
* Savings growth visualization

---

## Intelligent Financial Insights

FinTrack AI analyzes transaction patterns to provide:

* Highest spending category detection
* Lowest spending category analysis
* Spending comparison
* Savings percentage calculation
* Financial observations

---

## Budget Management

Features include:

* Create category-based budgets
* Set monthly limits
* Monitor budget usage
* Identify overspending categories

---

## Savings Goal Tracking

Users can:

* Create savings goals
* Track progress
* Update saved amounts
* Monitor remaining targets

---

## Financial Reports

Export financial information as:

* CSV reports
* Excel reports
* PDF statements

---

# Technology Stack

## Programming Language

* Python

## Framework

* Streamlit

## Data Processing

* Pandas

## Data Visualization

* Plotly

## Report Generation

* FPDF2
* OpenPyXL

## Data Storage

* CSV-based local storage

---

# Project Structure

```
FinTrack-AI/

│
├── app.py                 # Main Streamlit application
│
├── styles.py              # Custom UI styling and theme
│
├── ui_components.py       # Reusable Streamlit components
│
├── transactions.csv       # Transaction data storage
│
├── budgets.csv            # Budget information storage
│
├── goals.csv              # Savings goal storage
│
├── requirements.txt       # Project dependencies
│
└── README.md
```

---

# Running the Application

Follow these steps to run FinTrack AI locally.

## Step 1: Clone the Repository

Clone the project:

```bash
git clone <repository-url>
```

Navigate into the project folder:

```bash
cd FinTrack-AI
```

---

## Step 2: Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv venv
```

Activate the environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

After activation, the terminal should display:

```
(venv)
```

---

## Step 3: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

Installed dependencies:

* Streamlit
* Pandas
* Plotly
* FPDF2
* OpenPyXL

---

## Step 4: Verify Project Files

Ensure the project contains:

```
FinTrack-AI/

├── app.py
├── styles.py
├── ui_components.py
├── requirements.txt
├── transactions.csv
├── budgets.csv
├── goals.csv
└── README.md
```

CSV files will be created automatically if they do not exist.

---

## Step 5: Start the Application

Run the Streamlit server:

```bash
streamlit run app.py
```

or:

```bash
python -m streamlit run app.py
```

---

## Step 6: Open the Dashboard

After successful execution, Streamlit will provide a local URL:

```
http://localhost:8501
```

Open this URL in your browser to access FinTrack AI.

---

# Using the Application

## Dashboard

View:

* Income summary
* Expense summary
* Current balance
* Savings information
* Recent transactions

---

## Transactions

To add a transaction:

1. Open the Transactions section.
2. Select transaction type.
3. Enter amount, category, date, and description.
4. Save the transaction.

Transactions can be searched, filtered, edited, or deleted.

---

## Analytics

Analyze:

* Spending patterns
* Income trends
* Expense categories
* Savings progress

---

## Settings

Manage:

* Budgets
* Savings goals
* Financial exports

---

# Reset Application Data

FinTrack AI stores data locally.

To reset the application:

1. Stop the Streamlit server.
2. Delete:

```
transactions.csv
budgets.csv
goals.csv
```

3. Restart the application.

The application will generate fresh files automatically.

---

# Future Enhancements

Planned improvements:

* AI chatbot financial assistant
* Machine learning expense prediction
* Receipt OCR scanning
* Bank API integration
* User authentication
* Cloud database migration
* Financial forecasting models
* Personalized recommendations

---

# Author

**Sriram M**

Python Backend Developer | AI/ML Enthusiast

GitHub:
https://github.com/sriram-dev00

LinkedIn:
https://www.linkedin.com/in/sriram-m-j-5491a7322/
