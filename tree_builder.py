class EmployeeNode:
    '''
    A class to represent a node in the binary tree.
    Attributes:
        name (str): The name of the employee.
        left (EmployeeNode): The left child node, representing the left subordinate.
        right (EmployeeNode): The right child node, representing the right subordinate.
    '''

    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None


class TeamTree:
    '''
    A class to represent a binary tree for managing a team structure.
    Attributes:
        root (EmployeeNode): The root node of the tree, representing the team lead.
    Methods:
        insert(manager_name, employee_name, side, current_node=None): Inserts a new employee under the specified manager.
        print_tree(node=None, level=0): Prints the tree structure starting from the given node.

    '''

    def __init__(self):
        self.root = None

    def insert(self, manager_name, employee_name, side, current_node=None):
        '''
        Recursively searches for manager_name and attaches employee_name on the given side.
        Returns True once the manager has been found (so the search stops),
        and False if the manager is not in this branch.
        '''
        is_top_call = current_node is None

        # Top-level call: validate input and start at the root
        if is_top_call:
            if self.root is None:
                print("❌ There is no team lead yet. Add a team lead first.")
                return False
            side = side.strip().lower()
            if side not in ("left", "right"):
                print(f"❌ '{side}' is not a valid side. Please enter LEFT or RIGHT.")
                return False
            current_node = self.root

        # Found the manager: try to fill the requested side
        if current_node.name == manager_name:
            if side == "left":
                if current_node.left is None:
                    current_node.left = EmployeeNode(employee_name)
                    print(f"✅ {employee_name} added to the LEFT of {manager_name}")
                else:
                    print(f"❌ {manager_name} already has a LEFT report: {current_node.left.name}")
            else:
                if current_node.right is None:
                    current_node.right = EmployeeNode(employee_name)
                    print(f"✅ {employee_name} added to the RIGHT of {manager_name}")
                else:
                    print(f"❌ {manager_name} already has a RIGHT report: {current_node.right.name}")
            return True  # manager found, stop searching

        # Not the manager: search the left subtree, then the right subtree.
        # Only recurse into children that exist; passing None would restart at the root.
        if current_node.left is not None:
            if self.insert(manager_name, employee_name, side, current_node.left):
                return True
        if current_node.right is not None:
            if self.insert(manager_name, employee_name, side, current_node.right):
                return True

        # Searched the whole tree and never found the manager
        if is_top_call:
            print(f"❌ Manager '{manager_name}' was not found.")
        return False

    def print_tree(self, node=None, level=0):
        '''
        Recursively prints the team structure, indenting each level.
        '''
        if node is None:
            if level == 0:
                node = self.root
                if node is None:
                    print("(The team is empty.)")
                    return
            else:
                return  # reached a leaf's empty child

        print("    " * level + "- " + node.name)
        self.print_tree(node.left, level + 1)
        self.print_tree(node.right, level + 1)


# Test your code here
def run_tests():
    company_directory = TeamTree()
    company_directory.root = EmployeeNode("Jordan")
    company_directory.insert("Jordan", "Taylor", "right")
    company_directory.insert("Jordan", "Riley", "left")
    company_directory.insert("Riley", "Dana", "right")
    company_directory.insert("Riley", "Morgan", "left")
    company_directory.print_tree()

    # Error cases
    company_directory.insert("Jordan", "Sam", "left")    # side already taken
    company_directory.insert("Alex", "Sam", "left")      # manager does not exist
    company_directory.insert("Taylor", "Sam", "up")      # invalid side


# CLI functionality
def company_directory():
    tree = TeamTree()

    while True:
        print("\n📋 Team Management Menu")
        print("1. Add Team Lead (root)")
        print("2. Add Employee")
        print("3. Print Team Structure")
        print("4. Exit")
        choice = input("Choose an option (1–4): ")

        if choice == "1":
            if tree.root:
                print("⚠️ Team lead already exists.")
            else:
                name = input("Enter team lead's name: ")
                tree.root = EmployeeNode(name)
                print(f"✅ {name} added as the team lead.")

        elif choice == "2":
            manager = input("Enter the manager's name: ")
            employee = input("Enter the new employee's name: ")
            side = input("Should this employee be on the LEFT or RIGHT of the manager? ")
            side = side.lower()
            tree.insert(manager, employee, side)

        elif choice == "3":
            print("\n🌳  Current Team Structure:")
            tree.print_tree()

        elif choice == "4":
            print("Good Bye!")
            break
        else:
            print("❌ Invalid option. Try again.")


if __name__ == "__main__":
    run_tests()
    company_directory()


'''
DESIGN MEMO
 
How recursive insertion worked:
The insert() method starts at the root and checks whether the current employee
is the manager we are looking for. If it is, the method checks whether the
requested side (left or right) is open and, if so, creates a new EmployeeNode
there. If the current employee is not the manager, the method calls itself on
the left child and then on the right child, so it works its way down the tree
one branch at a time. This is a depth-first search: each recursive call handles
one smaller subtree, and the process stops when the manager is found or every
branch has been checked.
 
Challenges finding the right spot:
The biggest issue was the default parameter current_node=None. Since None
means "start at the root," calling insert() on an empty child would restart the
search from the top and loop forever. I fixed this by only recursing into
children that actually exist. Another challenge was stopping the search once
the manager was found. I made insert() return True when the manager is found,
so the other branches stop searching and the "manager not found" message only
prints once. One limitation is that duplicate names
would match whichever employee is found first.
 
When trees are preferable:
Trees are the right choice whenever data is hierarchical, like org charts,
folders on a computer, the HTML elements of a web page, or decision trees. A
list or dictionary can store the employees, but it doesn't show who reports to
whom. A tree builds that relationship into the structure itself, and balanced
search trees can also find items in O(log n) time instead of checking every
item.
'''
