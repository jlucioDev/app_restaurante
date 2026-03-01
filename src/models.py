from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    papel = Column(String(50), nullable=False) # Ex: 'Garçom', 'Cozinha', 'Admin'
    senha = Column(String(50), nullable=True) # Pode ser melhorado para hash no futuro
    
    # Relação: Um usuário pode fazer vários pedidos
    pedidos = relationship("Pedido", back_populates="garcom")

    def __repr__(self):
        return f"<Usuario(nome='{self.nome}', papel='{self.papel}')>"

class Categoria(Base):
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    
    # Relação: Uma categoria tem vários produtos
    produtos = relationship("Produto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(nome='{self.nome}')>"

class Produto(Base):
    __tablename__ = 'produtos'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    preco = Column(Float, nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    
    # Relações
    categoria = relationship("Categoria", back_populates="produtos")
    itens_pedido = relationship("ItemPedido", back_populates="produto")

    def __repr__(self):
        return f"<Produto(nome='{self.nome}', preco={self.preco})>"

class Mesa(Base):
    __tablename__ = 'mesas'
    
    id = Column(Integer, primary_key=True)
    numero = Column(Integer, nullable=False, unique=True)
    status = Column(String(50), default="Livre") # Ex: 'Livre', 'Ocupada', 'Fechando'
    
    # Relação: Uma mesa pode ter vários pedidos
    pedidos = relationship("Pedido", back_populates="mesa")

    def __repr__(self):
        return f"<Mesa(numero={self.numero}, status='{self.status}')>"

class Pedido(Base):
    __tablename__ = 'pedidos'
    
    id = Column(Integer, primary_key=True)
    data_hora = Column(DateTime, default=datetime.now)
    status = Column(String(50), default="Pendente") # Ex: 'Pendente', 'Em Preparação', 'Finalizado', 'Entregue'
    
    mesa_id = Column(Integer, ForeignKey('mesas.id'), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=True) # Garçom que abriu o pedido
    
    # Relações
    mesa = relationship("Mesa", back_populates="pedidos")
    garcom = relationship("Usuario", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pedido(id={self.id}, mesa={self.mesa_id}, status='{self.status}')>"

class ItemPedido(Base):
    __tablename__ = 'itens_pedido'
    
    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    quantidade = Column(Integer, default=1, nullable=False)
    observacao = Column(String(255), nullable=True)
    
    # Relações
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_pedido")

    def __repr__(self):
        return f"<ItemPedido(produto_id={self.produto_id}, qtd={self.quantidade})>"


# Configuração e Criação do Banco
def criar_banco():
    engine = create_engine('sqlite:///restaurante.db', echo=True)
    Base.metadata.create_all(engine)
    print("Banco de dados SQLite (restaurante.db) criado com sucesso baseado nos modelos.")

if __name__ == "__main__":
    criar_banco()
