# Neural Network Ablation Study Results

## Baseline Network (All Functions)

- **Number of zero-error units:** 8
- **Complexities of zero-error units:** [3, 3, 3, 3, 3, 3, 3, 3]
- **Minimum error:** 0

### Symbolic Rules for Zero-Error Units

| Unit ID | Complexity | Rule |
|---------|------------|------|
| 4589 | 3 | X1 AND X2 OR X3 XOR X4 |
| 4610 | 3 | X1 AND X2 OR X4 XOR X3 |
| 5310 | 3 | X2 AND X1 OR X3 XOR X4 |
| 5331 | 3 | X2 AND X1 OR X4 XOR X3 |
| 6306 | 3 | X3 XOR X4 OR X1 AND X2 |
| 6317 | 3 | X3 XOR X4 OR X2 AND X1 |
| 6706 | 3 | X4 XOR X3 OR X1 AND X2 |
| 6717 | 3 | X4 XOR X3 OR X2 AND X1 |

## Ablation Results by Excluded Function

### Excluding AND
- **Number of zero-error units:** 0
- **Complexities:** []
- **Minimum error:** 0
- **Result:** No zero-error units found

### Excluding OR
- **Number of zero-error units:** 0
- **Complexities:** []
- **Minimum error:** 0
- **Result:** No zero-error units found

### Excluding XOR
- **Number of zero-error units:** 0
- **Complexities:** []
- **Minimum error:** 0
- **Result:** No zero-error units found

### Excluding NAND
- **Number of zero-error units:** 8
- **Complexities:** [3, 3, 3, 3, 3, 3, 3, 3]
- **Minimum error:** 0

**Symbolic Rules:**
| Unit ID | Rule |
|---------|------|
| 4589 | X1 AND X2 OR X3 XOR X4 |
| 4610 | X1 AND X2 OR X4 XOR X3 |
| 5310 | X2 AND X1 OR X3 XOR X4 |
| 5331 | X2 AND X1 OR X4 XOR X3 |
| 6306 | X3 XOR X4 OR X1 AND X2 |
| 6317 | X3 XOR X4 OR X2 AND X1 |
| 6706 | X4 XOR X3 OR X1 AND X2 |
| 6717 | X4 XOR X3 OR X2 AND X1 |

### Excluding NOR
- **Number of zero-error units:** 8
- **Complexities:** [3, 3, 3, 3, 3, 3, 3, 3]
- **Minimum error:** 0

**Symbolic Rules:** *(Same as NAND exclusion)*

### Excluding XNOR
- **Number of zero-error units:** 8
- **Complexities:** [3, 3, 3, 3, 3, 3, 3, 3]
- **Minimum error:** 0

**Symbolic Rules:**
| Unit ID | Rule |
|---------|------|
| 3054 | X1 AND X2 OR X3 XOR X4 |
| 3071 | X1 AND X2 OR X4 XOR X3 |
| 3502 | X2 AND X1 OR X3 XOR X4 |
| 3519 | X2 AND X1 OR X4 XOR X3 |
| 4146 | X3 XOR X4 OR X1 AND X2 |
| 4156 | X3 XOR X4 OR X2 AND X1 |
| 4440 | X4 XOR X3 OR X1 AND X2 |
| 4450 | X4 XOR X3 OR X2 AND X1 |

### Excluding AND NOT
- **Number of zero-error units:** 8
- **Complexities:** [3, 3, 3, 3, 3, 3, 3, 3]
- **Minimum error:** 0

**Symbolic Rules:** *(Same as baseline)*

### Excluding NOT AND
- **Number of zero-error units:** 8
- **Complexities:** [3, 3, 3, 3, 3, 3, 3, 3]
- **Minimum error:** 0

**Symbolic Rules:** *(Same as baseline)*

### Excluding IMPLICATION
- **Number of zero-error units:** 8
- **Complexities:** [3, 3, 3, 3, 3, 3, 3, 3]
- **Minimum error:** 0

**Symbolic Rules:**
| Unit ID | Rule |
|---------|------|
| 1942 | X1 AND X2 OR X3 XOR X4 |
| 1951 | X1 AND X2 OR X4 XOR X3 |
| 2296 | X2 AND X1 OR X3 XOR X4 |
| 2305 | X2 AND X1 OR X4 XOR X3 |
| 2702 | X3 XOR X4 OR X1 AND X2 |
| 2711 | X3 XOR X4 OR X2 AND X1 |
| 2834 | X4 XOR X3 OR X1 AND X2 |
| 2843 | X4 XOR X3 OR X2 AND X1 |

### Excluding EQUIVALENCE
- **Number of zero-error units:** 8
- **Complexities:** [3, 3, 3, 3, 3, 3, 3, 3]
- **Minimum error:** 0

**Symbolic Rules:** *(Same as XNOR exclusion)*

## Summary

| Excluded Function | Zero-Error Units | Complexities | Min Error |
|-------------------|------------------|--------------|-----------|
| **Baseline** | 8 | [3, 3, 3, 3, 3, 3, 3, 3] | 0 |
| AND | 0 | [] | 0 |
| OR | 0 | [] | 0 |
| XOR | 0 | [] | 0 |
| NAND | 8 | [3, 3, 3, 3, 3, 3, 3, 3] | 0 |
| NOR | 8 | [3, 3, 3, 3, 3, 3, 3, 3] | 0 |
| XNOR | 8 | [3, 3, 3, 3, 3, 3, 3, 3] | 0 |
| AND NOT | 8 | [3, 3, 3, 3, 3, 3, 3, 3] | 0 |
| NOT AND | 8 | [3, 3, 3, 3, 3, 3, 3, 3] | 0 |
| IMPLICATION | 8 | [3, 3, 3, 3, 3, 3, 3, 3] | 0 |
| EQUIVALENCE | 8 | [3, 3, 3, 3, 3, 3, 3, 3] | 0 |

## Key Findings

- **Critical Functions:** AND, OR, and XOR are essential - removing any of them eliminates all zero-error units
- **Non-Critical Functions:** NAND, NOR, XNOR, AND NOT, NOT AND, IMPLICATION, and EQUIVALENCE can be removed without affecting performance
- **Consistent Pattern:** All zero-error units follow the same logical structure: `(X1 AND X2) OR (X3 XOR X4)` or its permutations
- **Complexity:** All successful units maintain complexity level 3
