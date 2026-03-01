import flet as ft


class AdminView(ft.View):

    def __init__(self, page):
        super().__init__(
            route="/admin",
            appbar=ft.AppBar(title=ft.Text("Página Administração"), bgcolor=ft.Colors.BLUE_400),
            controls=[
                ft.Row(
                    expand=True,
                    
                    controls=[
                        ft.Container(
                            bgcolor=ft.Colors.BLUE_600, 
                            width=300, 
                            
                        ),
                        ft.Container(
                            expand=True ,
                            bgcolor=ft.Colors.GREEN_600, 
                        )
                ])
            ],
        )
    
    async def open_home_view(self, e):
        await self.page.push_route("/")

