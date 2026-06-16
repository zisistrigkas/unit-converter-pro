# Unit & Currency Converter Pro

## 🚀 Features
- **Real-time Currency Exchange:** Fetches daily live exchange rates directly from the **European Central Bank (ECB)** via XML.
- **Offline Reliability:** Seamless fallback mechanism; automatically uses cached rates if the internet connection is unavailable.
- **Multi-Category Support:** Handles conversions for Length, Weight, Speed, and Temperature.
- **Transaction History:** Keeps a log of recent conversions for user convenience.

## 🧠 Technical Highlights
- **API Integration:** Utilizes the `requests` library to fetch and `xml.etree.ElementTree` to parse live financial data.
- **Robust Error Handling:** Implements `try-except` blocks to handle network failures gracefully.
- **GUI Engineering:** Uses `tkinter` and `ttk` for a native, responsive desktop experience.

## 🛠 How to Run
1. Ensure you have **Python** installed.
2. Install the necessary library:
   ```bash
   pip install requests
