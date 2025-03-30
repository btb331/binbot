import network
import socket

from machine import Pin, PWM

from time import sleep

class Movement:

    def __init__(self) -> None:
        self.left_motor = PWM(Pin(2))
        self.right_motor = PWM(Pin(3))
        self.left_motor.freq(50)
        self.left_motor.duty_u16(0)
        self.right_motor.freq(50)
        self.right_motor.duty_u16(0)
        self.fwdValue = 8100
        self.bckValue = 1650

    def forwardStep(self, step):
        step = int(step)
        self.forward()
        if step > 0:
            sleep(step/10)
            self.stop()

    def backwardsStep(self, step):
        step = int(step)
        self.backwards()
        if step > 0:
            sleep(step/10)
            self.stop()

    def leftStep(self, step, pivot = True):
        step = int(step)
        self.left(pivot)
        if step > 0:
            sleep(step/10)
            self.stop()

    def rightStep(self, step, pivot = True):
        step = int(step)
        self.right(pivot)
        if step > 0:
            sleep(step/10)
            self.stop()

    def forward(self):
        self.reset()
        self.right_motor.duty_u16(self.fwdValue)
        sleep(0.05)
        self.left_motor.duty_u16(self.bckValue)

    def backwards(self):
        self.reset()
        self.right_motor.duty_u16(self.bckValue)
        sleep(0.05)
        self.left_motor.duty_u16(self.fwdValue)

    def left(self, pivot = True):
        self.reset()
        if pivot:
            print("left pivot")
            self.right_motor.duty_u16(self.bckValue)
        else:
            self.right_motor.duty_u16(0)
            print("left turn")
        sleep(0.05)
        self.left_motor.duty_u16(self.bckValue)

    def right(self, pivot = True):
        self.reset()
        self.right_motor.duty_u16(self.fwdValue)
        sleep(0.05)
        if pivot:
            self.left_motor.duty_u16(self.fwdValue)
        else:
            self.left_motor.duty_u16(0)
    
    def reset(self):
        self.left_motor.duty_u16(0)
        self.right_motor.duty_u16(0)
        sleep(0.25)
    
    def stop(self):
        self.left_motor.duty_u16(0)
        self.right_motor.duty_u16(0)



movement = Movement()

#region wifi
ssid = 'xxx'
password = 'xxx'
#endregion

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Directional Buttons</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            font-family: Arial, sans-serif;
        }
        .button-container {
            display: grid;
            grid-template-columns: 100px 100px 100px;
            grid-template-rows: 100px 100px;
            gap: 10px;
        }
        button {
            width: 100px;
            height: 50px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Control Panel</h1>
    <div class="button-container">
        <button onclick="forward()">Forward</button>
        <button onclick="makeRequest('left', 0,  true)">Pivot Left</button>
        <button onclick="makeRequest('right', 0, true)">Pivot Right</button>
        <button onclick="backward()">Backward</button>
        <button onclick="stop()">Stop</button>
        <button onclick="makeRequest('left', 0, false)">Turn left</button>
        <button onclick="makeRequest('right', 0, false)">Turn right</button>
    </div>
    <div class="button-container">
            Step:
            <button onclick="stepChange(false, 10)" style="height: 30px;width: 40px;">-10</button>
            <button onclick="stepChange(false, 1)" style="height: 30px;width: 40px;">-1</button>
            <span id="step"> 5 </span>
            <button onclick="stepChange(true, 1)" style="height: 30px;width: 40px;">+1</button>
            <button onclick="stepChange(true, 10)" style="height: 30px;width: 40px;">+10</button>
        </div>
    <div class="button-container">
        <button onclick="makeRequest('forward', true, false)">Forward step</button>
        <button onclick="makeRequest('left', true, false)">Turn Left step</button>
        <button onclick="makeRequest('right', true, false)">Turn Right step</button>
        <button onclick="makeRequest('backward', true, false)">Backward step</button>
        <button onclick="makeRequest('stop', false, false)">Stop</button>
        <button onclick="makeRequest('left', true, true)">Pivot Left step</button>
        <button onclick="makeRequest('right', true, true)">Pivot Right step</button>
    </div>

    <script>

        function makeRequest(direction, step, pivot = true) {
            if (step) {
                span = document.getElementById("step")
                step = parseInt(span.innerHTML)
            }else{
                step = 0
            }
            var loc = window.location.href;
            url = `${loc}${direction}?`
            if (step) {
                url = url + "step=" + step + "&"
            }
            url = url + "pivot=" + pivot
            
            console.log(url)
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Network response was not ok: ${response.statusText}`);
                    }
                    console.log(`${direction} request sent successfully`);
                })
                .catch(error => console.error(`There was a problem with the fetch operation:`, error));
        }
        function forward() {
            makeRequest('forward', false);
        }

        function backward() {
            makeRequest('backward', false);
        }

        function left() {
            makeRequest('left', false);
        }

        function right() {
           makeRequest('right', false);
        }

        function stop() {
           makeRequest('stop', false);
        }

        function stepChange(increase, increment) {
            span = document.getElementById("step")
            current = parseInt(span.innerHTML)
            if (increase) {
                newValue = current + increment
            }
            else {
                newValue = current - increment
            }
            if (newValue < 1) {
                newValue = 1
            }
            span.innerHTML = newValue
        }
    </script>
</body>
</html>

"""

max_wait = 30
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    sleep(3)

if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
led = Pin("LED", Pin.OUT)
led.on()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        stepRequest = 0

        request = str(request)
        url = request.split(" ")[1]
        print(url)
        params = url.split("?")
        pivot = True
        if len(params) > 1:
            params = params[1]
            params = params.split('&')
            variables = {}
            for param in params:
                val = param.split('=')
                variables[val[0]] = val[1]
            print(variables)
            if 'step' in variables:
                stepRequest = variables['step']
            if 'pivot' in variables:
                pivot = variables['pivot']
                if pivot == 'false':
                    pivot = False
        print(stepRequest)
        if 'forward' in request:
            movement.forwardStep(stepRequest)
        if 'backward' in request:
            movement.backwardsStep(stepRequest)
        if 'left' in request:
            movement.leftStep(stepRequest, pivot)
        if 'right' in request:
            movement.rightStep(stepRequest, pivot)
        if 'stop' in request:
            movement.stop()

        if url == "/":
            response = html
        else:
            response = "OK"

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')
