#type: ignore
# boot.py -- run on boot-up
import network #type: ignore
from machine import Pin, ADC
def do_connect(ssid, key):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Conectando-se à rede...')
        sta_if.active(True)
        sta_if.connect(ssid, key)
        if not sta_if.isconnected():
            print('Conexão falhou')
            return False
    print('network config:', sta_if.ifconfig())
    return True

rele = Pin(25, Pin.OUT)
rele_oe = rele.off
rele_off = rele.on
rele_off()
hsensor = ADC(Pin(35))
hsensor.atten(ADC.ATTN_11DB)
svurl = 'svurl'
ssid = 'ssid'
passw = 'password'
