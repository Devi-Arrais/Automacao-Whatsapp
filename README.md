🚍 Automação de Inscrição do Transporte Universitário

Projeto desenvolvido para automatizar o preenchimento do formulário de utilização do transporte universitário da minha cidade.

O objetivo surgiu a partir de uma necessidade pessoal: os formulários eram disponibilizados muito cedo, exigindo que os estudantes acordassem antes do horário habitual para garantir uma vaga no transporte. Para evitar perder a inscrição e automatizar esse processo repetitivo, desenvolvi esta solução utilizando Python.

📖 Sobre o Projeto

A aplicação monitora o WhatsApp Web em tempo real e identifica automaticamente mensagens que contenham links do Google Forms utilizados para a solicitação do transporte universitário.

Ao detectar um novo formulário:

O link é extraído da mensagem.
O formulário é aberto em um navegador real.
Os dados do estudante são preenchidos automaticamente.
O formulário é enviado.

Dessa forma, o estudante consegue realizar a inscrição rapidamente, reduzindo o risco de perder sua vaga.

⚙️ Tecnologias Utilizadas
Python 3
Playwright
Selenium WebDriver
Google Chrome
dotenv
WhatsApp Web
Google Forms
🧠 Funcionamento
Monitoramento do WhatsApp

O sistema utiliza o Playwright para abrir o WhatsApp Web com um perfil persistente, permitindo manter a sessão autenticada.

Ele monitora constantemente as mensagens recebidas e procura por links de formulários do Google Forms.

Detecção do Formulário

Ao identificar uma URL válida, o sistema chama automaticamente o módulo responsável pelo preenchimento.

Preenchimento Automático

Utilizando Selenium e um perfil real do navegador, o sistema:

Marca a opção de registro do e-mail.
Preenche nome completo.
Preenche CPF.
Seleciona o tipo de utilização do transporte.
Seleciona a universidade.
Envia o formulário.

Os dados pessoais são carregados através de variáveis de ambiente, garantindo maior segurança.

🎓 Motivação

Este projeto foi desenvolvido durante minha graduação em Sistemas de Informação como uma forma de aplicar conhecimentos de automação, manipulação de navegadores e desenvolvimento em Python para resolver um problema real do cotidiano universitário.

Além de facilitar minha rotina, o projeto serviu como oportunidade de aprendizado em:

Automação web.
Manipulação de sessões e perfis de navegador.
Integração entre diferentes bibliotecas Python.
Tratamento de eventos em tempo real.
⚠️ Aviso

Este projeto foi desenvolvido exclusivamente para fins educacionais e uso pessoal.

Seu funcionamento depende da estrutura atual do Google Forms e do WhatsApp Web, podendo exigir ajustes caso essas plataformas sofram alterações.

Ainda preciso fazer alteração no preenchimento para conferir se os campos estão preenchido corretamente e analizar se enviou mesmo.

👨‍💻 Autor

Feito com ❤️ por um estudante que prefere dormir mais

Davi Arrais Feitosa
Estudante de Sistemas de Informação(IFCE campos Crato)
Residente Campos Sales CE