from . import echo, order, admin_panel, artist_cmds
from .state_dispenser import state_dispenser

labelers = [echo.labeler, order.order_labeler,
            admin_panel.admin_labeler,
            artist_cmds.artist_labeler]


__all__ = ('labelers', 'state_dispenser')
