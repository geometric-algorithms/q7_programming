# q7_programming

This project implements two different versions of a **2D Range Tree** for efficient 2D range queries over a set of points:

- **A**: Standard 2D Range Tree with simple associated structures.
- **B**: Optimized 2D Range Tree with improved associated structures for faster queries.

A comparison script is also included to benchmark both versions.

---

## 📂 Directory Structure

```
.
├── A/
│   ├── A.py           # Implementation of Version A
│   ├── __init__.py
│   └── __pycache__/
├── B/
│   ├── B.py           # Implementation of Version B
│   ├── __init__.py
│   └── __pycache__/
├── compare.py         # Benchmark and compare Version A and B
├── final_project.pdf  # Project report/documentation
├── input.txt          # Input file (see below)
├── README.md          # You are here
└── run.sh             # Script to easily run the project
```

---

## 🛠 Requirements

- Python 3.10+ (Recommended: Python 3.12)
- Required Python packages:
  - `matplotlib`

You can install missing packages with:

```bash
pip install matplotlib
```

---

## 🚀 How to Run

First, make sure you give execute permissions to the `run.sh` script (only once):

```bash
chmod +x run.sh
```

Then you can run:

| Task                          | Command       | What it does                               |
| ----------------------------- | ------------- | ------------------------------------------ |
| Run Version A                 | `./run.sh -a` | Launch Version A (simple 2D range tree)    |
| Run Version B                 | `./run.sh -b` | Launch Version B (optimized 2D range tree) |
| Compare A vs B (benchmarking) | `./run.sh -c` | Compare preprocessing and query times      |

---

## 📥 Input Points

- If **`input.txt`** exists, the programs will **read points from it**.

  - Format: Each line should contain two numbers (x and y coordinates), **space-separated**.

    Example:

    ```
    10.5 23.1
    -5.2 17.8
    34.0 -10.0
    ```

- If **`input.txt` is missing**, **1000 random points** will be generated automatically.

---

## 📦 Querying

When running Version A or B:

- You will be **prompted** to input four numbers:

  ```
  xmin xmax ymin ymax
  ```

  (representing the lower and upper bounds of a query rectangle).

- If your input is invalid, a **random query rectangle** will be used instead.

- The result will be **visualized**:
  - All points in light grey
  - Queried points (inside the rectangle) in red
  - Query rectangle shown with a blue dashed line.

---

## 📈 Comparison (Benchmark)

Running `./run.sh -c` will:

- Generate point sets of various sizes (100 → 50,000 points).
- Measure and plot:
  - **Preprocessing time**
  - **Query time**
- Log if the outputs from A and B **match** for correctness.
- Show a **log-log plot** comparing times for both implementations.

---

## ⚠️ Notes

- Make sure **`A/`** and **`B/`** directories are not renamed.
- If you edit `A.py` or `B.py`, make sure you keep the function names `preprocess` and `query` unchanged, or the comparison script will fail.
- If you encounter display errors with matplotlib, ensure you are using an environment that supports GUI windows, or switch the backend in the code (e.g., to `Agg` for non-GUI).

---

## 🧠 Quick Summary

| Component  | Description                                  |
| ---------- | -------------------------------------------- |
| Version A  | Baseline 2D Range Tree                       |
| Version B  | Faster, optimized 2D Range Tree              |
| compare.py | Tests speed and correctness of both versions |
| run.sh     | Easy-to-use launcher script                  |
| input.txt  | Input points file                            |

---
