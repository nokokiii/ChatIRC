class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node


class LinkedList:
    def __init__(self, lst: list):
        prev_node = None
        for elem in reversed(lst):
            prev_node = Node(elem, prev_node)

        self.head = prev_node

    def __len__(self):
        count = 0
        current_node = self.head

        while current_node is not None:
            current_node = current_node.next_node
            count += 1

        return count

    def __str__(self):
        linked_list_str = "["
        current_node = self.head

        while current_node is not None:
            linked_list_str += f"{current_node.value}, "
            current_node = current_node.next_node

        linked_list_str = linked_list_str[:-2]

        return linked_list_str + "]"

    def add_node(self, new_value):
        new_node = Node(new_value)
        if self.head is None:
            self.head = new_node
        else:
            current_node = self.head

            while current_node.next_node is not None:
                current_node = current_node.next_node

            current_node.next_node = new_node

    def find_contract_number(self, last_name):
        current_node = self.head
        while current_node is not None:
            if current_node.value[1] == last_name:
                return current_node.value[2]
            current_node = current_node.next_node

        return -1


n = int(input())
m = int(input())

linked_lst = LinkedList([])

for _ in range(n):
    first_name, last_name, contract_num = input().split()
    linked_lst.add_node((first_name, last_name, contract_num))

for _ in range(m):
    last_name = input().strip()
    print(linked_lst.find_contract_number(last_name))