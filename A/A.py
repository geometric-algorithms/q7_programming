import random
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

def buildYTree(points):
    if not points:
        return None
    mid = len(points) // 2
    return Node(
        point=points[mid],
        left=buildYTree(points[:mid]),
        right=buildYTree(points[mid+1:])
    )

def build2DRangeQueryTree(x_root, points):
    if not x_root:
        return None
    left_points = [p for p in points if p[0] < x_root.point[0]]
    right_points = [p for p in points if p[0] > x_root.point[0]]
    assoc_y = buildYTree(points)
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
    while node:
        if xmin <= node.point[0] <= xmax:
            return node
        elif node.point[0] < xmin:
            node = node.right
        else:
            node = node.left
    return None

def findSplitYNode(root, ymin, ymax):
    node = root
    while node:
        if ymin <= node.point[1] <= ymax:
            return node
        elif node.point[1] < ymin:
            node = node.right
        else:
            node = node.left
    return None

def collectY(node, ymin, ymax, collected):
    if not node:
        return
    if ymin <= node.point[1] <= ymax:
        collected.append(node.point)
    collectY(node.left, ymin, ymax, collected)
    collectY(node.right, ymin, ymax, collected)

def queryY(root, ymin, ymax):
    result = []
    split = findSplitYNode(root, ymin, ymax)
    if not split:
        return result
    if ymin <= split.point[1] <= ymax:
        result.append(split.point)

    node = split.left
    while node:
        if node.point[1] >= ymin:
            if node.right:
                collectY(node.right, ymin, ymax, result)
            if ymin <= node.point[1] <= ymax:
                result.append(node.point)
            node = node.left
        else:
            node = node.right

    node = split.right
    while node:
        if node.point[1] <= ymax:
            if node.left:
                collectY(node.left, ymin, ymax, result)
            if ymin <= node.point[1] <= ymax:
                result.append(node.point)
            node = node.right
        else:
            node = node.left
    return result

def query(xmin, xmax, ymin, ymax):
    global _range_query_tree_root
    if _range_query_tree_root is None:
        raise Exception("Tree not built. Call preprocess(points) first.")

    result = []
    split = findSplitNode(_range_query_tree_root, xmin, xmax)
    if not split:
        return result
    if xmin <= split.point[0] <= xmax and ymin <= split.point[1] <= ymax:
        result.append(split.point)

    node = split.left
    while node:
        if node.point[0] >= xmin:
            if node.right:
                temp = queryY(node.right.associated_structure, ymin, ymax)
                result.extend(p for p in temp if xmin <= p[0] <= xmax)
            if xmin <= node.point[0] <= xmax and ymin <= node.point[1] <= ymax:
                result.append(node.point)
            node = node.left
        else:
            node = node.right

    node = split.right
    while node:
        if node.point[0] <= xmax:
            if node.left:
                temp = queryY(node.left.associated_structure, ymin, ymax)
                result.extend(p for p in temp if xmin <= p[0] <= xmax)
            if xmin <= node.point[0] <= xmax and ymin <= node.point[1] <= ymax:
                result.append(node.point)
            node = node.right
        else:
            node = node.left
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
