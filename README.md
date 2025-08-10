# 🏦 Largest Banks ETL Project
![status](https://img.shields.io/badge/status-passed-brightgreen)

### ✅ Project Status
This project is **functionally complete and tested**, but **open for future improvements and enhancements**.

📄 [View full ETL pipeline in Jupyter Notebook](bank_project.ipynb)

A mini-project demonstrating a complete ETL (Extract–Transform–Load) pipeline using Python.  
The project scrapes market capitalization data for the world's largest banks, converts it into multiple currencies, stores the results in CSV and SQLite, and generates visual insights.

---

## 📁 Project Structure
```
Largest-Banks-ETL/
├── data/                                     ← Input data files
│ └── exchange_rate.csv                       ← Currency exchange rates
├── images/                                   ← Generated charts and process screenshots
│ ├── extract_output_result.png
│ ├── transform_result.png
│ ├── load_to_bd_result.png
│ ├── run_query_result.png
│ └── top5_banks_market_cap.svg
├── output/                                   ← ETL output
│ ├── Largest_banks_data.csv                  ← Full cleaned dataset
│ ├── top5_banks.csv                          ← Top 5 banks by market cap
│ └── code_log.txt                            ← ETL execution log
├── src/                                      ← Source code
│ └── bank_project.py                         ← Python version of ETL logic
├── bank_project.ipynb                        ← Full ETL pipeline in Jupyter Notebook
├── test_transform.py                         ← Unit test for transformation logic
├── requirements.txt                          ← Project dependencies
├── LICENSE
└── README.md
```
---


---

## 🛠️ Skills & Tools

- **Python** : core programming language
- **pandas** : data manipulation and transformation
- **numpy** : numerical computations
- **requests** : downloading HTML content
- **BeautifulSoup (bs4)** : HTML parsing and web scraping
- **sqlite3** : storing processed data in a local database
- **matplotlib** : data visualization
- **logging** : logging process and errors
- **Jupyter Notebook** : interactive development

---

## 🔄 ETL Process Overview

### 1️⃣ Extract
- Scrapes the archived Wikipedia page of the largest banks by market capitalization  
- Extracts `Name` and `MC_USD_Billion` columns

### 2️⃣ Transform
- Reads currency exchange rates from [`data/exchange_rate.csv`](data/exchange_rate.csv)
- Converts market capitalization from USD to GBP, EUR and INR
- Rounds values to two decimal places

### 3️⃣ Load
- Saves the full dataset to: [`output/Largest_banks_data.csv`](output/Largest_banks_data.csv)  
- Saves the Top 5 banks by market cap to: [`output/top5_banks.csv`](output/top5_banks.csv)  
- Stores all data in SQLite database `Banks.db`  
- Logs operations in: [`output/code_log.txt`](output/code_log.txt)

---

## 📊 Visual Insights

Using **matplotlib**, the project generates charts for quick analysis:

- **Top 5 Banks by Market Capitalization**  
  [`images/top5_banks_market_cap.svg`](images/top5_banks_market_cap.svg)

### 📌 Key Insights:
- Clear market dominance by a few global players
- The difference in capitalization between top banks is substantial
- Visual representation makes it easier to compare values across currencies
- The largest bank by market capitalization is **JPMorgan Chase** — over **$430 billion**
- The Top 5 are mostly **American** and **Chinese** banks, showing U.S. and Chinese dominance in global banking
- **European** and **Indian** banks are rare in the top ranks — usually only 1–2 positions
- Currency conversion (USD, EUR, GBP) does not change the ranking order, indicating stable relative positions

---

## ⚙️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/CloudDataPalina/Largest-Banks-ETL.git
cd Largest-Banks-ETL
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Python script
```bash
python src/bank_project.py
```

### 4. (Optional) Run unit tests
```bash
python test_transform.py
```
---

## 📊 Sample Output (Top 5 Banks)
| Name   | MC\_USD\_Billion | MC\_GBP\_Billion | MC\_EUR\_Billion |
| ------ | ---------------- | ---------------- | ---------------- |
| Bank A | 350.50           | 280.40           | 315.45           |
| Bank B | 300.20           | 240.16           | 270.18           |
| Bank C | 280.00           | 224.00           | 252.00           |
| Bank D | 260.10           | 208.08           | 234.09           |
| Bank E | 250.50           | 200.40           | 225.45           |

---

## ✅ Summary
In this mini-project:
- ***Extracted*** financial data via web scraping from Wikipedia (archived page)
- ***Transformed*** market capitalization to multiple currencies
- ***Loaded*** results into CSV and SQLite for storage and analysis
- 🧾 ***Logged*** all operations for traceability
- 📊 ***Visualized*** Top 5 banks by market capitalization

This project is a practical example of how ETL techniques can be applied to real-world financial data for quick analytics and decision-making.

---

## 👩‍💻 Author

**Palina Krasiuk**  
Aspiring Cloud Data Engineer | ex-Senior Accountant  
[LinkedIn](https://www.linkedin.com/in/palina-krasiuk-954404372/) • [GitHub Portfolio](https://github.com/CloudDataPalina)
