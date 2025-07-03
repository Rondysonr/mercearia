import subprocess

# Adiciona todos os arquivos
subprocess.run(["git", "add", "."], check=True)

# Faz commit com mensagem fixa
subprocess.run(["git", "commit", "-m", "save"], check=True)

# Envia para o repositório remoto
subprocess.run(["git", "push"], check=True)

# Puxa as alterações do repositório
subprocess.run(["git", "pull"], check=True)
