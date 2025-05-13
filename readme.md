# AI Agent System from Scratch

This project implements an AI agent system from scratch using Python. The system is designed to simulate a ReAct (Reasoning + Acting) loop with a single google search tool. It also involves 5 Major Agentic in AI engineering including evaluator, orchestrator, parallel execution, PromptChaining, and Routing

## Components Overview

### 1. **Evaluator**
- **Purpose**: Iteratively evaluates and improves the quality of generated summaries.
- **Key Features**:
  - Evaluates summaries based on criteria like coverage, accuracy, conciseness, and grammar.
  - Re-runs the summarization loop until the evaluator approves the summary or the maximum retries are reached.
- **File**: `evaluator.py`

### 2. **Orchestrator**
- **Purpose**: Decomposes a complex user query into sub-questions, processes them in parallel, and aggregates the results into a final response.
- **Key Features**:
  - Uses an orchestrator prompt to break down the query.
  - Runs sub-questions in parallel using worker prompts.
  - Aggregates worker responses into a comprehensive final answer.
- **File**: `orchestrator.py`

### 3. **Parallel Execution**
- **Purpose**: Executes multiple LLM calls concurrently to improve efficiency.
- **Key Features**:
  - Runs prompts on different models in parallel.
  - Aggregates responses into a single high-quality answer.
- **File**: `parallel.py`

### 4. **Prompt Chaining**
- **Purpose**: Guides the LLM through a sequence of prompts to achieve a complex task step-by-step.
- **Key Features**:
  - Supports two workflows:
    1. Passing only the previous response as input to the next step.
    2. Passing the entire accumulated context along with the original input.
  - Useful for tasks like trip planning or multi-step reasoning.
- **File**: `PromptChaining.py`

### 5. **Routing**
- **Purpose**: Selects the most appropriate model for a given user query based on its complexity and type.
- **Key Features**:
  - Uses a router prompt to decide between models like `gpt-4o`, `gpt-4o-mini`, and `o1-mini`.
  - Ensures optimal performance by matching the query to the model's strengths.
- **File**: `routing.py`

### 5. **ReAct Agent**:
## Features
- **ReAct Loop**: The agent operates in a loop of `Thought`, `Action`, `PAUSE`, and `Observation`.
- **Tool Integration**:
  - **Web Search**: Uses google search api to fetch relevant informations.
- **Customizable System Prompt**: The agent's behavior is defined by a system prompt that can be tailored to specific use cases.a
- **Extensible Design**: Additional tools and functionalities can be easily integrated.

## How It Works
1. **Thought**: The agent reasons about the question or task it has been given.
2. **Action**: The agent selects an action to perform (e.g., `search_web`).
3. **PAUSE**: The agent pauses after performing the action and waits for an observation.
4. **Observation**: The result of the action is provided as an observation.
5. **Answer**: After sufficient iterations, the agent outputs a final answer.
