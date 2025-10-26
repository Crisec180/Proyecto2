# O(n log n) - Tiempo logarítmico (como mergesort)
def merge_sort(arr, key=None):
    
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    
    return merge(left, right, key)



