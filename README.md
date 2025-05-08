# ☔️ The Daily Drip

**The Daily Drip** is an interactive Streamlit dashboard for exploring and visualizing daily rainfall data. It provides a clean, engaging UI to upload, clean, and analyze rain measurements, including donut charts for rain intensity, daily distributions, and key weather stats.

---

## 📊 Features

- 📤 Upload your own CSV rain dataset from MeteoBlue
- 🧹 Built-in data cleaning
- 📅 Date range filtering
- 🌧️ Rain intensity classification
- 📈 Donut chart + bar chart visualizations with Plotly
- 📥 Download cleaned data

---

## 📁 Project Structure

## Project Structure

```
daily-drip/
├── data-prep
|   ├── data-prep-rain.ipynb     # 1st try at data cleaning logic via notebook
|   ├── rain-data-processed.csv
├── historical-data             # where historical data is stored
|    ├── original-data.csv
├── main.py                     # Streamlit app – handles UI, charts, and layout
├── data_cleaning.py            # Data cleaning logic – handles formatting and classification
├── fallback.csv                # Default dataset used when no CSV is uploaded
├── requirements.txt
├── README.md
```

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.9+
- pip or uv (Rust-based package manager)

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
# or if using uv
uv pip install -r requirements.txt
```

### ▶️ Run the App

```bash
streamlit run main.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📂 How It Works

- If a user uploads a CSV file, it is cleaned via `data_cleaning.py`.
- If no upload is provided, a default dataset (`fallback.csv`) is loaded.
- Data is processed and classified by rain intensity, then plotted.
- Metrics like total, average, max rainfall, and frequency are calculated.
- All visuals are updated based on user-selected date filters.

---

## 🧠 Tech Stack

- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [Pandas](https://pandas.pydata.org/)
- Python 3.9+

---

## 💡 Future Ideas

- Multi-location data selection
- Export to Excel not just csv
- Long-term trend analysis

---

## 👤 Author

Made with ☕ and ☔️ by [@Tiago3BC](https://github.com/Tiago3BC)

---
