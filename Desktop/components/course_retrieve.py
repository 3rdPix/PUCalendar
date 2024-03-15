"""
Contains the function `search_for_courses` that uses official university API
to retrieve information of courses matching a pattern
"""
import requests
from bs4 import BeautifulSoup

def _extract_course_data(html_snippet: str) -> list:
    """
    Parse HTML from buscacursos.uc.cl to read results of the search
    """
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

def search_for_courses(search_pattern: str, year: str, semester: str) -> list:
    """
    Searches for courses that match the pattern
    -------------------------------------------
    `search_pattern: str`: any nrc-like or name-like
    `year: str`: as string, for example, `"2024"`
    `semester: str`: as string. Only "1" or "2".
    -------------------------------------------
    Returns a list with all courses matching the pattern in the form of 
    dictionaries.
    """
    name_url = f'https://buscacursos.uc.cl/?cxml_semestre=2024-1&cxml_sigla=&cxml_nrc=&cxml_nombre={search_pattern}&cxml_categoria=TODOS&cxml_area_fg=TODOS&cxml_formato_cur=TODOS&cxml_profesor=&cxml_campus=TODOS&cxml_unidad_academica=TODOS&cxml_horario_tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS'
    nrc_url = f'https://buscacursos.uc.cl/?cxml_semestre=2024-1&cxml_sigla={search_pattern}&cxml_nrc=&cxml_nombre=&cxml_categoria=TODOS&cxml_area_fg=TODOS&cxml_formato_cur=TODOS&cxml_profesor=&cxml_campus=TODOS&cxml_unidad_academica=TODOS&cxml_horario_tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS'
    name_response = requests.get(name_url).text
    nrc_response = requests.get(nrc_url).text
    courses_with_matching_name = _extract_course_data(name_response)
    courses_with_matching_nrc = _extract_course_data(nrc_response)
    return courses_with_matching_name + courses_with_matching_nrc

