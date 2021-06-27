# Programação Distribuida - Relógios vetoriais
> Autor: Ariel Rossetto Ril
> Matrícula: 15105050
> Email: ariel.ril@edu.pucrs.br
> Repositório: https://github.com/arielril/distr-prog-vectorial-clocks

## Introdução
Neste trabalho é apresentado uma implementação de um programa distribuido que utiliza relógios vetoriais para sincronização entre processos. Cada processo do programa distribuido possui uma lista de referência para identificacação de onde esta cada processo (IP e porta) para realizar o envio de pacotes UDP.

## Desenvolvimento
Para realizar o desenvolvimento deste trabalho foi utilizado a linguagem de programação **Python** e os pacotes:
- *socket*: utilizado para comunicação UDP
- *threading*: para execução dos procesos de recebimento e envio de mensagens de forma independente

### Organização
O programa desenvolvido esta organizado em:
- Index
- Starter
- Node

#### Index
Este é o arquivo principal para organizar a incialização dos processos e coordenação de encerramento. Neste arquivo é realizado o parsing do arquivo de configuração (*data/config*) na função *parse_config* e é realizado a inicialização da espera do inicio de execução executando a função *await_start*.

![[Pasted image 20210627124442.png]]

#### Starter
Ester arquivo foi criado apenas para inicializar a execução do programa, realizando o envio de uma mensagem de inicialização para os processos usando um grupo multicast.

![[Pasted image 20210627124620.png]]

#### Node
Este é o arquivo principal do trabalho, pois possui toda a lógica para comunicação entre processos, sincronização de processos utilizando relógios vetoriais e controle  do relógio local de cada processo. Cada instância possui um dicionário informando onde cada processo está  localizado para envio de mensagens de sincronização. Neste arquivo existe os métodos:

- *\_\_init\_\_*: para realizar a inicialização de uma instância de um processo
- *interact*: o qual realiza a geração de eventos locais (incremento do relógio local) e realiza a geração de eventos de mensagem para entre processos (incremento do relógio local e envio de mensagem para outro processo)
- *listen*: para receber as mensagens de outros procesoss e realizar a sincronização do relógio vetorial
- *await_start*: para esperar a mensagem de inicialização, escutando o grupo multicast UDP

![[Pasted image 20210627130402.png]]

## Demonstração

### Máquinas virtuais
Para inicias as máquinas virtuais para a demonstração é necessário ter a ferramenta **vagrant**(https://www.vagrantup.com) instalada além de possuir VirtualBox instalado. Após instalar as ferramentas necessárias é preciso estar na pasta `machine`, a qual contém o arquivo `Vagrantfile` com as configurações necessárias para inciar 3 máquinas virtuais, para executar o comando `vagrant up`.

![[Screen Shot 2021-06-27 at 11.44.04 AM.png]]

### Simulação
Para executar a simulação é possível iniciar a quantidade que quiser de conexões com as máquinas virtuais, para este trabalho foi utilizado 3 máquinas virtuais. Para este trabalho foi utilizado 6 terminais, 2 em cada máquina virtual. Em 5 terminais foram inicializados os processos para execução da simulação e um terminal foi utilizado para executar o arquivo de inicialização.

![[Screen Shot 2021-06-27 at 11.45.16 AM.png]]

![[Pasted image 20210627205633.png]]



