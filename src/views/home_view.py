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
                            self._create_card("Administração", ft.Icons.SETTINGS, "/admin"),
                            self._create_card("Cliente", ft.Icons.RESTAURANT, "/cliente"),
                            self._create_card("Cozinha", ft.Icons.KITCHEN, "/cozinha"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=30
                    )],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    expand=True
            )
        ]
        

    async def mudar_tela(self, e, rota):
        await self.page.push_route(rota)

    def _create_card(self, title, icon, rota):
        async def ao_clicar(e):
            await self.mudar_tela(e, rota)

        card = ft.Container(
            content=ft.Column([
                ft.Icon(icon=icon, size=60, color=ft.Colors.WHITE),
                ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ], 
                alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            
            width=250,
            height=200,
            bgcolor=ft.Colors.ORANGE_800,
            border_radius=15,
            padding=20,
            on_click=ao_clicar,
            scale=1.0,
            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.BOUNCE_OUT),
            on_hover=self._on_hover
        )
        return card

    def _on_hover(self, e):
        # Transforma o e.data em texto para garantir a leitura ("true" ou True convertem para verificação segura)
        is_hovering = str(e.data).lower() == "true"
        # Mudei a escala pra 1.05 para o cartão não sair da tela (1.50 dobrava de tamanho)
        e.control.scale = 1.05 if is_hovering else 1.0
        e.control.update()
