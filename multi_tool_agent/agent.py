"""Main agent configuration for the hackathon project."""

import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from .tools import myTool


my_agent = Agent(
    model="gemini-2.5-flash",
    name="my_agent",
    description="Does things with stuff",
    instruction="With the stuff, you must do the thing",
    tools=[myTool]
)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Root agent for the hackathon project",
    instruction="With the stuff, you must do the thing",
    tools=[myTool]
)