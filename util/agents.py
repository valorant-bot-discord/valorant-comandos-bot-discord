import requests


def agents():
    response = requests.get("https://valorant-api.com/v1/agents")
    agents = []
    for agent in response.json()["data"]:
        if agent["isPlayableCharacter"]:
            agents.append(agent["displayName"])

    return agents
