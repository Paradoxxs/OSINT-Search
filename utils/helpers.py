# coding: utf-8

from dataclasses import dataclass, field
from typing import Union, Dict, Any
import random
import os
from dotenv import load_dotenv, find_dotenv
import requests


load_dotenv(find_dotenv())

def get_env_var(env):
    return os.getenv(env)

@dataclass
class QueryResponse:
    """All responses used in Enumerator must have `platform` and `selector`"""
    platform: str
    selector: str
    exists: Union[bool, None] = None
    metadata: Union[Dict[Any, Any], None] = None
    url: Union[str, None] = None



def get_useragent():

    url = "https://jnrbsn.github.io/user-agents/user-agents.json"
    response = requests.get(url)
    user_agents = response.json()
    return random.choice(user_agents)


@dataclass
class UserAgent:

    user_agent: str = field(init=False)

    def __post_init__(self):
        self.user_agent = self.get_agent(self.device)

    def get_agent(self) -> str:
        url = "https://jnrbsn.github.io/user-agents/user-agents.json"
        response = requests.get(url)
        user_agents = response.json()
        return random.choice(user_agents)

    

    