## Bibliotecas utilizadas no projeto
Aqui você encontrara uma explicação rapida de como as bibliotecas foram utilizadas dentro do projeto.
## dotenv
É uma biblioteca responsavel por ler os pares de chave presentes ````.env```` e converte-los a variaveis de ambiente. 

Observe que no nosso ```main.py```, temos como primeira linha o ``load_dotenv()`` que por padrão segue uma serie de passos logo ao rodarmos o ``main.py``:
1. Procure por um ``.env`` arquivo no mesmo diretório que o script Python (ou superior na árvore de diretórios).
2. Le cada par chave-valor e adicione-o a ``os.environ``.
3. Não substituir uma variável de ambiente que já está definida, a menos que você passe explicitamente override=True.

[Fonte](https://pypi.org/project/python-dotenv/)
## OS
A biblioteca OS do python se encarrega de interagir com o sistema operacional.

Quando declaramos uma variavel de ambiente em python, podemos declarar ela pelo terminal com o codigo:
``$Env:MINHA_VAR = "meu_valor_secreto"``
Isso fara com que dentro daquela sessão, possamos acessar essa variavel e utiliza-la, mas logo apos fechar essa sessao essa variavel ira sumir. 

O ``os.environ`` é capaz de interagir com o terminal e adicionar a variavel de ambiente individualmente:
``os.environ['NOVA_VARIAVEL'] = 'seu_valor'``

Como visto anteriormente o ``os.environ`` esta embutido dentro do ``load_dotenv()`` então agora podemos entender que quando rodamos o ``load_dotenv()`` ele internamente esta adicionando todas as chave/valor presentes no ``.env``, dentro da nossa sessão.

O ``os.getenv`` nada mais é que o ``os`` pegando a variavel da sessao e provavelmente atribuindo ela a outra variavel interna do projeto. Exemplo:
```var_interno = os.getenv("var_da_sessao")``

[fonte](https://docs.python.org/pt-br/3.14/library/os.html)