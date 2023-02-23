from .client import main_menu
from .admin import main_menu
from .admin.distribution import register_distribution
from .admin.stat import register_stat
from .admin.additional_funcs import register_additional_funcs
from .admin.referral_links import register_refferal_links
from .admin.sponsers import register_sponsers
from .admin.admins_management import register_admins_management
from .backwards import register_back


def register_handlers(dp):
    client.main_menu.register_client_main_menu(dp)
    admin.main_menu.register_admin_panel(dp)
    backwards.register_back(dp)
    admin.distribution.register_distribution(dp)
    admin.stat.register_stat(dp)
    admin.additional_funcs.register_additional_funcs(dp)
    admin.referral_links.register_refferal_links(dp)
    admin.sponsers.register_sponsers(dp)
    admin.admins_management.register_admins_management(dp)
