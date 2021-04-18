# iSpirito Bot

Esse projeto foi realizado como parte do primeiro iHackathon! Feito por [Daniel Henrique](https://github.com/danhenrik) e [Gabriel Sellin](https://github.com/sellings-dev/)

Trata-se de um bot do telegram representando o mascote da empresa da iJunior, feito para auxiliar com tarefas pessoais e funcionalidades em grupos da empresa.

## Quickstart

Esse bot já está rodando atualmente em um servidor Heroku. Basta encontrá-lo pesquisando @iSpirito_Bot no telegram e já é possível interagir com o mesmo.

## Arquivos

- `app.py`: Arquivo principal, inicializa o bot e processos auxiliares
- `db.py`: Conexão com o banco de dados. MongoDB Atlas
- `env.py`: Arquivo para importação das variáveis de ambiente do .env
- `mail.py`: Configuração do serviço de envio de email
- `scheduledEvents.py`: Arquivo contendo funções de monitoramento de eventos programados
- `/convs`: Módulo contendo em arquivos separados cada uma das conversas aninhadas, incluindo o ConversationHandler associado e as funções de cada estado da conversa.

## Tecnologias Utilizadas

- python-telegram-bot: Biblioteca para gerenciamento de interações com o bot
- smtplib: Biblioteca para configuração de servidor SMTP e envio de email
- pymongo: Biblioteca para gerenciamento de conexão e interação com MongoDB
- schedule: Biblioteca usada para gerenciar eventos programados
- threading e multiprocessing: Bibliotecas usadas para gerenciar múltiplos processos dentro do mesmo programa

#### Agradecimentos especiais à equipe organizadora do evento!
