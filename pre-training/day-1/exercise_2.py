def get_result(marks):
    """Return grade label based on marks achieved."""
    if marks >= 90:
        grade = "Distinction"
    elif marks >= 60:
        grade = "Pass"
    else:
        grade = "Fail"
    return grade


# Boundary / edge-case checks
boundary_cases = [0, 59, 60, 89, 90]
print("--- Boundary Tests ---")
for marks in boundary_cases:
    print(f"{marks} -> {get_result(marks)}")

# Sample student scores
print("\n--- Student Scores ---")
student_scores = [45, 72, 91, 60, 38, 85]
for marks in student_scores:
    print(f"{marks} -> {get_result(marks)}")

