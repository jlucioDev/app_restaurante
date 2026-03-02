import flet as ft
from views.home_view import HomeView
from views.admin_dashboard_view import AdminDashboardView
from views.admin_cadastros_view import AdminCadastrosView
from views.admin_cozinha_view import AdminCozinhaView
from views.admin_usuario_view import AdminUsuarioView
from views.admin_configuracoes_view import AdminConfiguracoesView
from views.cozinha_view import CozinhaView

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    

    def nova_rota(route=None):
        page.views.clear()

        # Sempre adiciona a Home por debaixo de tudo na pilha
        page.views.append(HomeView(page))

        # Roteamento modular Admin
        if page.route == "/admin" or page.route == "/admin/dashboard":
            page.views.append(AdminDashboardView(page))
        elif page.route == "/admin/cadastros":
            page.views.append(AdminCadastrosView(page))
        elif page.route == "/admin/cozinha":
            page.views.append(AdminCozinhaView(page))
        elif page.route == "/admin/usuario":
            page.views.append(AdminUsuarioView(page))
        elif page.route == "/admin/configuracoes":
            page.views.append(AdminConfiguracoesView(page))
            
        # Outras telas isoladas
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