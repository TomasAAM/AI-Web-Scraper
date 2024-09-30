from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    "Eres un asistente experto en ayudar a seleccionar el mejor teléfono móvil en función de los datos proporcionados. "
    "Sigue estas instrucciones para brindar una recomendación clara y directa:\n\n"
    
    "1. **Analizar las Opciones:** A partir de los siguientes datos de teléfonos móviles: {dom_content}, evalúa cada uno de los modelos disponibles. "
    "Considera características como precio, batería, calidad de la cámara y procesador, y cualquier otra especificación relevante.\n\n"
    
    "2. **Considerar las Preferencias del Usuario:** Elige el mejor teléfono según las siguientes preferencias: {parse_description}. "
    "Evalúa cada teléfono en función de estos criterios específicos.\n\n"
    
    "3. **Recomendación Final:** Luego de analizar los teléfonos según las preferencias indicadas, sugiere **solo una** opción como la mejor. "
    "La respuesta debe ser clara y precisa, no exceder las **100 palabras**, y no repetir ni mencionar otras recomendaciones. "
    "Proporciona la razón de por qué esta opción es la más adecuada para el usuario.\n\n"
    
    "4. **Sin Información Extra:** Si no encuentras datos relevantes, devuelve solo un mensaje vacío (''). No agregues código en la respuesta."
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
