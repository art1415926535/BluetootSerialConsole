import bluetooth


class Controller:
    def __init__(self):

        self.bd_addr = ""
        self.bd_name = ""
        self.update_prompt()

        self.commands = {
            "connect": self.connect,
            "disconnect": self.disconnect,
            "send": self.send,
            "help": self.help,
        }

    def connect(self, name=''):
        if self.bd_addr:
            self.disconnect()

        selected = self.__choose_device(name)
        if selected:
            self.__socket_connect()
            self.update_prompt()

    def __choose_device(self, name):
        if not name:
            print("Searching for devices...")
            nearby_devices = bluetooth.discover_devices()

            num = 0
            print("Select your device by entering its coresponding number or type [exit]:")
            for i, device in enumerate(nearby_devices):
                print("{number}: {addr} {name}".format(number=i+1, addr=device,
                        name=bluetooth.lookup_name(device)))

            user_input = input("> ")
            if user_input == 'exit':
                exit(0)
            try:
                selection = int(user_input)-1
            except ValueError:
                print("Value error")
                return False
        else:
            print("Searching for", name)
            nearby_devices = bluetooth.discover_devices()
            selection = -1
            for i, device in enumerate(nearby_devices):
                if name == bluetooth.lookup_name(device):
                    selection = i

        if 0 <= selection < len(nearby_devices):
            self.bd_addr = nearby_devices[selection]
            self.bd_name = bluetooth.lookup_name(nearby_devices[selection])
            print("You have selected", self.bd_name)
            return True
        else:
            print("Device not found")
            return False

    def __socket_connect(self):
        self.sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        port = 0
        max_port = 3
        connected = False

        while not connected and port <= max_port:
            try:
                self.sock.connect((self.bd_addr, port))
                connected = True
                print("Connected!")
            except:
                port += 1
        if port > max_port:
            print("Connected error: port detection failed")
            self.disconnect()
            self.loop()

    def update_prompt(self):
        if self.bd_addr:
            self.prompt = "{addr} [{name}]> ".format(addr=self.bd_addr, name=self.bd_name)
        else:
            self.prompt= "> "

    def disconnect(self):
        self.sock.close()
        self.bd_addr = ''
        self.bd_name = ''
        self.update_prompt()

    def send(self, data=''):
        if self.bd_addr:
            self.sock.send(bytes(data, 'UTF-8'))
        else:
            print("Error: socket not bound. Try connect to device.")

    def help(self):
        text = [
            "Commands:",
            " connect [DEVICE_NAME]:  search new device or connect by DEVICE_NAME",
            " disconnect :  disconnect from " + (
                    self.bd_name if self.bd_name else "device"),
            " send DATA :  send DATA",
            " help :  this text",
            " exit :  stops console loops and exits program"
        ]
        print()
        print('\n'.join(text))
        print()

    def loop(self):
        while True:
            cmd = input(self.prompt)

            if cmd == "exit":
                break

            self.exec_command(cmd)

    def exec_command(self, cmd):
        try:
            if cmd.find(' ') != -1:
                command = cmd[:cmd.find(' ')]
                data = cmd[cmd.find(' ')+1:]
                self.commands[command](data)
            else:
                command = cmd
                self.commands[command]()

        except KeyError:
            print("Error: command not found")


if __name__ == '__main__':
    controller = Controller()
    controller.loop()
