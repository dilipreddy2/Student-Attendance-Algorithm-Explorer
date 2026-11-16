
# 1. LINEAR SEARCH
def linear_search(students, target_id):

    steps = []

    for i, student in enumerate(students):
        steps.append(
            f"Checking student ID {student['id']}"
        )

        if student["id"] == target_id:
            return student, steps

    steps.append("Student not found")
    return None, steps



# 2. BINARY SEARCH
def binary_search(students, target_id):

    steps = []

    low = 0
    high = len(students) - 1

    while low <= high:

        mid = (low + high) // 2

        steps.append(
            f"Checking student ID {students[mid]['id']}"
        )

        if students[mid]["id"] == target_id:
            return students[mid], steps

        elif students[mid]["id"] < target_id:
            low = mid + 1

        else:
            high = mid - 1

    steps.append("Student not found")

    return None, steps

# 3. BUBBLE SORT
def bubble_sort(students):

    students = students.copy()
    steps = []

    n = len(students)

    for i in range(n):

        for j in range(0, n - i - 1):

            steps.append(
                f"Comparing {students[j]['name']} and {students[j+1]['name']}"
            )

            if students[j]["percentage"] > students[j+1]["percentage"]:

                students[j], students[j+1] = students[j+1], students[j]

                steps.append("Swapped student records")

    return students, steps



# 4. MERGE SORT
def merge_sort(students):

    steps = []

    def divide(arr):

        if len(arr) <= 1:
            return arr

        mid = len(arr) // 2

        left = divide(arr[:mid])
        right = divide(arr[mid:])

        return merge(left, right)

    def merge(left, right):

        result = []
        i = 0
        j = 0

        while i < len(left) and j < len(right):

            steps.append("Comparing attendance percentages")

            if left[i]["percentage"] <= right[j]["percentage"]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        steps.append("Merged sorted student records")

        return result

    sorted_students = divide(students.copy())

    return sorted_students, steps
