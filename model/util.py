"""Converte um texto em número inteiro. Se estiver vazio ou não for número,
devolve None.
Serve para tudo que vem de formulário ou da URL: tudo chega como TEXTO
(ex: "12"), e o banco precisa do número 12.
Também protege: se alguém digitar "abc" ou "1 OR 1=1" na URL, vira None."""

def para_inteiro(texto):
    if texto.isdigit(): # isdigit() = o texto só tem números?
        return int(texto)
    return None

