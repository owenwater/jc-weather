#!/usr/bin/python

from alfred_weather import WeatherWorkflow
from jcalfred import Item
from datetime import date

ICON_NAME=u"clear"
TODAY = u"today"
TOMORROW = u"tomorrow"
TIME_FORMAT=u"%H:%M"
class SunPhaseWorkflow(WeatherWorkflow):

    def _sun_phase_description(self, sunrise, sunset):
        content = ""
        if sunrise:
            content += u"Sunrise: {}".format(sunrise.strftime(TIME_FORMAT))
        if sunset:
            content += u", Sunset: {}".format(sunset.strftime(TIME_FORMAT))
        return content

    def _create_item(self, day_desc, content):
        title = u'{}: {}'.format(day_desc, content)
        icon = self._get_icon(ICON_NAME)
        return Item(title, icon=icon, valid=False)


    def tell_sun(self, location):
        """Tell sunrise and sunset time for today and following few days"""
        
        location = location.strip()
        weather = self._get_weather(location)

        items = []

        #TODO: alert

        today = self._get_current_date()
        today_sunrise = weather['info']['sunrise']
        today_sunset = weather['info']['sunset']
        offset = date.today() - today
        
        #TODO: remove code duplicated with super class here
        days = weather['forecast']
        if len(days) > self.config['days']:
            days = days[:self.config['days']]

        for day in days:
            if day['date'] == today:
                day_desc =  TODAY
            elif day['date'].day - today.day == 1:
                day_desc = TOMORROW
            else:
                day_desc = (day['date'] + offset).strftime('%A')
            #END TODO

            content = self._sun_phase_description(day.get('sunrise'), day.get('sunset'))

            if content == "":
                continue

            

            items.append(self._create_item(day_desc, content))
        
        if len(items) == 0:
            #Weather underground only return sunrise/sunset time of current day
            content = self._sun_phase_description(today_sunrise, today_sunset)
            if content != "":
                items.append(self._create_item(TODAY, content))

        return items



if __name__=="__main__":
    ap = SunPhaseWorkflow()
    ap.tell('sun')
