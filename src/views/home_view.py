import flet as ft


class HomeView(ft.View):

    def __init__(self, path):
        super().__init__(
            route=path,
            appbar= ft.AppBar(title=ft.Text("Página HOME"), bgcolor=ft.Colors.BLUE_400),
            can_pop=False,

            controls=[
                ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Button(
                            content=ft.Text("Abrir Admin"),
                            on_click=self.open_admin_view
                        ),
                        ft.Button(
                            content=ft.Text("Abrir Cozinha"),
                            on_click=self.open_cozinha_view
                        )
                ])
            ],
        )
    
    async def open_admin_view(self, e):
        await self.page.push_route("/admin")
        
    async def open_cozinha_view(self, e):
        await self.page.push_route("/cozinha")
        
