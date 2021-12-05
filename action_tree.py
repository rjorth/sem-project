from state_fluents import get_world_fluents
 # Add goal states
 # multiple parents
 # add labels to goal states
 #

class Node:
    def __init__(self, positive_fluents, goal_name = None):
        # self.name = name
        # self.fluents = {"mug_on_table_a": 0, "mug_on_table_b": 0, "holding_mug": 0, "phone_on_table_a": 0, "phone_on_table_b": 0, "holding_phone": 0}
        self.fluents = get_world_fluents()

        for f in positive_fluents:
            self.fluents[f] = 1

        self.children_nodes = []
        self.edges = []
        self.parent_edges = []
        self.goal = goal_name
        self.possible_goals = []

    def is_goal(self):
        if self.goal is None:
            return False
        return True

    def is_leaf(self):
        if self.children_nodes == []:
            return True
        return False

    def get_label(self):
        return self.goal

    def label_parents(self, label):
        if label not in self.possible_goals:
            self.possible_goals.append(label)

        if self.parent_edges == []:
            return

        for parent in self.parent_edges:
            parent.parent_node.label_parents(label)

    def add_child_node(self, positive_fluents, action, goal_name = None):
        child_node = Node(positive_fluents, goal_name)
        self.children_nodes.append(child_node)
        edge = Edge(self, child_node, action)
        self.edges.append(edge)
        child_node.parent_edges.append(edge)
        return child_node

    def create_parent_connection(self, parent, action):
        parent.children_nodes.append(self)
        edge = Edge(parent, self, action)
        parent.edges.append(edge)
        self.parent_edges.append(edge)

    def find_child_action(self, action):
        for e in self.edges:
            if e.action == action:
                return e.child_node
        return False

class Edge:
    def __init__(self, parent_node, child_node, action):
        self.parent_node = parent_node
        self.child_node = child_node
        self.action = action

def print_node(node):
    cur_node = node

    for parent in cur_node.parent_edges:
        print(parent.action)

    print(cur_node.fluents)
    print(cur_node.possible_goals)

    children = cur_node.children_nodes
    for c in children:
        print_node(c)

def create_moving_items_tree():
    root = Node(["mug_on_table_a", "phone_on_table_a"])

    pick_up_mug_action = root.add_child_node(["holding_mug", "phone_on_table_a"], "pickup mug")
    place_mug_on_table_b_action = pick_up_mug_action.add_child_node(["mug_on_table_b", "phone_on_table_a"], "place table_b", "mug on table b")
    place_mug_on_table_c_action = pick_up_mug_action.add_child_node(["mug_on_table_c", "phone_on_table_a"], "place table_c", "mug on table c")

    pick_up_phone_action = root.add_child_node(["holding_phone", "mug_on_table_a"], "pickup phone")
    place_phone_on_table_b_action = pick_up_phone_action.add_child_node(["phone_on_table_b", "mug_on_table_a"], "place table_b", "phone on table b")
    place_phone_on_table_c_action = pick_up_phone_action.add_child_node(["phone_on_table_c", "mug_on_table_a"], "place table_c", "phone on table c")

    pickup_phone_while_mug_on_table_b_action = place_mug_on_table_b_action.add_child_node(["mug_on_table_b", "holding_phone"], "pickup phone")


    pickup_mug_while_phone_on_table_b_action = place_phone_on_table_b_action.add_child_node(["phone_on_table_b", "holding_mug"], "pickup mug")
    # potb = phone on table b
    place_mug_on_table_b_potb = pickup_mug_while_phone_on_table_b_action.add_child_node(["mug_on_table_b", "phone_on_table_b"], "place table_b", "mug and phone on table b")
    place_mug_on_table_b_potb.create_parent_connection(pickup_phone_while_mug_on_table_b_action, "place table_b")

    pickup_phone_while_mug_on_table_c_action = place_mug_on_table_c_action.add_child_node(["mug_on_table_c", "holding_phone"], "pickup phone")
    pickup_mug_while_phone_on_table_c_action = place_phone_on_table_c_action.add_child_node(["phone_on_table_c", "holding_mug"], "pickup mug")
    # potb = phone on table b
    place_mug_on_table_c_potb = pickup_mug_while_phone_on_table_c_action.add_child_node(["mug_on_table_c", "phone_on_table_c"], "place table_c", "mug and phone on table c")
    place_mug_on_table_c_potb.create_parent_connection(pickup_phone_while_mug_on_table_c_action, "place table_c")

    a = root.find_child_action("pickup mug")
    fl = a.fluents
    # print_node(root)
    find_leaves_and_label_parents(root)
    return root

def find_leaves_and_label_parents(node):
    if node.is_goal():
        node.label_parents(node.get_label())

    if not node.is_leaf():
        for child in node.children_nodes:
            find_leaves_and_label_parents(child)

#boxes_tree = create_moving_items_tree()

# print_node(boxes_tree)
