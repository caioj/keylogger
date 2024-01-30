# Keylogger e Monitoramento - Projeto Desafio Módulo 2

Este é um projeto simples de keylogger e monitoramento para fins educacionais. O script Python é projetado para coletar informações do sistema, registros de teclas pressionadas, capturas de tela e conteúdo da área de transferência.

**Nota:** Este script é destinado apenas para fins educacionais e deve ser usado de maneira ética e legal.

## Funcionalidades

1. **Coleta de Dados:**
   - Informações do sistema (hostname, endereço IP, processador, sistema operacional, etc.).
   - Logs de teclas pressionadas.
   - Capturas de tela.
   - Conteúdo da área de transferência.

2. **Envio de Dados:**
   - Envio de logs e capturas de tela por e-mail ou Telegram.

3. **Criptografia:**
   - Criptografia dos arquivos de logs antes de enviá-los.

4. **Verificação Diária:**
   - Verificação diária de um diretório específico.

## Requisitos

- Python 3.x
- Bibliotecas Python: `schedule`, `requests`, `pynput`, `PIL`, `cryptography`, `win32clipboard`
