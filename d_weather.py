import random as r
import json
import warnings
import requests
import contextlib

try:
    from functools import partialmethod
except ImportError:
    # Python 2 fallback: https://gist.github.com/carymrobbins/8940382
    from functools import partial

    class partialmethod(partial):
        def __get__(self, instance, owner):
            if instance is None:
                return self

            return partial(self.func, instance, *(self.args or ()), **(self.keywords or {}))

@contextlib.contextmanager
def no_ssl_verification():
    old_request = requests.Session.request
    requests.Session.request = partialmethod(old_request, verify=False)

    warnings.filterwarnings('ignore', 'Unverified HTTPS request')
    yield
    warnings.resetwarnings()

    requests.Session.request = old_request

conditions = ['Rainy', 'Cloudy', 'Sunny', 'Snowy', 'Stormy']
weather = conditions[r.randint(0,len(conditions) - 1)]
humidity = 0
temperature = 0
if(weather == 'Rainy'):
    humidity = r.randint(50, 100)
    temperature = r.randint(37, 85)
elif(weather == 'Cloudy'):
    humidity = r.randint(30, 70)
    temperature = r.randint(20, 95)
elif(weather == 'Sunny'):
    humidity = r.randint(10, 50)
    temperature = r.randint(20, 100)
elif(weather == 'Snowy'):
    humidity = r.randint(40, 80)
    temperature = r.randint(0, 25)
else:
    humidity = r.randint(70, 100)
    temperature = r.randint(60, 85)

def getWeather2():
    return ("Today's Forecast: " + weather + ", " + str(temperature) + "° Farenheit, " + str(humidity) + "% humidity.")


def getWeather():
    url = "http://api.openweathermap.org/data/2.5/weather?q=Atlanta,ga&appid=c2b65a5f2239fba3ad4b2affc41868a7"
    resp = requests.get(url=url)
    data = json.loads(resp.text)
    description = data["weather"][0]["description"]
    temperature = 1.8 * (data["main"]["temp"] - 273.15) + 32
    humidity = data["main"]["humidity"]
    return "Today's Forecast: " + description + ", " + str(int(temperature)) + "° Farenheit, " + str(humidity) + "% humidity."