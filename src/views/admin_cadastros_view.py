import flet as ft
from components.sidebar import Sidebar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Categoria

class AdminCadastrosView(ft.View):
    # Using class-level property for engine
    engine = create_engine('sqlite:///d:/app_flet_route_exemple/src/restaurante.db')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def load_categorias(self, data_table):
        db = self.SessionLocal()
        categorias = db.query(Categoria).all()
        
        data_table.rows.clear()
        for cat in categorias:
            data_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(cat.id))),
                        ft.DataCell(ft.Text(cat.nome)),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(icon=ft.Icons.EDIT, icon_color=ft.Colors.BLUE_400, data=cat.id, on_click=self.edit_categoria),
                                ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_400, data=cat.id, on_click=self.delete_categoria)
                            ])
                        )
                    ]
                )
            )
        db.close()
        try:
            if data_table.page:
                data_table.update()
        except Exception:
            pass

    def add_categoria(self, e, txt_nome, data_table):
        if not txt_nome.value: return
        db = self.SessionLocal()
        nova_categoria = Categoria(nome=txt_nome.value)
        db.add(nova_categoria)
        db.commit()
        db.close()
        txt_nome.value = ""
        txt_nome.update()
        self.load_categorias(data_table)
        
    def edit_categoria(self, e):
        # We will dispatch an edit dialog in the future
        pass
        
    def delete_categoria(self, e):
        db = self.SessionLocal()
        cat = db.query(Categoria).filter(Categoria.id == e.control.data).first()
        if cat:
            db.delete(cat)
            db.commit()
        db.close()
        
        # We reload the layout by triggering a faux click on the Categorias tab
        # or we could find the table reference. For simplicity let's reload the view.
        self.page.run_task(self.page.push_route, "/admin/cadastros")

    def __init__(self, page):
        super().__init__(
            route="/admin/cadastros", 
            bgcolor=ft.Colors.GREY_900,
            padding=0
        )
        
        # Sub-views container (right side panel)
        self.main_content = ft.Container(
            expand=True,
            bgcolor=ft.Colors.GREY_100,
            content=self.build_content()
        )
        
        # Instantiate common sidebar and set active tab
        self.sidebar = Sidebar(on_menu_change=self.handle_content_change)
        for item in self.sidebar.items_top_sidebar + self.sidebar.items_bottom_sidebar:
            item.set_checked(item.text_val == "Cadastros")

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
        if menu_name == "Dashboard":
            self.page.run_task(self.page.push_route, "/admin/dashboard")
        elif menu_name == "Cadastros":
            self.page.run_task(self.page.push_route, "/admin/cadastros")
        elif menu_name == "Cozinha":
            self.page.run_task(self.page.push_route, "/admin/cozinha")
        elif menu_name == "Usuário":
            self.page.run_task(self.page.push_route, "/admin/usuario")
        elif menu_name == "Configurações":
            self.page.run_task(self.page.push_route, "/admin/configuracoes")
        elif menu_name == "Sair":
            self.page.run_task(self.page.push_route, "/")
            
    def build_content(self):
        # -----------------------------------------------------
        # CATEGORIAS TAB CONTENT
        # -----------------------------------------------------
        txt_nome_categoria = ft.TextField(label="Nome da Categoria", expand=True, border_color=ft.Colors.GREY_600, color=ft.Colors.GREY_900)
        dt_categorias = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Nome")),
                ft.DataColumn(ft.Text("Ações")),
            ],
            rows=[]
        )
        
        btn_salvar_cat = ft.Button("Salvar", icon=ft.Icons.SAVE, bgcolor=ft.Colors.ORANGE_800, color=ft.Colors.WHITE, on_click=lambda e: self.add_categoria(e, txt_nome_categoria, dt_categorias))
        
        categorias_layout = ft.Container(
            content=ft.Column([
                ft.Text("Adicionar Nova Categoria", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                ft.Row([txt_nome_categoria, btn_salvar_cat]),
                ft.Divider(color=ft.Colors.GREY_500),
                ft.Text("Listagem de Categorias", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_800),
                dt_categorias
            ], expand=True),
            padding=10,
            expand=True
        )
        
        # Load intial data
        self.load_categorias(dt_categorias)

        # -----------------------------------------------------
        # DYNAMIC TAB SWITCHING LOGIC
        # -----------------------------------------------------
        content_area = ft.Container(
            content=ft.Text("Lista de Usuários via BD em breve...", color=ft.Colors.GREY_400), 
            padding=20, 
            expand=True
        )
        
        # The distinct content for each tab
        tab_contents = {
            "Usuários": ft.Text("Lista de Usuários via BD em breve...", color=ft.Colors.GREY_400),
            "Produtos": ft.Text("Lista de Produtos via BD em breve...", color=ft.Colors.GREY_400),
            "Categorias": categorias_layout,
            "Mesas": ft.Text("Gerenciamento de Mesas via BD em breve...", color=ft.Colors.GREY_400)
        }
        
        def on_tab_click(e):
            # Update active button visual
            for c in tab_row.controls:
                is_active = (c.data == e.control.data)
                color = ft.Colors.ORANGE_500 if is_active else ft.Colors.GREY_400
                c.content.controls[0].color = color
                c.content.controls[1].color = color
                c.update()
                
            # Update content view
            content_area.content = tab_contents[e.control.data]
            content_area.update()

        tab_row = ft.Row([
            ft.TextButton(
                content=ft.Row([ft.Icon(ft.Icons.PERSON, color=ft.Colors.ORANGE_500), ft.Text("Usuários", color=ft.Colors.ORANGE_500)]),
                data="Usuários", on_click=on_tab_click
            ),
            ft.TextButton(
                content=ft.Row([ft.Icon(ft.Icons.FASTFOOD, color=ft.Colors.GREY_400), ft.Text("Produtos", color=ft.Colors.GREY_400)]),
                data="Produtos", on_click=on_tab_click
            ),
            ft.TextButton(
                content=ft.Row([ft.Icon(ft.Icons.CATEGORY, color=ft.Colors.GREY_400), ft.Text("Categorias", color=ft.Colors.GREY_400)]),
                data="Categorias", on_click=on_tab_click
            ),
            ft.TextButton(
                content=ft.Row([ft.Icon(ft.Icons.TABLE_RESTAURANT, color=ft.Colors.GREY_400), ft.Text("Mesas", color=ft.Colors.GREY_400)]),
                data="Mesas", on_click=on_tab_click
            ),
        ])

        return ft.Container(
            content=ft.Column([
                ft.Text("Gerenciamento de Cadastros", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                tab_row,
                ft.Divider(color=ft.Colors.GREY_500),
                content_area
            ], expand=True),
            padding=20, expand=True
        )
