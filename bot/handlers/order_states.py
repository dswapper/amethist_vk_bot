from vkbottle import BaseStateGroup


class OrderStates(BaseStateGroup):
    ordering = 'ordering'
    support_dialog = 'support_dialog'
    choosing_prod_type = 'choosing_product_type'
    choosing_skin_model = 'choosing_skin_model'
    choosing_skin_style = 'choosing_skin_style'
    choosing_totem_type = 'choosing_totem_type'
    sending_references = 'sending_references'
    waiting_completion = 'waiting_completion'
