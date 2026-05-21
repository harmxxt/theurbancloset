# signals.py intentionally left minimal.
# Invoice generation is triggered from orders/views.py AFTER
# all OrderItems are saved — not on post_save of Order,
# because post_save fires before items exist.
