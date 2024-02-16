# coding: utf-8

from dataclasses import dataclass, field
from typing import Union, Dict, Any
import random
import os
from dotenv import load_dotenv, find_dotenv
import requests
from datetime import datetime

load_dotenv(find_dotenv())

def get_env_var(env):
    return os.getenv(env)

def convert_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    return obj

def public_emails():
    return ["gmail.com","hotmail.com","yahoo.com","aol.com","msn.com","live.com"]

def splitEmail(email):
    email_split = email.split("@")
    username = email_split[0]
    domain = email_split[1]
    return username,domain

@dataclass
class QueryResponse:
    """All responses used in Enumerator must have `platform` and `selector`"""
    platform: str
    selector: str
    exists: Union[bool, None] = None
    metadata: Union[Dict[Any, Any], None] = None
    url: Union[str, None] = None


@dataclass
class UserAgent:

    user_agent: str = field(init=False)

    def __post_init__(self):
        self.user_agent = self.get_agent()

    def get_agent(self) -> str:
        url = "https://jnrbsn.github.io/user-agents/user-agents.json"
        response = requests.get(url)
        user_agents = response.json()
        return random.choice(user_agents)

    

    