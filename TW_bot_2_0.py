
from selenium import webdriver      # first log on page, do not know how to extract token YET
import time                         # for sleep function to wait for load different data
import requests                     # requests
from bs4 import BeautifulSoup       # parsing requested web
#import webbrowser                   # only open fuction on overview page
import re                           # regular expressions
#import urllib
from selenium.webdriver.chrome.options import Options
import sys

def close_session():
    # end up session for good
    INSTANCE_FIRST.SESSION.close()
    
def delete_smth(smth):
    del smth

gameworld = 'cs58'                      # change this

print('starting...')
class LOGIN():
    # credentials
    username = 'MyName'                # change this
    password = 'Mypass'                # change this

    def __init__(self):

        # URLs                         # change this - url - by language server you are on
        self.url = 'https://www.divokekmeny.cz/'                                         # official web for chromedriver --> log on and get cookies
        self.post_authurl = f'https://www.divokekmeny.cz/page/play/{gameworld}'

    def update_cookies(dr, sess):
        for cookie in dr.get_cookies():
            c = {cookie['name']: cookie['value']}
            # update session cookies, append(c) does not work, because of CookieJar object - does not have this function
            sess.cookies.update(c)

        # url method = GET, send me on overview page


    def start(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--headless")
        # initiate chromedriver window 
        self.driver = webdriver.Chrome('C:/Users/smeli/Desktop/Tribal_Wars/chromedriver', options=self.chrome_options)
        #get start url
        time.sleep(2)
        self.driver.get(self.url)
        time.sleep(2)

        # log on form filling and submit
        time.sleep(1)
        self.driver.find_element_by_name('username').send_keys(LOGIN.username)
        time.sleep(1)
        self.driver.find_element_by_name('password').send_keys(LOGIN.password)
        time.sleep(1)
        self.driver.find_element_by_class_name('btn-login').click()

        # initiate requests session
        self.SESSION = requests.Session()
        
        # set user agent into headers
        self.SESSION.headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36" }
        #SESSION.headers.update(headers)

        # for full log on web ˇ , but do not needed, ==> GET request for auth_get 
        #driver.find_element_by_class_name('world_button_active').click()
        time.sleep(4)
        # function for transfer cookies from chromedriver-u do request session to provide requests - get, post 
        LOGIN.update_cookies(self.driver, self.SESSION)
        # wait for loading all other stuffs
        time.sleep(4)
        # quit chromedriver, lates use only requests
        self.driver.quit()
        time.sleep(1)
        self.res = self.SESSION.get(self.post_authurl, timeout=10) # verify=False
        # after this request, it gets on https://cs69.divokekmeny.cz/game.php?screen=overview&intro
        time.sleep(2)

# stable log on
INSTANCE_LOGIN = LOGIN()
INSTANCE_LOGIN.start()
print('loged in')

class FIRST():

    def __init__(self):
        
        self.data = ''
        self.h_token = ''
        self.h_token_and_resources_url = f'https://{gameworld}.divokekmeny.cz/game.php?village=3726&screen=api&ajax=resources_schedule&id=3726'
        self.SESSION = INSTANCE_LOGIN.SESSION
        
    def first(self):
        
        # set tribal wars header
        self.SESSION.headers = {'X-Requested-With':'XMLHttpRequest'}
        self.SESSION.headers = {'TribalWars-Ajax':'1'}
        time.sleep(2)
        # extract h_token ... needed for post requests in url
        self.res = self.SESSION.get(self.h_token_and_resources_url, timeout=5)
        self.data = self.res.json()
        #print(self.data)
        self.h_token = self.data['game_data']['csrf']
        #print(self.h_token)
        #print(self.res.elapsed.total_seconds())# or only .elapsed

        
INSTANCE_FIRST = FIRST()
INSTANCE_FIRST.first()
print('Got main response')

########################################################################

# extract village informations:
class DATA():

    def __init__(self):
##        musi byt pod sebou
##        self.I_player_id = '', self.I_village_id = '', self.I_world = '',
##        self.I_count_villages = '', self.I_points = '', self.I_points_formatted = '',
##        self.I_rank = '', self.I_new_report = '', self.I_new_forum_post = '',
##        self.I_new_quest = '', self.I_incomings = '', self.I_supports = '',
##        self.I_premium = '', self.I_AccountManager = '', self.I_FarmAssistent = '',
##        self.I_coord = '', self.I_trader_away = '', self.I_storage_max = '',
##        self.I_wood = '', self.I_stone = '', self.I_iron = '',
##        self.B_main = '', self.B_barracks = '', self.B_stable = '',
##        self.B_garage = '', self.B_watchtower = '',  self.B_snob = '',
##        self.B_smith = '', self.B_place = '', self.B_statue = '',
##        self.B_market = '', self.B_wood = '', self.B_stone = '',
##        self.B_iron = '', self.B_farm = '', self.B_storage = '',
##        self.B_hide = '', self.B_wall = '', 
        self.data = INSTANCE_FIRST.data
        self.SESSION = INSTANCE_FIRST.SESSION
        
    def basic_info(self):
        self.I_player_id = self.data['game_data']['player']['id']
        self.I_village_id = self.data['game_data']['village']['id']
        self.I_world = self.data['game_data']['world']
        self.I_count_villages = self.data['game_data']['player']['villages']
        self.I_points = self.data['game_data']['player']['points']
        self.I_points_formatted = self.data['game_data']['player']['points_formatted']# neporebné
        self.I_rank = self.data['game_data']['player']['rank']
        self.I_new_report = self.data['game_data']['player']['new_report']
        self.I_new_forum_post = self.data['game_data']['player']['new_forum_post']
        self.I_new_quest = self.data['game_data']['player']['new_quest']
        self.I_incomings = self.data['game_data']['player']['incomings']
        self.I_supports = self.data['game_data']['player']['supports']
        self.I_premium = self.data['game_data']['features']['Premium']['active']
        self.I_AccountManager = self.data['game_data']['features']['AccountManager']['active']
        self.I_FarmAssistent = self.data['game_data']['features']['FarmAssistent']['active']
        self.I_trader_away = self.data['game_data']['village']['trader_away']
        self.I_storage_max = self.data['game_data']['village']['storage_max']
        self.I_coord = self.data['game_data']['village']['coord']
        self.I_x = self.data['game_data']['village']['x']
        self.I_y = self.data['game_data']['village']['y']

    def get_buildings_in_account(self):
        self.B_main = self.data['game_data']['village']['buildings']['main']
        self.B_barracks = self.data['game_data']['village']['buildings']['barracks']
        self.B_stable = self.data['game_data']['village']['buildings']['stable']
        self.B_garage = self.data['game_data']['village']['buildings']['garage']
        #self.B_watchtower = self.data['game_data']['village']['buildings']['watchtower']
        self.B_snob = self.data['game_data']['village']['buildings']['snob']
        self.B_smith = self.data['game_data']['village']['buildings']['smith']
        self.B_place = self.data['game_data']['village']['buildings']['place']
        self.B_statue = self.data['game_data']['village']['buildings']['statue']
        self.B_market = self.data['game_data']['village']['buildings']['market']
        self.B_wood = self.data['game_data']['village']['buildings']['wood']
        self.B_stone = self.data['game_data']['village']['buildings']['stone']
        self.B_iron = self.data['game_data']['village']['buildings']['iron']
        self.B_farm = self.data['game_data']['village']['buildings']['farm']
        self.B_storage = self.data['game_data']['village']['buildings']['storage']
        self.B_hide = self.data['game_data']['village']['buildings']['hide']
        self.B_wall = self.data['game_data']['village']['buildings']['wall']

        
    def parse_overview_page_for_hrefs(self):
        self.res = INSTANCE_LOGIN.res
        soup = BeautifulSoup(self.res.content, "html.parser")
        elem = soup.select('a')
        for i in range(len(elem)):
            print(elem[i].get('href'))
            
    def parse_victim_info(self):
        x = 507
        y = 564  
        self.get_info_about_victim_url = f'https://{gameworld}.divokekmeny.cz/game.php?village={INSTANCE_DATA.I_village_id}&screen=api&ajax=target_selection&input=%09{x}%7C{y}&type=coord&request_id=1&limit=5&offset=0'
        self.res = self.SESSION.get(self.get_info_about_victim_url)
        self.victim_info = self.res.json()
        #print(self.victim_info)

    def get_resources(self):
        self.I_wood = INSTANCE_FIRST.data['game_data']['village']['wood']
        self.I_stone = INSTANCE_FIRST.data['game_data']['village']['stone']
        self.I_iron = INSTANCE_FIRST.data['game_data']['village']['iron']
        
    def my_units(self):
        self.get_village_units_url = f'https://{gameworld}.divokekmeny.cz/game.php?village={INSTANCE_DATA.I_village_id}&screen=place&ajax=home_units'
        self.res = self.SESSION.get(self.get_village_units_url)
        my_village_units_info = self.res.json()
        #print(my_village_units_info)
        self.U_spear = my_village_units_info['response']['spear']
        self.U_sword = my_village_units_info['response']['sword']
        self.U_axe = my_village_units_info['response']['axe']
        self.U_archer = my_village_units_info['response']['archer']
        self.U_spy = my_village_units_info['response']['spy']
        self.U_light = my_village_units_info['response']['light']
        self.U_marcher = my_village_units_info['response']['marcher']
        self.U_heavy = my_village_units_info['response']['heavy']
        self.U_ram = my_village_units_info['response']['ram']
        self.U_catapult = my_village_units_info['response']['catapult']
        self.U_knight = my_village_units_info['response']['knight']
        self.U_snob = my_village_units_info['response']['snob']

    # get buildings already builded in account to list
    def is_built(self, needed_to_upgrade):
        # no idea of other way to proceed this function
        if int(INSTANCE_FIRST.data['game_data']['village']['buildings'][str(needed_to_upgrade)]) != 0:
            print(int(INSTANCE_FIRST.data['game_data']['village']['buildings'][str(needed_to_upgrade)]))
            return True
        else:
            return False

    def parse_main_page_for_time_and_needed_resources(self, needed_to_upgrade):

        print(needed_to_upgrade)
        self.main_screen_url = f'https://{gameworld}.divokekmeny.cz/game.php?village=3726&screen=main'
        self.res = self.SESSION.get(self.main_screen_url, allow_redirects=False, timeout=5)
        self.data = self.res.content
        self.soup = BeautifulSoup(self.data, "html.parser")

        soup = self.soup
        data = soup.find('div', attrs={'id':'building_wrapper'})
        #print(data)
        soup = BeautifulSoup(str(data), "html.parser")
        #print(soup.prettify())

        data = soup.find('tr', attrs={'id':f'main_buildrow_{needed_to_upgrade}'})
        #print(data.prettify())
        ######################################################verify = str(data.attrs.values()).strip('dict_values()[]')
        #print(verify)
        soup = BeautifulSoup(str(data), "html.parser")
        self.wood = soup.find('td', class_='cost_wood')
        self.wood = self.wood.span.nextSibling
        #print(self.wood)
        self.stone = soup.find('td', class_='cost_stone')
        self.stone = self.stone.span.nextSibling
        #print(self.stone)
        self.iron = soup.find('td', class_='cost_iron')
        self.iron = self.iron.span.nextSibling
        #print(self.iron)
        self.time = soup.find('span', class_='icon header time')
        self.time = self.time.parent.span.nextSibling
        #print(self.time)
        self.population = soup.find('span', class_='icon header population')
        #####self.population = self.population.parent.span.nextSibling
        #print(self.population)
        #can_build = soup.find('td', class_='build_options')

        self.queue_number = 0
        datad = self.soup.find('div', attrs={'id':'buildqueue_wrap'})
        soup = BeautifulSoup(str(datad), "html.parser")
        for i in soup.find_all('tr'):
                if 'buildorder' in str(i.attrs):
                    self.queue_number += 1
        #print(self.queue_number,'==> full queue, have to wait if no premium')
        return True



            
########################################################################

INSTANCE_DATA = DATA()
INSTANCE_DATA.basic_info()
INSTANCE_DATA.get_buildings_in_account()
print('Got basic info')

#INSTANCE_DATA.parse_victim_info()
#INSTANCE_DATA.my_units()
#if int(INSTANCE_DATA.I_count_villages) > 1:
    # repeat for every village ,, get them id in request ... FIRST
#INSTANCE_DATA.get_resources()
#INSTANCE_DATA.get_buildings_in_account()


class TO_UPGRADE():
    
    # building list:      screen=
    buildings = ['main', 'wood', 'stone',                       # 0, 1, 2
                'iron', 'farm', 'storage',                      # 3, 4, 5
                'barracks', 'stable', 'garage',                 # 6, 7, 8
                'smith', 'snob', 'watchtower',                  # 9, 10, 11
                'market', 'statue', 'place', 'wall', 'hide']    # 12, 13, 14, 15, 16

    def __init__(self):

        self.post_data = ''
        self.SESSION = INSTANCE_FIRST.SESSION
        #self.repeat = 0
        
    """
    if posting: data = post_data in post request, never with & ... always a dictionary!
    or give posted data in posted url
    data=  - does not get f{smth} !!! 
    or simply get url from web 
    """

    def decision(self):

        print('making decisions...')

##        def basic_decision():
##            if int(INSTANCE_DATA.B_wood) <= 5:
##                self.building_in_list = "wood"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_stone) <= 5:
##                self.building_in_list = "stone"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_iron) <= 5:
##                self.building_in_list = "iron"
##                return self.building_in_list
##                break
##
##            elif int(INSTANCE_DATA.B_wall) <= 2:
##                self.building_in_list = "wall"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_main) <= 6:
##                self.building_in_list = "main"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_farm) <= 4:
##                self.building_in_list = "farm"
##                return self.building_in_list
##                break
##
##            elif int(INSTANCE_DATA.B_barracks) <= 5:
##                self.building_in_list = "barracks"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_storage) <= 5:
##                self.building_in_list = "storage"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_hide) <= 1:
##                self.building_in_list = "hide"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_market) <= 3:
##                self.building_in_list = "market"
##                return self.building_in_list
##                break
##
##        def  little_advanced_decision():
##
##            if int(INSTANCE_DATA.B_wood) <= 10:
##                self.building_in_list = "wood"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_stone) <= 10:
##                self.building_in_list = "stone"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_iron) <= 10:
##                self.building_in_list = "iron"
##                return self.building_in_list
##                break
##
##            elif int(INSTANCE_DATA.B_wall) <= 4:
##                self.building_in_list = "wall"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_main) <= 8:
##                self.building_in_list = "main"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_farm) <= 6:
##                self.building_in_list = "farm"
##                return self.building_in_list
##                break
##
##            elif int(INSTANCE_DATA.B_barracks) <= 5:
##                self.building_in_list = "barracks"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_storage) <= 13:
##                self.building_in_list = "storage"
##                return self.building_in_list
##                break
##
##        def  more_advanced_decision():
##
##            if int(INSTANCE_DATA.B_wood) <= 15:
##                self.building_in_list = "wood"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_stone) <= 15:
##                self.building_in_list = "stone"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_iron) <= 15:
##                self.building_in_list = "iron"
##                return self.building_in_list
##                break
##
##            elif int(INSTANCE_DATA.B_main) <= 10:
##                self.building_in_list = "main"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_farm) <= 9:
##                self.building_in_list = "farm"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_storage) <= 19:
##                self.building_in_list = "storage"
##                return self.building_in_list
##                break
##
##        def  More_advanced_decision():
##
##            if int(INSTANCE_DATA.B_wood) <= 23:
##                self.building_in_list = "wood"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_stone) <= 23:
##                self.building_in_list = "stone"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_iron) <= 23:
##                self.building_in_list = "iron"
##                return self.building_in_list
##                break
##
##            elif int(INSTANCE_DATA.B_main) <= 12:
##                self.building_in_list = "main"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_farm) <= 12:
##                self.building_in_list = "farm"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_storage) <= 23:
##                self.building_in_list = "storage"
##                return self.building_in_list
##                break
##
##        def  MORE_advanced_decision():
##
##            if int(INSTANCE_DATA.B_wood) <= 27:
##                self.building_in_list = "wood"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_stone) <= 27:
##                self.building_in_list = "stone"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_iron) <= 27:
##                self.building_in_list = "iron"
##                return self.building_in_list
##                break
##
##            elif int(INSTANCE_DATA.B_main) <= 14:
##                self.building_in_list = "main"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_farm) <= 13:
##                self.building_in_list = "farm"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_wall) <= 10:
##                self.building_in_list = "wall"
##                return self.building_in_list
##                break
##
##        def  most_advanced_decision():
##
##            if int(INSTANCE_DATA.B_wood) <= 30:
##                self.building_in_list = "wood"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_stone) <= 30:
##                self.building_in_list = "stone"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_iron) <= 30:
##                self.building_in_list = "iron"
##                return self.building_in_list
##                break
##
##            elif int(INSTANCE_DATA.B_main) <= 16:
##                self.building_in_list = "main"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_farm) <= 15:
##                self.building_in_list = "farm"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_storage) <= 25:
##                self.building_in_list = "storage"
##                return self.building_in_list
##                break
##
##        def  Most_advanced_decision():
##
##            if int(INSTANCE_DATA.B_main) <= 20:
##                self.building_in_list = "main"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_farm) <= 18:
##                self.building_in_list = "farm"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_storage) <= 27:
##                self.building_in_list = "storage"
##                return self.building_in_list
##                break
##            elif int(INSTANCE_DATA.B_wall) <= 18:
##                self.building_in_list = "wall"
##                return self.building_in_list
##                break

        def  MOST_advanced_decision():
            if int(INSTANCE_DATA.B_smith) <= 20:
                self.building_in_list = "smith"
            elif int(INSTANCE_DATA.B_wall) <= 20:
                self.building_in_list = "wall"
            elif int(INSTANCE_DATA.B_snob) <= 1:
                self.building_in_list = "snob"
            elif int(INSTANCE_DATA.B_main) <= 30:
                self.building_in_list = "main"
            elif int(INSTANCE_DATA.B_farm) <= 20:                  #### farm
                self.building_in_list = "farm"

            elif int(INSTANCE_DATA.B_stable) <= 10:                #### stable
                self.building_in_list = "stable"
            elif int(INSTANCE_DATA.B_garage) <= 10:
                self.building_in_list = "garage"
            elif int(INSTANCE_DATA.B_barracks) <= 20:
                self.building_in_list = "barracks"
            elif int(INSTANCE_DATA.B_market) <= 15:                #### market
                self.building_in_list = "market"
            elif int(INSTANCE_DATA.B_storage) <= 30:
                self.building_in_list = "storage"

##        basic_decision()
##        little_advanced_decision()
##        more_advanced_decision()
##        More_advanced_decision()
##        MORE_advanced_decision()
##        most_advanced_decision()
##        Most_advanced_decision()
        MOST_advanced_decision()

        print('upgrading: ', self.building_in_list)

    def to_upgrade(self, building_in_list):

        def carry_on():
            INSTANCE_DATA.get_resources()
            if int(INSTANCE_DATA.wood) <= INSTANCE_DATA.I_wood and int(INSTANCE_DATA.stone) <= INSTANCE_DATA.I_stone and int(INSTANCE_DATA.iron) <= INSTANCE_DATA.I_iron:
                #and INSTANCE_DATA.population <= int(INSTANCE_DATA.):
                # only main screen
                self.upgrade_url = f"https://{gameworld}.divokekmeny.cz/game.php?village={INSTANCE_DATA.I_village_id}&screen=main&ajaxaction=upgrade_building&type=main&"
                # need to be changed in post_data to str()
                self.post_data = {
                        'id':f'{str(building_in_list)}',
                        'force':'1',
                        'destroy':'0',
                        'source':f'{INSTANCE_DATA.I_village_id}',
                        'h':f'{INSTANCE_FIRST.h_token}'
                        }
                self.res = self.SESSION.post(self.upgrade_url, data=self.post_data, allow_redirects=False)
                print('queue is: ', self.queue_num)
                print(building_in_list,'  upgraded!')

                return True
            else:
                print('queue is: ', self.queue_num)
                print('no supplyes for upgrade')
                return False

        if 66 - 6 == 60:
            if INSTANCE_DATA.parse_main_page_for_time_and_needed_resources(building_in_list):
                self.queue_num = INSTANCE_DATA.queue_number
                if self.queue_num < 2:

                        if carry_on():
                            self.queue_num += 1
                            self.count += 1
                            if (2 - self.queue_num) > 0:
                                self.can_continue = True
                            else:
                                self.can_continue = False

                            return True
                        else:
                            return False
                else:
                    print('queue is full: ', self.queue_num)
                    return False

                if INSTANCE_DATA.I_premium == True:
                    self.queue_num = INSTANCE_DATA.queue_number
                    if self.queue_num <= 5:
                        if carry_on():
                            self.queue_num += 1
                            self.count += 1
                            if (5 - self.queue_num) > 0:
                                self.can_continue = True
                            else:
                                self.can_continue = False

                            return True
                        else:
                            return False
                else:
                    print('No premium, queue is: ', self.queue_num)
                    return False

            else:
                return False
        else:
            print('havent biult yet')
            return False

print('Upgrading...')
INSTANCE_TO_UPGRADE = TO_UPGRADE()
#print(INSTANCE_TO_UPGRADE.decision())
INSTANCE_TO_UPGRADE.decision()
INSTANCE_TO_UPGRADE.to_upgrade(INSTANCE_TO_UPGRADE.building_in_list)

#if INSTANCE_TO_UPGRADE.can_continue == True:
    #while INSTANCE_TO_UPGRADE.can_continue == True:
        #INSTANCE_TO_UPGRADE.to_upgrade(INSTANCE_TO_UPGRADE.decision())



class ATTACK():

    def __init__(self):
        
        self.SESSION = INSTANCE_FIRST.SESSION
        # from place building
        self.get_attack_place_url = f'https://{gameworld}.divokekmeny.cz/game.php?village={INSTANCE_DATA.I_village_id}&screen=place'
        self.post_first_attack_post_url = f'https://{gameworld}.divokekmeny.cz/game.php?village={INSTANCE_DATA.I_village_id}&screen=place&try=confirm'
        self.post_second_attack_post_url = f'https://{gameworld}.divokekmeny.cz/game.php?village={INSTANCE_DATA.I_village_id}&screen=place&action=command'

        self.first_post_data = ''
        self.second_post_data = '' 
        self.ch = ''
        
    def attack(self):
        
        self.res = self.SESSION.get(self.get_attack_place_url)## 507, 564

        self.SESSION.headers = {'Upgrade-Insecure-Requests':'1'}
        self.SESSION.headers = {'Content-Type':'application/x-www-form-urlencoded'}

        self.first_post_data = {'ccfe79cc044c3d6999c74d':'4bf25466ccfe79',
                                'template_id':'',
                                'source_village':'3726',
                                'spear':'',
                                'sword':'',
                                'axe':'',
                                'archer':'',
                                'spy':'1',##
                                'light':'',
                                'marcher':'',
                                'heavy':'',
                                'ram':'',
                                'catapult':'',
                                'knight':'',
                                'snob':'',
                                'x':'507',
                                'y':'564',
                                'target_type':'coord',
                                'input':'507%7C564',    ## coordinations of victim
                                'attack':'%C3%9Atok'}
                                
        self.res = self.SESSION.post(self.post_first_attack_post_url, data = self.first_post_data, allow_redirects=False, timeout=5)
        self.ch = re.findall('name="ch" value="(.*?)"', self.res.text)
        self.ch = str(self.ch).strip("[']")
        #print(self.ch)
        self.second_post_data = {'attack':'true',
                                 'ch':f'{self.ch}',
                                 'x':'507',
                                 'y':'564',
                                 'source_village':'3726',
                                 'village':'3726',
                                 'attack_name':'',
                                 'spear':'0',
                                 'sword':'0',
                                 'axe':'0',
                                 'archer':'0',
                                 'spy':'1',##
                                 'light':'0',
                                 'marcher':'0',
                                 'heavy':'0',
                                 'ram':'0',
                                 'catapult':'0',
                                 'knight':'0',
                                 'snob':'0',                                 
                                 'building':'main',
                                 'h':f'{INSTANCE_FIRST.h_token}'}

        self.res = self.SESSION.post(self.post_second_attack_post_url, data = self.second_post_data,  allow_redirects=True, timeout=5)



#INSTANCE_ATTACK = ATTACK()
#INSTANCE_ATTACK.attack()

#INSTANCE_DATA.parse_overview_page()


time.sleep(3)

close_session()

sys.exit()








