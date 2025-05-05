from enum import Enum

class GeneroEnum(str, Enum):
    mulher_cisgenero = "Mulher cisgênera"
    homem_cisgenero = "Homem cisgênero"
    mulher_transexual = "Mulher transexual/transgênera"
    homem_transexual = "Homem transexual/transgênero"
    travesti = "Travesti"
    nao_binario = "Não binário"
    prefiro_nao_responder = "Prefiro não responder"
    outro = "Outro"

class EtniaEnum(str, Enum):
    branca = "branca"
    preta = "preta"
    parda = "parda"
    amarela = "amarela"
    indigena = "indígena"
    outro = "outro"

class EscolaridadeEnum(str, Enum):
    fundamental_incompleto = "fundamental incompleto"
    fundamental_completo = "fundamental completo"
    medio_incompleto = "médio incompleto"
    medio_completo = "médio completo"
    superior_incompleto = "superior incompleto"
    superior_completo = "superior completo"
    outro = "outro"

class SituacaoTrabalhoEnum(str, Enum):
    empregado = "empregado"
    desempregado = "desempregado"
    estudante = "estudante"
    autônomo = "autônomo"
    em_transicao_de_carreira = "em transição de carreira"
    outro = "outro"

class PresencialEnum(str, Enum):
    sim = "sim"
    nao = "não"
    talvez = "talvez"

class FonteProgramaEnum(str, Enum):
    instagram = "instagram"
    linkedin = "linkedin"
    whatsapp = "whatsapp"
    tv = "tv"
    outros = "outros"

class TipoPublicacao(str, Enum):
    blog = "blog"
    noticia = "noticia"