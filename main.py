import os
from typing import TypedDict, Annotated
import operator

import psycopg
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.budget_tool import analyze_budget
from tools.rag_tool import retrieve_context

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

# State
class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    budget_analysis: str
    rag_context: str
    itinerary: str
    llm_calls: int

# Flight Agent
def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)
    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(content=f"Flight results fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Hotel Agent
def hotel_agent(state: TravelState):

    city_code = state.get("city_code", "PAR")
    check_in = state.get("check_in", "2026-08-01")
    check_out = state.get("check_out", "2026-08-05")

    hotel_results = search_hotels(
        city_code=city_code,
        check_in=check_in,
        check_out=check_out
    )

    if not hotel_results:
        hotel_results = tavily_search(
            f"Best hotels for {state['user_query']}"
        )

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel search completed")
        ],
        "llm_calls": state.get("llm_calls", 0)
    }

#Budget Agent
def budget_agent(state: TravelState):

    prompt = f"""
    User Query:
    {state['user_query']}

    Flight Results:
    {state['flight_results']}

    Hotel Results:
    {state['hotel_results']}

    Analyze:
    1. Estimated total trip cost
    2. Cheapest option
    3. Luxury option
    4. Budget-saving suggestions
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "budget_analysis": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

#Rag Agent
def rag_agent(state: TravelState):

    context = retrieve_context(
        state["user_query"],
        k=3
    )

    return {
        "rag_context": context,
        "messages": [
            AIMessage(
                content="Travel guide context retrieved"
            )
        ],
        "llm_calls": state.get("llm_calls", 0)
    }

# Itinerary Agent
def itinerary_agent(state: TravelState):

    prompt = f"""
    Create a travel itinerary.

    User Query:
    {state['user_query']}

    Flight Results:
    {state['flight_results']}

    Budget Analysis:
    {state['budget_analysis']}

    Relevant Travel Guide / Visa / Packing Context:
    {state['rag_context']}

    Hotel Results:
    {state['hotel_results']}
    """

    response = llm.invoke([
        SystemMessage(
            content="You are an expert travel planner. Ground your itinerary in provided context."
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Final Response Agent
def final_agent(state: TravelState):

    final_prompt = f"""
    Generate final travel response.

    Flights:
    {state['flight_results']}

    Hotels:
    {state['hotel_results']}

    Budget Analysis:
    {state['budget_analysis']}

    Itinerary:
    {state['itinerary']}
    
    Rag_Agent:
    {state['rag_context']}

    """

    response = llm.invoke([
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("budget_agent", budget_agent)
graph.add_node("rag_agent", rag_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)

graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "budget_agent")
graph.add_edge("budget_agent", "rag_agent")
graph.add_edge("rag_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)


# Persistent connection so both CLI and Streamlit can share the compiled app
_conn = psycopg.connect(DATABASE_URL)
checkpointer = PostgresSaver(_conn)
checkpointer.setup()

app = graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    config = {
        "configurable": {
            "thread_id": "user_aarohi"
        }
    }

    user_input = input("Enter travel request: ")

    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "budget_analysis": "",
            "rag_context": "",
            "itinerary": "",
            "llm_calls": 0
        },
        config=config
    )


    print("\nFINAL RESPONSE:\n")

    for msg in result["messages"]:
        print(msg.content)