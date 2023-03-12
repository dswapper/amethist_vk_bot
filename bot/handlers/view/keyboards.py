from vkbottle import Keyboard, Text, OpenLink, KeyboardButtonColor
from bot.handlers.view.texts import *

# TODO: Refactor

# Keyboard start menu
kb_start_menu = Keyboard(inline=True)

kb_start_menu.add(Text(order_text), KeyboardButtonColor.POSITIVE)
kb_start_menu.row()
kb_start_menu.add(Text(support_text), KeyboardButtonColor.NEGATIVE)
kb_start_menu.row()
kb_start_menu.add(Text(cancel_text), KeyboardButtonColor.SECONDARY)
# kb_start_menu = kb_start_menu.get_json()


# Ordering keyboard
kb_choosing_order_type = Keyboard(inline=True)

kb_choosing_order_type.add(Text(product_skin_text), KeyboardButtonColor.SECONDARY)
kb_choosing_order_type.add(Text(product_totem_text), KeyboardButtonColor.SECONDARY)
kb_choosing_order_type.add(Text(cancel_text), KeyboardButtonColor.NEGATIVE)
# kb_choosing_order_type = kb_choosing_order_type.get_json()

# Totem type
kb_choosing_totem_type = Keyboard(inline=True)

kb_choosing_totem_type.add(Text(product_totem_2D), KeyboardButtonColor.SECONDARY)
kb_choosing_totem_type.add(Text(product_totem_3D), KeyboardButtonColor.SECONDARY)
kb_choosing_totem_type.add(Text(cancel_text), KeyboardButtonColor.NEGATIVE)

# Skin model
kb_choosing_skin_model = Keyboard(inline=True)

kb_choosing_skin_model.add(Text(product_skin_normal), KeyboardButtonColor.SECONDARY)
kb_choosing_skin_model.add(Text(product_skin_slim), KeyboardButtonColor.SECONDARY)
kb_choosing_skin_model.add(Text(cancel_text), KeyboardButtonColor.NEGATIVE)

# Skin style
kb_choosing_skin_style = Keyboard(inline=True)

kb_choosing_skin_style.add(Text(product_skin_air), KeyboardButtonColor.SECONDARY)
kb_choosing_skin_style.add(Text(product_skin_century), KeyboardButtonColor.SECONDARY)
kb_choosing_skin_style.add(Text(product_skin_shady), KeyboardButtonColor.SECONDARY)
kb_choosing_skin_style.add(Text(cancel_text), KeyboardButtonColor.NEGATIVE)

# Paying
kb_pay = Keyboard()
kb_pay.add(OpenLink(link='https://vk.com/drswapper', label='Оплатить заказ'), KeyboardButtonColor.POSITIVE)

# Next'n'Back
kb_next_n_back = Keyboard(inline=True)
kb_next_n_back.add(Text(back_msg), KeyboardButtonColor.NEGATIVE)
kb_next_n_back.add(Text(next_msg), KeyboardButtonColor.POSITIVE)
