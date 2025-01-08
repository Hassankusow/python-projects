class Node:
    def __init__(self, data):
        self.data = data  # Fitness data or any other type of data
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
        else:
            self._insert(data, self.root)

    def _insert(self, data, node):
        if data['current_weight'] < node.data['current_weight']:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert(data, node.left)
        else:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert(data, node.right)

    def search(self, weight):
        return self._search(weight, self.root)

    def _search(self, weight, node):
        if node is None:
            return None
        if weight == node.data['current_weight']:
            return node.data
        elif weight < node.data['current_weight']:
            return self._search(weight, node.left)
        else:
            return self._search(weight, node.right)

    def inorder_traversal(self):
        records = []
        self._inorder_traversal(self.root, records)
        return records

    def _inorder_traversal(self, node, records):
        if node is not None:
            self._inorder_traversal(node.left, records)
            records.append(node.data)
            self._inorder_traversal(node.right, records)
