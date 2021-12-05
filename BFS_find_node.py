import action_tree
import queue


class BFS:
    def find_node(self, cur_state, executedAction):
        q1 = queue.Queue()
        root = action_tree.create_moving_items_tree()

        q1.put(root)

        while not (q1.empty()):
            node = q1.get()

            # if the current state is found in the tree and the executed action is a
            # child action of that node, return the resulting state.
            if (node.fluents == cur_state) and (node.find_child_action(executedAction) != False):
                childNode = node.find_child_action(executedAction)
                return childNode
            for child in node.children_nodes:
                q1.put(child)
        return False