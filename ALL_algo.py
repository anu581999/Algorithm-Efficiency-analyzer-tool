def insertion_sort(arr):
    """
    Perform insertion sort on the input array.

    Parameters:
    - arr (list): The input list to be sorted.

    Yields:
    - list: The state of the array after each insertion.
    """
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]  # Current element to be compared

        # Move elements of arr[0..i-1] that are greater than key
        # to one position ahead of their current position
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]  # Shift elements to the right
            j -= 1
            yield arr

        arr[j + 1] = key  # Place key at its correct position
        yield arr


# ........

def bubble_sort(arr):
    """
    Perform bubble sort on the input array.

    Parameters:
    - arr (list): The input list to be sorted.

    Yields:
    - list: The state of the array after each swap.
    """
    n = len(arr)  # Get the length of the array
    for i in range(n):  # Traverse through the entire array
        for j in range(0, n-i-1):  # Iterate through unsorted part of the array
            if arr[j] > arr[j+1]:  # Compare adjacent elements
                # Swap elements if they are in the wrong order
                arr[j], arr[j+1] = arr[j+1], arr[j]
                yield arr  # Yield the current state of the array after the swap


# ........

def merge_sort(arr):
    # Check if the length of the array is greater than 1
    if len(arr) > 1:
        # Calculate the middle index of the array
        mid = len(arr) // 2

        # Split the array into left and right halves
        L = arr[:mid]
        R = arr[mid:]

        # Recursively apply merge_sort to both left and right halves
        yield from merge_sort(L)
        yield from merge_sort(R)

        # Merge the sorted left and right halves back into the original array
        i = j = k = 0
        while i < len(L) and j < len(R):
            # Compare elements from both halves and put the smaller one into the original array
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            yield arr

        # Append any remaining elements from the left and right halves (if any)
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
            yield arr
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
            yield arr

    return arr  # Return the sorted array

# ............

def quick_sort(arr, low=0, high=None):
    """
    Perform quicksort on the input array.

    Parameters:
    - arr (list): The input list to be sorted.
    - low (int): The starting index of the array (default is 0).
    - high (int): The ending index of the array (default is None).

    Yields:
    - list: The state of the array after each partitioning and sorting.
    """
    if high is None:
        high = len(arr) - 1

    # Check if there are more than one element in the array
    if low < high:
        # Find the partition index
        pi = partition(arr, low, high)
        # Recursively sort elements before and after the partition
        yield from quick_sort(arr, low, pi - 1)
        yield from quick_sort(arr, pi + 1, high)
        # Yield the current state of the array after sorting
        yield arr


# .........

def heapify(arr, n, i):
    """
    Heapify the subtree rooted at index 'i' in the input array 'arr'.

    Parameters:
    - arr (list): The input list representing the heap.
    - n (int): The size of the heap.
    - i (int): The index of the root of the subtree to be heapified.

    Yields:
    - None: Yields nothing during the heapification process.
    """
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    # Check if left child exists and is greater than the root
    if left < n and arr[i] < arr[left]:
        largest = left

    # Check if right child exists and is greater than the largest so far
    if right < n and arr[largest] < arr[right]:
        largest = right

    # Swap the root if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        # Recursively heapify the affected subtree
        yield from heapify(arr, n, largest)


def heap_sort(arr):
    """
    Perform heap sort on the input array 'arr'.

    Parameters:
    - arr (list): The input list to be sorted.

    Yields:
    - list: The state of the array after each heapification and sorting step.
    """
    n = len(arr)

    # Build a max heap
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)

    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        # Heapify the reduced heap
        yield from heapify(arr, i, 0)
        # Yield the current state of the array after sorting
        yield arr


# .....

def insertion_sort_bucket(arr):
    """
    Perform insertion sort on the input array 'arr'.

    Parameters:
    - arr (list): The input list to be sorted.

    Returns:
    - list: The sorted array after insertion sort.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def bucket_sort(arr, noOfBuckets=5):
    """
    Perform bucket sort on the input array 'arr' using the specified number of buckets.

    Parameters:
    - arr (list): The input list to be sorted.
    - noOfBuckets (int): The number of buckets to use in the bucket sort (default is 5).

    Yields:
    - list: The state of the array after each bucketing and sorting step.
    """
    max_value = max(arr)
    buckets = [[] for _ in range(noOfBuckets)]

    # Distribute elements into buckets based on their value
    for i in range(len(arr)):
        index = int(arr[i] / max_value * (noOfBuckets - 1))
        buckets[index].append(arr[i])

    output = []
    for i in range(noOfBuckets):
        # Sort each bucket using insertion sort
        buckets[i] = insertion_sort_bucket(buckets[i])
        # Combine the sorted buckets into the output array
        output.extend(buckets[i])
        # Yield the current state of the array after each bucket sort step
        yield output


# ...........

def counting_sort_radix(arr, exp):
    """
    Perform counting sort on the input array 'arr' based on the specified exponent 'exp'.

    Parameters:
    - arr (list): The input list to be sorted.
    - exp (int): The exponent for radix sorting.

    Returns:
    - None: The input array is modified in-place.
    """
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    # Count occurrences of each digit at the specified exponent place
    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1

    # Update the count array to represent cumulative counts
    for i in range(1, 10):
        count[i] += count[i - 1]

    # Build the output array by placing elements at their correct position
    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    # Copy the sorted output back to the original array
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    """
    Perform radix sort on the input array 'arr'.

    Parameters:
    - arr (list): The input list to be sorted.

    Yields:
    - list: The state of the array after each radix sorting step.
    """
    max_num = max(arr)
    exp = 1

    while max_num // exp > 0:
        counting_sort_radix(arr, exp)  # Call the modified counting_sort_radix
        yield arr
        exp *= 10

    return arr


def counting_sort(arr):
    """
    Perform counting sort on the input array 'arr'.

    Parameters:
    - arr (list): The input list to be sorted.

    Yields:
    - list: The state of the array after each counting sorting step.
    """
    max_val = max(arr)
    count_arr = [0] * (max_val + 1)

    # Count occurrences of each element in the array
    for number in arr:
        count_arr[number] += 1

    output = []
    # Build the sorted output array by placing elements at their correct position
    for i, count in enumerate(count_arr):
        output.extend([i] * count)
        yield output



# .....

#median and order (quick_select)
def partition(arr, low, high):
    """
    Partition the array around a pivot element for quicksort.

    Parameters:
    - arr (list): The input list to be partitioned.
    - low (int): The starting index of the array.
    - high (int): The ending index of the array.

    Returns:
    - int: The index of the pivot element after partitioning.
    """
    i = low - 1
    pivot = arr[high]

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def k_smallest(arr, l, r, k):
    """
    Find the k-th smallest element in the array using quick select.

    Parameters:
    - arr (list): The input list to find the k-th smallest element.
    - l (int): The left index of the current subarray.
    - r (int): The right index of the current subarray.
    - k (int): The value of k (1 to r - l + 1).

    Returns:
    - int: The k-th smallest element in the array.
    """
    if 0 < k <= r - l + 1:
        index = partition(arr, l, r)
        if index - l == k - 1:
            return arr[index]
        if index - l > k - 1:
            return k_smallest(arr, l, index - 1, k)
        return k_smallest(arr, index + 1, r, k - index + l - 1)
    else:
        print("Invalid value of k. Please enter a value within the valid range.")


