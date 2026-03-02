import flet as ft
from components.sidebar import Sidebar

class AdminConfiguracoesView(ft.View):
    def __init__(self, page):
        super().__init__(
            route="/admin/configuracoes", 
            bgcolor=ft.Colors.GREY_900,
            padding=0
        )
        
        
        # Sub-views container (right side panel)
        self.main_content = ft.Container(
            expand=True,
            bgcolor=ft.Colors.GREY_100,
            content=self.build_content()
        )
        
        # Instantiate common sidebar and set active tab
        self.sidebar = Sidebar(on_menu_change=self.handle_content_change)
        for item in self.sidebar.items_top_sidebar + self.sidebar.items_bottom_sidebar:
            item.set_checked(item.text_val == "Configurações")

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
            self.page.run_task(self.page.push_route, "/admin/dashboard")
        elif menu_name == "Cadastros":
            self.page.run_task(self.page.push_route, "/admin/cadastros")
        elif menu_name == "Cozinha":
            self.page.run_task(self.page.push_route, "/admin/cozinha")
        elif menu_name == "Usuário":
            self.page.run_task(self.page.push_route, "/admin/usuario")
        elif menu_name == "Configurações":
            self.page.run_task(self.page.push_route, "/admin/configuracoes")
        elif menu_name == "Sair":
            self.page.run_task(self.page.push_route, "/")
            
    def build_content(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("Configurações do Sistema", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                ft.Divider(color=ft.Colors.GREY_500),
                ft.Text("Parâmetros do restaurante, impostos, impressoras...", color=ft.Colors.GREY_400)
            ], expand=True),
            padding=20, expand=True
        )
