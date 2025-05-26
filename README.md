# 📬 Job Application Tracker

This project is an **interactive dashboard** built with Streamlit that allows you to visualize and analyze job applications data.

## 🚀 Main Features

- 🔍 Automatic extraction of relevant emails (using keywords and sender exclusions)
- 📊 Automatic classification of process status: Application, Interview, Offer, Rejection, Other
- 📈 Visualization of time trends and dynamic filters
- 📁 Manual application integration via Excel file
- 🗂️ Tabbed navigation to separate data sources

## 🗃️ Project Structure

```
jobAppAnalysis/
│
├── config/                # Additional project configuration
│
├── dashboard/             
│   └── dashboard.py       # Main dashboard code (Streamlit)
│
├── data/                  
│   ├── job_Applications.csv    # Exported log from LinkedIn
│   ├── raw_subjects.csv        # Processed email subjects
│   └── tracker.csv             # Automated job application tracking (from emails)
│
├── scripts/              
│   └── extract_raw_subjects.py # Script to extract and process top n email subjects
│
└── src/                   
│   ├── email_reader.py        # Logic to read emails (IMAP)
│   ├── keyword_analysis.py    # Keyword analysis and relevant info extraction
│   └── parser.py              # Functions to parse, clean, and transform data
│
├── main.py                # Main script to launch the app or processing
├── requirements.txt       
├── README.md              
└── .env                   # Environment variables (credentials and sensitive settings)
```

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/sue-btis/jobAppAnalysis
cd jobAppAnalysis
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/Scripts/activate  # or source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
```

3. Set up your `.env` file:
```env
IMAP_SERVER=imap.gmail.com
EMAIL_ACCOUNT=your_email@gmail.com
APP_PASSWORD=your_app_password
```

4. Run the script to generate the CSV:
```bash
python main.py
```

5. Launch the dashboard:
```bash
streamlit run dashboard/dashboard.py
```

## 📥 Data Sources

- **Automatic:** Emails with relevant keywords from gmail
- **Manual:** Excel file with custom data

## 📌 Requirements

- Python 3.10+
- Libraries: `pandas`, `streamlit`, `beautifulsoup4`, `plotly`, `imaplib`, etc.

## 🙌 Credits

Developed by Josue Escobar. Inspired by the need to track my job opportunities.

## 🔧 Areas for Improvement

- The filtering logic in `src/keyword_analysis.py` and `src/parser.py` is functional, but it is based on manually defined exclusion keywords
  tailored to my personal inbox (e.g., promotional or social emails). As a result, it may not generalize well to other users' email patterns.
  Enhancements could include:
  - Improving the keyword matching system.
  - Better handling of edge cases and reducing false positives/negatives.
  - A future improvement could involve allowing users to customize their own filtering rules or incorporating machine learning to adaptively filter noise.

