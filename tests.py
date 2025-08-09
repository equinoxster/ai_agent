#!/usr/bin/env python3

import sys
import os

# Add the calculator directory to the Python path so we can import the function
sys.path.append(os.path.join(os.path.dirname(__file__), 'calculator'))

from functions.write_file import write_file
from functions.run_python_file import run_python_file

def main():
    print("Testing write_file function:")
    print("=" * 60)
    
    # Test 1: Write to existing lorem.txt file
    print('Test 1: write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum")')
    result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result1)
    print()
    
    # Test 2: Write to new file in pkg directory
    print('Test 2: write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")')
    result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result2)
    print()
    
    # Test 3: Try to write outside working directory (should return error)
    print('Test 3: write_file("calculator", "/tmp/temp.txt", "this should not be allowed")')
    result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result3)
    print()

    

    print('Test 1: calculator/main.py (usage instructions)')
    print(run_python_file("calculator", "main.py"))

    print('\nTest 2: calculator/main.py with args ["3 + 5"]')
    print(run_python_file("calculator", "main.py", ["3 + 5"]))

    print('\nTest 3: calculator/tests.py')
    print(run_python_file("calculator", "tests.py"))

    print('\nTest 4: calculator/../main.py (should error)')
    print(run_python_file("calculator", "../main.py"))

    print('\nTest 5: calculator/nonexistent.py (should error)')
    print(run_python_file("calculator", "nonexistent.py"))

if __name__ == "__main__":
    main()
