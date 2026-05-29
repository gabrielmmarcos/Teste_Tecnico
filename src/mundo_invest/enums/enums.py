from enum import Enum


# status enum
class StatusEnum(str, Enum):
    AGUARDANDO_ANALISE = "Aguardando Análise"
    PROCESSADO = "Processado"


# status prioridade
class PrioridadeEnum(str, Enum):
    ALTA = "prioridade_alta"
    NORMAL = "prioridade_normal"
    # NONE = None
