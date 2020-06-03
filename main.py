import network
from machine import Pin,PWM
import socket #导入socket库

ap = network.WLAN(network.AP_IF)
ap.active(True)         
ap.config(essid='LJX_WiFi') #配置接入点信息
ap.config(authmode=3, password='12345678')

#1电机
M1A=PWM(Pin(13),  freq=1000,  duty=0)  #开发板GPIO13,14 连接L9110S(U3) IA IB
M1B=PWM(Pin(14),  freq=1000,  duty=0)  
#2电机
M2A=PWM(Pin(26),  freq=1000,  duty=0)  #开发板GPIO26,27 连接L9110S(U4) IA IB
M2B=PWM(Pin(27),  freq=1000,  duty=0)

led=Pin(2,Pin.OUT)# 初始化LED管脚，低电平点亮
usb_socket=Pin(17,Pin.OUT)
usb_socket.value(1)
 

def go_ahead():     #前进
	M1A.duty(650)
	M1B.duty(0)
	M2A.duty(650)
	M2B.duty(0)

def go_back():
	M1A.duty(0)
	M1B.duty(650)
	M2A.duty(0)
	M2B.duty(650)

def turn_right():
	M1A.duty(600)
	M1B.duty(0)
	M2A.duty(0)
	M2B.duty(0)

def turn_left():
	M1A.duty(0)
	M1B.duty(0)
	M2A.duty(600)
	M2B.duty(0)

def stop():
	M1A.duty(0)
	M1B.duty(0)
	M2A.duty(0)
	M2B.duty(0)
    
def web_page():
  if led.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  
  html = """<html>
	<head> 
	<title>ZhimaDIY Web Server</title> 
	<meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> 
  <style>
	  html
	  {
		  font-family: Helvetica; 
		  display:inline-block; 
		  margin: 0px auto; 
		  text-align: center;
	  }
  h1
  {
	  color: #0F3376; 
	  padding: 2vh;
   }
   p
   {
	   font-size: 1.5rem;
	}
	.button
	{
		display: inline-block; 
		background-color: #e7bd3b;
		border: none; 
		border-radius: 4px; 
		color: white; 
		padding: 16px 40px; 
		text-decoration: none; 
		font-size: 30px; 
		margin: 2px; 
		cursor: pointer;
	}
  .button2
  {
	  background-color: #4286f4;
  }
  .button_a
  {
	  font-size: 20px; 
  	  background-color: #e33e33;
  }
  .button_b
  {
	  font-size: 20px; 
  	  background-color: #00007f;
  }
  .button_l
  {
	  font-size: 20px; 
  	  background-color: #00557f;
  }
  .button_r
  {
	  font-size: 20px; 
  	  background-color: #55ffff;
  }
  .button_s
  {
  	  font-size: 20px; 
  	  background-color: #ff0000;
  }
  </style>
	</head>
		<body> 
				<h1>ESP Web Server</h1> 
		<p>
			GPIO state: <strong>""" + gpio_state + """</strong></p>
		<p>
			<a href="/?led=on">
				<button class="button">ON</button>
			</a>
		</p>
		<p>
		  <a href="/?led=off">
			  <button class="button button2">OFF</button>
		  </a>
		</p>
		<p>
		  <a href="/?advance">
			  <button class="button button_a">Advance</button>
		  </a>
		</p>
		<p>
		  <a href="/?left">
			  <button class="button button_l">Left</button>
		  </a>
		  <a href="/?right">
		  			  <button class="button button_r">Right</button>
		  </a>
		</p>
		<p>
		  <a href="/?back">
			  <button class="button button_b">Back</button>
		  </a>
		</p>
		<p>
		  <a href="/?s_stop">
			  <button class="button button_s">Stop</button>
		  </a>
		</p>
	</body>
</html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
print('after connecting wifi ,input this ip:')
print(ap.ifconfig()[0])
print('')
while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(2048)
  request = str(request)
  print('Content = %s' % request)
  
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  advance=request.find('/?advance')
  back=request.find('/?back')
  #print(back)
  left=request.find('/?left')
  right=request.find('/?right')
  s_stop=request.find('/?s_stop')
  if led_on == 6:
    print('LED ON')
    led.value(1)
    usb_socket.value(0)
  if led_off == 6:
    print('LED OFF')
    led.value(0)
    usb_socket.value(1)
  if advance == 6:
      go_ahead()
      print('Go ahead!')
  if back == 6:
      go_back()
      print('Go back!')
  if left == 6:
      turn_left()
      print('Turn left')
  if right== 6:
      turn_right()
      print('Turn right')
  if  s_stop==6:
      stop()
      print('Stop!!!')
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()   
    
