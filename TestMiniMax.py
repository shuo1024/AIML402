"""
@Auth ： shuo tang
@Email:  tansh643@student.otago.ac.nz
@Time ： 2024/8/6 10:22
"""


class TreeNode:
    def __init__(self, name=None, value=None):
        self.value = value
        self.name = name
        self.has_explore = False
        self.children = []

    def __eq__(self, other):
        if isinstance(other, TreeNode):
            return self.value == other.value and self.name == other.name and self.has_explore == other.has_explore
        return False

    def __repr__(self):
        return f"TreeNode({self.name, self.value, self.has_explore})"

    def add_child(self, children):
        for child in children:
            self.children.append(child)


def print_tree(node, level=0):
    indent = "  " * level
    print(f"{indent}{node}")
    for child in node.children:
        print_tree(child, level + 1)


def initTreeNode():
    A = TreeNode("A")

    a1 = TreeNode("a1")
    a2 = TreeNode("a2")

    b1 = TreeNode('b1')
    b2 = TreeNode('b2')
    b3 = TreeNode('b3')
    b4 = TreeNode('b4')

    a3 = TreeNode('a3', 9)
    a4 = TreeNode('a4', 3)
    a5 = TreeNode('a5', 100)
    a6 = TreeNode('a6', 1)
    a7 = TreeNode('a7', 20)
    a8 = TreeNode('a8', 3)
    a9 = TreeNode('a9', 100)
    a10 = TreeNode('a10', 0)

    A.add_child([a1, a2])

    a1.add_child([b1, b2])
    a2.add_child([b3, b4])

    b1.add_child([a3, a4])
    b2.add_child([a5, a6])

    b3.add_child([a7, a8])
    b4.add_child([a9, a10])
    # print_tree(A)
    return A


def find_min(node, a, b, enable_alpha_beta_pruning):
    if len(node.children) == 0:
        if enable_alpha_beta_pruning:
            node.has_explore = True
        return node.value, node
    children = node.children

    init_value = float('inf')
    result_node = None
    for child in children:
        if enable_alpha_beta_pruning:
            if a >= b:
                break
        best_value, best_choice = find_max(child, a, b, enable_alpha_beta_pruning)
        if best_value < init_value:
            init_value = best_value
            result_node = best_choice
        if enable_alpha_beta_pruning:
            b = min(b, best_value)

    node.value = init_value
    node.has_explore = True
    return init_value, result_node


def find_max(node, a, b, enable_alpha_beta_pruning):
    if len(node.children) == 0:
        if enable_alpha_beta_pruning:
            node.has_explore = True
        return node.value, node
    children = node.children
    init_value = -float('inf')
    result_node = None

    for child in children:
        if enable_alpha_beta_pruning:
            if a >= b:
                break
        best_value, best_choice = find_min(child, a, b, enable_alpha_beta_pruning)
        if best_value > init_value:
            init_value = best_value
            result_node = best_choice
        if enable_alpha_beta_pruning:
            a = max(a, best_value)

    node.value = init_value
    node.has_explore = True
    return init_value, result_node


if __name__ == '__main__':
    node = initTreeNode()
    a = -float('inf')
    b = float('inf')
    enable_alpha_beta_pruning = True
    # enable_alpha_beta_pruning = False

    find_max(node, a, b, enable_alpha_beta_pruning)

    print_tree(node)
