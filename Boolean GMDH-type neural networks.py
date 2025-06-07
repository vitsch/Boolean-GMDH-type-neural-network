#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python implemetation of Boolean GMDH-type neural network. The implementation includes ablation study of a test. 
"""

import numpy as np
from itertools import product
import copy

def initialize_empty_network():
    return {
        'Z': [],      # Outputs of each unit [unit_index][sample_index]
        'I12': [],    # Input connections [unit_index] = [input1_idx, input2_idx]
        'LF': [],     # Logical function index for each unit
        'E': [],      # Classification error for each unit
        'C': []       # Complexity level of each unit
    }

def define_logical_functions():
    return [
        lambda x, y: x and y,           # AND
        lambda x, y: x or y,            # OR
        lambda x, y: x != y,            # XOR
        lambda x, y: not (x and y),     # NAND
        lambda x, y: not (x or y),      # NOR
        lambda x, y: x == y,            # XNOR
        lambda x, y: x and not y,       # AND NOT
        lambda x, y: not x and y,       # NOT AND
        lambda x, y: not x or y,        # IMPLICATION
        lambda x, y: (x and y) or (not x and not y)  # EQUIVALENCE
    ]

def get_function_name(func_idx):
    """Return symbolic name for logical function index."""
    function_names = [
        'AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR',
        'AND NOT', 'NOT AND', 'IMPLICATION', 'EQUIVALENCE'
    ]
    return function_names[func_idx] if func_idx >= 0 else 'INPUT'

def generate_binary_combinations(m):
    """Generate all possible binary combinations for m attributes."""
    return np.array(list(product([0, 1], repeat=m)), dtype=int)

def generate_target_function(X):
    """Generate target values: (X1 AND X2) XOR X3."""
    #return ((X[:, 0] & X[:, 1]) ^ X[:, 2]).reshape(-1, 1)
    return ((X[:, 0] & X[:, 1]) | (X[:, 2] ^ X[:, 3])).reshape(-1, 1)
    #return ((X[:, 0] & X[:, 1]) & (X[:, 2] | X[:, 3])).reshape(-1, 1)  # ??

def get_input_complexities(complexity):
    if complexity == 1:
        return [0], [0]
    elif complexity == 2:
        return [0], [1]
    elif complexity == 3:
        return [0, 1], [2, 1]
    elif complexity == 4:
        return [0, 1], [3, 2]
    elif complexity == 5:
        return [0, 1, 2], [4, 3, 2]
    else:
        raise ValueError("Invalid complexity level")


def get_units_by_complexity(S, complexity_list):
    return [i for i, c in enumerate(S['C']) if c == complexity_list] #02/06

def compute_unit_output(U1, U2, func_idx, logical_functions):
    if len(U1) != len(U2):
        raise ValueError("Input arrays must have equal length")
    
    selected_function = logical_functions[func_idx]
    return [int(selected_function(bool(u1), bool(u2))) for u1, u2 in zip(U1, U2)]

def find_best_functions(U1, U2, T, logical_functions):
    if len(U1) != len(U2) or len(U1) != len(T):
        raise ValueError("Input and target arrays must have equal length")
        
    min_error = float('inf')
    best_functions = []
    
    for func_idx, func in enumerate(logical_functions):
        predictions = [int(func(bool(u1), bool(u2))) for u1, u2 in zip(U1, U2)]
        error = sum(abs(pred - t) for pred, t in zip(predictions, T.flatten()))
        
        if error < min_error:
            min_error = error
            best_functions = [func_idx]
        elif error == min_error:
            best_functions.append(func_idx)
    
    return best_functions, min_error

def build_complexity_level(S, T, complexity, logical_functions):
    # if not S or not T:
    #     raise ValueError("Network and target cannot be empty")
        
    input_complexities = get_input_complexities(complexity)
    C1, C2 = input_complexities
    
    new_units = initialize_empty_network()

    for k in range(len(C1)):  
        I1 = get_units_by_complexity(S, C1[k])
        I2 = get_units_by_complexity(S, C2[k])
        
        
        for i1 in I1:
            for i2 in I2:
                if i1 != i2:  # Avoid self-connections
                    U1 = S['Z'][i1]
                    U2 = S['Z'][i2]
                    
                    best_functions, min_error = find_best_functions(U1, U2, T, logical_functions)
                    
                    for func_idx in best_functions:
                        output = compute_unit_output(U1, U2, func_idx, logical_functions)
                        
                        new_units['Z'].append(output)
                        new_units['I12'].append([i1, i2])
                        new_units['LF'].append(func_idx)
                        new_units['E'].append(min_error)
                        new_units['C'].append(complexity)
    
    return new_units

def merge_units_into_network(main_network, new_units):
    for key in ['Z', 'I12', 'LF', 'E', 'C']:
        main_network[key].extend(new_units[key])

def build_network(X, T, C_MAX, logical_functions=None):
    if X.shape[0] != T.shape[0]:
        raise ValueError("Number of samples in X and T must match")
    
    if logical_functions is None:
        logical_functions = define_logical_functions()
    
    S = initialize_empty_network()
    
    # Add input attributes as complexity 0 units
    X_transposed = X.T
    for i in range(X_transposed.shape[0]):
        S['Z'].append(list(X_transposed[i]))
        S['I12'].append([])
        S['LF'].append(-1)
        S['E'].append(0)
        S['C'].append(0)
    
    # Build units of increasing complexity
    for complexity in range(1, C_MAX + 1):
        new_units = build_complexity_level(S, T, complexity, logical_functions)
        merge_units_into_network(S, new_units)
        if np.min(new_units['E']) == 0:       # 02/06
            break
    
    return S

def print_symbolic_rules(network):
    """Print symbolic rules for units with zero error."""
    print("\nSymbolic Rules for Zero-Error Units:")
    
    def build_rule(unit_idx, network, depth=0):
        """Recursively build symbolic rule for a unit."""
        if unit_idx < 0:
            return None
            
        inputs = network['I12'][unit_idx]
        func_idx = network['LF'][unit_idx]
        complexity = network['C'][unit_idx]
        
        # Base case: input attribute
        if complexity == 0:
            return f"X{unit_idx + 1}"
        
        # Get input unit representations
        input1_rule = build_rule(inputs[0], network, depth + 1) if inputs else None
        input2_rule = build_rule(inputs[1], network, depth + 1) if inputs else None
        
        if not input1_rule or not input2_rule:
            return None
            
        # Get function name
        func_name = get_function_name(func_idx)
        
        # Build rule string with proper parentheses for complex inputs
        if depth > 0 and complexity > 1:
            return f"({input1_rule} {func_name} {input2_rule})"
        return f"{input1_rule} {func_name} {input2_rule}"

    # Find and print rules for zero-error units
    zero_error_units = [i for i, e in enumerate(network['E']) if e == 0 and network['C'][i] > 0]
    
    if not zero_error_units:
        print("No zero-error units found.")
        return
        
    for idx in zero_error_units:
        rule = build_rule(idx, network)
        if rule:
            print(f"Unit {idx} (Complexity {network['C'][idx]}): {rule}")

def perform_ablation_study(X, T, C_MAX):
    """Perform ablation study by building networks with one logical function omitted."""
    all_functions = define_logical_functions()
    function_names = get_function_name(-1)  # Get all function names
    function_names = function_names[1:] if isinstance(function_names, list) else ['AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR', 'AND NOT', 'NOT AND', 'IMPLICATION', 'EQUIVALENCE']
    
    # Build baseline network
    print("\n=== Baseline Network (All Functions) ===")
    baseline_network = build_network(X, T, C_MAX)
    baseline_zero_error_units = [i for i, e in enumerate(baseline_network['E']) if e == 0 and baseline_network['C'][i] > 0]
    baseline_complexities = [baseline_network['C'][i] for i in baseline_zero_error_units]
    min_error = min(baseline_network['E']) if baseline_network['E'] else float('inf')
    
    print(f"Number of zero-error units: {len(baseline_zero_error_units)}")
    print(f"Complexities of zero-error units: {baseline_complexities}")
    print(f"Minimum error: {min_error}")
    print_symbolic_rules(baseline_network)
    
    # Perform ablation for each logical function
    results = []
    for i in range(len(all_functions)):
        # Create function list excluding the i-th function
        ablated_functions = all_functions[:i] + all_functions[i+1:]
        
        print(f"\n=== Ablation: Excluding {function_names[i]} ===")
        network = build_network(X, T, C_MAX, logical_functions=ablated_functions)
        zero_error_units = [j for j, e in enumerate(network['E']) if e == 0 and network['C'][j] > 0]
        complexities = [network['C'][j] for j in zero_error_units]
        min_error = min(network['E']) if network['E'] else float('inf')
        
        print(f"Number of zero-error units: {len(zero_error_units)}")
        print(f"Complexities of zero-error units: {complexities}")
        print(f"Minimum error: {min_error}")
        print_symbolic_rules(network)
        
        results.append({
            'excluded_function': function_names[i],
            'zero_error_units': len(zero_error_units),
            'complexities': complexities,
            'min_error': min_error
        })
    
    # Print summary
    print("\n=== Ablation Study Summary ===")
    print(f"Baseline: {len(baseline_zero_error_units)} zero-error units, complexities: {baseline_complexities}, min error: {min(baseline_network['E'])}")
    for result in results:
        print(f"Excluding {result['excluded_function']}: {result['zero_error_units']} zero-error units, complexities: {result['complexities']}, min error: {result['min_error']}")

def main():
    # Generate input data
    m = 4
    X = generate_binary_combinations(m)
    T = generate_target_function(X)
    
    # Perform ablation study
    C_MAX = 3
    perform_ablation_study(X, T, C_MAX)

if __name__ == "__main__":
    main()
