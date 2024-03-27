"""
Contains the function `search_for_courses` that uses official university API
to retrieve information of courses matching a pattern. Also contains classes
to represent courses.
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
            'nrc': columns[0].get_text().strip(),
            'code': columns[1].get_text().strip(),
            'name': columns[9].get_text().strip(),
            'campus': columns[11].get_text().strip(),
            'section': columns[4].get_text().strip(),  
            'dates': []  # Initialize an empty list for dates
        }

        try:
            course_dict['professor'] = \
                columns[10].find_all('a')[0].get_text().strip()
        except IndexError:
            course_dict['professor'] = 'Ninguno'

        # Extract dates from the table
        table_rows = row.find_all('tr')
        for table_row in table_rows:
            date_columns = table_row.find_all('td')
            if len(date_columns) == 3:
                date_info = [date_columns[0].get_text().strip(),
                             date_columns[1].get_text().strip(),
                             date_columns[2].get_text().strip()]
                course_dict['dates'].append(date_info)

        course_list.append(course_dict)
        
    return course_list

def search_for_puclasses(search_pattern: str,
                       year: str, semester: str) -> list[dict] | None:
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
    name_url = f'https://buscacursos.uc.cl/?cxml_semestre={year}-{semester}&cxml_sigla=&cxml_nrc=&cxml_nombre={search_pattern}&cxml_categoria=TODOS&cxml_area_fg=TODOS&cxml_formato_cur=TODOS&cxml_profesor=&cxml_campus=TODOS&cxml_unidad_academica=TODOS&cxml_horario_tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS'
    nrc_url = f'https://buscacursos.uc.cl/?cxml_semestre={year}-{semester}&cxml_sigla={search_pattern}&cxml_nrc=&cxml_nombre=&cxml_categoria=TODOS&cxml_area_fg=TODOS&cxml_formato_cur=TODOS&cxml_profesor=&cxml_campus=TODOS&cxml_unidad_academica=TODOS&cxml_horario_tipo_busqueda=si_tenga&cxml_horario_tipo_busqueda_actividad=TODOS'
    name_response = requests.get(name_url).text
    nrc_response = requests.get(nrc_url).text
    courses_with_matching_name = _extract_course_data(name_response)
    courses_with_matching_nrc = _extract_course_data(nrc_response)
    return courses_with_matching_name + courses_with_matching_nrc

class PUClass:
    """
    Main class to represent a course information, holds grades, color and
    other specifications
    """

    def __init__(self, alias: str, color: str,
                 dedicated_time: float=0.0, **kwargs: str) -> None:
        """
        Initializes the course with only an alias and its representative color.
        Can also receive other information with keys to save as part of the 
        course specific data.
        ---------------------------------------
        Basic keys:
         -'name': official name
         -'nrc': university's internal class-specific identifier
         -'code': university's internal course identifier
         -'professor': main professor
         -'campus'
         -'section'
         -'dates'
        """
        self.info: dict = {}
        self.info['alias'] = alias
        self.info['color'] = color
        self.info['dedicated_time'] = dedicated_time
        self.info.update(kwargs)

    def __str__(self) -> str:
        return f'{self.info.get('alias')} - section {self.info.get('section')}'