from datetime import datetime

from pydantic import BaseModel, EmailStr


# schemas do webhook para endpoint post
class WebhookResponse(BaseModel):
    event_id: str
    card_id: str
    timestamp: datetime
    cliente_email: EmailStr


# class WebhookPublic(WebhookResponse):
#     cliente_email: EmailStr


# schemas do webook para o endpoint get
class WebhookList(BaseModel):
    webhooks: list[WebhookResponse]
