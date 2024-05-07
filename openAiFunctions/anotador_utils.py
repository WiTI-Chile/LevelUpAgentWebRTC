
from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_ind_pregunta(text_audio, pregunta_1, pregunta_2, api_key):

  client = OpenAI(api_key = api_key)

  system_message = """Necesito tu asistencia para analizar fragmentos de texto de entrevistas y determinar con cuál de las dos preguntas proporcionadas se relaciona más cada fragmento. Te proporcionaré el texto de la entrevista y las dos preguntas. Debes evaluar el contenido y el contexto del texto para decidir si se relaciona más con la primera pregunta, con la segunda, o si no se relaciona con ninguna de ellas.

Se te proporcionará el texto de la entrevista y las dos preguntas para tu análisis:
1. Texto de la entrevista
2. Pregunta 1
3. Pregunta 2

Aquí tienes un ejemplo de cómo estructurar tu respuesta:
- Responde con '1' si el texto se relaciona principalmente con la primera pregunta.
- Responde con '2' si el texto se relaciona principalmente con la segunda pregunta.
- Responde con '-1' si el texto no se relaciona con ninguna de las preguntas.

Por favor, asegúrate de considerar el contexto y los detalles específicos tanto del texto de la entrevista como de las preguntas para hacer tu evaluación.

¿Con cuál pregunta crees que se relaciona más el texto de la entrevista?

Debes responder solo con el valor que corresponde sin argumentar ni introducir nada.
"""

  user_message = f"""**Dame la respuesta para los siguinetes texto de la entrevista y las dos preguntas:**
    **Texto de la entrevista**
    {text_audio}

    **Pregunta 1:**
    {pregunta_1}

    **Pregunta 2:**
    {pregunta_2}
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
    resp = int(resp) - 1
  except:
    print('error')
    resp = -1

  return resp

def get_embedding(text, api_key, model="text-embedding-3-large"):

  client = OpenAI(api_key = api_key)

  text = text.lower().strip().replace("\n", " ")

  try:
    res = client.embeddings.create(input = [text], model=model).data[0].embedding
    return res
  except:
    return None
  

def buscar_preguntas_similares(pregunta, df_preguntas, api_key, n_resultados=2):
    df = df_preguntas.copy()

    # Obtener el embedding para la pregunta dada
    busqueda_embed = get_embedding(pregunta, api_key, model='text-embedding-3-large')
    if busqueda_embed is None:
        #print("No se pudo obtener el embedding para la pregunta.")
        return None
    try:
      # Asegurarse de que el embedding de búsqueda esté en el formato correcto (2D)
      busqueda_embed_2d = np.array(busqueda_embed).reshape(1, -1)

      def calculate_similarity(embedding):
          if embedding is not None and not np.isnan(embedding).any():
              # Asegurarse que el embedding esté en formato 2D
              embedding_2d = np.array(embedding).reshape(1, -1)
              return cosine_similarity(embedding_2d, busqueda_embed_2d)[0][0]
          else:
              return -1

      # Calcular la similitud
      df["Similitud"] = df['Embedding_Pregunta'].map(calculate_similarity)

      # Ordenar los resultados por similitud
      df = df.sort_values("Similitud", ascending=False)
    except:
      return None

    return df.iloc[:n_resultados]