from openAiFunctions.anotador_utils import buscar_preguntas_similares, get_ind_pregunta
    
def anotador(texto_audio, df_preguntas, api_key):
  """
  Descripción:
      Esta función busca y devuelve la pregunta correspondiente de un JSON 
      basándose en el texto transcrito de un audio.

  Entradas:
      - df_preguntas (DataFrame): Un DataFrame de Pandas que representa el JSON. Debe incluir las 
        columnas 'texto de la pregunta', 'posición de la pregunta en el json' y 'embedding del texto de la pregunta'.
      - texto_audio (str): Texto transcrito del audio del entrevistador.
      - api_key (str): Llave de API para utilizar modelos de OpenAI.

  Salida:
      - Tupla (str, int): Contiene el texto y la posición de la pregunta correspondiente del JSON que 
        mejor se correlaciona con la sección indicada por el texto del audio. O None en caso de no corresponder a ninguna pregunta existente. 

  Ejemplo de uso:
      >>> pregunta_correspondiente = anotador(texto_audio, df_preguntas, api_key)
      >>> print(pregunta_correspondiente)
      ('Cómo te sintes con la logica de negocio?', (0, 0))
  """

  df = buscar_preguntas_similares(texto_audio, df_preguntas, api_key)

  if type(df) != type(None) and df.shape[0] >= 2:
    preg_1 = df.iloc[0,0]
    preg_2 = df.iloc[1,0]

    ind = get_ind_pregunta(texto_audio, preg_1, preg_2, api_key)

    if 0 <= ind <= 1:
      return df.iloc[ind,0], df.iloc[ind,1]

  return None