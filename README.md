# Topsis-Samiksha-102317096

A Python package implementing TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) for multi-criteria decision analysis.

## What is TOPSIS?

TOPSIS is a multi-criteria decision analysis method that identifies the best alternative based on the shortest distance from the ideal solution and the farthest distance from the negative-ideal solution.

## Installation
```bash
pip install Topsis-Samiksha-102317096
```

## Usage

### Command Line
```bash
topsis <InputDataFile> <Weights> <Impacts> <ResultFileName>
```

### Example
```bash
topsis input.csv "1,1,1,2" "+,+,-,+" result.csv
```

### Python Script
```python
from topsis_samiksha_102317096 import apply_topsis, validate_input
import pandas as pd

# Your implementation here
```

## Input File Format

- CSV file with 3 or more columns
- First column: Object/Variable names (e.g., M1, M2, M3...)
- Remaining columns: Numeric values only

Example:
```
Model,Price,Storage,Camera,Looks
M1,250,16,12,5
M2,200,16,8,3
M3,300,32,16,4
```

## Parameters

- **Weights**: Comma-separated numbers (e.g., "1,1,1,2")
- **Impacts**: Comma-separated +/- signs (e.g., "+,+,-,+")
  - `+` : Benefit criterion (higher is better)
  - `-` : Cost criterion (lower is better)

## Output

The result file contains all input columns plus:
- **Topsis Score**: Calculated score for each alternative
- **Rank**: Ranking based on Topsis score

## Error Handling

The package handles:
- File not found errors
- Invalid number of parameters
- Non-numeric values in data columns
- Mismatched weights/impacts count
- Invalid impact values

## Author

**Samiksha**  
Roll Number: 102317096

