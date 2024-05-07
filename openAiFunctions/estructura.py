import pandas as pd
from openAiFunctions.anotador_utils import get_embedding
import json

def json_to_dataframe(json_kam, api_key):

  dic_men = json.loads(json_kam)

  datos = []
  columns = ['Pregunta', 'Posicion']
  for i, skill in enumerate(dic_men['skills']):
    for j, dimension in enumerate(skill['dimensiones']):
      pregunta = dimension['description']
      datos.append([pregunta, (i,j)])

  df_preguntas = pd.DataFrame(datos, columns = columns)

  df_preguntas['Embedding_Pregunta'] = df_preguntas['Pregunta'].map(lambda x: get_embedding(x, api_key))

  return df_preguntas