
# HomeDisplay
a rather simple home display for time and temperature with shelly HT

## MainUI:

![MainUI](https://user-images.githubusercontent.com/76942248/114690073-a9e30180-9d16-11eb-822c-ea02a6508b49.png)

## ForecastUI:

![ForecastUI](https://user-images.githubusercontent.com/76942248/114690317-da2aa000-9d16-11eb-9fd2-965c9307e108.png)


## config.json:

set values as needed:

* fullscreen: ture/false
* display_size: [X, Y] in pixel
* mouse_visible: 0/1, 0 = not visible 
* bg_IMG: background image
* uirevtime: time the forecast ui is visible when screen is clicked (only if weather -> onecall: true)
* unit: C or F
* utctime: true/false
* font
  * name: name of font file
  * size (change as you need)
    * tiny
    * small
    * middle
    * big
    * giant
* colors
  * grey
  * light_grey
  * white
  * blue
  * red
* shelly (get from my.shelly.cloud)
  * statusServer: in user settings / security -> Server 
  * id: in your shelly HT -> settings -> device settings -> device id
  * authKey: in user settings / security -> authorization key
  * upinterval: minimum 10 or your update settings of your shelly ht in minutes
* weather (openweathermap.org account needed!)
  * apikey: your openweathermap apikey
  * url:  current weather data [Reference](https://openweathermap.org/current)
  * urlonecall: weather with forecast [Reference](https://openweathermap.org/api/one-call-api)
  * locationid: yor location [Reference](http://bulk.openweathermap.org/sample/)
  * lon: your longitude
  * lat: your latitude
  * units: [Reference](https://openweathermap.org/current#data)
  * exclude: [Reference](https://openweathermap.org/api/one-call-api)
  * onecall: true/false, true for forecast
  * iconsize: small/big

## additional info:
Font: [the wild breath of zelda](https://www.dafont.com/de/the-wild-breath-of-zelda.font)

Weather icons: [OpenWeatherMap](https://openweathermap.org/)

provided background images made by [Florian Kolaritsch](https://www.instagram.com/flovahkiin_/)

shelly api key and server

![ShellyAuthKeyServer](https://user-images.githubusercontent.com/76942248/114697822-a6ec0f00-9d1e-11eb-86c2-75d61ff6927a.png)

shelly device id

![ShellyDeviceID](https://user-images.githubusercontent.com/76942248/114697831-a94e6900-9d1e-11eb-8082-dfdedde9b6a6.png)

openweathermap api key

![OpenWeatherMapAPIKey](https://user-images.githubusercontent.com/76942248/114697847-ae131d00-9d1e-11eb-90da-29f0c5eaabde.png)

if there is a problem with the update time of your shelly ht edit the location settings from automatic detection to manual and fill in your location settings

![locationsetting](https://user-images.githubusercontent.com/76942248/114759329-51375700-9d5e-11eb-8835-f2755aa89d36.png)



  
