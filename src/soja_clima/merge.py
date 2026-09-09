"""Merge final entre clima e produção, já ambos agregados por
microrregião-safra/ano."""


def montar_base_final(clima_micro_safra, producao_micro_ano):
    """Inner join: uma linha só é útil para o modelo se tiver os dois
    lados (clima e produção) para o mesmo (microrregião, ano)."""
    return producao_micro_ano.merge(
        clima_micro_safra,
        left_on=['code_micro', 'ano'],
        right_on=['code_micro', 'safra'],
        how='inner',
    )
