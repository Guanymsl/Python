import argparse

class Node():
    #########################
    # DO NOT MODIFY CODES HERE
    # DO NOT MODIFY CODES HERE
    # DO NOT MODIFY CODES HERE
    # It's important and repeat three times
    #########################
    def __init__(self, key):
        self.value = key
        self.left_child = None
        self.right_child = None
    def __repr__(self):
        return str(self.value)

class BS_tree():
    def __init__(self):
        self.root = None

    def inorder(self, output):      # print the in-order traversal of binary search tree
        # TODO
        instr = self._inorder(self.root, "")
        output.write(instr + '\n')

    def preorder(self, output):     # print the pre-order traversal of binary search tree
        # TODO
        prestr = self._preorder(self.root, "")
        output.write(prestr + '\n')

    def postorder(self, output):    # print the post-order traversal of binary search tree
        # TODO
        poststr = self._postorder(self.root, "")
        output.write(poststr + '\n')

    def find_max(self, output):     # print the maximum number in binary search tree
        # TODO
        output.write(str(self._find_max(self.root)) + '\n')

    def find_min(self, output):     # print the minimum number in binary search tree
        # TODO
        output.write(str(self._find_min(self.root)) + '\n')

    def insert(self, key):          # insert one node
        # TODO
        if self.root == None:
            self.root = Node(key)

        else:
            current = self.root
            while current != None:
                if key > current.value:
                    if current.right_child == None:
                        current.right_child = Node(key)
                        break
                    else:
                        current = current.right_child

                elif key < current.value:
                    if current.left_child == None:
                        current.left_child = Node(key)
                        break
                    else:
                        current = current.left_child

                else:
                    break

    def delete(self, key):          # delete one node
        # TODO
        if self.root != None:
            self._delete(self.root, key)

    def level(self, output):        # print the height of binary search tree(leaf = 0)
        # TODO
        output.write(str(self._level(self.root)) + '\n')

    def internalnode(self, output): # print the internal node in binary search tree from the smallest to the largest
        # TODO
        internalstr = self._internalnode(self.root, "")
        output.write(internalstr + '\n')

    def leafnode(self, output):     # print the leafnode in BST from left to right
        # TODO
        leafstr = self._leafnode(self.root, "")
        output.write(leafstr + '\n')

    def _inorder(self, node: Node, s):
        if node != None:
            s += self._inorder(node.left_child, "")
            s += str(node.value) + ' '
            s += self._inorder(node.right_child, "")
        return s

    def _preorder(self, node: Node, s):
        if node != None:
            s += str(node.value) + ' '
            s += self._preorder(node.left_child, "")
            s += self._preorder(node.right_child, "")
        return s

    def _postorder(self, node: Node, s):
        if node != None:
            s += self._postorder(node.left_child, "")
            s += self._postorder(node.right_child, "")
            s += str(node.value) + ' '
        return s

    def _find_max(self, node: Node):
        if node != None:
            while node.right_child != None:
                node = node.right_child

            return node.value

    def _find_min(self, node: Node):
        if node != None:
            while node.left_child != None:
                node = node.left_child

            return node.value

    def _delete(self, node: Node, key):
        parent: Node = None

        while node != None:
            if key > node.value:
                parent = node
                node = node.right_child

            elif key < node.value:
                parent = node
                node = node.left_child

            else:
                break

        if node != None:
            l = 0
            r = 0
            if node.left_child != None:
                l += 1
            if node.right_child != None:
                r += 1

            if l + r == 0:
                if parent == None:
                    self.root = None
                else:
                    if parent.left_child != None and parent.left_child.value == key:
                        parent.left_child = None
                    else:
                        parent.right_child = None

            elif l + r == 1:
                if parent == None:
                    if l == 1:
                        self.root = node.left_child
                    else:
                        self.root = node.right_child

                else:
                    if parent.left_child != None and parent.left_child.value == key:
                        if l == 1:
                            parent.left_child = node.left_child
                        else:
                            parent.left_child = node.right_child

                    else:
                        if l == 1:
                            parent.right_child = node.left_child
                        else:
                            parent.right_child = node.right_child

            else:
                nextKey = self._find_min(node.right_child)
                if parent == None:
                    self.root = Node(nextKey)
                    self.root.left_child = node.left_child
                    self.root.right_child = node.right_child

                else:
                    if parent.left_child != None and parent.left_child.value == key:
                        parent.left_child = Node(nextKey)
                        parent.left_child.left_child = node.left_child
                        parent.left_child.right_child = node.right_child
                    else:
                        parent.right_child = Node(nextKey)
                        parent.right_child.left_child = node.left_child
                        parent.right_child.right_child = node.right_child

                self._delete(node.right_child, nextKey)

    def _level(self, node: Node):
        if node == None:
            return -1
        else:
            return max(self._level(node.left_child), self._level(node.right_child)) + 1

    def _internalnode(self, node: Node, s):
        if node != None:
            s += self._internalnode(node.left_child, "")
            if node.left_child != None or node.right_child != None:
                s += str(node.value) + ' '
            s += self._internalnode(node.right_child, "")
        return s

    def _leafnode(self, node: Node, s):
        if node != None:
            s += self._leafnode(node.left_child, "")
            if node.left_child == None and node.right_child == None:
                s += str(node.value) + ' '
            s += self._leafnode(node.right_child, "")
        return s

    def main(self, input_path, output_path):
        #########################
        # DO NOT MODIFY CODES HERE
        # DO NOT MODIFY CODES HERE
        # DO NOT MODIFY CODES HERE
        # It's important and repeat three times
        #########################
        output = open(output_path, 'w', newline='')
        with open(input_path, 'r', newline='') as file_in:
            f = file_in.read().splitlines()
            for lines in f:
                if lines.startswith("insert"):
                    value_list = lines.split(' ')
                    for value in value_list[1:]:
                        self.insert(int(value))
                if lines.startswith('inorder'):
                    self.inorder(output)
                if lines.startswith('preorder'):
                    self.preorder(output)
                if lines.startswith('postorder'):
                    self.postorder(output)
                if lines.startswith('max'):
                    self.find_max(output)
                if lines.startswith('min'):
                    self.find_min(output)
                if lines.startswith('delete'):
                    value_list = lines.split(' ')
                    self.delete(int(value_list[1]))
                if lines.startswith('level'):
                    self.level(output)
                if lines.startswith('internalnode'):
                    self.internalnode(output)
                if lines.startswith('leafnode'):
                    self.leafnode(output)
        output.close()
if __name__ == '__main__' :
    #########################
    # DO NOT MODIFY CODES HERE
    # DO NOT MODIFY CODES HERE
    # DO NOT MODIFY CODES HERE
    # It's important and repeat three times
    #########################
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default = './input_7.txt',help="Input file root.")
    parser.add_argument("--output", type=str, default = './output_7.txt',help="Output file root.")
    args = parser.parse_args()

    BS = BS_tree()
    BS.main(args.input, args.output)