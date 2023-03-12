import enum


class OrderStatus(enum.Enum):
    user_send_references = 'sendReferencesOrder'
    user_paid = 'paidOrder'
    artist_get_order = 'getOrder'
    artist_done = 'doneOrder'
    archive = 'archiveOrder'
