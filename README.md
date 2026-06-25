# Multi-Agent-AI-Travel-Planning-Booking-Platform-with-RAG-and-Budget-Optimization

This project is a Real-World Multi-Agent AI Travel Planning  built using LangGraph.

The system uses 6 AI agents that work together to plan a complete trip automatically.

## Features

- ✈️ Flight Search Agent
- 🏨 Hotel Search Agent
- 🗓️ Itinerary Planning Agent
- 💰Budget Optimization Agent
- 📚RAG Knowledge Retrieval
- 🤖 Final Response Agent
- 🧠 Memory using PostgreSQL
- 🌐 Real-time API Integration
- 💻 Streamlit Web Interface

---

# Tech Stack

- LangGraph
- LangChain
- Groq
- Llama 3.3 70B
- PostgreSQL
- Streamlit
- Tavily API
- AviationStack API
- RAG (Retrieval-Augmented Generation)
- Python

---

## ✈️ End-To-End Travel Planning Powered by Multi Agent AI and RAG 
![image alt](https://github.com/Darshansrr/Multi-Agent-AI-Travel-Planning-Booking-Platform-with-RAG-and-Budget-Optimization/blob/a5063a73af9ee00bfc09f0d183e0f3516a9bac00/file_000000006cec7206b5f928538f0c631e.png)

## Video Demo

[video Demo](https://github.com/Darshansrr/Multi-Agent-AI-Travel-Planning-Booking-Platform-with-RAG-and-Budget-Optimization/blob/e39f7ca6fdbc79d4935da1dfeffdd4e5df25fb92/video_20260625_171848.mp4)

# Step 1: Create Python Environment

Open the terminal inside the project folder and run:

		python -m venv langgraph_env3


Now activate the environment:

#### Windows

		langgraph_env3\Scripts\activate

---

# Step 2: Install Dependencies

Run the following command:

		pip install langgraph langchain langchain-openai langchain-groq langchain-community langchain-tavily psycopg[binary] psycopg_pool python-dotenv tavily-python requests streamlit

		pip install -U "psycopg[binary,pool]"  langgraph-checkpoint-postgres

---

# Step 3: Install PostgreSQL

Download and install PostgreSQL: https://www.postgresql.org/download/

⚠️ Important:
While installing PostgreSQL, remember:
- PostgreSQL Password
- Port Number

You will need them later while creating the database connection string.

---

# Step 4: Create Database

Open PostgreSQL and run:

CREATE DATABASE langgraph_memory_demo;


---

# Step 5: Setup `.env` File

Create a `.env` file inside the project folder.

Add the following keys:

GROQ_API_KEY=your_groq_api_key

TAVILY_API_KEY=your_tavily_api_key

AVIATIONSTACK_API_KEY=your_aviationstack_api_key

DATABASE_URL=postgresql://username:password@localhost:5433/databasename


---

# Step 6: Get API Keys [For Free, Just Login]

## Get Groq API Key

https://console.groq.com

---

## Get Tavily API Key

https://tavily.com
  
---

## Get AviationStack API Key

https://aviationstack.com

---

# Step 7: Run the Application

#### Run Multi-Agent System in Terminal

		python main.py


This will test the multi-agent system through the terminal.

---

#### Run Streamlit Web App


		streamlit run frontend.py


This will launch the Multi-Agent AI web application.

---


---

## Project Workflow

1. Flight Agent retrieves flight information.
2. Hotel Agent searches accommodation options.
3. Budget Agent analyzes overall trip cost.
4. RAG Agent retrieves travel-related knowledge and guidelines.
5. Itinerary Agent generates a personalized travel plan.
6. Final Agent combines all outputs into a comprehensive response.
7. PostgreSQL stores conversation memory.


## System Architecture

```text
User Query
      │
      ▼
┌─────────────────────┐
│ LangGraph Workflow  │
└──────────┬──────────┘
           │
           ├── Flight Agent ──► AviationStack API
           ├── Hotel Agent ───► Hotel Search API
           ├── RAG Agent ─────► Travel Knowledge Base
           │
           ▼
┌─────────────────────┐
│ Budget Optimization │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Itinerary Planning  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Final Response      │
└──────────┬──────────┘
           ▼
 PostgreSQL Memory
           │
           ▼
   Streamlit Frontend
```

## Future Enhancements

- Flight and hotel booking integration
- Multi-currency budget planning
- Personalized recommendations based on user preferences
- Voice-enabled travel assistant
- Multi-language support
- Email and PDF itinerary export
- Live travel alerts and notifications
- Mobile application support

 ## Business Impact

- Automates end-to-end travel planning using a multi-agent AI architecture.
- Optimizes trip costs through budget-aware recommendation strategies.
- Enhances decision-making with real-time travel data and RAG-based knowledge retrieval.
- Delivers personalized travel itineraries by coordinating specialized AI agents.
- Improves user experience by consolidating flights, hotels, budgeting, and travel insights into a single platform.
        
## Key Capabilities

- Multi-Agent AI Orchestration
- Budget-Aware Travel Planning
- Knowledge Retrieval using RAG
- Personalized Itinerary Generation
- Persistent Memory with PostgreSQL
- Real-Time Travel Data Integration

## Example Prompt

Plan a 7-day Japan trip including flights, hotels, sightseeing, visa requirements, and budget optimization under ₹2 Lakhs


