from menus.base import NavigationNode
from cms.menu_bases import CMSAttachMenu
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _

class UserMenu(CMSAttachMenu):

    name = _('User Menu')

    def get_nodes(self, request):
        nodes = []

        menu_id = 1
        root_id = menu_id

        # root node
        greeting = 'Hello, {0}'.format(request.user.get_full_name() or request.user) if request.user.is_authenticated() else 'Log in'
        title = '<i class="fa fa-user hidden-xs hidden-md hidden-lg"></i><span class="hidden-sm">{0}</span>'
        n = NavigationNode(title.format(greeting), "/user/", menu_id)
        nodes.append(n)

        # anonymous menus
        menu_id += 1
        n = NavigationNode(_('Log in'), "/login/", menu_id, root_id, attr={'visible_for_authenticated':False})
        nodes.append(n)

        menu_id += 1
        n = NavigationNode(_('Register'), "/register/", menu_id, root_id, attr={'visible_for_authenticated':False})
        nodes.append(n)

        menu_id += 1
        n = NavigationNode(_('Help'), "/help/ticket/new/guest/", menu_id, root_id, attr={'visible_for_authenticated':False})
        nodes.append(n)

        # authenticated menus
        menu_id += 1
        dashboard_id = menu_id
        n = NavigationNode(_('Dashboard'), "/user/dashboard/", menu_id, root_id, attr={'visible_for_anonymous':False})
        nodes.append(n)

        menu_id += 1
        n = NavigationNode(_('Experiment'), "https://horizon.chameleon.tacc.utexas.edu/", menu_id, root_id, attr={'visible_for_anonymous':False})
        nodes.append(n)

        menu_id += 1
        n = NavigationNode(_('Log out'), "/logout/", menu_id, root_id, attr={'visible_for_anonymous':False})
        nodes.append(n)

        # user section dashboard sub-menu
        menu_id += 1
        n = NavigationNode(_('Dashboard'), "/user/dashboard/", menu_id, dashboard_id, attr={'visible_for_anonymous':False})
        nodes.append(n)

        menu_id += 1
        n = NavigationNode(_('Projects'), "/user/projects/", menu_id, dashboard_id, attr={'visible_for_anonymous':False})
        nodes.append(n)

        menu_id += 1
        n = NavigationNode(_('FutureGrid@Chameleon'), "/user/projects/futuregrid/", menu_id, dashboard_id, attr={'visible_for_anonymous':False})
        nodes.append(n)

        menu_id += 1
        n = NavigationNode(_('Help Desk'), "/user/help/", menu_id, dashboard_id, attr={'visible_for_anonymous':False})
        nodes.append(n)

        menu_id += 1
        n = NavigationNode(_('Profile'), "/user/profile/", menu_id, dashboard_id, attr={'visible_for_anonymous':False})
        nodes.append(n)

        return nodes

menu_pool.register_menu(UserMenu)