
import socket
import pyaudio
import threading
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

version = 1.0

class AudioClientWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.title_label = Label(text="PRIME FM", font_size=27, color=(24/255, 87/255, 255/255, 1))
        self.add_widget(self.title_label)

        self.ip_input = TextInput(multiline=False, hint_text="IP", font_size=12,
                                  background_color=(1, 1, 1, 1), foreground_color=(24/255, 87/255, 255/255, 1),
                                  size_hint=(1, None), height=40)
        self.add_widget(self.ip_input)

        self.port_input = TextInput(multiline=False, hint_text="PORT", font_size=12,
                                    background_color=(1, 1, 1, 1), foreground_color=(24/255, 87/255, 255/255, 1),
                                    size_hint=(1, None), height=40)
        self.add_widget(self.port_input)

        self.connect_button = Button(text="CONNECT", font_size=15, background_color=(24/255, 87/255, 255/255, 1),
                                     color=(0, 0, 0, 1), size_hint=(1, None), height=40)
        self.connect_button.bind(on_release=self.connect_to_server)
        self.add_widget(self.connect_button)

        self.disconnect_button = Button(text="DISCONECT", font_size=15, background_color=(24/255, 87/255, 255/255, 1),
                                        color=(0, 0, 0, 1), size_hint=(1, None), height=40, disabled=True)
        self.disconnect_button.bind(on_release=self.disconnect_from_server)
        self.add_widget(self.disconnect_button)

        self.status_label = Label(text="Стан: Відключено", color=(24/255, 87/255, 255/255, 1))
        self.add_widget(self.status_label)

        self.version_label = Label(text=f"Version: {version}", color=(24/255, 87/255, 255/255, 1))
        self.add_widget(self.version_label)

        self.site_label = Label(text="WEBSITE: https://primsua.wixsite.com/prime-fm", color=(24/255, 87/255, 255/255, 1))
        self.add_widget(self.site_label)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.connected = False

    def connect_to_server(self, instance):

        if self.connected:
            return

        server_ip = self.ip_input.text
        server_port = int(self.port_input.text)

        server_address = (server_ip, server_port)

        try:
            self.client_socket.connect(server_address)
            self.stream = self.audio.open(format=pyaudio.paInt16,
                                          channels=1,
                                          rate=44100,
                                          output=True,
                                          frames_per_buffer=4096)

            self.connected = True
            self.connect_button.disabled = True
            self.disconnect_button.disabled = False
            self.status_label.text = "Стан: Підключено: ⚡PRIME FM⚡"

            threading.Thread(target=self.receive_audio).start()

        except Exception as e:
            self.status_label.text = f"Помилка з'єднання: {str(e)}"

    def disconnect_from_server(self, instance):
        if not self.connected:
            return

        try:
            self.client_socket.close()
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()

            self.connected = False
            self.connect_button.disabled = False
            self.disconnect_button.disabled = True
            self.status_label.text = "Стан: Відключено"

        except Exception as e:
            self.status_label.text = f"Помилка Відключення: {str(e)}"

    def receive_audio(self):
        while self.connected:
            try:
                data = self.client_socket.recv(4096)
                self.stream.write(data)

            except Exception as e:
                self.status_label.text = f"Помилка прийому аудіо: {str(e)}"
                self.disconnect_from_server(None)
                break


class AudioClientApp(App):
    def build(self):
        client_widget = AudioClientWidget()
        return client_widget


if __name__ == "__main__":
    AudioClientApp().run()

