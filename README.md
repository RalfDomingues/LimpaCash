<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>README - Script de Limpeza de Arquivos Temporários</title>
</head>
<body>

  <h1>Script de Limpeza de Arquivos Temporários (Windows)</h1>
  <p>
    Este script em <strong>Python</strong> foi desenvolvido para realizar a 
    <strong>limpeza de arquivos temporários e pastas de cache no Windows</strong>, 
    incluindo diretórios de usuários e a lixeira do sistema.
  </p>

  <h2>Funcionalidades</h2>
  <ul>
    <li>Remove arquivos e pastas temporárias do Windows.</li>
    <li>Limpa caches em <code>C:\Windows</code> (Temp, Logs, Prefetch, etc.).</li>
    <li>Remove arquivos de <code>AppData</code> de cada usuário do sistema.</li>
    <li>Opção interativa para esvaziar a Lixeira.</li>
    <li>Executa automaticamente com privilégios de administrador.</li>
  </ul>

  <h2>Requisitos</h2>
  <ul>
    <li>Windows 10 ou superior.</li>
    <li>Python 3.6 ou superior.</li>
    <li>Permissão de administrador (o script solicita automaticamente).</li>
  </ul>

  <h2>Como usar</h2>
  <ol>
    <li>Clone este repositório ou baixe o arquivo <code>limpeza_windows.py</code>.</li>
    <li>Abra o <strong>Prompt de Comando</strong> ou <strong>PowerShell</strong>.</li>
    <li>Execute:
      <pre><code>python limpeza_windows.py</code></pre>
    </li>
    <li>Ao final, será perguntado se deseja esvaziar a lixeira. 
      <br>Você tem 10 segundos para responder:
      <ul>
        <li><code>s</code> → esvaziar</li>
        <li><code>n</code> ou nenhuma resposta → não limpar</li>
      </ul>
    </li>
  </ol>

  <h2>Avisos</h2>
  <ul>
    <li>Utilize com cautela: os arquivos são excluídos permanentemente.</li>
    <li>É recomendado fechar programas antes da execução, para evitar erros de arquivos em uso.</li>
    <li>O script não remove arquivos críticos do Windows, mas sempre use por sua conta e risco.</li>
  </ul>

</body>
</html>
