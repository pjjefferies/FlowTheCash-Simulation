python -m coverage run -m pytest

python -m coverage report -m > coverage_report.txt

"C:\Program Files\Sublime Text 3\sublime_text.exe" coverage_report.txt