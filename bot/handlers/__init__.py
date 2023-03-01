from . import echo, order, admin, artist

labelers = [echo.labeler, order.labeler, admin.admin_labeler, artist.artist_labeler, admin.user_labeler]

__all__ = ('labelers')