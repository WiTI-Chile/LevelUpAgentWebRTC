Resumen del Funcionamiento del Algoritmo Anotador:

El algoritmo principal se encuentra en el archivo `anotador.py`, específicamente en la función `anotador()`. Esta función gestiona el proceso de anotación y sus parámetros son los siguientes:

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

Pre-requisitos:
    - Para preparar los datos que el algoritmo anotador espera, se debe utilizar el método `json_to_dataframe()` ubicado en el archivo con el nombre 'estructura()'. Este método debe recibir el JSON a completar y devuelve un DataFrame de Pandas preparado con las columnas requeridas: texto de la pregunta, posición de la pregunta en el JSON y el embedding del texto de la pregunta.
