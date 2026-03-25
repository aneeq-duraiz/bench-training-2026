def average(scores):
    """Return the mean of a list of scores."""
    return sum(scores) / len(scores)


def letter_grade(avg):
    """Map a numeric average to a letter grade."""
    if avg >= 90:
        return "A"
    if avg >= 80:
        return "B"
    if avg >= 70:
        return "C"
    if avg >= 60:
        return "D"
    return "F"


def find_top_student(students):
    """Return the student dict with the highest average score."""
    top = None
    top_avg = None
    for student in students:
        avg = average(student["scores"])
        if top_avg is None or avg > top_avg:
            top_avg = avg
            top = student
    return top


students = [
    {"name": "Sara",  "scores": [85, 90, 88]},
    {"name": "Ali",   "scores": [60, 55, 62]},
    {"name": "Zara",  "scores": [92, 95, 91]},
    {"name": "Omar",  "scores": [75, 78, 80]},
    {"name": "Nadia", "scores": [50, 58, 53]},
]

top_student = find_top_student(students)
ranked = sorted(students, key=lambda s: average(s["scores"]), reverse=True)

print(f"{'Name':<6} | {'Avg':>5} | Grade")
print("-" * 22)
for s in ranked:
    avg = average(s["scores"])
    grade = letter_grade(avg)
    row = f"{s['name']:<6} | {avg:>5.1f} | {grade}"
    if s is top_student:
        row += "  <-- top"
    print(row)

