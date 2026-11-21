import glob
import os
from pathlib import Path

from dao.usuario_dao import UsuarioDAO

PASTA_UPLOADS = Path(__file__).resolve().parent.parent / "static" / "uploads"
EXTENSOES_PERMITIDAS = {".jpg", ".jpeg", ".png"}
TAMANHO_MAXIMO = 2 * 1024 * 1024  # 2 MB


class Foto:
    @staticmethod
    def salvar(id_usuario, arquivo):
        """Salva a foto de perfil no disco e grava o nome dela no banco.
        'arquivo' é o que vem de request.files['foto'].
        Devolve (True, nome_do_arquivo) se deu certo, ou (False, "mensagem de erro") se não."""
        extensao = os.path.splitext(arquivo.filename)[1].lower()
        if extensao not in EXTENSOES_PERMITIDAS:
            return False, "A foto precisa ser .jpg ou .png."

        # Descobre o tamanho do arquivo sem precisar salvar primeiro:
        # vai até o fim do arquivo (seek), olha a posição (tell) e volta pro início.
        arquivo.seek(0, os.SEEK_END)
        tamanho = arquivo.tell()
        arquivo.seek(0)
        if tamanho > TAMANHO_MAXIMO:
            return False, "A foto não pode passar de 2 MB."

        PASTA_UPLOADS.mkdir(parents=True, exist_ok=True)

        # Apaga qualquer foto anterior desse usuário (pode ter ficado com outra extensão)
        for antiga in glob.glob(str(PASTA_UPLOADS / f"usuario_{id_usuario}.*")):
            os.remove(antiga)

        nome_arquivo = f"usuario_{id_usuario}{extensao}"
        arquivo.save(PASTA_UPLOADS / nome_arquivo)

        UsuarioDAO().atualizar_foto(id_usuario, nome_arquivo)
        return True, nome_arquivo
