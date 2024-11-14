# Automação de NFS

## Objetivo

Aplicação que permite a automação de processos de envio de notas fiscais recebidas por e-mail.

## Como usar

### Clonando repositório
```bash
git clone https://github.com/user/automacao-nfs.git
```

### Criando ambiente virtual
```bash
python -m venv <nome_do_ambiente>
```

### Ativando ambiente virtual
```bash
<nome_do_ambiente>\Scripts\activate
```

### Instalação de dependências
```bash
pip install requirements.txt
```

 Passe as credenciais de acesso:
 - Para o e-mail no onde será buscado as notas ficais (bot_web.py).
 - Para o e-mail que irá enviar as notas fiscais (disparo_email.py).

### Rodando o script
```bash
python main.py
```
