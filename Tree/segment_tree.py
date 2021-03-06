# Range Query (Using Segment Tree)
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

size = len(arr)
sum = 0
arr_sum = [0]*size

for i in range(size):
    sum += arr[i]
    arr_sum[i] = sum

print("Array : ", arr)
print("Sum Array : ", arr_sum)

# To find the sum from index 1 to 4

left = 2
right = 4

answer = arr_sum[right]
if left > 0:
    answer -= arr_sum[left - 1]

print("The sum from index ", left," to ", right," is ",answer)

# update index

index = 5
updated_value = 9
print("Value at index ", index," is ", arr[index], ", Updated Value : ", updated_value)
delta = updated_value - arr[index]
print("Difference : ", delta)
arr[index] = updated_value

for i in range(index, size):
    arr_sum[i] += delta

print("Updated Array : ", arr_sum)

# Segment tree


class Node:
    def __init__(self, le, ri):
        data = arr_sum[ri]
        if le > 0:
            data -= arr_sum[le - 1]
        self.data = data

        self.leftIndex = le
        self.left = None

        self.rightIndex = ri
        self.right = None


class Tree:
    def __init__(self):
        self.root = None

    def insert(self, root, le, ri):
        if root is None:
            root = Node(le, ri)
        else:
            if le <= ri:
                mid = int((le + ri) / 2)
                root.left = self.insert(root.left, le, mid)
                root.right = self.insert(root.right, mid + 1, ri)
        return root

    def print_tree(self, root):
        if root is not None:

            # use the comment code when you want to confirm tree fix
            # if root.leftIndex == root.rightIndex:
            #     print("Left ", root.leftIndex, " Right ", root.rightIndex, " sum = ", root.data)

            print("Left ", root.leftIndex, " Right ", root.rightIndex, " sum = ", root.data)
            self.print_tree(root.left)
            self.print_tree(root.right)

    # Go to each leaf Node and fix the tree
    def fix_tree(self, root):
        if root is not None:

            if root.left is None and root.right is None:
                if root.leftIndex != root.rightIndex:
                    root.left = self.insert(root.left, root.leftIndex, root.leftIndex)
                    root.right = self.insert(root.right, root.rightIndex, root.rightIndex)

            self.fix_tree(root.left)
            self.fix_tree(root.right)

    def find_sum(self, root, le, ri):
        if root is not None:
            sum = 0
            if root.leftIndex >= le and root.rightIndex <= ri:
                return root.data
            elif root.leftIndex >= le or root.rightIndex <= ri:
                sum += self.find_sum(root.right, le, ri)
                sum += self.find_sum(root.left, le, ri)
                return int(sum)

        else:
            return 0

    def update_tree(self, root, updated_index, diff):
        if root is not None:

            if updated_index >= root.leftIndex:
                if updated_index <= root.rightIndex:
                    root.data += diff
                    self.update_tree(root.left, updated_index, diff)
                    self.update_tree(root.right, updated_index, diff)


final = size - 1
t = Tree()
t.root = Node(0, final)
temp = final
depth = 2
if final > 7:
    depth = -2
# Finding depth
while temp >= 1:
    temp = int(temp/2)
    depth += 1

t.root = t.insert(t.root, 0, final)


for i in range(depth):
    if t.root.left.leftIndex <= t.root.left.rightIndex:
        t.root.left = t.insert(t.root.left, t.root.left.leftIndex, t.root.left.rightIndex)
    if t.root.right.leftIndex <= t.root.right.rightIndex:
        t.root.right = t.insert(t.root.right, t.root.right.leftIndex, t.root.right.rightIndex)

t.fix_tree(t.root)
t.print_tree(t.root)

# Update value in the segment tree
index = 5
new_val = 6
old_val = arr[index]
diff = new_val - old_val
print("\nUpdating value of index ", index, " from ", old_val," to ", new_val)

t.update_tree(t.root, index, diff)
print("\nSum Array using Segment Tree : [ ", end="")
for i in range(size):
    data = t.find_sum(t.root, 0, i)
    print(data, end=" ")
print("]\n")
