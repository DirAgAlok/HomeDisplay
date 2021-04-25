#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, pygame
from pygame.locals import *
import cevent
import requests
#import time
from datetime import datetime, date
import locale
import os
#import threading
import math
import json



class App(cevent.CEvent):
    def __init__(self):
        self.running = True  
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
                
        #setting default values
        self._display_surf = None
        self.size = self.width, self.height = (800, 480)
        self._backgroundImg = None
        self.mouse_visible = 0
        self.fullscreen = False
        
        self._ht_values = []
        self._ht_values_temp = []
        self.tmp = 0
        self.hum = 0
        self.ht_time = 0
        self.ht_up_time = 0
        self.ht_up_time_M = 0
        self.ht_up_time_H = 0
        self.ht_up_interval = 12
        self.time = ""
        self.today = ""
        self.seconds = ""
        self.weekday = ""
        self.date = ""
        self.curr_time_H = 0
        self.curr_time_M = 0
        self.r = 0
        self.ht_update_time = 0
        self.ht_need_to_update = 0
        self.font = "{0}/res/{1}".format(self.dir_path, 'MyFont.otf')
        self.weather_need_update = 0
        self.weather_update_time = 0
        self.weather = []
        self.weather_icon_size = "big"
        self.uiswitch = False
        self.uitime = 0
        self.uirevtime = 30
        self.bgIMG = "ColorBlack.png"
        self.onecall = True
        self.unit = "C"
        self.timezone = 0
        self.utctime = False
         
        #setting default colors
        self.grey = (30, 30, 30)
        self.light_grey = (128, 128, 128)
        self.white = (255,255,255) 
        self.blue = (0, 136, 204)
        self.red = (195, 28, 74)
        
        #setting default text sizes
        self.tiny = 25
        self.small = 50
        self.middle = 70
        self.big = 150
        self.giant = 200
        
        #setting default locale
        self.locale = "de_DE"
        
        #setting default surfaces
        self.current_time_surf = pygame.Surface((0,0))
        self.current_time_surf_rect = pygame.Surface((0,0))
        self.current_time_S_surf = pygame.Surface((0,0))
        self.current_date_surf = pygame.Surface((0,0))
        self.current_day_surf = pygame.Surface((0, 0))
        self.ht_up_time_surf = pygame.Surface((0,0))
        self.weather_icon_surf = pygame.Surface((0,0))
        
        #setting default weather icons path
        self.icon_path = "{0}/res/img/weather_{1}/{2}.png"
        
        
        
    def on_init(self):
        
        self._running = True
        pygame.init()
        
        config_file = open('{0}/config.json'.format(self.dir_path))
        self.config = json.load(config_file)
        self.set_config_values()
        config_file.close()
        
        pygame.mouse.set_visible(self.mouse_visible)
                     
        #setting up base
        if(self.fullscreen):
            self._display_surf = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        else:
            self._display_surf = pygame.display.set_mode(self.size)
        
        locale.setlocale(locale.LC_ALL, self.locale)
        self.tinyfont = pygame.font.Font(self.font, self.tiny)
        self.smallfont = pygame.font.Font(self.font, self.small)
        self.middlefont = pygame.font.Font(self.font, self.middle)
        self.bigfont = pygame.font.Font(self.font, self.big)
        self.giantfont = pygame.font.Font(self.font, self.giant)
        
        #setting up images
        self._backgroundImg = pygame.image.load("{0}/res/img/{1}".format(self.dir_path, self.bgIMG))
        self._backgroundImg = pygame.transform.scale(self._backgroundImg, (self.width, self.height))
        self._backgroundImgRect = self._backgroundImg.get_rect()
        self._backgroundImg.convert_alpha()
        self._backgroundImg.set_alpha(128)
                
        self._display_surf.fill(self.grey)
        self._display_surf.blit(self._backgroundImg, self._backgroundImgRect)

        #getting values at startup
        #time
        self.getDateTime()
        #weather values
        if(self.onecall):
            self.weather = self.getWeather_onecall(self.weather_url_onecall, self.api_key, self.location_lon, self.location_lat, self.units, self.exclude)
        else:
            self.weather = self.getWeather(self.weather_url, self.location_id, self.api_key, self.units)
        #ht values
        self._ht_values = self.getStat(self.status_Server, self.PARAMS)
        self.set_ht_update_time()
        
               
    #eventhandler
    def on_event(self, event):
        if event.type == QUIT:
            self.on_exit()
 
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.on_lbutton_down(event)
            elif event.button == 2:
                self.on_mbutton_down(event)
            elif event.button == 3:
                self.on_rbutton_down(event)

    
    def on_loop(self):
        
        self.getDateTime()
        if(self.ht_update_time >= self.curr_time_M and self.ht_need_to_update == 1):
            self.ht_need_to_update = 0  
            
        if(self.ht_update_time <= self.curr_time_M):
            if(self.ht_need_to_update == 0):
                self._ht_values = self.getStat(self.status_Server, self.PARAMS)
                self.ht_need_to_update = 1
                self.set_ht_update_time()
                    
        if(self.weather_update_time == self.curr_time_H and self.weather_need_update == 1):
            self.weather_need_update = 0
                    
        if(self.weather_update_time <= self.curr_time_H):
            if(self.weather_need_update == 0):
                if(self.onecall):
                    self.weather = self.getWeather_onecall(self.weather_url_onecall, self.api_key, self.location_lon, self.location_lat, self.units, self.exclude)
                else:
                    self.weather = self.getWeather(self.weather_url, self.location_id, self.api_key, self.units)
                self.weather_need_update = 1
                                               
    def set_ht_update_time(self):
        self.ht_up_time = self.split_string(str(self._ht_values[2]),":")
        try:
            self.ht_up_time_M = int(self.ht_up_time[1])
        except:
            self.ht_up_time_M = self.curr_time_M + self.ht_up_interval
        
        self.ht_update_time = self.ht_up_time_M + self.ht_up_interval
        
        if(self.ht_update_time >= 60):
            self.ht_update_time -= 60
            if(self.ht_update_time <0):
                self.ht_update_time = 0
                     
    def on_render(self):        
        
        if(self.uiswitch):
            self.forecastUI()
            
            if(self.uitime + self.uirevtime < int(self.seconds)):
                self.uiswitch = False           
        else:
            self.mainUI()
              
        pygame.display.flip()
        
    def clearWindow(self):
        self._display_surf.fill(self.grey)
        self._display_surf.blit(self._backgroundImg, self._backgroundImgRect)
        
    def on_cleanup(self):
        pygame.quit()
        
    def on_execute(self):
        
        if self.on_init() == False:
            self._running = False
     
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)          
            self.on_loop()
            self.on_render()        
        self.on_cleanup()
        
    def on_exit(self):
        self._running = False
      
    def getStat(self, serverName, params):
        
        self._ht_values_temp = self._ht_values
        
        try:
            self.r = requests.post(url = serverName, data = params)
        except:
            return self._ht_values_temp
        
        if(self.r.status_code == 200):
            data = self.r.json()
            if(data == "{}"):
                return self._ht_values_temp;
            else:
                tmp = round(data['data']['device_status']['tmp']['value'], 1)
                hum = round(data['data']['device_status']['hum']['value'], 1)
                uxtime = data['data']['device_status']['unixtime']
                if(uxtime == 0):
                   try:
                        time = self._ht_values_temp[2]
                   except:
                        time = self.time
                else:
                    if(self.utctime):
                        time = datetime.utcfromtimestamp(uxtime).strftime("%H:%M")
                    else:    
                        time = datetime.fromtimestamp(uxtime).strftime("%H:%M")
                return tmp, hum, time
        else:
            return self._ht_values_temp
    
    #get weather data with currtent min and max temp
    def getWeather(self, weather_url, city_id, api_key, units):
        
        params = {'id': city_id, 'appid': api_key, 'units': units}
        _weather_temp = self.weather
        
        try:
            self.weather_req_onecall = requests.get(url=weather_url_onecall, params=params)
        except:
            self.weather_need_update = 0
            return _weather_temp
    
        if(self.weather_req.status_code == 200):
            _weather_data = self.weather_req.json()
            _weather_tmp = math.ceil(_weather_data['main']['temp'])
            _weather_tmp_max = math.floor(_weather_data['main']['temp_max'])
            _weather_tmp_min = math.ceil(_weather_data['main']['temp_min'])
            _weather_icon = _weather_data['weather'][0]['icon']
            self.timezone = _weather_data['timezone']
              
            self.weather_update_time = self.curr_time_H + 1
            if(self.weather_update_time >= 24):
                self.weather_update_time = 0
              
            return _weather_tmp, _weather_tmp_min, _weather_tmp_max, _weather_icon
        else:
            self.weather_need_update = 0
            return _weather_temp   
    
    #get weather data with daily min and max temp   
    def getWeather_onecall(self, weather_url_onecall, api_key,  lon, lat, units, exclude):
        
        params = {'appid': api_key, 'lon': lon, 'lat': lat, 'units': units, 'exclude': exclude}
        _weather_temp = self.weather
        
        try:
            self.weather_req_onecall = requests.get(url=weather_url_onecall, params=params)
        except:
            self.weather_need_update = 0
            return _weather_temp
        
        if(self.weather_req_onecall.status_code == 200):
            try:
                _weather_data_onecall = self.weather_req_onecall.json()
            except:
                _weather_data_onecall = _weather_temp
                
            _weather_curr_temp = math.ceil(_weather_data_onecall['current']['temp'])
            _weather_curr_icon = _weather_data_onecall['current']['weather'][0]['icon']
            _weather_day_min = math.floor(_weather_data_onecall['daily'][0]['temp']['min'])
            _weather_day_max = math.ceil(_weather_data_onecall['daily'][0]['temp']['max'])
            self.timezone = _weather_data_onecall['timezone_offset']
            
            #forecast
            _dt = 0
            _forecastday = ()
            _forecast_icon = ()
            _forecast_temp_min = ()
            _forecast_temp_max = ()
            while _dt <8:
                #_forecastday = _forecastday +  (time.strftime("%a", time.localtime(int(_weather_data_onecall['daily'][_dt]['dt']))) , )
                _forecastday = _forecastday + (datetime.fromtimestamp(int(_weather_data_onecall['daily'][_dt]['dt'])).strftime("%a") , )
                _forecast_icon = _forecast_icon + (_weather_data_onecall['daily'][_dt]['weather'][0]['icon'] , )
                _forecast_temp_min = _forecast_temp_min + (math.floor(_weather_data_onecall['daily'][_dt]['temp']['min']) , )
                _forecast_temp_max = _forecast_temp_max + (math.ceil(_weather_data_onecall['daily'][_dt]['temp']['max']) , )
                
                _dt += 1

            
            self.weather_update_time = self.curr_time_H + 1
            if(self.weather_update_time >= 24):
                self.weather_update_time = 0
            
            return _weather_curr_temp, _weather_day_min, _weather_day_max, _weather_curr_icon, _forecastday, _forecast_icon, _forecast_temp_min, _forecast_temp_max
            
        else:
            self.weather_need_update = 0
            return _weather_temp
    
    def split_string(self, string_to_split, seperator):
        return string_to_split.split(seperator)
        
    def getDateTime(self):
        self.date_time = datetime.now()
        self.date = self.date_time.strftime("%d.%m.%Y")
        self.weekday = self.date_time.strftime("%a")
        self.time = self.date_time.strftime("%H:%M")
        self.seconds = self.date_time.strftime("%S")
        self.curr_time_H = int(self.time.split(":")[0])
        self.curr_time_M = int(self.time.split(":")[1])
          
    def mainUI(self):
        self.clearWindow()
        #format surfaces
        try:
            self.temp_humi_surf = self.bigfont.render(str(self._ht_values[0]) +u"\u00B0{0}  ".format(self.unit) + str(self._ht_values[1]) + "%" , True , self.white)    #u"\u00B0C" = °C in unicode 
        except:
            self.temp_humi_surf = self.bigfont.render("Connect Error", True, self.red)
        self.ht_up_time_surf = self.tinyfont.render(str(self._ht_values[2]), True, self.blue)
        self.current_time_surf = self.giantfont.render(self.time, True, self.white)
        self.current_time_surf_rect = self.current_time_surf.get_rect()
        self.current_time_S_surf = self.middlefont.render(self.seconds, True, self.blue)
        self.current_date_surf = self.middlefont.render(self.date, True, self.white)
        self.current_day = self.weekday
        self.weather_icon_surf = pygame.image.load(self.icon_path.format(self.dir_path, self.weather_icon_size, self.weather[3]))
        
        self.weather_temp_surf = self.middlefont.render(str(int(self.weather[0]))+u"\u00B0{0}".format(self.unit), True, self.white)
        self.weather_temp_min_surf = self.tinyfont.render(str(int(self.weather[1]))+u"\u00B0{0}".format(self.unit), True, self.blue)
        self.weather_temp_max_surf = self.tinyfont.render(str(int(self.weather[2]))+u"\u00B0{0}".format(self.unit), True, self.blue)
        
        
        if(self.current_day == "So"):
            self.daycolor = self.red
        elif(self.current_day =="Sa"):
            self.daycolor = self.blue
        else:
            self.daycolor = self.white
            
        self.current_day_surf = self.middlefont.render(self.current_day, True , self.daycolor)
        
        #set positions of surfaces
        #temp, humi
        _temp_humi_surf_posX = self.width/2 - self.temp_humi_surf.get_width()/2
        _temp_humi_surf_posY = 0
        _ht_up_time_surf_posX = self.width/2 - self.ht_up_time_surf.get_width()/2
        _ht_up_time_surf_posY = _temp_humi_surf_posY + self.temp_humi_surf.get_height()- self.ht_up_time_surf.get_height()
        #time
        _current_time_surf_posX = self.width/2 - self.current_time_surf.get_width()/2
        _current_time_surf_posY = self.height/3
        _current_time_S_surf_posX = _current_time_surf_posX + self.current_time_surf.get_width() + 20
        _current_time_S_surf_posY = _current_time_surf_posY + self.current_time_surf.get_height()/2
        #date
        _day_date_distance = 30
        _date_surf_width = self.current_day_surf.get_width() + self.current_date_surf.get_width() + _day_date_distance # date width + day width + distance between
        _current_day_surf_posX = self.width/2 - _date_surf_width/2  
        _currtent_date_surf_posX = _current_day_surf_posX + self.current_day_surf.get_width() + _day_date_distance    
        _current_day_date_posY = self.height - self.current_day_surf.get_height()
        #weather
        _weather_min_max_distance = 20
        _weather_icon_posX = _current_time_surf_posX/2 - self.weather_icon_surf.get_width()/2 
        _weather_icon_posY = _current_time_surf_posY #- self.weather_icon_surf.get_height()/3 
        _weather_temp_posX = _current_time_surf_posX/2 - self.weather_temp_surf.get_width()/2
        _weather_temp_posY = _weather_icon_posY + self.weather_icon_surf.get_height()
        _weather_min_max_surf_width = self.weather_temp_min_surf.get_width() + self.weather_temp_max_surf.get_width() + _weather_min_max_distance
        _weather_min_posX = _current_time_surf_posX/2 - _weather_min_max_surf_width/2
        _weather_max_posX = _weather_min_posX + self.weather_temp_min_surf.get_width() + _weather_min_max_distance
        _weather_min_max_posY = _weather_temp_posY + self.weather_temp_surf.get_height()
    
        #display Temp, Humi and updatetime 
        self._display_surf.blit(self.temp_humi_surf, (_temp_humi_surf_posX, _temp_humi_surf_posY)) 
        self._display_surf.blit(self.ht_up_time_surf, (_ht_up_time_surf_posX, _ht_up_time_surf_posY))
               
        #display Time and Date
        self._display_surf.blit(self.current_time_surf, (_current_time_surf_posX, _current_time_surf_posY))
        self._display_surf.blit(self.current_time_S_surf, (_current_time_S_surf_posX, _current_time_S_surf_posY))
        self._display_surf.blit(self.current_day_surf, (_current_day_surf_posX, _current_day_date_posY))
        self._display_surf.blit(self.current_date_surf, (_currtent_date_surf_posX, _current_day_date_posY))
             
        #display weather     
        self._display_surf.blit(self.weather_icon_surf, (_weather_icon_posX, _weather_icon_posY))
        self._display_surf.blit(self.weather_temp_surf, (_weather_temp_posX, _weather_temp_posY))
        self._display_surf.blit(self.weather_temp_min_surf, (_weather_min_posX, _weather_min_max_posY))
        self._display_surf.blit(self.weather_temp_max_surf, (_weather_max_posX, _weather_min_max_posY))
       
    def forecastUI(self):
        self.clearWindow()
        forecast_day_surf = ()
        forecast_icon_surf = ()
        forecast_temp_min_surf = ()
        forecast_temp_max_surf = ()
        forecast_day_posX = ()
        forecast_day_posY = ()
        forecast_icon_posX = ()
        forecast_icon_posY = ()
        forecast_temp_min_posX = ()
        forecast_temp_max_posX = ()
        forecast_temp_min_max_posY = ()
        fcc = 0
        posXcount = 1
        posYcount = 0
        _forecast_min_max_distance = 20
        
        while fcc < 8:
            forecast_day_surf = forecast_day_surf + (self.smallfont.render(self.weather[4][fcc], True, self.white) , )
            forecast_icon_surf = forecast_icon_surf + (pygame.image.load(self.icon_path.format(self.dir_path, self.weather_icon_size, self.weather[5][fcc])) , )
            forecast_temp_min_surf = forecast_temp_min_surf + (self.tinyfont.render(str(int(self.weather[6][fcc]))+u"\u00B0{0}".format(self.unit), True, self.light_grey) , )
            forecast_temp_max_surf = forecast_temp_max_surf + (self.tinyfont.render(str(int(self.weather[7][fcc]))+u"\u00B0{0}".format(self.unit), True, self.light_grey) , )
            
            forecast_day_posX = forecast_day_posX[:fcc] + (self.width/5 *posXcount - forecast_day_surf[fcc].get_width()/2 , )
            forecast_day_posY = forecast_day_posY[:fcc] + (self.height/2 * posYcount  + 20, )
            forecast_icon_posX = forecast_icon_posX[:fcc] +(self.width/5 *posXcount - forecast_icon_surf[fcc].get_width()/2 , )
            forecast_icon_posY = forecast_icon_posY[:fcc] +(forecast_day_posY[fcc] + forecast_day_surf[fcc].get_height(), )
            forecast_min_max_surf_width = forecast_temp_min_surf[fcc].get_width() + forecast_temp_max_surf[fcc].get_width() + _forecast_min_max_distance
            forecast_temp_min_posX = forecast_temp_min_posX[:fcc] + (self.width/5 *posXcount - forecast_min_max_surf_width/2 , )
            forecast_temp_max_posX = forecast_temp_max_posX[:fcc] + (forecast_temp_min_posX[fcc] + forecast_temp_min_surf[fcc].get_width() + _forecast_min_max_distance , )
            forecast_temp_min_max_posY = forecast_temp_min_max_posY[:fcc] + (forecast_icon_posY[fcc] + forecast_icon_surf[fcc].get_height() , )
            
            if(fcc == 3):
                posYcount +=1
                posXcount = 0
           
            self._display_surf.blit(forecast_icon_surf[fcc], (forecast_icon_posX[fcc], forecast_icon_posY[fcc]))
            self._display_surf.blit(forecast_day_surf[fcc], (forecast_day_posX[fcc], forecast_day_posY[fcc]))
            self._display_surf.blit(forecast_temp_min_surf[fcc], (forecast_temp_min_posX[fcc], forecast_temp_min_max_posY[fcc]))
            self._display_surf.blit(forecast_temp_max_surf[fcc], (forecast_temp_max_posX[fcc], forecast_temp_min_max_posY[fcc]))
            
            posXcount +=1
            fcc +=1
   
    def on_lbutton_down(self, event):
        if(self.onecall):
            self.uiswitch += 1
            self.uitime = int(self.seconds)
            if(self.uiswitch >1):
                self.uiswitch = 0
        else:
            self.uiswitch = 0
      
    def set_config_values(self):
        #setting UI values
        self.fullscreen = self.config['fullscreen'] 
        self.size = self.width, self.height = self.config['display_size'] 
        self.mouse_visible =  self.config['mouse_visible'] 
        self.bgIMG = self.config['bg_IMG'] 
        self.uirevtime = self.config['uirevtime']  
        self.unit = self.config['unit']
        self.locale = self.config['locale']
        self.font ="{0}/res/{1}".format(self.dir_path, self.config['font']['name'])
        self.tiny = self.config['font']['size'][0]['tiny'] 
        self.small = self.config['font']['size'][0]['small']
        self.middle = self.config['font']['size'][0]['middle']
        self.big = self.config['font']['size'][0]['big']
        self.giant = self.config['font']['size'][0]['giant']
        self.light_grey = self.config['colors']['light_grey']
        self.white = self.config['colors']['white']
        self.blue = self.config['colors']['blue']
        self.red = self.config['colors']['red']
        
        
        #Setting shelly values
        self.status_Server = self.config['shelly']['statusServer']
        self.ht_id = self.config['shelly']['id']
        self.auth_key = self.config['shelly']['authKey']
        self.PARAMS = {'auth_key': self.auth_key, 'id' : self.ht_id}
        self.utctime = self.config['utctime']
        
        #setting OpenWeatherMap.org values
        self.weather_url = self.config['weather']['url']
        self.weather_url_onecall = self.config['weather']['urlonecall']
        self.location_id = self.config['weather']['locationid']
        self.location_lon = self.config['weather']['lon']
        self.location_lat = self.config['weather']['lat'] 
        self.exclude = self.config['weather']['exclude']
        self.api_key = self.config['weather']['apikey']
        self.units = self.config['weather']['units']
        self.onecall = self.config['weather']['onecall']
        self.weather_icon_size = self.config['weather']['iconsize']
        
           
if __name__ == "__main__" : 
    theApp = App()
    event = App()
    theApp.on_execute() 
