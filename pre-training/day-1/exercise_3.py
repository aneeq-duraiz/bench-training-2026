# Prompt user until a valid number between 1 and 12 is entered
chosen = None
while chosen is None:
    raw = input("Pick a number from 1 to 12: ").strip()
    if raw.isdigit() and 1 <= int(raw) <= 12:
        chosen = int(raw)
    else:
        print("That's not valid — try again.")


def show_times_table(num):
    """Print the multiplication table for a given number."""
    col_width = len(str(num * 12))
    for multiplier in range(1, 13):
        product = num * multiplier
        print(f"{num:>2} x {multiplier:>2} = {product:>{col_width}}")


# Show the table for the chosen number
show_times_table(chosen)
print()

# Show all tables from 1 to 12
for n in range(1, 13):
    show_times_table(n)
    if n < 12:
        print()

