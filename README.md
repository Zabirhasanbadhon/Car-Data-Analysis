# 🚗 Cars Data Analysis

A modern desktop application for exploring, cleaning, filtering, and analyzing car data. Built with **Python**, **Tkinter**, and **Pandas**, this project provides a user-friendly graphical interface for common data-analysis tasks without requiring Jupyter Notebook.

## ✨ Features

- **Dashboard overview**
  - Total number of records
  - Number of dataset columns
  - Total missing cells
  - Number of unique car manufacturers
- **Dataset explorer**
  - Load a CSV dataset using a file picker
  - Browse records in a scrollable table
  - Search across row values
  - Export the current dataset view to CSV
- **Data cleaning**
  - Inspect missing values by column
  - Fill missing `Cylinders` values with the column mean
  - Remove records where `Weight > 4000`
- **Filters and analysis**
  - Filter cars with `Origin` equal to `Asia` or `Europe`
  - Filter cars where `Horsepower > 200`
  - View value counts for `Make`
  - View value counts for `Origin`
- **Data transformation**
  - Increase values in `MPG_City` by 3
- **Modern interface**
  - Dark-themed dashboard
  - Sidebar navigation
  - Data tables and scrollbars
  - Status indicators and clear action buttons

> The app expects the selected CSV file to contain the columns used by an operation, such as `Make`, `Origin`, `Cylinders`, `Weight`, `Horsepower`, and `MPG_City`. The dataset can contain additional columns; they are displayed automatically.

## 🛠️ Built With

- **Python 3**
- **Tkinter** — desktop graphical user interface
- **Pandas** — data loading, cleaning, filtering, and analysis

## 📁 Project Structure

```text
Cars-Data-Analysis-GUI/
├── cars_data_analysis_gui.py
├── Cars_Dataset.csv             # Add your dataset here, if you plan to include it
└── README.md
```

The dataset is selected from inside the application, so it does not have to be stored in the project folder. Only commit a dataset if you have permission to share it.

## ⚙️ Requirements

- Python 3.9 or newer recommended
- Pandas

Tkinter is included with most standard Windows Python installations. On some Linux distributions, you may need to install the system package for Tkinter.

### 4. Load your dataset

1. Click **Load CSV Dataset** in the left sidebar.
2. Select your car dataset CSV file.
3. Explore the overview dashboard and open the Dataset Explorer, Data Cleaning, or Filters & Analysis sections.
4. Use **Export current view** to save the current table data as a CSV file.

## 📊 Data Operations

| Operation | Description |
|---|---|
| Dataset overview | Displays record count, column count, missing-cell count, and unique makes |
| Missing-value inspection | Shows the number of missing values in each column |
| Fill missing cylinders | Replaces missing `Cylinders` values with the mean of that column |
| Origin filter | Selects records whose `Origin` is `Asia` or `Europe` |
| Weight filter | Removes records with `Weight > 4000` from the working dataset |
| Horsepower filter | Selects records with `Horsepower > 200` |
| Make value counts | Counts records for each manufacturer |
| Origin value counts | Counts records for each origin |
| City MPG transformation | Adds 3 to values in `MPG_City` |
| CSV export | Saves the current view to a new CSV file |

## 📝 Notes

- **Column names matter:** operations use the column names listed above. If your CSV uses different names, rename the columns or update the code.
- **Working data:** cleaning and transformation actions modify the in-memory working dataset. Multiple operations can affect subsequent results.
- **Original file:** the application does not overwrite the source CSV automatically. Export results to save them.
- **Table display:** for responsiveness, the table renders up to 2,000 rows at a time. Exporting the current view includes all rows in that view.
- **Charts:** the current GUI focuses on dashboard metrics, tables, filters, and data-cleaning actions; it does not require Matplotlib.

## 🧯 Troubleshooting

### `ModuleNotFoundError: No module named 'pandas'`

Install Pandas:

```bash
python -m pip install pandas
```

### The app opens, but the table is empty

Click **Load CSV Dataset** and choose a valid CSV file.

### A message says a column is missing

Check that the CSV contains the required column with the exact expected name, such as `Horsepower` or `MPG_City`.

### Tkinter is unavailable

On Windows, reinstall or modify your Python installation to include Tcl/Tk. On Ubuntu/Debian-based Linux systems, you may need:

```bash
sudo apt install python3-tk
```

**Made with Python, Tkinter, and Pandas.**
