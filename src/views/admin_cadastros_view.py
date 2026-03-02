import flet as ft
from components.sidebar import Sidebar

class AdminCadastrosView(ft.View):
    def __init__(self, page):
        super().__init__(
            route="/admin/cadastros", 
            bgcolor=ft.Colors.GREY_900,
            padding=0
        )
        
        self.page = page
        
        # Sub-views container (right side panel)
        self.main_content = ft.Container(
            expand=True,
            bgcolor=ft.Colors.GREY_100,
            content=self.build_content()
        )
        
        # Instantiate common sidebar and set active tab
        self.sidebar = Sidebar(on_menu_change=self.handle_content_change)
        for item in self.sidebar.items_top_sidebar + self.sidebar.items_bottom_sidebar:
            item.set_checked(item.text_val == "Cadastros")

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
        if menu_name == "Dashboard":
            self.page.go("/admin/dashboard")
        elif menu_name == "Cadastros":
            self.page.go("/admin/cadastros")
        elif menu_name == "Cozinha":
            self.page.go("/admin/cozinha")
        elif menu_name == "Usuário":
            self.page.go("/admin/usuario")
        elif menu_name == "Configurações":
            self.page.go("/admin/configuracoes")
        elif menu_name == "Sair":
            self.page.go("/")
            
    def build_content(self):
        content_area = ft.Container(
            content=ft.Text("Lista de Usuários via BD em breve...", color=ft.Colors.GREY_400), 
            padding=20, 
            expand=True
        )
        
        tab_contents = {
            "Usuários": ft.Text("Lista de Usuários via BD em breve...", color=ft.Colors.GREY_400),
            "Produtos": ft.Text("Lista de Produtos via BD em breve...", color=ft.Colors.GREY_400),
            "Categorias": ft.Text("Lista de Categorias via BD em breve...", color=ft.Colors.GREY_400),
            "Mesas": ft.Text("Gerenciamento de Mesas via BD em breve...", color=ft.Colors.GREY_400)
        }
        
        def on_tab_click(e):
            for c in tab_row.controls:
                is_active = (c.data == e.control.data)
                color = ft.Colors.ORANGE_500 if is_active else ft.Colors.GREY_400
                c.content.controls[0].color = color
                c.content.controls[1].color = color
                c.update()
                
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
