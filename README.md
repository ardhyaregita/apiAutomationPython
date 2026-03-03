# ✈️ API Automation Testing with Python

Welcome to my API Automation learning repository! 🚀 

This project documents my journey transitioning from manual API testing via Postman's UI to writing automated test scripts from scratch using Python. 

## 🛠️ Tech Stack
- **Language:** Python 3.x
- **Testing Framework:** `pytest`
- **HTTP Library:** `requests`
- **Target API (Dummy App):** [Airport Gap API](https://airportgap.com/)

## 🧪 Test Scenarios Covered
Currently, the tests are focused on the `GET` method. The scenarios executed in `test_airport_idn.py` include:
- `get_all_airports`
- `get_airports_by_id` (Success, Not Found, Invalid)
- `get_airports_by_pagination` (Success, Invalid, Out of range)

**Key Assertions Validated:**
- HTTP Status Codes (`response.status_code`)
- Array Length (`len(data)`)
- Data Type validation (`isinstance`)
- Response Headers (`response.headers`)

## 🚀 How to Run the Tests Locally

If you want to clone and run this project on your local machine, follow these steps:

1. **Clone the repository:**
   git clone [https://github.com/ardhyaregita/apiAutomationPython.git](https://github.com/ardhyaregita/apiAutomationPython.git)
   cd apiAutomationPython
2. **Install dependencies:**
   Make sure you have Python installed, then install the required libraries:
   pip install pytest requests
3. **Execute the tests:**
   Run the tests using pytest with the verbose flag (-v) for a detailed output:
   pytest test_airport_idn.py -v
