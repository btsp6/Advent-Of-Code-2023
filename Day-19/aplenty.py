import json

with open("aplenty.in", "r") as f:
    workflows = [line.rstrip() for line in f]

workflows = {line.partition("{")[0]: line.partition("{")[2][:-1] for line in workflows}

def parse_workflow(workflow_str):
    cases = workflow_str.split(",")
    workflow = []
    for case in cases:
        if ":" in case:
            check, _, result = case.partition(":")
            workflow.append((check, result))
        else:
            workflow.append((case,))
    return workflow

workflows = {name: parse_workflow(line) for name, line in workflows.items()}

with open("parts.in", "r") as f:
    parts = [line.rstrip() for line in f]

for c in "xmas":
    parts = [line.replace(c, f'"{c}"') for line in parts]
parts = [line.replace("=", ":") for line in parts]
parts = [json.loads(line) for line in parts]
parts = [{key: int(value) for key, value in line.items()} for line in parts]

def eval_workflow(workflow, part):
    x = part["x"]
    m = part["m"]
    a = part["a"]
    s = part["s"]
    for step in workflow:
        if len(step) == 2:
            check, result = step
            if eval(check):
                return result
        else:
            return step[0]

def part1():
    accepted = []
    for part in parts:
        curr_workflow = "in"
        while True:
            result = eval_workflow(workflows[curr_workflow], part)
            if result == "A":
                accepted.append(part)
                break
            if result == "R":
                break
            curr_workflow = result
    output = 0
    for acc in accepted:
        output += sum(acc.values())
    print(output)

def part2():
    pass

part1()