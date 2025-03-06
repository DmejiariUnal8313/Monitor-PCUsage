from ecologits import EcoLogits
from openai import OpenAI

# Initialize EcoLogits
EcoLogits.init()

# Define a function to perform a query
def perform_query(api_key, model, messages):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response

# Define different queries
queries = [
    {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Tell me a funny joke!"}]
    },
    {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "What's the weather like today?"}]
    },
    {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Give me a recipe for a chocolate cake."}]
    }
]

# Perform the queries and print the results
api_key = "<OPENAI_API_KEY>"
for query in queries:
    response = perform_query(api_key, query["model"], query["messages"])
    print(f"Query: {query['messages'][0]['content']}")
    print(f"Energy consumption: {response.impacts.energy.value} kWh")
    print(f"GHG emissions: {response.impacts.gwp.value} kgCO2eq")
    if response.impacts.has_warnings:
        for w in response.impacts.warnings:
            print(f"Warning: {w}")
    if response.impacts.has_errors:
        for e in response.impacts.errors:
            print(f"Error: {e}")
    print("\n")
