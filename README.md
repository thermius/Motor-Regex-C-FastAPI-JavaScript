# Regex Engine — C + FastAPI + JavaScript

Motor de expressões regulares desenvolvido em **C**, baseado na **Construção de Thompson** para geração e execução de **Autômatos Finitos Não Determinísticos (AFN)**.

O núcleo do motor é compilado como uma **biblioteca compartilhada (`.so`)** e integrado ao backend Python através de **ctypes**. Uma interface web em JavaScript permite enviar expressões regulares e strings para análise através de **HTTP/JSON**.

## Arquitetura

```text
┌─────────────────────┐
│     JavaScript      │
│      Frontend       │
└──────────┬──────────┘
           │ HTTP / JSON
           ▼
┌─────────────────────┐
│       FastAPI       │
│       Python        │
└──────────┬──────────┘
           │ ctypes
           ▼
┌─────────────────────┐
│  libmotor_regex.so  │
│         C           │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│      Motor Regex    │
│   Lexer + Parser    │
│   Pós-fixa + AFN    │
└─────────────────────┘
```

## Funcionamento

O usuário fornece:

* uma string para análise;
* uma expressão regular.

O frontend envia os dados para a API FastAPI. O backend converte os dados para o formato esperado pelo código C e chama diretamente a função `MotorRegex()` através da biblioteca compartilhada.

O motor processa a expressão regular, constrói o AFN e verifica se a string pertence à linguagem definida pela expressão.

## Integração C ↔ Python

A função pública do motor possui a seguinte interface:

```c
int MotorRegex(char *string, char *regex);
```

O Python utiliza `ctypes` para carregar a biblioteca:

```python
motor_regex = ctypes.CDLL("./libmotor_regex.so")
```

e define a assinatura da função:

```python
motor_regex.MotorRegex.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p
]

motor_regex.MotorRegex.restype = ctypes.c_int
```

O retorno indica o resultado da análise:

```text
 0  → string reconhecida
-1  → string rejeitada
```

## Tecnologias

* **C**
* **Python**
* **FastAPI**
* **ctypes**
* **JavaScript**
* **HTTP/JSON**
* **Construção de Thompson**
* **AFN**

## 🔨 Compilação do Motor Regex

O motor regex é compilado como uma biblioteca compartilhada (`.so`) para posterior integração com Python através de `ctypes`.

### 1. Compile a biblioteca

Na raiz do projeto, execute:

```bash
gcc -fPIC -shared -Iinclude -o libmotor_regex.so motor_regex.c
```

### 2. Verifique a biblioteca

Após a compilação, o arquivo `libmotor_regex.so` será criado no diretório atual:

```bash
ls -l libmotor_regex.so
```

### 3. Execute a API

Com a biblioteca compilada, inicie o servidor FastAPI:

```bash
fastapi dev main.py
```

A API estará disponível em:

```text
http://127.0.0.1:8000
```

### 4. Execute o index.html 

## 🧹 Gerenciamento eficiente de memória com Valgrind

O projeto foi testado com Valgrind para verificar o gerenciamento dinâmico de memória:

```text
==4951== 
==4951== HEAP SUMMARY:
==4951==     in use at exit: 0 bytes in 0 blocks
==4951==   total heap usage: 322 allocs, 322 frees, 13,231 bytes allocated
==4951== 
==4951== All heap blocks were freed -- no leaks are possible
==4951== 
==4951== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
thermius@arch: 
```
**Resultado:** 322 alocações e 322 liberações, sem vazamentos de memória ou erros detectados pelo Valgrind no teste realizado.

## 📄 Licença

© 2026. Todos os direitos reservados.

Este projeto é disponibilizado exclusivamente para fins de portfólio e demonstração técnica. O código-fonte não pode ser copiado, redistribuído, modificado ou utilizado, integral ou parcialmente, sem autorização prévia e explícita do autor.









Motor-Regex-C-FastAPI-JavaScript
