import flet as ft


class AdminView(ft.View):

    def __init__(self, page):

        self.txtNomeUsuario = ft.Text("João Lúcio", weight=ft.FontWeight.BOLD, size=25,color=ft.Colors.WHITE)
        self.txtPerfilUsuario = ft.Text("Administrador do Sistema", size=18, color=ft.Colors.GREY_300)

        super().__init__(
            route="/admin", bgcolor=ft.Colors.GREY_900,
            appbar = ft.AppBar(title=ft.Text(""), bgcolor=ft.Colors.ORANGE_800),
            padding=0,
            controls=[
                ft.Row(
                    expand=True,
                    margin=10 ,
                    controls=[
                        ft.Container(# sidebar
                            bgcolor=ft.Colors.GREY_900, 
                            width=250,
                            content=ft.Column([
                                ft.Container(content=ft.Column([
                                    ft.IconButton(icon=ft.Icons.MENU, on_click=self._on_click_menu, data="open", icon_color=ft.Colors.GREY_600),
                                    ft.CircleAvatar(
                                    content=ft.Text("JL")
                                    ),
                                    self.txtNomeUsuario,
                                    self.txtPerfilUsuario
                                ]),padding=0),
                                ft.Container(height=50),

                                ft.Container(content=ft.Column([
                                    self._create_sidebarItens(ft.Icons.HOME_OUTLINED, "Dashboard", "/"),
                                    self._create_sidebarItens(ft.Icons.INSERT_COMMENT_OUTLINED, "Cadastros", "/"),
                                    self._create_sidebarItens(ft.Icons.KITCHEN_OUTLINED, "Cozinha", "/"),
              
                                ]), expand=True, height=100)

                            ])
                            
                        ),
                        ft.Container(
                            expand=True ,
                            bgcolor=ft.Colors.BLACK, 
                        )
                ])
            ],
        )

    
    async def open_home_view(self, e):
        await self.page.push_route("/")

    def _create_sidebarItens(self, icon, text, rota):
        card = ft.Container(padding=10, content=ft.Row([
            ft.Icon(icon=icon, size=25, color=ft.Colors.GREY_600),
            ft.Text(text, size=18, color=ft.Colors.GREY_600),
        ]), 
        bgcolor=ft.Colors.TRANSPARENT,
        border_radius=10,
        height=50,
        #scale=1.0,
        #animate_scale=ft.Animation(duration=100, curve=ft.AnimationCurve.BOUNCE_OUT),
        on_hover=self._on_hover
        )
        return card

    def _on_hover(self, e: ft.ControlEvent):
        # Transforma o e.data em texto para garantir a leitura ("true" ou True convertem para verificação segura)
        is_hovering = str(e.data).lower() == "true"
        is_transparent = str(e.control.bgcolor) == "Colors.TRANSPARENT"

        # Mudei a escala pra 1.05 para o cartão não sair da tela (1.50 dobrava de tamanho)
        #e.control.scale = 1.05 if is_hovering else 1.0
        e.control.bgcolor=ft.Colors.ORANGE_800 if is_transparent else ft.Colors.TRANSPARENT 
        e.control.content.controls[0].color = ft.Colors.GREY_300 if is_transparent else ft.Colors.GREY_600
        e.control.content.controls[1].color = ft.Colors.GREY_300 if is_transparent else ft.Colors.GREY_600
        e.control.update()

    def _on_click_menu(self, e):
        isOpen = e.control.data == "open"
        print(e.control.data)
        if isOpen:
            self.controls[0].controls[0].width = 46
            #self.controls[0].controls[0].bgcolor = ft.Colors.BLACK_54
            self.txtNomeUsuario.visible = False
            self.txtPerfilUsuario.visible = False
            e.control.data = "closed"
        else:
            self.controls[0].controls[0].width = 250
            #self.controls[0].controls[0].bgcolor = ft.Colors.GREY_900 
            self.txtNomeUsuario.visible = True
            self.txtPerfilUsuario.visible = True
            e.control.data = "open"
        
    def abrir_dashboad(self):
        card = ft.Column([
            ft.Text("Você está na DashBoard", size=50, color=ft.Colors.GREY_500)
        ])
        return card