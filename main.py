from jogo_adivinhacao import JogoAdivinhacao
import tkinter as tk

class Interface:  
    def __init__(self: object, master: tk.Tk) -> None:
        self.master = master
        self.jogo = JogoAdivinhacao()
        self.len_x = 285
        self.len_y = 225
        self.layout()
        self.rodar_jogo()

    def layout(self: object) -> None:
        """
        Método responsável por criar todos elementos que estarão\
        na interface.
        """
        #Configuracoes janela
        self.master.title("Jogo de Adivinhação")
        self.master.geometry(f"{self.len_x}x{self.len_y}")

        #Dica
        self.label_dica = tk.Label(self.master, text="")
        self.label_dica.place(x=0, y=10)

        #Palavra sorteada
        self.label_palavra = tk.Label(self.master, text="")
        self.label_palavra.place(x=0, y=40)
             
        #Input resposta
        self.entrada_resposta = tk.Entry(self.master, justify="center")
        self.entrada_resposta.place(x=0, y=110, width=100)
        
        #Retorno
        self.label_retorno = tk.Label(self.master, text="")
        self.label_retorno.place(x=0, y=75)
        
        #Botao resposta
        self.botao_resposta = tk.Button(
            self.master,
            text="Enviar resposta",
            command=self.receber_resposta
        )
        self.botao_resposta.place(x=155, y=150)
        
        #Botao trocar palava
        self.botao_troca_palavra = tk.Button(
            self.master,
            text="Trocar palavra",
            command=self.trocar_palavra
        )
        self.botao_troca_palavra.place(x=30, y=150)
        
        #Vidas restantes
        self.label_vidas = tk.Label(self.master, text="")
        self.label_vidas.place(x=0, y=190)
      
    def centraliza_palavra(self: object, widget: tk.Widget, texto: str = "") -> None:
        """
        Método responsável por centralizar os elementos necessários\
        na interface.

        Args:
            widget (tk.Widget): elemento que deve ser centralizado
            texto (str): texto opcional para mudar no widget
        """
        if texto:
            widget.config(text=texto)
        widget.update_idletasks()
        width_palavra = widget.winfo_width()
        posicao = (self.len_x - width_palavra) / 2
        widget.place_configure(x=posicao)
        
    def receber_resposta(self: object) -> None:
        """
        Método que recebe a resposta do usuário e chama a função\
        do jogo verifica_resposta que realizada o comparativo com\
        a resposta dada e a certa.
        """  
        resposta = self.entrada_resposta.get()
        if resposta:
            resposta_correta = self.jogo.verifica_resposta(resposta)
            self.atualizar_resultado(resposta_correta)
        else:
            self.entrada_resposta.delete(0, tk.END)
            
    def atualizar_resultado(self: object, resposta: bool) -> None:
        """
        Método resonsável por atualizar o label e dar uma resposta\
        ao usuário caso ele acerte ou erre a palavra.

        Args:
            resposta (bool): resposta dada pela classe JogoAdivinhacao
        """
        def limpar_resposta() -> None:
            """
            Método resposável por deixar o label de retorno com a\
            escrita padrão novamente
            """
            self.centraliza_palavra(self.label_retorno, "Resposta:")
            self.entrada_resposta.delete(0, tk.END)
            if self.jogo.tentativa == 0 or resposta:
                self.trocar_palavra()
                
        if resposta:
            self.centraliza_palavra(self.label_retorno, "Resposta correta!")
        else:
            self.jogo.tentativa -= 1
            self.centraliza_palavra(self.label_retorno, "Resposta errada!")
            self.label_vidas.config(text=f"Vidas restantes: {self.jogo.tentativa}")
            
        self.master.after(1500, limpar_resposta)
        
    def rodar_jogo(self: object) -> None:
        """
        Método responsável por fazer o jogo funcionar dentro da\
        interface, ele chama todos os métodos necessários da\
        classe JogoAdivinhação para dar andamento ao jogo e\
        é responsável por chamar o método de centralização\
        dos elementos.
        """
        def divisor_dica() -> str:
            """
            Método que quebra a linha da dica caso ela seja\
            maior do que 40 caracteres e modifica a posição\
            da dica para melhor visualização

            Returns:
                str: dica formatada com quebra de linha.
            """
            if len(self.dica) > 80:
                return self.rodar_jogo()
            dica_dividida = self.dica.split(" ")
            tamanho = 0
            
            for i in dica_dividida:
                if tamanho + len(i) + 1 > 40:
                    break
                else:
                    tamanho += len(i) + 1
                    
            nova_dica = ""
            
            for letra in self.dica:
                nova_dica += letra
                if len(nova_dica) == tamanho:
                    nova_dica += "\n"
                    
            self.label_dica.place_configure(y=5) #Sobe a posição da dica para não haver conflito com outros elementos
            return nova_dica
        try:
            self.jogo.iniciar_jogo()
            self.dica = self.jogo.gerar_dica()
            if len(self.dica) > 40:
                self.dica = divisor_dica()
            else:
                self.label_dica.place_configure(y=10) #Volta a dica para a posição inicial

            #Centralizando os elementos
            for (chave, valor) in {
                self.label_vidas: f"Vidas restantes: {self.jogo.tentativa}",
                self.label_dica: self.dica,
                self.label_palavra: "___ "*self.jogo.tamanho,
                self.label_retorno: "Resposta:",
                self.entrada_resposta: ""
            }.items():
                self.centraliza_palavra(chave, valor)
        except BaseException:
            self.rodar_jogo()
    
    def trocar_palavra(self: object) -> None:
        """
        Método responsável por trocar a palavra, resetar a\
        vida para 5, limpar o campo de entrada e chamar o\
        método rodar_jogo.
        """
        self.entrada_resposta.delete(0, tk.END) # Limpando o campo de entrada.
        self.jogo.tentativa = 5
        self.rodar_jogo()
    
if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
    