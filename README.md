# irrigador-automatico

Este repositório contém o código utilizado no projeto de um irrigador automático feito com ESP32 para uma disciplina de faculdade.
Existem duas versões: uma feita com c++ e usando a ferramenta Blynk como interface de usuário, e outra utilizando micropython, uma interface web simples e uma api local.

![image](https://github.com/RenderV/irrigador-automatico/assets/92237089/b954ffcc-515b-4da8-b93a-3ec61b1dfcf0)

COM BLYNK:

![image](https://github.com/RenderV/irrigador-automatico/assets/92237089/f7a15d54-7dd1-4677-abdb-64f0e860fcc2)

#### Funcionamento

O algoritmo analisa os valores do sensor de umidade e converte em porcentagem. Para isso, foi realizada uma calibração do sensor, baseado nos valores mínimos e máximos dos sensores quando colocado em ambientes secos e submersos na água. 
A bomba pode ser acionada manualmente ou de forma automática. No modo automático, caso a umidade esteja abaixo de um valor pré-definido, a irrigação é realizada. Depois, para evitar a ativação contínua da bomba em caso de problemas no sensor, é estabelecido um intervalo de tempo pelo qual a bomba não pode ser reativada. O ESP32 envia periodicamente as informações do sensor para o servidor por meio de uma REST API, permitindo sua monitoração constante. Além disso, o dispositivo verifica regularmente se há novos comandos a serem recebidos (polling).

#### Materiais Utilizados

- ESP32
- Sensor de Umidade
- Mangueira de 1m
- Mini Bomba de Água
- Relé
- Vaso
- Bateria 12V 7A/h
- Painel Fotovoltaico
- Caixa
- Controlador de Carga
- Tinta

![image](https://github.com/RenderV/irrigador-automatico/assets/92237089/6ca4d3df-66a2-473d-9532-3ad7eb847f25)


#### Integrantes do grupo

André Pereira, César Almeida, Darlan Oliveira, Gustavo Tamezava, Lucas Campos, Renderson de Meira, Thiago Honma e Vinícius Araújo
