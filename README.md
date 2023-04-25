# WS2812 RGB Strip Weather Indicator

## Using a RGB Light Strip to indicate the 24 hour temperature range

###### I bought myself the excellent [Maker Advent Calendar - The 12 Projects of Codemas last Christmas](https://thepihut.com/products/maker-advent-calendar-includes-raspberry-pi-pico-h) . Sadly I didn't stick with my original plan just to work through a day at a time and treat myself to the goodies contained within. Come March, I finally thought to take a look in the last drawer, which turned out to contain a nice WS2812 addressable RGB light strip, sometimes known as NeoPixels.

###### Now the point is to use the goodies with the included RPi Pico H, but all the things I thought to use it for required internet access, so I hooked it up to a RPi 4 for this project instead.

### What You Need
###### 1. A Raspberry Pi with a power lead
###### 2. A micro SD card for some OS
###### 3. A WS2812 addressable RGB light strip
###### 4. A bread board or the willingness to solder directly to your GPIO pins (optional)
###### 5. Jumper leads (optional)
###### 6. An API key for the UK MET office API

###### With the strip I had, you could use female-female jumpers to go straight to the GPIO pins, but I didn't have any, so went through the breadboard.

IMAGE TO BE HERE - wiring guide

###### Once you have your API key, you need to hit the site list end point to get the ID for the location you want your forecast for. The API covers roughly 5000 sites across the UK. You'll use this when requesting your forecast.

###### From this point, you should be able to use the code in the repo wholesale, subbing in your API key for the hashed out example, likewise with the location code.

###### The pixel pin referenced in the code refers to the GPIO pin you use. It isn't absolute that you use this one, just be sure to reference correctly in your code.

###### As I expected to be the case, but disappointingly nevertheless, the temperature range in the UK is often so narrow over 24 hours that it's actually hard to distinguish any real difference in the pixels. In the 24 hour period I test this, the temperature range was 4-8 degrees, so only 3 colours on display, based on my RGB dictionary. You might find a better range. I went with -5C up to +25C as I figured that most temperatures in the UK will normally fall in this range; anything above or below just hitting the max or min colour option. I did consider adding in wind speed and percentage chance of precipitation with some method of distinguishing which forecast you're seeing, but given the relative lack of success on the temp scale...I didn't bother!







