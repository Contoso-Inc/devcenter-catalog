import os
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import MessageRole, BingGroundingTool
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

agents_client = AgentsClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

# [START create_agent_with_bing_grounding_tool]
conn_id = os.environ["BING_CONNECTION_ID"]

# Initialize agent bing tool and add the connection id
bing = BingGroundingTool(connection_id=conn_id)

# Create agent with the bing tool 
with agents_client:
    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="travel-agent",
        instructions=(
            "You are a travel assistant specializing in providing up-to-date travel recommendations. "
            "For any travel-related queries, use the Bing Grounding Tool to search for the latest and most relevant information. "
            "Summarize the results clearly and concisely before responding to the user. "
            "After answering, ask the user if they would like a customized itinerary, and if so, inquire about the number of days they plan to travel. "
            "You must only respond to travel-related questions. If the query is unrelated to travel, politely inform the user that you can only assist with travel topics."
        ),
        tools=bing.definitions,
    )
    # [END create_agent_with_bing_grounding_tool]

    print(f"Created agent, ID: {agent.id}")
