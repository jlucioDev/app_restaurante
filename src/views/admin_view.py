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
            self.bgcolor = ft.Colors.ORANGE_800
            self.icon_ctrl.color = ft.Colors.GREY_100
            self.text_ctrl.color = ft.Colors.GREY_100
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
            self.bgcolor = ft.Colors.ORANGE_200 if is_transparent else ft.Colors.TRANSPARENT
            
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
        self.avatar = ft.CircleAvatar(
            align=ft.Alignment.CENTER ,
            content=ft.Text("JL", size=30), 
            color=ft.Colors.GREY_900, 
            bgcolor=ft.Colors.ORANGE_800, 
            radius=50,
            scale=1.0,
            animate_scale=ft.Animation(800, ft.AnimationCurve.DECELERATE)
        )
        
        self.txtNomeUsuario = ft.Text("João Lúcio", weight=ft.FontWeight.BOLD, size=25, color=ft.Colors.GREY_500, align=ft.Alignment.CENTER)
        self.txtPerfilUsuario = ft.Text("Administrador do Sistema", size=18, color=ft.Colors.GREY_700, align=ft.Alignment.CENTER)
        
        # Wrapped in animated containers to collapse space physically
        self.cont_nome = ft.Container(
            content=self.txtNomeUsuario,
            height=30, # default estimated height
            opacity=1.0,
            animate_size=ft.Animation(800, ft.AnimationCurve.DECELERATE),
            animate_opacity=500,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        self.cont_perfil = ft.Container(
            content=self.txtPerfilUsuario,
            height=25,
            opacity=1.0,
            animate_size=ft.Animation(800, ft.AnimationCurve.DECELERATE),
            animate_opacity=500,
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        # Create Items
        self.items_top_sidebar = [
            SidebarItem(ft.Icons.HOME_OUTLINED, "Dashboard", True, self._on_item_click),
            SidebarItem(ft.Icons.INSERT_COMMENT_OUTLINED, "Cadastros", False, self._on_item_click),
            SidebarItem(ft.Icons.KITCHEN_OUTLINED, "Cozinha", False, self._on_item_click),
        ]

        self.items_bottom_sidebar = [
            SidebarItem(ft.Icons.PERSON, "Usuário", False, self._on_item_click),
            SidebarItem(ft.Icons.SETTINGS, "Configurações", False, self._on_item_click),
            SidebarItem(ft.Icons.EXIT_TO_APP, "Sair", False, self._on_item_click)
        ]
        
        self.header_col = ft.Column([
            self.btn_menu,
            self.avatar,
            self.cont_nome,
            self.cont_perfil
        ])
        
        self.items_col_top = ft.Column(self.items_top_sidebar, expand=True)
        self.items_col_bottom = ft.Column(self.items_bottom_sidebar, expand=True)

        self.content = ft.Column([
            ft.Container(content=self.header_col, padding=0),
            ft.Container(height=50),
            ft.Container(content=self.items_col_top, expand=True, height=100),
            ft.Container(height= 50),
            ft.Divider(color=ft.Colors.GREY_800),
            ft.Container(content=self.items_col_bottom, expand=True, height=100)
            
        ])

    def _toggle_menu(self, e):
        self.is_open = not self.is_open
        
        if self.is_open:
            self.width = 250
            self.avatar.scale = 1.0
            self.cont_nome.opacity = 1.0
            self.cont_nome.height = 30
            self.cont_perfil.opacity = 1.0
            self.cont_perfil.height = 25
        else:
            self.width = 46
            self.avatar.scale = 1.0
            self.cont_nome.opacity = 0.0
            self.cont_nome.height = 0
            self.cont_perfil.opacity = 0.0
            self.cont_perfil.height = 0
            
        self.update()

    def _on_item_click(self, clicked_item: SidebarItem):
        # Clear all items
        for item in self.items_top_sidebar + self.items_bottom_sidebar:
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
            #appbar=ft.AppBar(title=ft.Text(""), bgcolor=ft.Colors.ORANGE_800),
            padding=0
        )
        
        # Sub-views container (right side panel)
        self.main_content = ft.Container(
            expand=True,
            bgcolor=ft.Colors.GREY_100,
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
        # """Routing mechanism inside the Admin panel"""
        if menu_name == "Dashboard":
            self.main_content.content = self.abrir_dashboard()
        elif menu_name == "Cadastros":
            self.main_content.content = self.abrir_cadastros()
        elif menu_name == "Cozinha":
            self.main_content.content = self.abrir_cozinha_admin()
        elif menu_name == "Sair":
            # Aqui faça ele voltar para homeView
            self.page.go("/")
            return

            
        self.main_content.update()

    def _create_info_card(self, title, value, icon, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=40, color=color),
                ft.Column([
                    ft.Text(title, size=14, color=ft.Colors.GREY_400),
                    ft.Text(value, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                ], spacing=0)
            ]),
            bgcolor=ft.Colors.GREY_200,
            shadow=ft.BoxShadow(0.5,20,ft.Colors.GREY_400) ,
            padding=20,
            border_radius=10,
            expand=True
        )

    def abrir_dashboard(self):
        # Caixa Actions
        btn_abrir_caixa = ft.ElevatedButton("Abrir Caixa", icon=ft.Icons.PLAY_ARROW, bgcolor=ft.Colors.GREEN_700, color=ft.Colors.WHITE)
        btn_fechar_caixa = ft.ElevatedButton("Fechar Caixa", icon=ft.Icons.STOP, bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE)
        row_acoes_caixa = ft.Row([btn_abrir_caixa, btn_fechar_caixa], alignment=ft.MainAxisAlignment.END)
        
        # Row 1: Financeiro
        row_financeiro = ft.Row([
            self._create_info_card("Valor Total Caixa", "R$ 1.250,00", ft.Icons.ATTACH_MONEY, ft.Colors.GREEN_400),
            self._create_info_card("Entradas", "R$ 1.400,00", ft.Icons.ARROW_UPWARD, ft.Colors.LIGHT_BLUE_400),
            self._create_info_card("Saídas", "R$ 150,00", ft.Icons.ARROW_DOWNWARD, ft.Colors.RED_400),
        ])
        
        # Row 2: Pedidos
        row_pedidos = ft.Row([
            self._create_info_card("Pedidos Pendentes", "5", ft.Icons.PENDING_ACTIONS, ft.Colors.RED_500),
            self._create_info_card("Em Preparação", "3", ft.Icons.SOUP_KITCHEN, ft.Colors.YELLOW_600),
            self._create_info_card("Finalizados (Hoje)", "42", ft.Icons.CHECK_CIRCLE, ft.Colors.GREEN_400),
        ])
        
        # Top Items list
        lt_itens = ft.ListView(expand=True, spacing=10)
        top_itens = [("Hambúrguer Artesanal", 15), ("Refrigerante Lata", 22), ("Pizza Margherita", 8)]
        for nome, qtd in top_itens:
            lt_itens.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.FASTFOOD, color=ft.Colors.ORANGE_800),
                    title=ft.Text(nome, color=ft.Colors.GREY_900),
                    trailing=ft.Text(f"{qtd} pedidos", color=ft.Colors.GREY_400)
                )
            )
            
        container_itens = ft.Container(
            content=ft.Column([
                ft.Text("Itens Mais Pedidos", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                lt_itens
            ]),
            bgcolor=ft.Colors.GREY_200,
            padding=20,
            shadow=ft.BoxShadow(0.5,20,ft.Colors.GREY_400),
            border_radius=10,
            expand=True
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Dashboard", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800),
                    row_acoes_caixa
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(color=ft.Colors.GREY_500),
                row_financeiro,
                ft.Container(height=10),
                row_pedidos,
                ft.Container(height=10),
                ft.Row([container_itens], expand=True)
            ], expand=True),
            padding=20, expand=True
        )
        
    def abrir_cadastros(self):
        
        content_area = ft.Container(
            content=ft.Text("Lista de Usuários via BD em breve...", color=ft.Colors.GREY_400), 
            padding=20, 
            expand=True
        )
        
        # The distinct content for each tab
        tab_contents = {
            "Usuários": ft.Text("Lista de Usuários via BD em breve...", color=ft.Colors.GREY_400),
            "Produtos": ft.Text("Lista de Produtos via BD em breve...", color=ft.Colors.GREY_400),
            "Categorias": ft.Text("Lista de Categorias via BD em breve...", color=ft.Colors.GREY_400),
            "Mesas": ft.Text("Gerenciamento de Mesas via BD em breve...", color=ft.Colors.GREY_400)
        }
        
        def on_tab_click(e):
            # Update active button visual
            for c in tab_row.controls:
                is_active = (c.data == e.control.data)
                color = ft.Colors.ORANGE_500 if is_active else ft.Colors.GREY_400
                c.content.controls[0].color = color
                c.content.controls[1].color = color
                c.update()
                
            # Update content view
            content_area.content = tab_contents[e.control.data]
            content_area.update()

        tab_row = ft.Row([
            ft.TextButton(
                content=ft.Row([ft.Icon(ft.Icons.PERSON, color=ft.Colors.ORANGE_500), ft.Text("Usuários", color=ft.Colors.ORANGE_500)]),
                data="Usuários", on_click=on_tab_click
            ),
            ft.TextButton(
                content=ft.Row([ft.Icon(ft.Icons.FASTFOOD, color=ft.Colors.GREY_400), ft.Text("Produtos", color=ft.Colors.GREY_400)]),
                data="Produtos", on_click=on_tab_click
            ),
            ft.TextButton(
                content=ft.Row([ft.Icon(ft.Icons.CATEGORY, color=ft.Colors.GREY_400), ft.Text("Categorias", color=ft.Colors.GREY_400)]),
                data="Categorias", on_click=on_tab_click
            ),
            ft.TextButton(
                content=ft.Row([ft.Icon(ft.Icons.TABLE_RESTAURANT, color=ft.Colors.GREY_400), ft.Text("Mesas", color=ft.Colors.GREY_400)]),
                data="Mesas", on_click=on_tab_click
            ),
        ])

        return ft.Container(
            content=ft.Column([
                ft.Text("Gerenciamento de Cadastros", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                tab_row,
                ft.Divider(color=ft.Colors.GREY_500),
                content_area
            ], expand=True),
            padding=20, expand=True
        )
        
    def abrir_cozinha_admin(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("Visão Administrativa da Cozinha", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                ft.Divider(color=ft.Colors.GREY_500),
                ft.Text("Monitor de Pedidos em tempo real será implementado aqui...", color=ft.Colors.GREY_400)
            ], expand=True),
            padding=20, expand=True
        )

    async def open_home_view(self, e):
        await self.page.push_route("/")
