import requests
import json
from bs4 import BeautifulSoup
sigla = '2233'
URL = f'https://buscacursos.uc.cl/?cxml_semestre=2024-1&cxml_sigla={sigla}&cxml_nrc=&cxml_nombre=&cxml_categoria=TODOS&cxml_area_fg=TODOS&cxml_formato_cur=TODOS&cxml_profesor=&cxml_campus=TODOS&cxml_unidad_academica=TODOS&cxml_horario_tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS'
respuesta = requests.get(URL)
print(respuesta.status_code)



# S-tier function

def extract_course_data(html_snippet) -> list:
    soup = BeautifulSoup(html_snippet, 'html.parser')
    rows = soup.find_all(class_=["resultadosRowPar", "resultadosRowImpar"])

    course_list = []

    for row in rows:
        columns = row.find_all('td')
        course_dict = {
            'NRC': columns[0].get_text().strip(),
            'Course Code': columns[1].get_text().strip(),
            'Course Name': columns[9].get_text().strip(),
            'Professor': columns[10].find_all('a')[0].get_text().strip(),  # Extract first professor
            'Location': columns[11].get_text().strip(),
            'Section': columns[6].get_text().strip(),  # Extract section number
            'Dates': []  # Initialize an empty list for dates
        }

        # Extract dates from the table
        table_rows = row.find_all('tr')
        for table_row in table_rows:
            date_columns = table_row.find_all('td')
            if len(date_columns) == 3:
                date_info = [date_columns[0].get_text().strip(),
                             date_columns[1].get_text().strip(),
                             date_columns[2].get_text().strip()]
                course_dict['Dates'].append(date_info)

        course_list.append(course_dict)

    return course_list
cursos = extract_course_data(respuesta.text)
for curso in cursos:
    with open(curso.get('Course Name') + '.json', 'w') as file:
        json.dump(curso, file)