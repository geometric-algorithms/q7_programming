import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import os
class Node:
    def __init__(self, point, associated_structure=None, left=None, right=None):
        self.point = point
        self.associated_structure = associated_structure
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node(point={self.point})"

def buildXTree(points):
    if not points:
        return None
    points.sort(key=lambda x: x[0])
    mid = len(points) // 2
    return Node(
        point=points[mid],
        left=buildXTree(points[:mid]),
        right=buildXTree(points[mid+1:])
    )

def buildYList(points, left_points, right_points):
    out = []
    left_ptr = 0
    right_ptr = 0
    for p in points:
        out.append([
            p,
            left_ptr if left_ptr < len(left_points) else -1,
            right_ptr if right_ptr < len(right_points) else -1
        ])
        if left_ptr < len(left_points) and left_points[left_ptr] == p:
            left_ptr += 1
        if right_ptr < len(right_points) and right_points[right_ptr] == p:
            right_ptr += 1
    return out

def build2DRangeQueryTree(x_root, points):
    if not x_root:
        return None
    left_points = [p for p in points if p[0] < x_root.point[0]]
    right_points = [p for p in points if p[0] > x_root.point[0]]
    assoc_y = buildYList(points, left_points, right_points)
    return Node(
        point=x_root.point,
        associated_structure=assoc_y,
        left=build2DRangeQueryTree(x_root.left, left_points),
        right=build2DRangeQueryTree(x_root.right, right_points)
    )

_range_query_tree_root = None

def preprocess(points):
    global _range_query_tree_root
    x_root = buildXTree(points)
    points.sort(key=lambda x: x[1])
    _range_query_tree_root = build2DRangeQueryTree(x_root, points)

def findSplitNode(root, xmin, xmax):
    node = root
    while node and (node.left or node.right):
        if xmin <= node.point[0] <= xmax:
            return node
        elif node.point[0] < xmin:
            node = node.right
        else:
            node = node.left
    return node

def findFirstGreaterOrEqual(lst, ymin):
    l, r = 0, len(lst) - 1
    while l <= r:
        m = (l + r) // 2
        if lst[m][0][1] < ymin:
            l = m + 1
        else:
            r = m - 1
    return l

def query(xmin, xmax, ymin, ymax):
    global _range_query_tree_root
    if _range_query_tree_root is None:
        raise Exception("Tree not built. Call preprocess(points) first.")

    result = []
    seen = set()
    split = findSplitNode(_range_query_tree_root, xmin, xmax)
    if not split:
        return result

    if xmin <= split.point[0] <= xmax and ymin <= split.point[1] <= ymax:
        result.append(split.point)
        seen.add(split.point)

    ptr = None
    if split.associated_structure:
        ptr = findFirstGreaterOrEqual(split.associated_structure, ymin)
        if ptr >= len(split.associated_structure):
            ptr = None
        else:
            temp_ptr = ptr
            while temp_ptr < len(split.associated_structure):
                p, _, _ = split.associated_structure[temp_ptr]
                if p[1] > ymax:
                    break
                if xmin <= p[0] <= xmax and ymin <= p[1] <= ymax and p not in seen:
                    result.append(p)
                    seen.add(p)
                temp_ptr += 1
            ptr = split.associated_structure[ptr][1] if ptr is not None and ptr < len(split.associated_structure) else None

    node = split.left
    while node:
        if node.point[0] >= xmin:
            if node.associated_structure and ptr is not None and ptr >= 0 and ptr < len(node.associated_structure):
                assoc = node.associated_structure
                temp_ptr = assoc[ptr][1]
                if temp_ptr >= 0 and temp_ptr < len(assoc):
                    while temp_ptr < len(assoc):
                        p, left_ptr, _ = assoc[temp_ptr]
                        if p[1] > ymax:
                            break
                        if xmin <= p[0] <= xmax and ymin <= p[1] <= ymax and p not in seen:
                            result.append(p)
                            seen.add(p)
                        temp_ptr += 1
            if xmin <= node.point[0] <= xmax and ymin <= node.point[1] <= ymax and node.point not in seen:
                result.append(node.point)
                seen.add(node.point)
            node = node.left
        else:
            node = node.right
            if node and node.associated_structure and ptr is not None and ptr >= 0 and ptr < len(node.associated_structure):
                ptr = node.associated_structure[ptr][1] if ptr < len(node.associated_structure) else None

    if split.associated_structure:
        ptr = findFirstGreaterOrEqual(split.associated_structure, ymin)
        if ptr < len(split.associated_structure):
            ptr = split.associated_structure[ptr][2]
        else:
            ptr = None

    node = split.right
    while node:
        if node.point[0] <= xmax:
            if node.associated_structure and ptr is not None and ptr >= 0 and ptr < len(node.associated_structure):
                assoc = node.associated_structure
                temp_ptr = ptr
                if temp_ptr >= 0:
                    while temp_ptr < len(assoc):
                        p, _, right_ptr = assoc[temp_ptr]
                        if p[1] > ymax:
                            break
                        if xmin <= p[0] <= xmax and ymin <= p[1] <= ymax and p not in seen:
                            result.append(p)
                            seen.add(p)
                        temp_ptr += 1
            if xmin <= node.point[0] <= xmax and ymin <= node.point[1] <= ymax and node.point not in seen:
                result.append(node.point)
                seen.add(node.point)
            node = node.right
        else:
            node = node.left
            if node and node.associated_structure and ptr is not None and ptr >= 0 and ptr < len(node.associated_structure):
                ptr = node.associated_structure[ptr][1] if ptr < len(node.associated_structure) else None

    return result
def main():


    points = []
    try:
        if os.path.exists('input.txt'):
            with open('input.txt', 'r') as f:
                for line in f:
                    x, y = map(float, line.strip().split())
                    points.append((x, y))
        else:
            raise FileNotFoundError
    except Exception as e:
        print(f"⚠️ Error reading input.txt ({e}). Generating random points.")
        N = 1000
        points = [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(N)]

    preprocess(points)

    try:
        print("Enter query rectangle xmin xmax ymin ymax (space-separated):")
        query_input = input().strip().split()
        if len(query_input) != 4:
            raise ValueError("Invalid input. Expected four numbers.")
        xmin, xmax, ymin, ymax = map(float, query_input)
        if xmin > xmax:
            xmin, xmax = xmax, xmin
        if ymin > ymax:
            ymin, ymax = ymax, ymin
    except Exception as e:
        print(f"⚠️ Error in input: {e}. Using random rectangle.")
        coords = [random.uniform(-100, 100) for _ in range(4)]
        xmin, xmax = sorted(coords[:2])
        ymin, ymax = sorted(coords[2:])

    result = query(xmin, xmax, ymin, ymax)

    plt.figure(figsize=(8, 6))
    if points:
        xs, ys = zip(*points)
        plt.scatter(xs, ys, label="All Points", color='lightgrey')

    if result:
        rx, ry = zip(*result)
        plt.scatter(rx, ry, label="Query Result", color='red')

    plt.plot([xmin, xmax, xmax, xmin, xmin], [ymin, ymin, ymax, ymax, ymin], 'b--', label="Query Rectangle")

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('2D Range Tree Query Visualization')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
