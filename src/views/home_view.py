import flet as ft


class HomeView(ft.View):

    def __init__(self, path):
        super().__init__(
            route=path,
            appbar= ft.AppBar(title=ft.Text("Página HOME"), bgcolor=ft.Colors.BLUE_400),
            can_pop=False,

            controls=[
                ft.Row(
                    expand=True,
                    
                    controls=[
                        ft.ElevatedButton(
                            text="Abrir Admin",
                            on_click=self.open_admin_view
                        )
                ])
            ],
        )
    
    async def open_admin_view(self, e):
        await self.page.push_route("/admin")
        
