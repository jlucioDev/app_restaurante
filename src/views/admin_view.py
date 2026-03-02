import flet as ft

class SidebarItem(ft.Container):
    def __init__(self, icon, text, is_checked, on_click_callback):
        super().__init__()
        self.text_val = text
        self.icon_val = icon
        self.data_checked = is_checked
        self.on_click_callback = on_click_callback
        
        # UI Elements
        self.icon_ctrl = ft.Icon(icon=icon, size=25, color=ft.Colors.GREY_600)
        self.text_ctrl = ft.Text(text, size=18, color=ft.Colors.GREY_600)
        
        # Container Setup
        self.padding = 10
        self.content = ft.Row([self.icon_ctrl, self.text_ctrl])
        self.data = is_checked
        self.border_radius = 10
        self.height = 50
        self.on_hover = self._on_hover
        self.on_click = self._on_click
        
        # Initial style applied based on `is_checked`
        self._set_style(self.data_checked)

    def _set_style(self, checked):
        if checked:
            self.bgcolor = ft.Colors.ORANGE_200
            self.icon_ctrl.color = ft.Colors.GREY_600
            self.text_ctrl.color = ft.Colors.GREY_600
        else:
            self.bgcolor = ft.Colors.TRANSPARENT
            self.icon_ctrl.color = ft.Colors.GREY_600
            self.text_ctrl.color = ft.Colors.GREY_600

    def set_checked(self, checked):
        self.data_checked = checked
        self.data = checked
        self._set_style(checked)
        self.update()

    def _on_hover(self, e):
        # Hover effect only if it's not the active (checked) item
        if not self.data_checked:
            is_transparent = self.bgcolor == ft.Colors.TRANSPARENT
            self.bgcolor = ft.Colors.ORANGE_800 if is_transparent else ft.Colors.TRANSPARENT
            
            # Highlight text/icon when hovering (Orange background -> Lighter grey text)
            hover_color = ft.Colors.GREY_300 if is_transparent else ft.Colors.GREY_600
            self.icon_ctrl.color = hover_color
            self.text_ctrl.color = hover_color
            self.update()

    def _on_click(self, e):
        if self.on_click_callback:
            self.on_click_callback(self)


class Sidebar(ft.Container):
    def __init__(self, on_menu_change):
        super().__init__()
        self.on_menu_change = on_menu_change
        
        self.is_open = True
        self.bgcolor = ft.Colors.GREY_900
        self.width = 250
        self.animate = ft.Animation(300, ft.AnimationCurve.DECELERATE)
        
        # Header Elements
        self.btn_menu = ft.IconButton(icon=ft.Icons.MENU, on_click=self._toggle_menu, icon_color=ft.Colors.GREY_600)
        self.avatar = ft.CircleAvatar(content=ft.Text("JL"))
        
        self.txtNomeUsuario = ft.Text("João Lúcio", weight=ft.FontWeight.BOLD, size=25, color=ft.Colors.WHITE)
        self.txtPerfilUsuario = ft.Text("Administrador do Sistema", size=18, color=ft.Colors.GREY_300)
        
        # Wrapped in animated containers to collapse space physically
        self.cont_nome = ft.Container(
            content=self.txtNomeUsuario,
            height=30, # default estimated height
            opacity=1.0,
            animate_size=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            animate_opacity=300,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        self.cont_perfil = ft.Container(
            content=self.txtPerfilUsuario,
            height=25,
            opacity=1.0,
            animate_size=ft.Animation(300, ft.AnimationCurve.DECELERATE),
            animate_opacity=300,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        # Create Items
        self.items = [
            SidebarItem(ft.Icons.HOME_OUTLINED, "Dashboard", True, self._on_item_click),
            SidebarItem(ft.Icons.INSERT_COMMENT_OUTLINED, "Cadastros", False, self._on_item_click),
            SidebarItem(ft.Icons.KITCHEN_OUTLINED, "Cozinha", False, self._on_item_click),
        ]
        
        self.header_col = ft.Column([
            self.btn_menu,
            self.avatar,
            self.cont_nome,
            self.cont_perfil
        ])
        
        self.items_col = ft.Column(self.items, expand=True)

        self.content = ft.Column([
            ft.Container(content=self.header_col, padding=0),
            ft.Container(height=50),
            ft.Container(content=self.items_col, expand=True, height=100)
        ])

    def _toggle_menu(self, e):
        self.is_open = not self.is_open
        
        if self.is_open:
            self.width = 250
            self.cont_nome.opacity = 1.0
            self.cont_nome.height = 30
            self.cont_perfil.opacity = 1.0
            self.cont_perfil.height = 25
        else:
            self.width = 46
            self.cont_nome.opacity = 0.0
            self.cont_nome.height = 0
            self.cont_perfil.opacity = 0.0
            self.cont_perfil.height = 0
            
        self.update()

    def _on_item_click(self, clicked_item: SidebarItem):
        # Clear all items
        for item in self.items:
            item.set_checked(False)
            
        # Select current item
        clicked_item.set_checked(True)
        
        # Notify parent view to change main content
        if self.on_menu_change:
            self.on_menu_change(clicked_item.text_val)


class AdminView(ft.View):
    def __init__(self, page):
        super().__init__(
            route="/admin", bgcolor=ft.Colors.GREY_900,
            appbar=ft.AppBar(title=ft.Text(""), bgcolor=ft.Colors.ORANGE_800),
            padding=0
        )
        
        # Sub-views container (right side panel)
        self.main_content = ft.Container(
            expand=True,
            bgcolor=ft.Colors.BLACK,
            content=self.abrir_dashboard() # Default view
        )
        
        # Sidebar control
        self.sidebar = Sidebar(on_menu_change=self.handle_content_change)

        self.controls = [
            ft.Row(
                expand=True,
                margin=10,
                controls=[
                    self.sidebar,
                    self.main_content
                ]
            )
        ]

    def handle_content_change(self, menu_name):
        """Routing mechanism inside the Admin panel"""
        if menu_name == "Dashboard":
            self.main_content.content = self.abrir_dashboard()
        elif menu_name == "Cadastros":
            self.main_content.content = self.abrir_cadastros()
        elif menu_name == "Cozinha":
            self.main_content.content = self.abrir_cozinha_admin()
            
        self.main_content.update()

    def abrir_dashboard(self):
        return ft.Column([
            ft.Text("Dashboard", size=50, color=ft.Colors.PURPLE_500),
            ft.Text("Módulo em construção...", color=ft.Colors.WHITE)
        ])
        
    def abrir_cadastros(self):
        return ft.Column([
            ft.Text("Gerenciamento de Cadastros", size=50, color=ft.Colors.BLUE_500),
            ft.Text("Módulo em construção...", color=ft.Colors.WHITE)
        ])
        
    def abrir_cozinha_admin(self):
        return ft.Column([
            ft.Text("Visão Administrativa da Cozinha", size=40, color=ft.Colors.ORANGE_500),
            ft.Text("Módulo em construção...", color=ft.Colors.WHITE)
        ])

    async def open_home_view(self, e):
        await self.page.push_route("/")
