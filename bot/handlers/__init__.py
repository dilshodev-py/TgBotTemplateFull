from bot.dispacher import dp
from bot.handlers import comments
from bot.handlers.get_group_id import channel
from bot.handlers.main_handler import main_router


dp.include_routers(*[
    main_router,
    comments,
    channel
])