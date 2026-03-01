import flet as ft
from datetime import datetime

class CozinhaView(ft.View):

    def __init__(self, page):
        # Dados simulados de pedidos
        self.pedidos = [
            {"id": 1, "status": "Pendente", "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "detalhes": "2x Hambúrguer, 1x Coca-Cola"},
            {"id": 2, "status": "Em Preparação", "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "detalhes": "1x Pizza Calabresa, 2x Suco Laranja"},
            {"id": 3, "status": "Finalizado", "data_hora": datetime.now().strftime("%d/%m/%Y %H:%M"), "detalhes": "1x Salada, 1x Água"}
        ]
        
        # Cria a lista visual de pedidos
        self.lista_pedidos = ft.ListView(expand=True, spacing=10)

        super().__init__(
            route="/cozinha",
            appbar=ft.AppBar(title=ft.Text("Visão da Cozinha - Pedidos"), bgcolor=ft.Colors.ORANGE_400),
            controls=[
                ft.Container(
                    content=self.lista_pedidos,
                    expand=True,
                    padding=20
                )
            ],
        )

        self.atualizar_lista_pedidos()

    def atualizar_lista_pedidos(self):
        self.lista_pedidos.controls.clear()
        
        for pedido in self.pedidos:
            # Define cor do card baseada no status
            cor_status = ft.Colors.GREY_200
            if pedido["status"] == "Pendente":
                cor_status = ft.Colors.RED_100
            elif pedido["status"] == "Em Preparação":
                cor_status = ft.Colors.YELLOW_100
            elif pedido["status"] == "Finalizado":
                cor_status = ft.Colors.GREEN_100

            card = ft.Card(
                bgcolor=cor_status,
                content=ft.Container(
                    padding=15,
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"Pedido #{pedido['id']}", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(f"Status: {pedido['status']}", size=16, italic=True),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        
                        ft.Text(f"Horário: {pedido['data_hora']}", size=14, color=ft.Colors.GREY_700),
                        
                        ft.Divider(),
                        
                        # Botões de ação
                        ft.Row([
                            ft.Button(
                                content=ft.Text("Ver Detalhes"),
                                icon=ft.Icons.VISIBILITY,
                                on_click=lambda e, p=pedido: self.mostrar_detalhes(p)
                            ),
                            ft.Button(
                                content=ft.Text("Em Preparação" if pedido["status"] == "Pendente" else "Finalizar"),
                                icon=ft.Icons.PLAY_ARROW if pedido["status"] == "Pendente" else ft.Icons.CHECK,
                                disabled=pedido["status"] == "Finalizado",
                                on_click=lambda e, p=pedido: self.alterar_status(p)
                            )
                        ], alignment=ft.MainAxisAlignment.END)
                    ])
                )
            )
            self.lista_pedidos.controls.append(card)
        
        try:
            self.update()
        except Exception:
            pass

    def mostrar_detalhes(self, pedido):
        dialog = ft.AlertDialog(
            title=ft.Text(f"Detalhes do Pedido #{pedido['id']}"),
            content=ft.Text(pedido['detalhes'], size=16),
            actions=[
                ft.TextButton("Fechar", on_click=lambda e: self.fechar_dialog(dialog))
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
        
    def fechar_dialog(self, dialog):
        dialog.open = False
        self.page.update()

    def alterar_status(self, pedido):
        if pedido["status"] == "Pendente":
            pedido["status"] = "Em Preparação"
        elif pedido["status"] == "Em Preparação":
            pedido["status"] = "Finalizado"
            
        self.atualizar_lista_pedidos()
