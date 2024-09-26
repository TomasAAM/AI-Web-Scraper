from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "You are tasked with organizing phone data and assisting in the selection of the best phone option based on specific preferences. Follow these instructions carefully: \n\n"
    
    "1. **Create a Table:** Extract and organize the phone data from the following content: {dom_content}. "
    "You must create a table where the columns represent the phone names and their features, such as price, battery life, camera quality, etc. Ensure the table is clean and properly formatted for easy comparison.\n\n"
    
    "2. **Consider Preferences:** Once the table is created, help choose the best phone option by considering the following preferences: {parse_description}. "
    "Evaluate each phone against these preferences (e.g., prioritize battery life, camera quality, budget constraints, etc.).\n\n"
    
    "3. **Return the Best Option:** After analyzing the phones based on the provided preferences, suggest the best option. "
    "Provide a brief explanation for why this phone is the best fit given the user's preferences, but do not include unnecessary comments or explanations beyond this."
    
    "4. **No Extra Content:** If no relevant data is found, return an empty string (''). Do not include additional comments or explanations in your response beyond the requested information."
)


model = OllamaLLM(model="llama3.2")


def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)
