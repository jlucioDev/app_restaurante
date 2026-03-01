import flet as ft
from views.home_view import HomeView
from views.admin_view import AdminView
from views.cozinha_view import CozinhaView


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    

    def nova_rota():
        page.views.clear()

        page.views.append(HomeView(page))

        if page.route == "/admin":
            page.views.append(AdminView(page))
            
        elif page.route == "/cozinha":
            page.views.append(CozinhaView(page))
            
        page.update()
       
    
    async def voltar_rota_anterior(e: ft.ViewPopEvent):
        if e.view is not None:
            print("View pop: ", e.view)
            page.views.pop()
            top_view = page.views[-1]
            await page.push_route(top_view.route)



    page.on_route_change = nova_rota
    page.on_view_pop = voltar_rota_anterior

    nova_rota()


# Executando o aplicativo
if __name__ == "__main__":
    ft.run(main)