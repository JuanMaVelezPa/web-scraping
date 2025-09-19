# Price Monitoring Script

This Python script monitors product prices from e-commerce websites. It uses multithreading for fast parallel processing and saves the data to a single CSV file.

## How to Use

1.  **Installation**: Install the required libraries with `pip install -r requirements.txt`.
2.  **Input File**: The script reads from `products.csv`. Ensure it has these columns: `Client`, `Code`, `Url`.
3.  **Run**: Execute the script with `python main_script.py`. The output is saved to `consolidated_prices.csv`.

---

## Automation

This project can run daily on GitHub Actions. The workflow is configured to run on a schedule, process the URLs, and upload the final CSV as a downloadable artifact.


## Contributing

Feel free to contribute by adding new scraping functions or improving existing ones!

## Developer Information

- **Name:** Juan Manuel Velez Parra
- **Email:** juanmavelezpa@gmail.com