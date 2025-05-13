Letter Anagram Solver
Overview
The Letter Anagram Solver is a Python-based application designed to generate all valid words from a set of scrambled input letters. The project implements three distinct algorithms to solve the problem: Brute Force Permutation, Backtracking Search, and Trie-based Search. Each algorithm is integrated with its own GUI for independent testing, along with a comparison GUI that visually compares their performance.
The solver supports grouped word outputs by length and is optimized for performance with threading to ensure GUI responsiveness.

Features
Three independent algorithms:


Brute Force Permutation


Backtracking Search


Trie-based Search


GUI interfaces for:


Individual algorithm testing


Performance comparison with visual charts


Grouped word outputs (2-letter words, 3-letter words, etc.)


Progress updates displayed in the GUI


Visual performance comparisons (execution time and words found)



Project Structure
letter_anagram_solver/
│
├── data/
│   └── english_words.txt           # Word dictionary
│
├── algorithms/
│   ├── brute_force.py              # Brute Force algorithm
│   ├── backtracking.py             # Backtracking algorithm
│   └── trie_based.py               # Trie-based algorithm
│
├── gui_brute_force.py              # GUI for Brute Force testing
├── gui_backtracking.py             # GUI for Backtracking testing
├── gui_trie_based.py               # GUI for Trie-based testing
├── gui_comparison.py               # GUI for algorithm comparison (charts)
└── README.md                       # Project overview


Setup
Clone the repository (or download the project folder).


Create a virtual environment (optional but recommended):


python -m venv venv
source venv/bin/activate  # On Linux/Mac
.\venv\Scripts\activate  # On Windows

Install dependencies:


pip install matplotlib

Ensure english_words.txt is in the data/ directory.



Running the Application
Brute Force GUI:


python gui_brute_force.py

Backtracking GUI:


python gui_backtracking.py

Trie-based GUI:


python gui_trie_based.py

Comparison GUI (with charts):


python gui_comparison.py


Algorithm Details
Brute Force: Generates all permutations and checks each against the dictionary. Suitable for up to 7-letter inputs.


Backtracking: Recursively builds words, pruning invalid paths early. Suitable for up to 9-letter inputs.


Trie-based: Uses a Trie structure for efficient prefix pruning. Suitable for up to 12-letter inputs.


All GUIs provide progress updates and grouped word outputs. The comparison GUI displays visual charts for execution time and word count across the algorithms.

Hardware Used for Testing
Device: Lenovo IdeaPad Slim 3 15AMN8


Processor: AMD Ryzen 5 7520U with Radeon Graphics


RAM: 16 GB


Performance metrics and scalability recommendations are based on this hardware configuration.

License
This project is for educational purposes and is provided as-is without warranty.

Acknowledgments
Dictionary Source: DWYL English Words List


Libraries used: tkinter, matplotlib



