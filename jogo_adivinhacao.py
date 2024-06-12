"""
Jogo de adivinhação em python.
---------------------------------------------------------------------
Ele utiliza a API com o gemini e é necessário ter uma chave para
fazer o chat funcionar.

A chave esta sendo passada diretamente no atributo google_API.

O chat é resposável por dar as dicas e palavras.
"""

from google import generativeai as genai
import os

class JogoAdivinhacao:
    def __init__(self: object) -> None:
        self.__tentativa = 5
        self.__palavra = None
        self.__google_API = os.environ.get("GEMINI_API")
        self.__chat = None
        self.__tamanho = None

    @property
    def tentativa(self: object) -> int:
        return self.__tentativa
    
    @tentativa.setter
    def tentativa(self: object, nova_tentativa: int) -> None:
        self.__tentativa = nova_tentativa

    @property
    def palavra(self: object) -> str | None:
        return self.__palavra
    
    @palavra.setter
    def palavra(self: object, nova_palavra: str) -> None:
        self.__palavra = nova_palavra

    @property
    def google_API(self: object) -> str:
        return self.__google_API
    
    @google_API.setter
    def google_API(self: object, google_API: str) -> None:
        self.__google_API = google_API
    
    @property
    def chat(self: object) -> genai:
        return self.__chat
    
    @chat.setter
    def chat(self: object, novo_chat: genai) -> None:
        self.__chat = novo_chat
        
    @property
    def tamanho(self: object) -> int | None:
        return self.__tamanho
    
    @tamanho.setter
    def tamanho(self: object, tamanho: int) -> None:
        self.__tamanho = tamanho

    def __str__(self: object) -> str:
        return f"""Palavra: {self.palavra}
Tentativas: {self.tentativa}
google_API: '{self.google_API}'
        """
        
    def sortear_palavra(self: object) -> str:
        """
        Método responsável por sortear uma palavra, caso a palavra\
        sorteada seja igual a anterior haverá um segundo sorteo.

        Returns:
            str: Retorna a palavra sorteada
        """
        palavra_escolhida = self.chat.send_message(
            f"Gere uma palavra para um jogo de adivinhação.\n\
            A palavra pode conter até 10 letras.\n\
            A palavra não pode ser {self.palavra}.\n\
            palavra sobre qualquer tema/assunto.\n\
            Verificar a grafia da palavra antes de enviar."
        ).text
        if palavra_escolhida == self.palavra:
            self.sortear_palavra()
        else:
            return palavra_escolhida.lower().strip()
       
    def gerar_chat(self: object) -> genai:
        """
        Método reponsável por gerar o chat do gemini e atribui este\
        chat ao atributo chat para que haja um histórico das\
        palavras sorteadas.

        Returns:
            genai: Retorna o chat criado
        """
        def gerar_modelo() -> genai:
            """
            Gera o modelo do chat mais suas configurações

            Returns:
                genai: Retorna o modelo criado
            """
            genai.configure(api_key=self.google_API)
            modelo = genai.GenerativeModel(
                model_name='models/gemini-1.0-pro',
                safety_settings={
                    "harassment": "block_none",
                    "hate": "block_none",
                    "sexual": "block_none",
                    "dangerous": "block_none"
                }, 
                generation_config={
                    "candidate_count" : 1,
                    "temperature" : 1
                }
                )
            return modelo        
        chat = gerar_modelo().start_chat()
        self.chat = chat
        return chat
    
    def gerar_dica(self: object) -> str:
        """
        Método responsável por gerar dica com base no chat gerado

        Returns:
            str: Retorna a dica em forma de texto
        """
        return self.chat.send_message(
            "De uma dica de no máximo 35 letras sobre uma palavra em um jogo de adivinhação.\n"
            f"A palavra sorteada é {self.palavra}.\n"
            "Escreva a dica neste formato: 'frase com a dica' \n"
            "Não ultrapassar 35 caracteres \n"
            "ELI5"
            ).text

    def iniciar_jogo(self: object) -> None:
        """
        Método responsável por rodar o jogo e que chamar o todos os\
        métodos necessários para o jogo funcionar.
        
        Ele cria o chat, se necessário, e sortea uma palavra
        """
        if not self.chat:
            self.gerar_chat()          
        self.palavra = self.sortear_palavra()
        self.tamanho = len(self.palavra)
    
    def verifica_resposta(self: object, resposta: str) -> bool:
        """
        Método responsável por verificar a resposta fornecida e\
        retornar um booleano.

        Args:
            resposta (str): Resposta dada pelo usuário.

        Returns:
            bool: Retorna True caso esteja certa a resposta ou\
                  false caso esteja errada.
        """
        resposta = str(resposta).strip().lower()
        if resposta == self.palavra:
            return True
        else:
            return False
       