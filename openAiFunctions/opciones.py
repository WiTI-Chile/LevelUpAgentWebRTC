from openai import OpenAI

def get_opcion(pregunta, respuesta, opciones, api_key):
    """
    Utiliza la API de OpenAI para determinar cuál de las opciones proporcionadas
    corresponde mejor a una respuesta dada para una pregunta específica.

Entrada:
    pregunta (str): El texto de la pregunta a la cual se relaciona la respuesta.
    respuesta (str): El texto de la respuesta que se debe evaluar con las opciones.
    opciones (str): Una lista que representa las opciones disponibles enumerdas de 0 hasta n.
    api_key (str): La clave de API para autenticar la solicitud hacia la API de OpenAI.

Ejemplo de formato de valores de entrada:
    pregunta = '¿Cómo sientes que el equipo recibe tus opiniones?'

    respuesta = "Por su puesto, mi equipo es genial nos entendemos muy bien todos"

    opciones = "
    0. Mis opiniones son siempre valoradas y consideradas.
    1. A veces siento que mis opiniones no son tomadas en cuenta.
    2. Rara vez se consideran mis puntos de vista.
    "

Salida:
    int: El índice de la opción que más se ajusta a la respuesta proporcionada.
         Retorna -1 si ninguna opción es adecuada.

    Raises:
    ValueError: Si la respuesta de la API no puede convertirse a un entero y no es `-1`.
    """

    client = OpenAI(api_key = api_key)

    system_message = """Necesito tu ayuda para determinar cuál opción de una lista corresponde a la respuesta de una pregunta dada. Te proporcionaré el texto de la pregunta, el texto de la posible respuesta y una lista de opciones. Tu tarea es realizar un análisis cuidadoso y detallado de la respuesta en relación con cada opción para decidir cuál número de opción se ajusta mejor a la respuesta, o si ninguna opción es adecuada.

Para garantizar una selección precisa, considera tanto el contenido explícito como los matices del lenguaje utilizado en la respuesta. Evalúa cómo cada opción refleja o contrasta con la respuesta dada y toma en cuenta cualquier implicación o sentimiento expresado en la respuesta.

Aquí tienes los elementos para tu análisis:
1. Texto de la pregunta: puntaje = 5
2. Texto de la posible respuesta:
3. Lista de opciones:

Instrucciones específicas:
- Revisa cuidadosamente la respuesta y las opciones.
- Analiza si la respuesta apoya directamente alguna de las opciones, contradice alguna o si ninguna opción capta completamente el espíritu de la respuesta.
- Responde exclusivamente con el número de la opción que mejor corresponda a la respuesta proporcionada, o con '-1' si ninguna opción es adecuada.

Debes responder exclusivamente con el número de la opción que mejor corresponda a la respuesta proporcionada, o con '-1' si ninguna opción es adecuada.
"""

    user_message = f"""**Dame la respuesta para las siguinetes textos de preguntas:  **
    **Texto de la pregunta**
    {pregunta}
    **Texto de la posible respuesta:**
    {respuesta}
    **Lista de opciones:**
    {opciones}
    """

    response = client.chat.completions.create(
      model="gpt-4-1106-preview",
      messages=[
          {"role": "system", "content": system_message},
          {"role": "user", "content": user_message}
      ],
      temperature = 0.0,
      max_tokens = 5
    )

    resp = response.choices[0].message.content

    try:
        resp = int(resp)
    except:
        print('ValueError')
        resp = -1
    return resp