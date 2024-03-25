def clear(state, obj):
    return f"CLEAR({obj})" in state

def on(state, obj1, obj2):
    return f"on({obj1},{obj2})" in state

def on_table(state, obj):
    return f"onTable({obj})" in state

def holding(state, obj):
    return f"HOLDING({obj})" in state

def arm_empty(state):
    return "armepty" in state

def stack(x, y):
    return f"STACK({x},{y})"

def unstack(x, y):
    return f"UNSTACK({x},{y})"

def pickup(x):
    return f"PICKUP({x})"

def putdown(x):
    return f"PUTDOWN({x})"

def apply_action(state, action):
    if action.startswith("STACK"):
        x, y = action.strip("STACK()").split(',')
        return state.replace(f"ON({x},{y})", "").replace(f"CLEAR({y})", f"ON({x},{y})").replace("ARMEMPTY", "")
    elif action.startswith("UNSTACK"):
        x, y = action.strip("UNSTACK()").split(',')
        return state.replace(f"ON({x},{y})", f"").replace(f"CLEAR({x})", f"CLEAR({y})").replace("ARMEMPTY", f"HOLDING({x})")
    elif action.startswith("PICKUP"):
        x = action.strip("PICKUP()")
        return state.replace(f"ONTABLE({x})", "").replace(f"CLEAR({x})", "").replace("ARMEMPTY", f"HOLDING({x})")
    elif action.startswith("PUTDOWN"):
        x = action.strip("PUTDOWN()")
        return state.replace(f"HOLDING({x})", f"").replace("ARMEMPTY", f"ONTABLE({x})")

def gsp(initial_state, goal_state):
    actions = []
    current_state = initial_state

    while current_state != goal_state:
        applicable_actions = []

        for action in ["stack", "unstack", "pickup", "putdown"]:
            for item1 in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
                if action == "stack":
                    for item2 in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
                        if item1 != item2 and on_table(current_state, item1) and clear(current_state, item2):
                            applicable_actions.append(stack(item1, item2))
                elif action == "unstack":
                    for item2 in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
                        if item1 != item2 and on(current_state, item1, item2) and arm_empty(current_state):
                            applicable_actions.append(unstack(item1, item2))
                elif action == "pickup":
                    if on_table(current_state, item1) and clear(current_state, item1) and arm_empty(current_state):
                        applicable_actions.append(pickup(item1))
                elif action == "putdown":
                    if holding(current_state, item1) and arm_empty(current_state):
                        applicable_actions.append(putdown(item1))

        for action in applicable_actions:
            next_state = apply_action(current_state, action)
            if next_state not in actions:
                actions.append(action)
                current_state = next_state
                break

    return actions

# Initial state
initial_state = "on(B,A) ^ onTable(A) ^ onTable(B) ^ on(D,C) ^ onTable(C) ^ onTable(F) ^ onTable(G) ^ on(H,I) ^ on(J,H) ^ onTable(I) ^ armepty"

# Goal state
goal_state = "on(B,A) ^ onTable(A) ^ on(D,C) ^ on(E,D) ^ onTable(C) ^ on(F,G) ^ onTable(G) ^ on(H,I) ^ onTable(I) ^ onTable(J) ^ armepty"

actions = gsp(initial_state, goal_state)
for action in actions:
    print(action)
