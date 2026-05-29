from mundo_invest.models.models import Cliente


# mutation para criar card no Pipefy
def create_pipefy_card_mutation(cliente: Cliente):

    return {
        "query": """
        mutation CreateCard(
            $pipe_id: ID!,
            $title: String!,
            $fields_attributes: [FieldValueInput]!
        ) {
            createCard(
                input: {
                    pipe_id: $pipe_id,
                    title: $title,
                    fields_attributes: $fields_attributes
                }
            ) {
                card {
                    id
                    title
                }
            }
        }
        """,
        "variables": {
            "pipe_id": 123456,
            "title": cliente.cliente_nome,
            "fields_attributes": [
                {
                    "field_id": "cliente_nome",
                    "field_value": cliente.cliente_nome,
                },
                {
                    "field_id": "cliente_email",
                    "field_value": cliente.cliente_email,
                },
                {
                    "field_id": "valor_patrimonio",
                    "field_value": str(cliente.valor_patrimonio),
                },
                {
                    "field_id": "tipo_solicitacao",
                    "field_value": cliente.tipo_solicitacao,
                },
            ],
        },
    }

# mutation para atualizar o card
def update_pipefy_card_field_mutation(
    card_id: str,
    field_id: str,
    new_value: str,
):

    return {
        "query": """
        mutation UpdateCardField(
            $card_id: ID!,
            $field_id: String!,
            $new_value: String!
        ) {
            updateCardField(
                input: {
                    card_id: $card_id,
                    field_id: $field_id,
                    new_value: $new_value
                }
            ) {
                card {
                    id
                    title
                }
            }
        }
        """,
        "variables": {
            "card_id": card_id,
            "field_id": field_id,
            "new_value": new_value,
        },
    }
