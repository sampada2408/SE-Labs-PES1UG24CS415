\# Lab 5: Static Code Analysis

\## Issue Identification and Resolution Report



\*\*Project:\*\* Flight Reservation System  

\*\*Tools Used:\*\* Pylint, Bandit, Flake8  

\*\*Language:\*\* Python



\### 1. Identified Issues and Fixes



| No. | Issue | Tool | Severity/Type | Fix Applied |

|---|---|---|---|---|

| 1 | Mutable default argument (`baggage\_tags=\[]`) | Pylint | Warning | Changed default to `None` and initialized an empty list inside the function. |

| 2 | Use of `eval()` | Bandit / Pylint | Medium | Replaced unsafe expression evaluation with direct numeric surcharge calculation. |

| 3 | MD5 hashing algorithm | Bandit | High | Replaced MD5 with SHA-256 using hashlib. |

| 4 | Insecure random PIN generation | Bandit | Low | Replaced random.randint() with secrets.randbelow(). |

| 5 | Shell command execution using os.system() | Bandit | High | Removed shell execution and used Python file operations. |

| 6 | Hardcoded API secret | Bandit | Low | Replaced hardcoded secret with an environment variable. |

| 7 | Bare except statement | Pylint / Flake8 / Bandit | Code quality | Removed broad exception handling and added explicit validation. |

| 8 | Unused math import | Pylint / Flake8 | Code quality | Removed the unused import. |

| 9 | Function names not following snake\_case | Pylint | Style | Renamed functions using snake\_case naming conventions. |

| 10 | Missing module and function docstrings | Pylint | Style | Added descriptive docstrings. |

| 11 | Line too long | Pylint / Flake8 | Formatting | Split long statements into multiple lines. |

| 12 | Missing final newline | Pylint / Flake8 | Formatting | Added a newline at the end of the file. |

| 13 | Unused local variables | Pylint / Flake8 | Code quality | Removed unnecessary variables. |

| 14 | File opened without encoding | Pylint | Warning | Used UTF-8 encoding when writing the manifest. |

| 15 | Global variable modification | Pylint | Warning | Replaced the global revenue variable with a mutable dictionary. |



\### 2. Security Improvements



\- Replaced unsafe `eval()` with direct mathematical calculations.

\- Used SHA-256 instead of the weak MD5 hashing algorithm.

\- Used the `secrets` module for secure boarding PIN generation.

\- Removed unsafe shell command execution.

\- Moved the API secret to an environment variable.

\- Used safer file handling with UTF-8 encoding.



\### 3. Code Quality Improvements



\- Followed Python naming conventions.

\- Added module and function docstrings.

\- Removed unused imports and variables.

\- Fixed formatting and indentation issues.

\- Replaced mutable default arguments.

\- Improved exception handling and input validation.



\### 4. Verification



The modified program was checked using:



1\. Pylint

2\. Bandit

3\. Flake8



The tools were run again after making the corrections to verify improvements in code quality, security, and formatting.



\### 5. Conclusion



Static code analysis helped identify security vulnerabilities, programming mistakes, and coding style violations in the Flight Reservation System. By fixing the identified issues, the program became more secure, readable, maintainable, and reliable.

