# Guia de Deploy no Streamlit Community Cloud

Este guia ensina como publicar o projeto **Carros Elétricos no Brasil** na plataforma oficial e gratuita do [Streamlit Community Cloud](https://share.streamlit.io/).

---

## Visão Geral

O **Streamlit Community Cloud** se conecta diretamente à sua conta do GitHub e oferece:
- Deploy automatizado e contínuo (cada `git push` atualiza o app em produção).
- Certificado SSL (HTTPS) gratuito e automático.
- URL pública para compartilhar com a equipe e clientes.
- Acesso fácil aos logs em tempo real para monitoramento.

---

## Pré-requisitos

1. Ter uma conta no [GitHub](https://github.com).
2. Ter o código do projeto versionado e publicado em um repositório no GitHub (público ou privado).
3. Ter uma conta no [Streamlit Community Cloud](https://share.streamlit.io) vinculada ao mesmo GitHub.

---

## Passo a Passo para o Deploy

### Passo 1: Subir o Projeto no GitHub

Se você ainda não enviou o projeto para o GitHub, crie um repositório e execute no terminal:

```bash
# Entre na pasta do projeto
cd carros-eletricos-dashboard

# Inicie o repositório git (se ainda não iniciado)
git init
git add .
git commit -m "feat: first commit da base do dashboard de carros eletricos"

# Conecte ao seu repositório remoto (ajuste a URL para o seu usuário/repo)
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git
git push -u origin main
```

---

### Passo 2: Conectar no Streamlit Community Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io/).
2. Faça login clicando em **Continue with GitHub**.
3. No painel principal, clique no botão superior direito: **"Create app"** ou **"New app"**.

---

### Passo 3: Configurar os Parâmetros da Aplicação

Na tela de configuração (Deploy an app), preencha:

1. **Repository:** Selecione o seu repositório (ex: `seu-usuario/seu-repositorio`).
2. **Branch:** `main` (ou a branch principal que você estiver utilizando).
3. **Main file path:** 
   - Se o repositório no GitHub contiver os arquivos do projeto diretamente na raiz:
     ```text
     app.py
     ```
   - Se o repositório no GitHub contiver a pasta `carros-eletricos-dashboard` no primeiro nível:
     ```text
     carros-eletricos-dashboard/app.py
     ```
4. **App URL (Opcional):** Você pode personalizar o subdomínio, por exemplo:
   `carros-eletricos-brasil.streamlit.app`.

---

### Passo 4: Concluir o Deploy

1. Clique em **"Deploy!"**.
2. O Streamlit iniciará o provisionamento da máquina virtual:
   - Clonará o repositório;
   - Detectará o arquivo `requirements.txt` automaticamente;
   - Instalará as dependências (`streamlit`, `pandas`, `plotly`);
   - Executará o arquivo principal.
3. Em menos de 2 minutos, seu painel estará online com URL pública compartilhável!

---

## Como a Plataforma Gerencia Dependências

O Streamlit Cloud lê automaticamente o arquivo `requirements.txt` presente:
- Na raiz do repositório; ou
- Na mesma pasta onde está o arquivo principal (`app.py`).

Certifique-se de que qualquer nova biblioteca adicionada pela equipe durante o desenvolvimento seja incluída no `requirements.txt` e no `pyproject.toml`.

---

## Gerenciamento de Segredos (Secrets)

Caso o time decida adicionar integrações futuras (como conexão com banco de dados PostgreSQL, Supabase ou APIs com chaves privadas):

1. **Localmente:** Crie o arquivo `.streamlit/secrets.toml` (já configurado no `.gitignore` para nunca ser enviado ao GitHub).
2. **Em Produção:**
   - No painel do Streamlit Cloud, acesse o app;
   - Clique nos três pontinhos `...` no canto inferior direito;
   - Selecione **Settings** > **Secrets**;
   - Cole suas variáveis no formato TOML:
     ```toml
     DB_USER = "admin"
     DB_PASSWORD = "super-secret-password"
     ```
   - No Python, acesse usando: `st.secrets["DB_USER"]`.

---

## Monitoramento e Resolução de Problemas (Troubleshooting)

### Visualizar Logs em Tempo Real
No canto inferior direito do app em execução, clique em **"Manage app"** para abrir o console de logs. Todos os `print()`, erros ou mensagens do Python aparecem ali.

### Caminho de Arquivos Relativos (FileNotFoundError)
Para evitar erros ao ler o CSV no servidor em nuvem, o código no `app.py` utiliza `Path(__file__).parent / "data" / "carros_eletricos_brasil.csv"`. Esta é a melhor prática recomendada, pois garante que o caminho seja sempre resolvido em relação à localização do próprio script, independentemente do diretório de trabalho de onde o processo foi disparado.

### Reiniciar ou Limpar Cache
Se os dados não forem atualizados imediatamente:
- Clique no menu sanduíche (canto superior direito do app) > **Clear cache** > **Rerun**.
- Ou no painel do Streamlit Cloud, selecione **Reboot app**.
