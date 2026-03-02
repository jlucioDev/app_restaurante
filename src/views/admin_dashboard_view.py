import flet as ft
from components.sidebar import Sidebar

class AdminDashboardView(ft.View):
    def __init__(self, page):
        super().__init__(
            route="/admin/dashboard", 
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
        # Select Dashboard item by default
        for item in self.sidebar.items_top_sidebar + self.sidebar.items_bottom_sidebar:
            item.set_checked(item.text_val == "Dashboard")

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
        # Routing mechanism using main.py router
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
            shadow=ft.BoxShadow(0.5,20,ft.Colors.GREY_400),
            padding=20,
            border_radius=10,
            expand=True
        )

    def build_content(self):
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
        lt_itens = ft.ListView(expand=True, spacing=10, divider_thickness=1)
        top_itens = [("Hambúrguer Artesanal", 15), ("Refrigerante Lata", 22), ("Pizza Margherita", 8)]
        for nome, qtd in top_itens:
            lt_itens.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.FASTFOOD, color=ft.Colors.ORANGE_800),
                    title=ft.Text(nome, color=ft.Colors.GREY_900),
                    trailing=ft.Text(f"{qtd} pedidos", color=ft.Colors.GREY_900)
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
