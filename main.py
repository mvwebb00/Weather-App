import sys
import requests
from PyQt5.QtWidgets import (QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize UI components
        self.city_label = QLabel('Enter city name:', self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton('Get Weather', self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()

    def initUI(self):
        # Set window title
        self.setWindowTitle('Weather App')

        # Create and set layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        # Center align labels and input
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Set object names for styling
        self.city_label.setObjectName('city_label')
        self.city_input.setObjectName('city_input')
        self.get_weather_button.setObjectName('get_weather_button')
        self.temperature_label.setObjectName('temperature_label')
        self.emoji_label.setObjectName('emoji_label')
        self.description_label.setObjectName('description_label')

        # Apply styles
        self.setStyleSheet('''
            QLabel, QPushButton {
                font-family: 'Arial';
            }

            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }

            QLineEdit#city_input {
                font-size: 40px;
            }

            QPushButton#get_weather_button {
                font-size: 30px;
                font-weight: bold;
            }

            QLabel#temperature_label {
                font-size: 75px;
                
            }

            QLabel#emoji_label {
                font-size: 100px;
                font-family: 'Segoe UI Emoji';
            }

            QLabel#description_label {
                font-size: 50px;
            }
        ''')

        # Connect button click to get_weather method
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        # OpenWeatherMap API key and URL
        api_key = "5b757916eea5205623747cf101eca2e4"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
       
        try:
            # Make API request
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Check if the response is successful
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            # Handle HTTP errors
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input.")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API Key.")
                case 403:
                    self.display_error("Forbidden:\nAccess is Denied.")
                case 404:
                    self.display_error("Not Found:\nCity not Found.")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later.")
                case 502:
                    self.display_error("Bad gateway:\nInvalid response from server.")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down.")
                case 504:
                    self.display_error("Gateway timeout:\nNo response from server.")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck internet connection.")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nRequest timed out.")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\nCheck the URL.")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"An error occurred:\n{req_error}")
        

    def display_error(self, message):
        # Display error message
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        # Display weather information
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        temperature_f = (temperature_k * 9/5) - 459.67
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]


        
        self.temperature_label.setText(f"{temperature_f:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):
        # Return emoji based on weather condition
        match weather_id:
            case 200 | 201 | 202 | 210 | 211 | 212 | 221 | 230 | 231 | 232:
                return "⛈️"
            case 300 | 301 | 302 | 310 | 311 | 312 | 313 | 314 | 321:
                return "🌧️"
            case 500 | 501 | 502 | 503 | 504 | 511 | 520 | 521 | 522 | 531:
                return "🌧️"
            case 600 | 601 | 602 | 611 | 612 | 613 | 615 | 616 | 620 | 621 | 622:
                return "❄️"
            case 701 | 711 | 721 | 731 | 741 | 751 | 761 | 762 | 771 | 781:
                return "🌫️"
            case 800:
                return "☀️"
            case 801 | 802:
                return "⛅"
            case 803 | 804:
                return "☁️"
            case _:
                return "❓"


if __name__ == '__main__':
    # Run the application
    app = QApplication(sys.argv)
    WeatherApp = WeatherApp()
    WeatherApp.show()
    sys.exit(app.exec_())