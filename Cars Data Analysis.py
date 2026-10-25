import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    HAS_MPL = True
except ImportError:
    HAS_MPL = False

BG = "#0b1120"
SIDEBAR = "#111a2e"
PANEL = "#151f33"
PANEL2 = "#1b2942"
TEXT = "#edf2ff"
MUTED = "#9aa9c4"
ACCENT = "#6c8cff"
TEAL = "#39d6bd"
ORANGE = "#ffb86b"
RED = "#ff6b81"
FONT = ("Segoe UI", 10)
TITLE_FONT = ("Segoe UI Semibold", 22)
HEAD_FONT = ("Segoe UI Semibold", 12)


class CarsAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cars Data Analysis | Insights Studio")
        self.root.geometry("1360x820")
        self.root.minsize(1050, 680)
        self.root.configure(bg=BG)

        self.original_df = None
        self.df = None
        self.view_df = None
        self.current_view_name = "Dataset preview"
        self.file_path = ""
        self._style()
        self._build_layout()
        self._show_welcome()

    def _style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=FONT)
        style.configure("Treeview", background=PANEL, fieldbackground=PANEL,
                        foreground=TEXT, rowheight=29, borderwidth=0)
        style.configure("Treeview.Heading", background=PANEL2, foreground=TEXT,
                        font=("Segoe UI Semibold", 9), relief="flat", padding=8)
        style.map("Treeview", background=[("selected", ACCENT)],
                  foreground=[("selected", "#ffffff")])
        style.configure("TCombobox", fieldbackground=PANEL2, background=PANEL2,
                        foreground=TEXT, arrowcolor=TEXT)
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=SIDEBAR, foreground=MUTED,
                        padding=(16, 10), borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", ACCENT)],
                  foreground=[("selected", "#ffffff")])

    def _build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=SIDEBAR, width=235)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", padx=22, pady=(26, 30))
        tk.Label(brand, text="◈  AUTO INSIGHT", bg=SIDEBAR, fg=TEAL,
                 font=("Segoe UI Semibold", 15)).pack(anchor="w")
        tk.Label(brand, text="CARS DATA ANALYSIS", bg=SIDEBAR, fg=MUTED,
                 font=("Segoe UI", 8)).pack(anchor="w", pady=(7, 0))

        tk.Label(self.sidebar, text="WORKSPACE", bg=SIDEBAR, fg="#7182a4",
                 font=("Segoe UI Semibold", 8)).pack(anchor="w", padx=22, pady=(0, 10))
        self.nav_buttons = {}
        for label, key in [
            ("⌂   Overview", "overview"),
            ("▦   Dataset Explorer", "dataset"),
            ("◉   Data Cleaning", "cleaning"),
            ("⌕   Filters & Analysis", "analysis"),
        ]:
            b = tk.Button(self.sidebar, text=label, anchor="w", relief="flat",
                           bd=0, padx=20, pady=12, cursor="hand2",
                           bg=SIDEBAR, fg=TEXT, activebackground=PANEL2,
                           activeforeground=TEAL,
                           font=("Segoe UI", 10),
                           command=lambda k=key: self._navigate(k))
            b.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[key] = b

        bottom = tk.Frame(self.sidebar, bg=SIDEBAR)
        bottom.pack(side="bottom", fill="x", padx=18, pady=20)
        tk.Button(bottom, text="＋  Load CSV Dataset", command=self.load_csv,
                  bg=ACCENT, fg="white", activebackground="#5576eb",
                  activeforeground="white", relief="flat", bd=0, cursor="hand2",
                  font=("Segoe UI Semibold", 10), pady=12).pack(fill="x")
        tk.Label(bottom, text="Tkinter • Pandas", bg=SIDEBAR, fg="#7182a4",
                 font=("Segoe UI", 8)).pack(anchor="w", pady=(13, 0))

        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)
        self.header = tk.Frame(self.main, bg=BG)
        self.header.pack(fill="x", padx=30, pady=(24, 16))
        self.page_title = tk.Label(self.header, text="Overview", bg=BG, fg=TEXT,
                                   font=TITLE_FONT)
        self.page_title.pack(side="left")
        self.status = tk.Label(self.header, text="● No dataset loaded", bg=BG,
                               fg=ORANGE, font=("Segoe UI", 9))
        self.status.pack(side="right", pady=8)

        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(fill="both", expand=True, padx=30, pady=(0, 24))
        self.pages = {}
        self._build_overview()
        self._build_dataset()
        self._build_cleaning()
        self._build_analysis()
        self._navigate("overview")

    def _card(self, parent, title, value, hint, accent=ACCENT):
        frame = tk.Frame(parent, bg=PANEL, highlightthickness=1,
                         highlightbackground="#23314b")
        tk.Frame(frame, bg=accent, height=3).pack(fill="x")
        inner = tk.Frame(frame, bg=PANEL)
        inner.pack(fill="both", expand=True, padx=18, pady=14)
        tk.Label(inner, text=title.upper(), bg=PANEL, fg=MUTED,
                 font=("Segoe UI Semibold", 8)).pack(anchor="w")
        val = tk.Label(inner, text=value, bg=PANEL, fg=TEXT,
                       font=("Segoe UI Semibold", 23))
        val.pack(anchor="w", pady=(7, 2))
        tk.Label(inner, text=hint, bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 8)).pack(anchor="w")
        return frame, val

    def _section(self, parent, title, subtitle=None):
        top = tk.Frame(parent, bg=BG)
        top.pack(fill="x", pady=(0, 13))
        tk.Label(top, text=title, bg=BG, fg=TEXT, font=HEAD_FONT).pack(anchor="w")
        if subtitle:
            tk.Label(top, text=subtitle, bg=BG, fg=MUTED,
                     font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 0))
        return top

    def _build_overview(self):
        page = tk.Frame(self.content, bg=BG)
        self.pages["overview"] = page
        self._section(page, "Your automotive data at a glance",
                      "Load your CSV to explore, clean, filter, and analyze the cars dataset.")
        cards = tk.Frame(page, bg=BG)
        cards.pack(fill="x", pady=(2, 20))
        self.metric_labels = {}
        for title, key, hint, color in [
            ("Total records", "rows", "Cars in current dataset", ACCENT),
            ("Data columns", "cols", "Available attributes", TEAL),
            ("Missing cells", "missing", "Across all columns", ORANGE),
            ("Car makes", "makes", "Unique manufacturers", RED),
        ]:
            card, value_label = self._card(cards, title, "—", hint, color)
            card.pack(side="left", fill="both", expand=True, padx=(0, 12))
            self.metric_labels[key] = value_label

        panel = tk.Frame(page, bg=PANEL, highlightthickness=1,
                         highlightbackground="#23314b")
        panel.pack(fill="both", expand=True)
        tk.Label(panel, text="QUICK ACTIONS", bg=PANEL, fg=MUTED,
                 font=("Segoe UI Semibold", 8)).pack(anchor="w", padx=20, pady=(18, 12))
        actions = [
            ("▦  Explore dataset", "Browse all columns and records.", lambda: self._navigate("dataset")),
            ("◉  Check missing values", "Review null counts and fill Cylinders with its mean.", lambda: self._navigate("cleaning")),
            ("⌕  Filter cars", "View Asia/Europe origins or cars above 200 horsepower.", lambda: self._navigate("analysis")),
        ]
        for title, desc, cmd in actions:
            row = tk.Frame(panel, bg=PANEL2)
            row.pack(fill="x", padx=18, pady=5)
            tk.Button(row, text=title, command=cmd, bg=PANEL2, fg=TEXT,
                      activebackground="#263858", activeforeground=TEAL,
                      relief="flat", bd=0, font=("Segoe UI Semibold", 10),
                      padx=14, pady=10).pack(side="left")
            tk.Label(row, text=desc, bg=PANEL2, fg=MUTED,
                     font=("Segoe UI", 9)).pack(side="left", padx=10)
        self.overview_note = tk.Label(panel, text="Start by selecting your Cars_Dataset.csv file.",
                                      bg=PANEL, fg=ORANGE, font=("Segoe UI", 9))
        self.overview_note.pack(anchor="w", padx=20, pady=(16, 18))

    def _build_dataset(self):
        page = tk.Frame(self.content, bg=BG)
        self.pages["dataset"] = page
        self._section(page, "Dataset explorer", "Search, inspect, and export the current table.")
        toolbar = tk.Frame(page, bg=BG)
        toolbar.pack(fill="x", pady=(0, 12))
        tk.Label(toolbar, text="Search rows", bg=BG, fg=MUTED).pack(side="left")
        self.search_var = tk.StringVar()
        search = tk.Entry(toolbar, textvariable=self.search_var, bg=PANEL2, fg=TEXT,
                          insertbackground=TEXT, relief="flat", width=28)
        search.pack(side="left", padx=(10, 14), ipady=7)
        search.bind("<KeyRelease>", lambda e: self._render_table())
        tk.Button(toolbar, text="↻ Reset view", command=self.reset_view,
                  bg=PANEL2, fg=TEXT, relief="flat", padx=12, pady=8).pack(side="left", padx=3)
        tk.Button(toolbar, text="Export current view", command=self.export_csv,
                  bg=TEAL, fg="#06221e", relief="flat", padx=12, pady=8,
                  font=("Segoe UI Semibold", 9)).pack(side="right")
        self.table_frame = tk.Frame(page, bg=PANEL)
        self.table_frame.pack(fill="both", expand=True)
        self.tree = None
        self.table_info = tk.Label(page, text="No data loaded", bg=BG, fg=MUTED)
        self.table_info.pack(anchor="w", pady=(9, 0))

    def _build_cleaning(self):
        page = tk.Frame(self.content, bg=BG)
        self.pages["cleaning"] = page
        self._section(page, "Data cleaning", "Run the data-quality operations from your original notebook.")
        self.null_summary = tk.Frame(page, bg=PANEL, highlightthickness=1,
                                     highlightbackground="#23314b")
        self.null_summary.pack(fill="both", expand=True, pady=(0, 14))
        tk.Label(self.null_summary, text="MISSING VALUES BY COLUMN", bg=PANEL,
                 fg=MUTED, font=("Segoe UI Semibold", 9)).pack(anchor="w", padx=18, pady=(16, 8))
        self.null_text = tk.Text(self.null_summary, bg=PANEL, fg=TEXT, relief="flat",
                                 font=("Consolas", 10), height=12, wrap="none",
                                 insertbackground=TEXT)
        self.null_text.pack(fill="both", expand=True, padx=18, pady=(0, 14))
        buttons = tk.Frame(page, bg=BG)
        buttons.pack(fill="x")
        tk.Button(buttons, text="Inspect null values", command=self.inspect_nulls,
                  bg=PANEL2, fg=TEXT, relief="flat", padx=14, pady=11).pack(side="left", padx=(0, 8))
        tk.Button(buttons, text="Fill Cylinders with mean", command=self.fill_cylinders,
                  bg=ACCENT, fg="white", relief="flat", padx=14, pady=11).pack(side="left", padx=8)
        tk.Button(buttons, text="Remove Weight > 4000", command=self.remove_heavy,
                  bg="#9b6bff", fg="white", relief="flat", padx=14, pady=11).pack(side="left", padx=8)
        tk.Button(buttons, text="Increase MPG_City by 3", command=self.increase_mpg,
                  bg=TEAL, fg="#06221e", relief="flat", padx=14, pady=11).pack(side="left", padx=8)

    def _build_analysis(self):
        page = tk.Frame(self.content, bg=BG)
        self.pages["analysis"] = page
        self._section(page, "Filters & analysis", "Apply the exact filters and value counts used in your notebook.")
        controls = tk.Frame(page, bg=PANEL, highlightthickness=1,
                            highlightbackground="#23314b")
        controls.pack(fill="x", pady=(0, 14))
        tk.Label(controls, text="FILTER OPERATIONS", bg=PANEL, fg=MUTED,
                 font=("Segoe UI Semibold", 9)).grid(row=0, column=0, sticky="w", padx=18, pady=(16, 8), columnspan=4)
        tk.Button(controls, text="Origin is Asia or Europe", command=self.filter_asia_europe,
                  bg=ACCENT, fg="white", relief="flat", padx=13, pady=10).grid(row=1, column=0, padx=18, pady=(0, 16), sticky="w")
        tk.Button(controls, text="Horsepower > 200", command=self.filter_horsepower,
                  bg=PANEL2, fg=TEXT, relief="flat", padx=13, pady=10).grid(row=1, column=1, padx=8, pady=(0, 16), sticky="w")
        tk.Button(controls, text="Show Make value counts", command=self.make_counts,
                  bg=PANEL2, fg=TEXT, relief="flat", padx=13, pady=10).grid(row=1, column=2, padx=8, pady=(0, 16), sticky="w")
        tk.Button(controls, text="Show Origin value counts", command=self.origin_counts,
                  bg=PANEL2, fg=TEXT, relief="flat", padx=13, pady=10).grid(row=1, column=3, padx=8, pady=(0, 16), sticky="w")
        result_panel = tk.Frame(page, bg=PANEL, highlightthickness=1,
                                highlightbackground="#23314b")
        result_panel.pack(fill="both", expand=True)
        self.analysis_title = tk.Label(result_panel, text="Analysis results", bg=PANEL,
                                       fg=TEXT, font=HEAD_FONT)
        self.analysis_title.pack(anchor="w", padx=18, pady=(16, 8))
        self.analysis_text = tk.Text(result_panel, bg=PANEL, fg=TEXT, relief="flat",
                                     font=("Consolas", 10), wrap="none",
                                     insertbackground=TEXT)
        self.analysis_text.pack(fill="both", expand=True, padx=18, pady=(0, 14))
        self.analysis_text.insert("1.0", "Load a dataset, then choose an analysis operation.")

    def _navigate(self, key):
        for p in self.pages.values():
            p.pack_forget()
        self.pages[key].pack(fill="both", expand=True)
        titles = {"overview": "Overview", "dataset": "Dataset Explorer",
                  "cleaning": "Data Cleaning", "analysis": "Filters & Analysis"}
        self.page_title.configure(text=titles[key])
        for k, b in self.nav_buttons.items():
            b.configure(bg=PANEL2 if k == key else SIDEBAR,
                        fg=TEAL if k == key else TEXT)
        if key == "dataset":
            self._render_table()
        if key == "cleaning" and self.df is not None:
            self.inspect_nulls()

    def _show_welcome(self):
        self._update_metrics()

    def _require_data(self):
        if self.df is None:
            messagebox.showwarning("No dataset", "Please load your Cars_Dataset.csv file first.")
            return False
        return True

    def load_csv(self):
        path = filedialog.askopenfilename(title="Select Cars Dataset CSV",
                    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not path:
            return
        try:
            loaded = pd.read_csv(path)
        except Exception as exc:
            messagebox.showerror("Could not load CSV", str(exc))
            return
        self.file_path = path
        self.original_df = loaded.copy()
        self.df = loaded.copy()
        self.view_df = self.df.copy()
        self.current_view_name = "Dataset preview"
        self.status.configure(text="● Dataset loaded", fg=TEAL)
        self.overview_note.configure(text=f"Loaded: {path}", fg=TEAL)
        self._update_metrics()
        self._render_table()
        self.inspect_nulls()
        self._navigate("overview")

    def _update_metrics(self):
        if self.df is None:
            vals = {"rows": "—", "cols": "—", "missing": "—", "makes": "—"}
        else:
            vals = {"rows": f"{len(self.df):,}", "cols": str(len(self.df.columns)),
                    "missing": f"{int(self.df.isna().sum().sum()):,}",
                    "makes": str(self.df["Make"].nunique()) if "Make" in self.df else "—"}
        for key, val in vals.items():
            if key in self.metric_labels:
                self.metric_labels[key].configure(text=val)

    def _set_view(self, data, name):
        self.view_df = data.copy()
        self.current_view_name = name
        self._render_table()
        self.table_info.configure(text=f"{name}  •  {len(data):,} rows shown")
        self._navigate("dataset")

    def _render_table(self):
        if not hasattr(self, "tree"):
            return
        for child in self.table_frame.winfo_children():
            child.destroy()
        if self.view_df is None:
            tk.Label(self.table_frame, text="Load a CSV dataset to see records here.",
                     bg=PANEL, fg=MUTED).pack(padx=30, pady=40)
            self.tree = None
            return
        data = self.view_df
        term = self.search_var.get().strip().lower() if hasattr(self, "search_var") else ""
        if term:
            mask = data.astype(str).apply(lambda col: col.str.lower().str.contains(term, na=False)).any(axis=1)
            data = data[mask]
        wrap = tk.Frame(self.table_frame, bg=PANEL)
        wrap.pack(fill="both", expand=True)
        yscroll = ttk.Scrollbar(wrap, orient="vertical")
        xscroll = ttk.Scrollbar(wrap, orient="horizontal")
        tree = ttk.Treeview(wrap, columns=list(data.columns), show="headings",
                            yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        yscroll.config(command=tree.yview)
        xscroll.config(command=tree.xview)
        for col in data.columns:
            tree.heading(col, text=str(col))
            tree.column(col, width=max(100, min(170, len(str(col))*12)), minwidth=80, anchor="w")
        # Limit rendered rows for responsive GUI; export still exports the full current view.
        for idx, row in data.head(2000).iterrows():
            values = ["" if pd.isna(v) else str(v) for v in row.tolist()]
            tree.insert("", "end", values=values)
        tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        wrap.rowconfigure(0, weight=1)
        wrap.columnconfigure(0, weight=1)
        self.tree = tree
        if hasattr(self, "table_info"):
            extra = " (first 2,000 rows rendered)" if len(data) > 2000 else ""
            self.table_info.configure(text=f"{self.current_view_name} • {len(data):,} rows{extra}")

    def reset_view(self):
        if not self._require_data():
            return
        self.view_df = self.df.copy()
        self.current_view_name = "Current dataset"
        self.search_var.set("")
        self._render_table()

    def export_csv(self):
        if self.view_df is None:
            messagebox.showwarning("No data", "Load a dataset first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                    filetypes=[("CSV files", "*.csv")], initialfile="cars_analysis_export.csv")
        if path:
            try:
                self.view_df.to_csv(path, index=False)
                messagebox.showinfo("Export complete", f"Saved {len(self.view_df):,} rows to:\n{path}")
            except Exception as exc:
                messagebox.showerror("Export failed", str(exc))

    def inspect_nulls(self):
        if not self._require_data():
            return
        counts = self.df.isnull().sum()
        self.null_text.delete("1.0", "end")
        self.null_text.insert("1.0", f"Dataset shape: {self.df.shape[0]} rows × {self.df.shape[1]} columns\n")
        self.null_text.insert("end", f"Total missing cells: {int(counts.sum())}\n\n")
        self.null_text.insert("end", counts.to_string())
        self.null_text.insert("end", "\n\nNote: the original notebook fills missing values in Cylinders with the mean of Cylinders.")
        self._update_metrics()

    def fill_cylinders(self):
        if not self._require_data():
            return
        if "Cylinders" not in self.df:
            messagebox.showerror("Missing column", "The dataset does not contain a 'Cylinders' column.")
            return
        numeric = pd.to_numeric(self.df["Cylinders"], errors="coerce")
        mean_value = numeric.mean()
        self.df["Cylinders"] = numeric.fillna(mean_value)
        self.view_df = self.df.copy()
        self.current_view_name = "After filling Cylinders"
        self.inspect_nulls()
        self._update_metrics()
        self._render_table()
        messagebox.showinfo("Cleaning complete", f"Missing Cylinders values filled with mean: {mean_value:.2f}")

    def remove_heavy(self):
        if not self._require_data():
            return
        if "Weight" not in self.df:
            messagebox.showerror("Missing column", "The dataset does not contain a 'Weight' column.")
            return
        before = len(self.df)
        weight = pd.to_numeric(self.df["Weight"], errors="coerce")
        self.df = self.df.loc[~(weight > 4000)].copy()
        removed = before - len(self.df)
        self.view_df = self.df.copy()
        self.current_view_name = "Weight ≤ 4000"
        self._update_metrics()
        self._set_view(self.view_df, self.current_view_name)
        messagebox.showinfo("Filter applied", f"Removed {removed:,} records where Weight > 4000.")

    def increase_mpg(self):
        if not self._require_data():
            return
        if "MPG_City" not in self.df:
            messagebox.showerror("Missing column", "The dataset does not contain an 'MPG_City' column.")
            return
        self.df["MPG_City"] = pd.to_numeric(self.df["MPG_City"], errors="coerce") + 3
        self.view_df = self.df.copy()
        self.current_view_name = "MPG_City increased by 3"
        self._update_metrics()
        self._set_view(self.view_df, self.current_view_name)
        messagebox.showinfo("Transformation complete", "Added 3 to every numeric value in MPG_City.")

    def filter_asia_europe(self):
        if not self._require_data():
            return
        if "Origin" not in self.df:
            messagebox.showerror("Missing column", "The dataset does not contain an 'Origin' column.")
            return
        result = self.df[self.df["Origin"].isin(["Asia", "Europe"])]
        self._set_view(result, "Origin: Asia or Europe")
        self._show_result("Cars from Asia or Europe", result.head(100).to_string(index=False),
                          f"Matching records: {len(result):,}\n\nShowing up to the first 100 rows below:\n\n")

    def filter_horsepower(self):
        if not self._require_data():
            return
        if "Horsepower" not in self.df:
            messagebox.showerror("Missing column", "The dataset does not contain a 'Horsepower' column.")
            return
        hp = pd.to_numeric(self.df["Horsepower"], errors="coerce")
        result = self.df[hp > 200]
        self._set_view(result, "Horsepower > 200")
        self._show_result("Cars with Horsepower > 200", result.head(100).to_string(index=False),
                          f"Matching records: {len(result):,}\n\nShowing up to the first 100 rows below:\n\n")

    def make_counts(self):
        if not self._require_data():
            return
        if "Make" not in self.df:
            messagebox.showerror("Missing column", "The dataset does not contain a 'Make' column.")
            return
        counts = self.df["Make"].value_counts(dropna=False)
        self._show_result("Make value counts", counts.to_string(),
                          f"Unique Make values: {self.df['Make'].nunique()}\n\n")

    def origin_counts(self):
        if not self._require_data():
            return
        if "Origin" not in self.df:
            messagebox.showerror("Missing column", "The dataset does not contain an 'Origin' column.")
            return
        counts = self.df["Origin"].value_counts(dropna=False)
        self._show_result("Origin value counts", counts.to_string(),
                          f"Origin categories: {self.df['Origin'].nunique()}\n\n")

    def _show_result(self, title, content, prefix=""):
        self.analysis_title.configure(text=title)
        self.analysis_text.delete("1.0", "end")
        self.analysis_text.insert("1.0", prefix + content)
        self._navigate("analysis")


def main():
    root = tk.Tk()
    app = CarsAnalysisApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
