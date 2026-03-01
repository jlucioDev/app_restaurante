import flet as ft


class HomeView(ft.View):

    def __init__(self, page):
        super().__init__(route="/", bgcolor=ft.Colors.GREY_900)
        self.appbar= ft.AppBar(title=ft.Text("Página HOME"), bgcolor=ft.Colors.BLUE_400),
        self.can_pop=False
            
        self.controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Sistema de Restaurante", size=50, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_800),
                    ft.Text("Selecione o seu perfil de acesso", size=20, color=ft.Colors.WHITE),
                    ft.Container(height=40), #Espaçador
                    ft.Row([
                            self._create_card("Administração", ft.Icons.SETTINGS, "/admin")
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=30
                    )],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    expand=True
            )
        ]
        
    
    async def open_admin_view(self, e):
        await self.page.push_route("/admin")
        
    async def open_cozinha_view(self, e):
        await self.page.push_route("/cozinha")

    def _create_card(self, title, icon, route):
        card = ft.Container(
            content=ft.Column([
                ft.Icon(icon=icon, size=60, color=ft.Colors.WHITE),
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=250,
            height=200,

            )

        )
        return card
