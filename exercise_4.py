"""
Exercise 4: Name Formatting with Initials
Format full name: capitalize first name, use initials for last name and middle names
"""


def format_name(full_name):
    """
    Format full name according to the rules:
    - Remove extra spaces (beginning, end, middle)
    - First name: capitalize first letter, rest lowercase
    - Last name and middle names: take first character, uppercase

    Format: FirstNameLMN (where L, M, N are initials)

    Examples:
    " le thi Be Nho " -> "NhoLTB"
    " nguyen mat tROi " -> "TroiNM"
    """
    # Remove leading/trailing spaces and multiple spaces in between
    name = ' '.join(full_name.split())

    if not name:
        return None, "Empty name!"

    # Split into words
    words = name.split()

    if len(words) < 2:
        return None, "Name must have at least 2 words (last name and first name)!"

    # The last word is the first name
    first_name = words[-1].capitalize()

    # The remaining words are last name and middle names
    initials = ''.join(word[0].upper() for word in words[:-1])

    # Combine: FirstName + Initials
    formatted_name = first_name + initials

    return formatted_name, None


def main():
    """Main function to run the program"""
    print("=== Name Formatter ===\n")

    full_name = input("Enter full name: ")

    formatted_name, error = format_name(full_name)

    if error:
        print(f"\nError: {error}")
    else:
        print(f"\nFormatted name: {formatted_name}")


def test_cases():
    """Test the function with example cases"""
    print("=== Test Cases ===\n")

    test_data = [
        (" le thi Be Nho ", "NhoLTB"),
        (" nguyen mat tROi ", "TroiNM"),
        ("tran van minh", "MinhTV"),
        ("  Nguyen    Thi    Thu    Ha  ", "HaNTT"),
        ("pham   anh", "AnhP"),
        ("   ", None),  # Empty name
        ("SingleName", None),  # Single word
    ]

    for full_name, expected in test_data:
        formatted_name, error = format_name(full_name)
        if error:
            result = "✓" if expected is None else "✗"
            print(f"Input: '{full_name}'")
            print(f"  Error: {error} {result}\n")
        else:
            result = "✓" if formatted_name == expected else "✗"
            print(f"Input: '{full_name}'")
            print(f"  Output: {formatted_name} (Expected: {expected}) {result}\n")


if __name__ == "__main__":
    # Run main program
    main()

    # Uncomment to run test cases
    # print("\n" + "="*50 + "\n")
    # test_cases()
