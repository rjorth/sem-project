import argparse
import re
import math
import sys
import enum
from BFS_find_node import BFS
from state_fluents import get_world_fluents
import random

# import BFS_find_node

# NEEDS TO BE PYTHON3
from robot_interface import RobotInterface


class Tags(enum.Enum):
    pickup = 1 #red CUBE
    place = 2 # GREEN BUBE
    mug = 3 # BLUE CUBES
    phone = 67 # GREEN PAPER WITH A C
    table_a = 1001 # BOX 1
    table_b = 1002 #BOX 2
    table_c = 1003 # BOX 3


class Observation:
    def __init__(self, tag, category):
        self.tag = tag
        self.category = category


if __name__ == '__main__':
    # robot_ip = ""
    robot_ip = "169.254.39.147"
    robot = RobotInterface(robot_ip)

    categories = {"pickup": "action", "place": "action", "mug": "object", "table_a": "surface", "table_b": "surface"}
    effects = {}
    observations = []
    actions = [1, 2] # 1 is red box, 2 is green box
    objects = [3, 67, 1001, 1002, 1003] # white box 1 is 1001, white box 2 is 1002, whitebox 3 is 1003, 3 is green box, 67 is green C paper
    # surfaces = [1001, 1002, 1003]  # ids of surfaces]
    # print(robot.observe())

    # cur_state = {"mug_on_table_a": 1, "mug_on_table_b": 0, "holding_mug": 0}
    cur_state = get_world_fluents()
    cur_state["mug_on_table_a"] = 1
    cur_state["phone_on_table_a"] = 1
    # o = [{"id": 1, "test": "ggdh"}, {"id": 3, "test": "ddbyjdyjy"}, {"id": 2, "test": "ddbyjdyjy"},
    #     {"id": 1002, "test": "dgdh"},
    #     {"id": 1003, "test": "dggdy"}]
    executed_actions = []
    bfs_search = BFS()
    # for readCode in o:


    while True:
        x = robot.observe()
        #try:
        readCode = x[0]
        # new_arr = first.values()
        apriltag_id = readCode["id"]
        # observations.append(Observation(Tags(apriltag_id).name, categories[Tags(apriltag_id).name]))
        observations.append(apriltag_id)
        print("See anything ", apriltag_id)
        # after observing an action, call pepper to search for an object
        # after finding an object, call pepper to search for a surface
        # then can look for another action again as normal
        if apriltag_id in actions:
            # observations.append(Observation(Tags(apriltag_id).name, categories[Tags(apriltag_id).name]))
            observations.append(apriltag_id)
            object_found = False

            while not object_found:
                rand = random.sample(objects, len(objects))
                print("rand", rand)
                for object in rand:
                    obs = robot.observe(target_tag_id=object)
                    if len(obs) == 1 and object == obs[0]['id']:
                        object_found = True
                        observations.append(object)
                        print("See Object", object)

                            # observations.append(Observation(Tags(object).name, "object"))
                        executed_action = str(Tags(observations[len(observations) - 2]).name) + " " + str(
                            Tags(observations[
                                     len(observations) - 1]).name)
                        print(executed_action)

                        # code for looking up the action in the tree

                        print(bfs_search.find_node(cur_state, executed_action))
                        if (bfs_search.find_node(cur_state, executed_action)):
                            executed_actions.append(executed_action)
                            print(executed_actions)
                            robot.say(str(executed_action))
                            cur_node = bfs_search.find_node(cur_state, executed_action)
                            cur_state = bfs_search.find_node(cur_state, executed_action).fluents
                            if (len(cur_node.possible_goals) == 1):
                                pursued_goal = cur_node.possible_goals[0]
                                robot.say("The goal is, " + str(pursued_goal))
                                full_plan = executed_actions
                                bottom_tree = False
                                while not bottom_tree:
                                    cur_node = bfs_search.find_node(cur_state, cur_node.edges[0].action)
                                    full_plan.append(cur_node.parent_edges[0].action)
                                    if cur_node.children_nodes == []:
                                        bottom_tree = True
                                    else:
                                        cur_state = cur_node.fluents
                                        executed_action = cur_node.children_nodes[0].action

                                print("The goal is: ", pursued_goal, '\nThe plan is: ', full_plan)

                                break
                            break
                        print(executed_action, cur_state)
                        observations = []
                        break
        #except:
         #   pass



    # if ((observations[len(observations) - 1].category == "object") and (
    #         observations[len(observations) - 2].category == "action")):

# robot.shutdown()
