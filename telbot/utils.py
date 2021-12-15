import json


def load_env(path):
    """load env json file"""
    with open(path) as f:
        env = json.load(f)
        return env


if __name__ == "__main__":
    env: json = load_env("env.json")
#     # print(env)
