from . import echo, order, admin_panel, artist_cmds

labelers = [echo.labeler, order.labeler,
            admin_panel.admin_labeler,
            artist_cmds.artist_labeler]

__all__ = ('labelers')
