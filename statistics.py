import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36'}
# url = 'https://www.khl.ru/clubs/dynamo_msk/'

team_id = {
    'Ак Барс': '0', 'Сибирь': '1', 'Автомобилист': '2', 'Трактор': '3', 'Нефтехимик': '4', 'Металлург Мг': '5', 'Авангард': '6',
'Адмирал': '7', 'Барыс': '8', 'Салават Юлаев': '9', 'Амур': '10', 'Куньлунь РС': '11', 'СКА': '12', 'Динамо Мск': '13', 'Йокерит': '14',
'Спартак': '15', 'Северсталь': '16', 'Динамо Р': '17', 'ЦСКА': '18', 'Витязь': '19', 'Торпедо НН': '20', 'Локомотив': '21',
'Динамо Мн': '22', 'ХК Сочи': '23'
}

season = '0'


def actually_games_parse(headers, url):
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        print('OK')
        soup = bs(request.content, 'html.parser')
        div = soup.find_all('div', class_='b-half_block')
        upcoming_games = div[0].find_all('li', class_='b-wide_tile_item')
        upcoming_game_homes = []
        upcoming_game_guests = []
        upcoming_game_dates = []
        upcoming_game_urls = []
        for i in range(len(upcoming_games) - 1):
            upcoming_game_homes.append(upcoming_games[i].find_all('b')[0].text.strip())
            upcoming_game_dates.append(upcoming_games[i].find_all('b')[1].text.strip())
            upcoming_game_guests.append(upcoming_games[i].find_all('b')[2].text.strip())
            upcoming_game_urls.append('https://www.khl.ru' + upcoming_games[i].find('li').a['href'])
        print(upcoming_game_homes)
        print(upcoming_game_dates)
        print(upcoming_game_guests)
        print(upcoming_game_urls)

        last_games = div[1].find_all('li', class_='b-wide_tile_item')
        last_games_homes = []
        last_games_guests = []
        last_games_dates = []
        last_games_urls = []
        for i in range(len(last_games) - 1):
            last_games_homes.append(last_games[i].find_all('b')[0].text.strip())
            last_games_dates.append(last_games[i].find_all('b')[1].text.strip())
            last_games_guests.append(last_games[i].find_all('b')[2].text.strip())
            last_games_urls.append('https://www.khl.ru' + last_games[i].find('li').a['href'])
        print(last_games_homes)
        print(last_games_dates)
        print(last_games_guests)
        print(last_games_urls)
    else:
        print('ERROR')

#######################################################################################################################
############################ Парсинг информации о матче ###############################################################
#######################################################################################################################

def penalty_per_game_parse(soup):
    goals_wrapper = soup.find('div', class_='dataTables_wrapper').table.tbody.find_all('tr')
    home_penalty = []
    home_penalty_total = []
    guest_penalty = []
    guest_penalty_total = []
    guest = False
    total = False
    for i in goals_wrapper:
        for j in i.find_all('td'):
            if j.text.strip() == 'Итого':
                break
            if len(j.text.strip()) == 0:
                guest = True
            if guest == True:
                if j.text.strip().find('Всего') != -1 or total == True:
                    if len(j.text.strip()) > 0:
                        guest_penalty_total.append(j.text.strip())
                    total = True
                    continue
                if len(j.text.strip()) > 0:
                    guest_penalty.append(j.text.strip())
            else:
                if j.text.strip().find('Всего') != -1 or total == True:
                    home_penalty_total.append(j.text.strip())
                    total = True
                    continue
                home_penalty.append(j.text.strip())
        guest = False
        total = False
    penalties = []

    for i in range(0, len(home_penalty), 4):
        penalty = {}
        penalty['time'] = home_penalty[i]
        i += 1
        penalty['player_name'] = home_penalty[i]
        i += 1
        penalty['duration'] = home_penalty[i]
        i += 1
        penalty['reason'] = home_penalty[i]
        penalties.append(penalty)

    for i in range(0, len(home_penalty), 4):
        penalty = {}
        penalty['time'] = home_penalty[i]
        i += 1
        penalty['player_name'] = home_penalty[i]
        i += 1
        penalty['duration'] = home_penalty[i]
        i += 1
        penalty['reason'] = home_penalty[i]
        penalties.append(penalty)

    print(penalties)
    # print(home_penalty)
    # print(guest_penalty)
    # print(home_penalty_total)
    # print(guest_penalty_total)


def uneven_strenght(soup):
    tds_uneven_strength_home = soup.find_all('div', class_='dataTables_wrapper')[1].table.tbody.find_all('tr')[0].find_all('td')
    uneven_strenght_home = {
        'powerplay_count': tds_uneven_strength_home[1].text, 'powerplay_goals_count': tds_uneven_strength_home[2].text,
        'implemented_powerplay_percent': tds_uneven_strength_home[3].text, 'powerplay_missed_goals_count': tds_uneven_strength_home[4].text,
        'shorthand_count': tds_uneven_strength_home[5].text, 'shorthanded_missed_goals_count': tds_uneven_strength_home[6].text,
        'implemented_shorthand_percent': tds_uneven_strength_home[7].text, 'shorthanded_goals_count': tds_uneven_strength_home[8].text,
        'team': team_id[tds_uneven_strength_home[0].text]
    }

    tds_uneven_strength_guest = soup.find_all('div', class_='dataTables_wrapper')[1].table.tbody.find_all('tr')[1].find_all('td')
    uneven_strenght_guest = {
        'powerplay_count': tds_uneven_strength_guest[1].text, 'powerplay_goals_count': tds_uneven_strength_guest[2].text,
        'implemented_powerplay_percent': tds_uneven_strength_guest[3].text,
        'powerplay_missed_goals_count': tds_uneven_strength_guest[4].text,
        'shorthand_count': tds_uneven_strength_guest[5].text,
        'shorthanded_missed_goals_count': tds_uneven_strength_guest[6].text,
        'implemented_shorthand_percent': tds_uneven_strength_guest[7].text,
        'shorthanded_goals_count': tds_uneven_strength_guest[8].text,
        'team': team_id[tds_uneven_strength_guest[0].text]
    }
    print(uneven_strenght_home)
    print(uneven_strenght_guest)


def goal_scores(soup):
    tds_scores_home = soup.find_all('div', class_='dataTables_wrapper')[2].table.tbody.find_all('tr')[0].find_all('td')
    goal_scores_home = {
        '5x5_goals_count': tds_scores_home[2].text, '5x4_goals_count': tds_scores_home[3].text,
        '5x3_goals_count': tds_scores_home[4].text, '4x4_goals_count': tds_scores_home[5].text,
        '4x3_goals_count': tds_scores_home[6].text, '3x3_goals_count': tds_scores_home[7].text,
        '3x4_goals_count': tds_scores_home[8].text, '3x5_goals_count': tds_scores_home[9].text,
        '4x5_goals_count': tds_scores_home[10].text, 'empty_net_goals_count': tds_scores_home[11].text,
        'bullit_goals_count': tds_scores_home[12].text, 'total_goals_count':  tds_scores_home[13].text,
        'team': team_id[tds_scores_home[0].text]
    }

    tds_scores_guest = soup.find_all('div', class_='dataTables_wrapper')[2].table.tbody.find_all('tr')[1].find_all('td')
    goal_scores_guest = {
        '5x5_goals_count': tds_scores_guest[2].text, '5x4_goals_count': tds_scores_guest[3].text,
        '5x3_goals_count': tds_scores_guest[4].text,
        '4x4_goals_count': tds_scores_guest[5].text, '4x3_goals_count': tds_scores_guest[6].text,
        '3x3_goals_count': tds_scores_guest[7].text,
        '3x4_goals_count': tds_scores_guest[8].text, '3x5_goals_count': tds_scores_guest[9].text,
        '4x5_goals_count': tds_scores_guest[10].text,
        'empty_net_goals_count': tds_scores_guest[11].text, 'bullit_goals_count': tds_scores_guest[12].text,
        'total_goals_count': tds_scores_guest[13].text,
        'team': team_id[tds_scores_guest[0].text]
    }
    print(goal_scores_home)
    print(goal_scores_guest)


def goal_against(soup):
    tds_against_home = soup.find_all('div', class_='dataTables_wrapper')[3].table.tbody.find_all('tr')[0].find_all('td')
    goal_against_home = {
        '5x5_miss_count': tds_against_home[2].text, '5x4_miss_count': tds_against_home[3].text,
        '5x3_miss_count': tds_against_home[4].text, '4x4_miss_count': tds_against_home[5].text,
        '4x3_miss_count': tds_against_home[6].text, '3x3_miss_count': tds_against_home[7].text,
        '3x4_miss_count': tds_against_home[8].text, '3x5_miss_count': tds_against_home[9].text,
        '4x5_miss_count': tds_against_home[10].text, 'empty_net_miss_count': tds_against_home[11].text,
        'bullit_miss_count': tds_against_home[12].text, 'total_miss_count': tds_against_home[13].text,
        'team': team_id[tds_against_home[0].text]
    }

    tds_against_guest = soup.find_all('div', class_='dataTables_wrapper')[3].table.tbody.find_all('tr')[1].find_all('td')
    goal_against_guest = {
        '5x5_miss_count': tds_against_guest[2].text, '5x4_miss_count': tds_against_guest[3].text,
        '5x3_miss_count': tds_against_guest[4].text,
        '4x4_miss_count': tds_against_guest[5].text, '4x3_miss_count': tds_against_guest[6].text,
        '3x3_miss_count': tds_against_guest[7].text,
        '3x4_miss_count': tds_against_guest[8].text, '3x5_miss_count': tds_against_guest[9].text,
        '4x5_miss_count': tds_against_guest[10].text,
        'empty_net_miss_count': tds_against_guest[11].text, 'bullit_miss_count': tds_against_guest[12].text,
        'total_miss_count': tds_against_guest[13].text,
        'team': team_id[tds_against_guest[0].text]
    }
    print(goal_against_home)
    print(goal_against_guest)

# узнать id периодов
def shots_on_goal(soup):
    j = 0
    for i in soup.find_all('div', class_='dataTables_wrapper')[4].table.tbody.find_all('tr'):
        buf = i.find_all('td')
        shots_on_goal_home = {
            'goals_count': buf[1].text.strip(), 'shoots_count': buf[2].text.strip(),
            'implemented_goal_shoot_percent': buf[3].text.strip(), 'time_period_id': j
        }
        shots_on_goal_guest = {
            'goals_count': buf[4].text.strip(), 'shoots_count': buf[5].text.strip(),
            'implemented_goal_shoot_percent': buf[6].text.strip(), 'time_period_id': j
        }

        j += 1
        print(shots_on_goal_home)
        print(shots_on_goal_guest)


def other_indicators(soup):
    j = 0
    for i in soup.find_all('div', class_='dataTables_wrapper')[5].table.tbody.find_all('tr'):
        buf = i.find_all('td')
        indicators_home = {
            'blocked_shots_count': buf[1].text.strip(), 'body_contact_count': buf[2].text.strip(),
            'attack_time': buf[3].text.strip(), 'time_period_id': j
        }
        indicators_guest = {
            'goals_count': buf[4].text.strip(), 'shoots_count': buf[5].text.strip(),
            'implemented_goal_shoot_percent': buf[6].text.strip(), 'time_period_id': j
        }

        j += 1
        print(indicators_home)
        print(indicators_guest)


def game_protocol_parse(headers, url):
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        print('OK')
        soup = bs(request.content, 'html.parser')
        penalty_per_game_parse(soup)
        uneven_strenght(soup)
        goal_scores(soup)
        goal_against(soup)
        shots_on_goal(soup)
        other_indicators(soup)

    else:
        print('ERROR')

#######################################################################################################################
############################ Парсинг резюме матча #####################################################################
#######################################################################################################################

def goal_stats(soup):
    div = soup.find('div', class_='b-text_translation_cover').find_all('div', class_='b-txt_block')
    div1 = soup.find('div', class_='b-text_translation_cover').find_all('div', class_='b-center_scale_point')
    home_score = ['0']
    for i in range(len(div)):
        print(div1[i].find('span', class_='e-event_time').text)
        print(div1[i].h3.text)
        change = div1[i].h3.b.text
        if home_score[0] != div1[i].h3.b.text and change > home_score[0]:
            print('home scores!')
            home_score[0] = change

        else:
            print('guest scores!')

        assists = []
        author_goal = div[i].h5.a.text
        status = div[i].p.text
        for j in div[i].find_all('p', class_='e-action_player'):
            assists.append(j.text)
        print(author_goal)
        print(assists)
        print(status)


def stats_per_game(soup):
    round_items = soup.find_all('li', class_='e-round_diagram_item')
    team_names = soup.find_all('div', class_='e-header-info')
    some_informations = soup.find('div', class_='b-line-structure b-small_tablet_block').find_all('li', class_='b-wide_line_item')

    home_team = {
        'goals_count': round_items[0].input['value'],
        'shoots_count': round_items[1].input['value'],
        'powerplay_goals_count': some_informations[0].find_all('td')[0].text.strip(),
        'shorthanded_goals_count': some_informations[1].find_all('td')[0].text.strip(),
        'powerplay_count': some_informations[2].find_all('td')[0].text.strip(),
        'faceoff_wins_count': some_informations[3].find_all('td')[0].text.strip(),
        'penalty_time': some_informations[4].find_all('td')[0].text.strip(),
        'distance': some_informations[5].find_all('td')[0].text.strip(),
        'puck_owned_time': some_informations[6].find_all('td')[0].text.strip(),
        'team': team_id[team_names[0].text.strip()]
    }

    guest_team = {
        'goals_count': round_items[2].input['value'],
        'shoots_count': round_items[3].input['value'],
        'powerplay_goals_count': some_informations[0].find_all('td')[2].text.strip(),
        'shorthanded_goals_count': some_informations[1].find_all('td')[2].text.strip(),
        'powerplay_count': some_informations[2].find_all('td')[2].text.strip(),
        'faceoff_wins_count': some_informations[3].find_all('td')[2].text.strip(),
        'penalty_time': some_informations[4].find_all('td')[2].text.strip(),
        'distance': some_informations[5].find_all('td')[2].text.strip(),
        'puck_owned_time': some_informations[6].find_all('td')[2].text.strip(),
        'team': team_id[team_names[1].text.strip()]
    }
    print(home_team)
    print(guest_team)


def resume_game_parse(headers, url):
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        print('OK')
        soup = bs(request.content, 'html.parser')
        # goal_stats(soup)
        stats_per_game(soup)

    else:
        print('ERROR')

#######################################################################################################################
############################ Парсинг статистики команды ###############################################################
#######################################################################################################################

def periods_stats_parse(url, session):
    urls = ['first-period', 'second-period', 'two-periods', 'third-period', 'three-periods', 'overtime']
    id = 0
    for i in urls:
        alt_url = url + i + '/'
        request = session.get(alt_url, headers=headers)
        id += 1
        if request.status_code == 200:
            print('OK')
            soup = bs(request.content, 'html.parser')
            for k in soup.find('table', id='teams_dataTable').find_all('tr'):
                kk = k.find_all('td')
                if len(kk) != 0:
                    stats = {'team': team_id[kk[0].text.strip()],
                    'win_period count': kk[2].text.strip(), 'draw_period_count': kk[3].text.strip(),
                    'lose_period_count': kk[4].text.strip(), 'score_count': kk[5].text.strip(),
                    'game_without_goals_count': kk[6].text.strip(), 'shutout_games_count': kk[7].text.strip(),
                    'goals_count': kk[8].text.strip(), 'missed_count': kk[9].text.strip(), 'penalty_time': kk[10].text.strip(),
                    'against_penalty_time': kk[11].text.strip(), 'time_period_id': id
                    }
                    print(stats)
        else:
            print('ERROR')


def bullits_game_stats_parse(url, session):
    alt_url = url + 'shootouts/'
    request = session.get(alt_url, headers=headers)
    if request.status_code == 200:
        print('OK')
        soup = bs(request.content, 'html.parser')
        for k in soup.find('table', id='teams_dataTable').find_all('tr'):
            kk = k.find_all('td')
            if len(kk) != 0:
                stats = {
                    'team': team_id[kk[0].text.strip()], 'bullits_game_count': kk[3].text.strip(), 'wins_count': kk[4].text.strip(),
                        'lose_count': kk[5].text.strip(), 'bullits_shoot_count': kk[6].text.strip(),
                        'bullits_goal_count': kk[7].text.strip(), 'bullits_goal_count_percent': kk[8].text.strip(),
                        'against_bullits_shoot_count': kk[9].text.strip(), 'against_bullits_goals_count': kk[10].text.strip(),
                        'against_bullits_goal_count_percent': kk[11].text.strip()
                        }
                if kk[11].text.strip() == '-':
                    stats['against_bullits_goal_count_percent'] = 0
                if kk[8].text.strip() == '-':
                    stats['bullits_goal_count_percent'] = 0
                print(stats)
        else:
            print('ERROR')


def foules_parse(url, session):
    alt_url = url + 'foules/'
    request = session.get(alt_url, headers=headers)
    if request.status_code == 200:
        print('OK')
        soup = bs(request.content, 'html.parser')
        for k in soup.find('table', id='teams_dataTable').find_all('tr'):
            kk = k.find_all('td')
            if len(kk) != 0:
                stats = {'team': team_id[kk[0].text.strip()],
                    '2_minutes_penalty_count': kk[3].text.strip(), '5_minutes_penalty_count': kk[4].text.strip(),
                    '10_minutes_penalty_count': kk[5].text.strip(), '20_minutes_penalty_count': kk[6].text.strip(),
                    '25_minutes_penalty_count': kk[7].text.strip(), 'penalty_shoot_count': kk[8].text.strip(),
                    'team_penalty_time': kk[9].text.strip(), 'goalkeeper_penalty_time': kk[10].text.strip(),
                    'home_penalty_time': kk[11].text.strip(), 'road_penalty_time': kk[12].text.strip(),
                    'total_penalty_time': kk[13].text.strip(), 'average_penalty_time_per_game': kk[14].text.strip(),
                    'against_total_penalty_time': kk[15].text.strip(),
                    'against_average_penalty_time_per_game': kk[16].text.strip()
                    }
                print(stats)
        else:
            print('ERROR')


def shots_parse(url, session):
    alt_url = url + 'shots/'
    request = session.get(alt_url, headers=headers)
    if request.status_code == 200:
        print('OK')
        soup = bs(request.content, 'html.parser')
        for k in soup.find('table', id='teams_dataTable').find_all('tr'):
            kk = k.find_all('td')
            if len(kk) != 0:
                stats = {'team': team_id[kk[0].text.strip()],
                    'home_goal_shoots_count': kk[2].text.strip(), 'home_implemented_goal_shoots_count': kk[3].text.strip(),
                    'home_implemented_goal_shoots_percent': kk[4].text.strip(), 'guest_goal_shoots_count': kk[5].text.strip(),
                    'guest_implemented_goal_shoots_count': kk[6].text.strip(),
                    'guest_implemented_goal_shoots_percent': kk[7].text.strip(),
                    'total_goal_shoots_count': kk[8].text.strip(), 'total_implemented_goal_shoots_count': kk[9].text.strip(),
                    'total_implemented_goal_shoots_percent': kk[10].text.strip()
                    }
                print(stats)
        else:
            print('ERROR')


def pp_parse(url, session):
    alt_url = url + 'powerplay-gf/'
    stats = {}
    request = session.get(alt_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        for k in soup.find('table', id='teams_dataTable').find_all('tr'):
            kk = k.find_all('td')
            if len(kk) != 0:
                stats['team'] = team_id[kk[0].text.strip()]
                stats['powerplays_count'] = kk[3].text.strip()
                stats['powerplay_goals_count'] = kk[4].text.strip()
                stats['implemented_powerplays_percent'] = kk[5].text.strip()
                stats['missed_goals_powerplays_count'] = kk[6].text.strip()
                stats['shorthanded_count'] = kk[7].text.strip()
                stats['shorthanded_goals_count'] = kk[8].text.strip()
                stats['implemented_shorthanded_percent'] = kk[9].text.strip()
                stats['missed_goals_shorthanded_count'] = kk[10].text.strip()
                print(stats)
        else:
            print('ERROR')


def goals_for(url, session):
    alt_url = url + 'goals-for/'
    request = session.get(alt_url, headers=headers)
    stats = {}
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        for k in soup.find('table', id='teams_dataTable').find_all('tr'):
            kk = k.find_all('td')
            if len(kk) != 0:
                stats['team'] = team_id[kk[0].text.strip()]
                stats['5x5_goals_count'] = kk[3].text.strip()
                stats['5x4_goals_count'] = kk[4].text.strip()
                stats['5x3_goals_count'] = kk[5].text.strip()
                stats['4x4_goals_count'] = kk[6].text.strip()
                stats['4x3_goals_count'] = kk[7].text.strip()
                stats['3x3_goals_count'] = kk[8].text.strip()
                stats['3x4_goals_count'] = kk[9].text.strip()
                stats['3x5_goals_count'] = kk[10].text.strip()
                stats['4x5_goals_count'] = kk[11].text.strip()
                stats['empty_net_goals_count'] = kk[12].text.strip()
                stats['bullit_goals_count'] = kk[13].text.strip()
                stats['total_goals_count'] = kk[14].text.strip()
                stats['average_goals_count_per_game'] = kk[15].text.strip()
                print(stats)
        else:
            print('ERROR')


def goals_against(url, session):
    alt_url = url + 'goals-against/'
    request = session.get(alt_url, headers=headers)
    stats = {}
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        for k in soup.find('table', id='teams_dataTable').find_all('tr'):
            kk = k.find_all('td')
            if len(kk) != 0:
                stats['team'] = team_id[kk[0].text.strip()]
                stats['5x5_miss_count'] = kk[3].text.strip()
                stats['5x4_miss_count'] = kk[4].text.strip()
                stats['5x3_miss_count'] = kk[5].text.strip()
                stats['4x4_miss_count'] = kk[6].text.strip()
                stats['4x3_miss_count'] = kk[7].text.strip()
                stats['3x3_miss_count'] = kk[8].text.strip()
                stats['3x4_miss_count'] = kk[9].text.strip()
                stats['3x5_miss_count'] = kk[10].text.strip()
                stats['4x5_miss_count'] = kk[11].text.strip()
                stats['empty_net_miss_count'] = kk[12].text.strip()
                stats['bullit_miss_count'] = kk[13].text.strip()
                stats['total_miss_count'] = kk[14].text.strip()
                stats['average_miss_count_per_game'] = kk[15].text.strip()
                print(stats)
        else:
            print('ERROR')


def home_and_road_stats(url, session):
    urls = ['home', 'road']
    id = 1
    for i in urls:
        alt_url = url + i + '/'
        request = session.get(alt_url, headers=headers)
        id += 1
        if request.status_code == 200:
            print('OK')
            soup = bs(request.content, 'html.parser')
            for k in soup.find('table', id='teams_dataTable').find_all('tr'):
                kk = k.find_all('td')
                if len(kk) != 0:
                    stats = {'id': id}
                    stats['team'] = team_id[kk[0].text.strip()]
                    stats['games_count'] = kk[2].text.strip()
                    stats['win_count'] = kk[3].text.strip()
                    stats['overtime_win_count'] = kk[4].text.strip()
                    stats['bullit_wins_count'] = kk[5].text.strip()
                    stats['bullit_lose_count'] = kk[6].text.strip()
                    stats['overtime_lose_count'] = kk[7].text.strip()
                    stats['lose_count'] = kk[8].text.strip()
                    stats['goalless_games_count'] = kk[10].text.strip()
                    stats['shutout_games_count'] = kk[11].text.strip()
                    stats['score_count'] = kk[9].text.strip()
                    stats['goals_count'] = kk[12].text.strip()
                    stats['miss_goals_count'] = kk[13].text.strip()
                    stats['penalty_time'] = kk[14].text.strip()
                    stats['penalty_time_against'] = kk[15].text.strip()
                    print(stats)
        else:
            print('ERROR')


def parse_team_stats(headers, url):
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        print('OK')
        soup = bs(request.content, 'html.parser')
        for i in soup.find('table', id='teams_dataTable').find_all('tr'):
            kk = i.find_all('td')
            if len(kk) != 0:
                stats = {}
                stats['team'] = team_id[kk[0].text.strip()]
                stats['games_count'] = kk[2].text.strip()
                stats['win_count'] = kk[3].text.strip()
                stats['overtime_wins_count'] = kk[4].text.strip()
                stats['bullit_wins_count'] = kk[5].text.strip()
                stats['bullit_lose_count'] = kk[6].text.strip()
                stats['overtime_lose_count'] = kk[7].text.strip()
                stats['lose_count'] = kk[8].text.strip()
                stats['goalless_games_count'] = kk[10].text.strip()
                stats['shutout_games_count'] = kk[11].text.strip()
                stats['score_count'] = kk[9].text.strip()
                stats['goals_count'] = kk[12].text.strip()
                stats['miss_goals_count'] = kk[13].text.strip()
                stats['penalty_time'] = kk[14].text.strip()
                stats['penalty_time_against'] = kk[15].text.strip()
                stats['season'] = season
                stats['type_of_game'] = '2'

                url = "http://127.0.0.1:8000/api/hockey_app/team_main_stats/"

                local_id = requests.request("GET", url, headers=headers)
                print(local_id.text)

                payload = "{" \
                          "\"games_count\": "           + stats['games_count'] + "," \
                          "\"win_count\":"              + stats['win_count'] + "," \
                          "\"overtime_wins_count\": "   + stats['overtime_wins_count'] + "," \
                          "\"lose_count\": "            + stats['lose_count'] + "," \
                          "\"shutout_games_count\": "   + stats['shutout_games_count'] + "," \
                          "\"goalless_games_count\": "  + stats['goalless_games_count'] + "," \
                          "\"bullit_wins_count\": "     + stats['bullit_wins_count'] + "," \
                          "\"score_count\": "           + stats['score_count'] + "," \
                          "\"goals_count\": "           + stats['goals_count'] + "," \
                          "\"miss_goals_count\": "      + stats['miss_goals_count'] + "," \
                          "\"penalty_time\": "          + stats['penalty_time'] + "," \
                          "\"penalty_time_against\": "  + stats['penalty_time_against'] + "," \
                          "\"team\": "                  + stats['team'] + "," \
                          "\"season\": "                + stats['season'] + "," \
                          "\"type_of_game\": 2," \
                          "\"bullit_lose_count\": "     + stats['bullit_lose_count'] + "," \
                          "\"overtime_lose_count\": "   + stats['overtime_lose_count'] + "}"

                headers = {
                    'Content-Type': "application/json",
                    'User-Agent': "PostmanRuntime/7.17.1",
                    'Accept': "*/*",
                    'Cache-Control': "no-cache",
                    'Postman-Token': "3d53cec3-5067-420c-919d-f8bc428c0c59,71a71433-ae6d-45da-91c2-cbb57e7c9e3c",
                    'Host': "127.0.0.1:8000",
                    'Accept-Encoding': "gzip, deflate",
                    'Content-Length': "454",
                    'Connection': "keep-alive",
                    'cache-control': "no-cache"
                }

                response = requests.request("POST", url, data=payload, headers=headers)

                # print(response.text)
                # print(stats)


        # periods_stats_parse(url, session)
        # bullits_game_stats_parse(url, session)
        # foules_parse(url, session)
        # shots_parse(url, session)
        # pp_parse(url, session)
        # goals_for(url, session)
        # goals_against(url, session)
        # home_and_road_stats(url, session)

    else:
        print('ERROR')

#######################################################################################################################
############################ Парсинг информации о игроках #############################################################
#######################################################################################################################

def players_parse(headers, url):
    session = requests.Session()
    request = session.get(url, headers=headers)
    if request.status_code == 200:
        print('OK')
        soup = bs(request.content, 'html.parser')
        table_players = soup.find('table', class_='nowrap stripe compact hover m-table_small k-pldt').find('tbody').find_all('tr')
        for s in table_players:
            player = s.find_all('td')
            info_player= {
                'name': player[0].text,
                'number': player[1].text,
                'nationality': player[4].text.strip(),
            }

            if player[2].text == 'нападающий':
                info_player['amplua_id'] = 2
            elif player[2].text == 'защитник':
                info_player['amplua_id'] = 1
            elif player[2].text == 'вратарь':
                info_player['amplua_id'] = 0

            monthDict = {
                'Января': '1', 'Февраля': '2', 'Марта': '3', 'Апреля': '4', 'Мая': '5', 'Июня': '6', 'Июля': '7',
                'Августа': '8', 'Сентября': '9', 'Октября': '10', 'Ноября': '11', 'Декабря': '12'
            }

            bitrhday_date = player[3].text.split()[2] + '-' + monthDict[player[3].text.split()[1]] + '-' + player[3].text.split()[0]
            contract_date = player[5].text.split()[2] + '-' + monthDict[player[5].text.split()[1]] + '-' + player[5].text.split()[0]
            info_player['birthday'] = bitrhday_date
            info_player['date_of_contract_expiration'] = contract_date
            info_player['status_id'] = 0

            print(info_player)
            link = 'https://www.khl.ru' + player[0].a['href']
            req = session.get(link, headers=headers)
            if req.status_code == 200:
                soup = bs(req.content, 'html.parser')
                k = soup.find('div', class_='b-content_section m-stats').find('tbody').find_all('tr')[1].find_all('td')
                if info_player['amplua_id'] == 0:
                    stats_player = {
                        'team': team_id[k[0].text.strip().split(' ')[0]], 'games_count': k[2].text,
                        'win_count': k[3].text, 'defeat_count': k[4].text, 'bullit_count': k[5].text,
                        'shoots_count': k[6].text, 'missed_pucks_count': k[7].text, 'reflected_pucks_count': k[8].text,
                        'reflected_pucks_count_percent': k[9].text, 'reliability_factor': k[10].text,
                        'goals_count': k[11].text, 'assists_count': k[12].text, 'shutouts_count': k[13].text,
                        'penalty_time': k[14].text, 'playing_time': k[15].text
                    }
                    print(stats_player)
                else:
                    stats_player = {
                    'team': team_id[k[0].text.strip().split(' ')[0]], 'games_count': k[2].text, 'goals_count': k[3].text,
                    'assists_count': k[4].text, 'scores_count': k[5].text, 'plus_minus': k[6].text, 'plus': k[7].text,
                    'minus': k[8].text, 'penalty_time': k[9].text, 'even_strength_goals_count': k[10].text,
                    'power_play_goals_count': k[11].text, 'shorthanded_goals_count': k[12].text,
                    'overtime_goals_count': k[13].text, 'winning_goals_count': k[14].text, 'final_bullits_count': k[15].text,
                    'goal_shoot_count': k[16].text, 'implemented_goal_shoot_percent': k[17].text,
                    'average_shoot_count_per_game': k[18].text, 'faceoff_count': k[19].text, 'win_faceoff_count': k[20].text,
                    'win_faceoff_count_percent': k[21].text, 'average_playing_time': '00:' + k[22].text,
                    'average_change_count_per_game': k[23].text, 'body_contact_count': k[24].text,
                    'blocked_shoot_count': k[25].text, 'foal_against_count': k[26].text
                    }
                    print(stats_player)
            else:
                print('ERROR')
    else:
        print('ERROR')

# actually_games_parse(headers, url)

# url = 'https://www.khl.ru/game/851/82017/protocol/'
# game_protocol_parse(headers, url)

# url = 'https://www.khl.ru/game/851/82019/resume/'
# resume_game_parse(headers, url)

url = 'https://www.khl.ru/stat/teams/851/'
parse_team_stats(headers, url)
#
# urls = [
#     'https://www.khl.ru/clubs/dynamo_msk/team/',
#     'https://www.khl.ru/clubs/dinamo_r/team/',
#     'https://www.khl.ru/clubs/jokerit/team/',
#     'https://www.khl.ru/clubs/severstal/team/',
#     'https://www.khl.ru/clubs/ska/team/',
#     'https://www.khl.ru/clubs/spartak/team/',
#     'https://www.khl.ru/clubs/vityaz/team/',
#     'https://www.khl.ru/clubs/dinamo_mn/team/',
#     'https://www.khl.ru/clubs/lokomotiv/team/',
#     'https://www.khl.ru/clubs/torpedo/team/',
#     'https://www.khl.ru/clubs/cska/team/',
#     'https://www.khl.ru/clubs/hc_sochi/team/',
#     'https://www.khl.ru/clubs/avtomobilist/team/',
#     'https://www.khl.ru/clubs/ak_bars/team/',
#     'https://www.khl.ru/clubs/metallurg_mg/team/',
#     'https://www.khl.ru/clubs/neftekhimik/team/',
#     'https://www.khl.ru/clubs/sibir/team/',
#     'https://www.khl.ru/clubs/traktor/team/',
#     'https://www.khl.ru/clubs/salavat_yulaev/team/',
#     'https://www.khl.ru/clubs/avangard/team/',
#     'https://www.khl.ru/clubs/admiral/team/',
#     'https://www.khl.ru/clubs/amur/team/',
#     'https://www.khl.ru/clubs/barys/team/',
#     'https://www.khl.ru/clubs/kunlun/team/'
# ]
# for url in urls:
#     players_parse(headers, url)