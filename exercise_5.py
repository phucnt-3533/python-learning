"""
Exercise 5: Count Occurrences and Sort by Frequency
Input N elements, output dictionary with value as key and count as value,
sorted by count in ascending order
"""


def count_and_sort(elements):
    """
    Count occurrences of each element and sort by frequency

    Args:
        elements: List of elements

    Returns:
        Dictionary with element as key and count as value, sorted by count
    """
    # Count occurrences
    count_dict = {}
    for element in elements:
        count_dict[element] = count_dict.get(element, 0) + 1

    # Sort by count (value) in ascending order
    sorted_dict = dict(sorted(count_dict.items(), key=lambda item: item[1]))

    return sorted_dict


def main():
    """Main function to run the program"""
    print("=== Count Occurrences ===\n")

    try:
        # Input number of elements
        n = int(input("Enter number of elements: "))

        if n <= 0:
            print("Error: Number of elements must be positive!")
            return

        # Input elements
        print(f"Enter {n} elements (separated by space): ")
        elements_str = input()
        elements = list(map(int, elements_str.split()))

        if len(elements) != n:
            print(f"Error: Expected {n} elements, got {len(elements)}!")
            return

        # Count and sort
        result = count_and_sort(elements)

        # Print result
        print(f"\nResult: {result}")

    except ValueError:
        print("Error: Invalid input! Please enter valid integers.")
    except Exception as e:
        print(f"Error: {e}")


def test_cases():
    """Test the function with example cases"""
    print("=== Test Cases ===\n")

    test_data = [
        ([1, 2, 4, 5, 2, 4, 1, 6, 4, 3], {5: 1, 6: 1, 3: 1, 1: 2, 2: 2, 4: 3}),
        ([1, 1, 1, 2, 2, 3], {3: 1, 2: 2, 1: 3}),
        ([5, 5, 5, 5], {5: 4}),
        ([1, 2, 3, 4, 5], {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}),
        ([7], {7: 1}),
    ]

    for elements, expected in test_data:
        result = count_and_sort(elements)
        match = result == expected
        result_symbol = "✓" if match else "✗"

        print(f"Input: {elements}")
        print(f"Output: {result}")
        print(f"Expected: {expected} {result_symbol}\n")


if __name__ == "__main__":
    # Run main program
    main()

    # Uncomment to run test cases
    # print("\n" + "="*50 + "\n")
    # test_cases()
