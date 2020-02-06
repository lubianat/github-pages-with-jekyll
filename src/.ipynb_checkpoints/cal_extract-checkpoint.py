import re
from icalendar import Calendar, Event
import datetime as dt
import os

def convert_curly_to_straight_quotes(text):
    text = text.replace('“', '"')
    text = text.replace('”', '"')
    return(text)



def extract_title_from_quotes(text):
    
    text = convert_curly_to_straight_quotes(text)
    pattern = r'"([\s\S]*?)"'
    m = re.findall(pattern, text)
    title = str(m).replace("\\n", " ")
    title = str(title).replace("['", "")
    title = str(title).replace("']", "")
    print(title)
    return(title)

def extract_date(phrase):
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

    for index , mes in enumerate(meses):
        if mes in phrase:
            mes_n = index + 1
            inicio_mes = phrase.find(mes) 
            dia = re.findall(r'\d+',phrase[inicio_mes-6:inicio_mes-4])[0]
        elif  "Data" in phrase:
            data_index = phrase.find("Data: ")
            dia = int(phrase[data_index+6:data_index+8])
            mes_n = int(phrase[data_index+9:data_index+11])
        else:
        #######
            pattern_dia = r'([0-9][0-9])/'
            dia = re.findall(pattern_dia, event)
            if dia:
                dia = int(dia[0])
        #######
            pattern_mes = r'/([0-9][0-9])'
            mes_n = re.findall(pattern_mes, event)
            if mes_n:
                mes_n = int(mes_n[0])
                
    if phrase.find('2020'):
        ano = "2020"
    elif phrase.find('2021'):
        ano = "2021"
    
    return(int(dia), int(mes_n), int(ano))


## Extrac time based on a dangling "h"

def extract_time(phrase):
    h_solto = phrase.find(" h\n")
    
    if h_solto != -1:
        horario = str(phrase[h_solto-2:h_solto])
    else:
        pattern = r'([0-9][0-9])h'
        horario = int(re.findall(pattern, phrase)[0])
    
    print(horario)
    return(int(horario))


def extract_place(phrase):
    locais = ['anfiteatro', 'auditório', 'auditorio']

    for index , local in enumerate(locais):
        if local in phrase.lower():
            inicio_local = phrase.lower().find(local)
            fim_local = phrase.lower().find("\n", inicio_local)
            local_final = phrase[inicio_local : fim_local]

    return(local_final)





def make_event( title, place, day, month, year, hour, minute, text = "", link = ""):
    
    event_start = dt.datetime(year, month, day, hour, minute, 0)
    event_end = dt.datetime(year, month, day, hour + 1, minute, 0)
    
    evento = Event()
    evento.add('dtstart', event_start)
    evento.add('dtend', event_end)
    # evento.add('summary', title )
    evento.add('location', place)
    evento.add('description', title + "\n" + link + "\n" + text)
    return(evento)



def magic_extract_event(phrase):
    title = extract_title_from_quotes(phrase)
    day, month, year = extract_date(phrase)
    hour = extract_time(phrase)
    place = extract_place(phrase)
    return(make_event(title,place,day,month,year,hour, minute = 0, text = phrase))


def export_event(event, directory = ".", name = "example.ics"):
    cal = Calendar()
    cal.add_component(event)
    f = open(os.path.join(directory, name), 'wb')
    f.write(cal.to_ical())
    f.close()
    
def pegar_infos_do_icb(link, cal):

    page = requests.get(link)

    soup = BeautifulSoup(page.text, 'html.parser')
# Pull all text from the BodyText div
    event_info = soup.find(class_='single_content')

# Pull text from all instances of <a> tag within BodyText div
    event_info_items = event_info.find_all('p')


    titulo = soup.find(class_='single_tit').contents[0]
    for info in event_info_items:
        if "Palestrante" in str(info.contents[0]):
            palestrante = info.contents[1]
        if "Data" in str(info.contents[0]):
            data = info.contents[1]
    
    

    event_info_items_all= event_info.find_all()

    for j, info in enumerate(event_info_items_all):
        if len(info.contents) > 2:
            for i, elem in enumerate(info.contents):
                if "Horário:" in str(elem) and len(info.contents) > i-1 :
                    horario = info.contents[i+1]
  
    event_info_items_links= event_info.find_all("a")

    for links  in event_info_items_links:
        local = links.contents[0]            
                
    for j, info in enumerate(event_info_items_all):
        if len(info.contents) > 2:
            for i, elem in enumerate(info.contents):
                if local in str(elem) and len(info.contents) > i-1 :
                    local = local + info.contents[i+1]
               
                
                
    print(link)
    print(titulo)
    print(palestrante)
    print(hora)
    print(data)
    print(local)
    
    
    
    import datetime as dt

    year = 2019
    day = int(data[1:3])
    month = int(data[4:6])

    time_start = int(horario[1:3])

    time_end = time_start + 1

    event_start = dt.datetime(year, month, day, time_start, 0, 0)
    event_end = dt.datetime(year, month, day, time_end, 0, 0)

    print(local_date.strftime('%d/%m/%Y %H:%M:%S %Z'))
    event = Event()
    event.add('dtstart', event_start)
    event.add('dtend', event_end)
    #event.add('summary', titulo )
    event.add('location', local)
    event.add('description', titulo + "\n" + palestrante + "\n" + link )
    cal.add_component(event)


    return(cal)