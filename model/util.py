"""Converte um texto em número inteiro. Se estiver vazio ou não for número,
devolve None.
Serve para tudo que vem de formulário ou da URL: tudo chega como TEXTO
(ex: "12"), e o banco precisa do número 12.
Também protege: se alguém digitar "abc" ou "1 OR 1=1" na URL, vira None."""

def para_inteiro(texto):
    if texto.isdigit(): # isdigit() = o texto só tem números?
        return int(texto)
    return None

def formatar_whatsapp(telefone):
    """Transforma o telefone salvo (ex: "86999990000") no formato que o link
    do WhatsApp pede: só números, com o código do Brasil (55) na frente."""
    numeros = ''.join(c for c in telefone if c.isdigit())
    return '55' + numeros