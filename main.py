import time
import os
import sys
import atexit
import logging
import daemon


def welcome_text(text):
    return f"""\
        --..,_                     _,.--.
        `'.'.                .'`__ o  `;__. {text}
            '.'.            .'.'`  '---'`  `
                '.`'--....--'`.'
                `'--....--'`
    """

## Deamon main class
class App:

    def __init__(self, command):
        self.command = command
        self.stdin_path = '/tmp/pyd'
        self.stdout_path = '/tmp/pyd/out.txt'
        self.stderr_path = '/tmp/pyd/err.txt'
        self.pid_path = '/tmp/pyd/pyd.pid'

        # configs
        logging.basicConfig(filename=self.stdout_path, encoding='utf-8', level=logging.DEBUG)

        # start command
        if self.command == 'start':
            # checking pid
            if self.check_pid() is True:
                logging.warning('deamon is already is running')
                sys.exit(1)
            else:
                self.setPid(self.stdin_path, self.pid_path, self.get_pid())
                self.run()
        
        # stop command
        if self.command == 'stop':
            self.stop_deamon()

    # Create or Write the pid file
    def setPid(self, path, filePath, pid):

        if not os.path.exists(path):
            os.makedirs(path)

        mode = 'w' if os.path.exists(filePath) else 'x' 
        file = open(filePath, mode)
        file.write(str(pid))
        file.close()

    # remove a pid file
    def remove_pid(self):
        try:
            logging.error('removing pid')
            os.remove(self.pid_path)
        except FileNotFoundError:
            logging.error('pid file not found')

    # checking pid file
    def check_pid(self):
        return os.path.exists(self.pid_path)
    
    # Getting current process PID
    def get_pid(self):
        return os.getpid()

    def read_pid_file(self):
        file = open(self.pid_path, 'r')
        data = file.read()
        file.close()
        return int(data)
    
    def get_running_pid(self):
        try:
            return self.read_pid_file()
        except FileNotFoundError:
            return 0

    # stop deamon
    def stop_deamon(self):
        pid = self.get_running_pid()
        if pid != 0:
            logging.error(f'pid :{pid} is removing')
            os.kill(pid, 9)
            self.remove_pid()

        sys.exit(1)


    # Running deamon
    def run(self):
        while True:
            print(f"pyd is running pid {self.get_pid()}")
            time.sleep(10)


def main():
    print(welcome_text('Python deamon example'))
    command = sys.argv[1]
    app = App(command)
    print(app)

if __name__ == '__main__':
    
    main()