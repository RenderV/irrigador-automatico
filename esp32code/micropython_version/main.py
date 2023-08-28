# type: ignore
import utime
import urequests
import random

class lil_logger:
    def __init__(self):
        self.last_log = ''
        self.last_call = 0
    def __call__(self, log, delay=10):
        if self.last_log == log and utime.time() - self.last_call < delay:
            pass
        elif self.last_log == log:
            print(log)
            self.last_call = utime.time()
        else:
            print(log)
            self.last_call = utime.time()
            self.last_log = log


def connect_loop(ssid, key):
    while True:
        try:
            if do_connect(ssid, key):
                break
        except OSError:
            utime.sleep(1)

def get_humidity(minh=940, maxh=2695):
    then = utime.time()
    last = []
    for i in range(100):
        h = hsensor.read()
        last.append(h)
    avg = sum(last)/len(last)
    pct_avg = 1-(0 + (avg - minh) * (1 - 0) / (maxh - minh))
    pct_avg = 0 if pct_avg < 0 else pct_avg
    return pct_avg

def update_humidity(value, last_update=0):
    r = urequests.put(svurl+f'/update_humidity?info={value}')
    r.close()
    return utime.time()

def timed_irrigation(action, last_activation, activation_time):
    if action == 'OFF' and utime.time()-last_activation >= activation_time:
        rele_off()
        return False
    elif action=='ON':
        rele_on()
        print('[INFO] Bomba ativada.')
        return True

def main():
    log = lil_logger()
    connect_loop(ssid, passw)
    i = 1
    min_time = 60
    last_activation = 0
    min_humidity = 0.6
    activation_time = 2
    last_update = 0
    update_interval = 1
    last_activation=0
    rele_is_on = False
    while True:
        try:
            h = get_humidity()
            if utime.time() - last_update > update_interval:
                try:
                    print(f'[I] Enviado valor de umidade: {h*100:.2f}')
                    last_update = update_humidity(h, last_update)
                except OSError:
                    log('[E] Erro de rede: não foi possível conectar-se ao servidor')
            elapsed = utime.time() - last_activation
            if h <= min_humidity and elapsed >= 10:
                # rele_on()
                rele_is_on = timed_irrigation('ON', last_activation, activation_time)
                last_activation = utime.time()
                if not rele_is_on:
                    log(f'[I] Valor de umidade abaixo do mínimo de {min_humidity}. Regando por {activation_time} segundos...')
                    # utime.sleep(activation_time)
                    log(f'[I] Próxima irrigação automática não pode ocorrer em menos de {min_time} segundos.')
                continue
            elif elapsed <= 10 and h <= min_humidity:
                # rele_off()
                rele_is_on = timed_irrigation('OFF', last_activation, activation_time)
                if not rele_is_on:
                    log(f'[I] Última ativação ocorreu em menos de {min_time} segundos, mas a humidade é menor que {min_humidity*100}%.')
                else:
                    print('[INFO] Bomba desativada')
            else:
                # rele_off()
                rele_is_on = timed_irrigation('OFF', last_activation, activation_time)
            utime.sleep(0.2)
        except ValueError:
            log('[E] Valor inválido.', 4)

main()
