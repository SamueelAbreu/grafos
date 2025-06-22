import re
# 2. Parser corrigido
def parse_instance_fully_correct(file_path: str):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    data = {
        "meta": {},
        "ReN": [],
        "ReE": [],
        "ReA": [],
        "NonRequiredArcs": []
    }

    section = None
    for line in lines:
        line = line.strip()
        if not line or line.startswith("the data is"):
            continue
        if line.startswith("Name:"):
            data["meta"]["name"] = line.split(":")[1].strip()
        elif line.startswith("Capacity:"):
            data["meta"]["capacity"] = int(line.split(":")[1].strip())
        elif line.startswith("Depot Node:"):
            data["meta"]["depot"] = int(line.split(":")[1].strip())
        elif re.match(r"#\w+:", line):
            key, value = line.split(":")
            data["meta"][key.strip()] = int(value.strip())
        elif line.startswith("ReN."):
            section = "ReN"
        elif line.startswith("ReE."):
            section = "ReE"
        elif line.startswith("ReA."):
            section = "ReA"
        else:
            parts = re.split(r'\s+', line)
            if section == "ReN" and len(parts) == 3 and parts[0].startswith("N"):
                nid = int(parts[0][1:])
                demand = int(parts[1])
                scost = int(parts[2])
                data["ReN"].append((nid, demand, scost))
            elif section == "ReE" and len(parts) == 6 and parts[0].startswith("E"):
                _, u, v, cost, demand, scost = parts
                data["ReE"].append((int(u), int(v), int(cost), int(demand), int(scost)))
            elif section == "ReA" and len(parts) == 6 and parts[0].startswith("A"):
                _, u, v, cost, demand, scost = parts
                data["ReA"].append((int(u), int(v), int(cost), int(demand), int(scost)))
            elif (line.startswith("NrA") or line.startswith("ARC")) and len(parts) == 4:
                _, u, v, cost = parts
                data["NonRequiredArcs"].append((int(u), int(v), int(cost)))

    return data