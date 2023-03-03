from vkbottle import Keyboard, Text, KeyboardButtonColor
from bot.handlers.keyboard.texts import *
from bot.enums.order_type import OrderType

# Keyboard start menu
kb_start_menu = Keyboard(inline=True)

kb_start_menu.add(Text(order_text), KeyboardButtonColor.POSITIVE)
kb_start_menu.row()
kb_start_menu.add(Text(support_text), KeyboardButtonColor.NEGATIVE)
kb_start_menu.row()
kb_start_menu.add(Text(cancel_text), KeyboardButtonColor.SECONDARY)
kb_start_menu = kb_start_menu.get_json()


# Ordering keyboard
kb_choosing_order_type = Keyboard(inline=True)

kb_choosing_order_type.add(Text(product_skin_text), KeyboardButtonColor.SECONDARY)
kb_choosing_order_type.add(Text(product_totem_text), KeyboardButtonColor.SECONDARY)
kb_choosing_order_type.add(Text(cancel_text), KeyboardButtonColor.NEGATIVE)
kb_choosing_order_type = kb_choosing_order_type.get_json()




