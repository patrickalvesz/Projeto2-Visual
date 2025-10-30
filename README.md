# 🖼️ Projeto de Filtros de Imagem

Este projeto acadêmico tem como objetivo aplicar diferentes **filtros de imagem** em arquivos enviados pelo usuário, utilizando **Python (Flask)** e **Pillow (PIL)**. A interface web foi desenvolvida em **HTML/CSS** com elementos dinâmicos em JavaScript, oferecendo uma experiência simples e intuitiva.

---

## 🎯 Objetivo
Desenvolver uma aplicação web que permita o upload de uma imagem e a aplicação de filtros visuais, como:
- **Sépia (Sepia)** – simula tons envelhecidos;
- **Sketch (Desenho)** – transforma a imagem em um esboço em preto e branco;
- **Color Pop** – mantém apenas uma cor destacada e converte o restante para tons de cinza.

---

## 🧠 Tecnologias Utilizadas
- **Python 3**
- **Flask** (framework web)
- **Pillow (PIL)** – manipulação de imagens
- **HTML5 / CSS3 / JavaScript**
- **Bootstrap-like CSS (customizado)**

---

## ⚙️ Estrutura do Projeto
```
Projeto2-Visual/
│
├── app.py                # Código principal em Flask (backend)
├── index.html            # Template da interface web (frontend)
└── static/uploads/       # Pasta onde as imagens enviadas e processadas são salvas
```

---

## 🚀 Como Executar
1. Instale as dependências:
   ```bash
   pip install flask pillow
   ```

2. Execute o servidor Flask:
   ```bash
   python app.py
   ```

3. Acesse o projeto no navegador:
   ```
   http://127.0.0.1:5000/
   ```

4. Envie uma imagem, escolha um filtro e veja o resultado!

---

## 👨‍💻 Autores
Trabalho desenvolvido por:

- **Patrick Alves Gonçalves – 10409363**  
- **Nicholas dos Santos Leal – 10409210**  
- **Gustavo Ibara – 10389067**

---

## 🏫 Observações
Projeto desenvolvido para fins acadêmicos, com foco em prática de **processamento digital de imagens** e **aplicações web**.  
O sistema permite upload, visualização, download e troca dinâmica de filtros.
