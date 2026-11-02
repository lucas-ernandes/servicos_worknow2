
    /* ---------- Mostrar / ocultar senha = LOGIN & CADASTRO---------- */
    document.querySelectorAll('[data-alternar-senha]').forEach(botao => {
    botao.addEventListener('click', () => {
        const campo = document.getElementById(botao.dataset.alternarSenha);
        if (!campo) return;

        const mostrando = campo.type === 'text';
        campo.type = mostrando ? 'password' : 'text';

        const icone = botao.querySelector('i');
        if (icone) {
            icone.classList.toggle('fa-eye', mostrando);
            icone.classList.toggle('fa-eye-slash', !mostrando);
        }

        botao.setAttribute('aria-label', mostrando ? 'Mostrar senha' : 'Ocultar senha');
    });
});

(function () {
    const form = document.getElementById('form-cadastro');
    if (!form) return; // só roda na página de cadastro
 
    const extrasProfissional = document.getElementById('extras-profissional');
    const endereco = document.getElementById('endereco_referencia');
    const rotuloEndereco = document.getElementById('rotulo-endereco');
    const opcionalEndereco = document.getElementById('opcional-endereco');
    const ajudaEndereco = document.getElementById('ajuda-endereco');
    const senha = document.getElementById('senha');
    const confirmar = document.getElementById('confirmar_senha');
    const telefone = document.getElementById('telefone');
    const descricao = document.getElementById('descricao');
    const contador = document.getElementById('contador-descricao');
    const botaoCriar = document.getElementById('btn-criar-conta');
 
    /* ---------- Tipo de conta (cliente / profissional) ---------- */
    function tipoSelecionado() {
        return form.querySelector('input[name="tipo"]:checked').value;
    }
 
    function atualizarTipo() {
        const ehProfissional = tipoSelecionado() === 'profissional';
 
        // Campos exclusivos do profissional: mostrados e validados só nesse caso.
        // Campos desativados não são enviados nem entram na validação.
        extrasProfissional.hidden = !ehProfissional;
        extrasProfissional.querySelectorAll('input, textarea').forEach(el => {
            el.disabled = !ehProfissional;
        });
 
        // O campo de endereço é o mesmo para os dois, só muda o texto e a obrigatoriedade
        endereco.required = ehProfissional;
        opcionalEndereco.hidden = ehProfissional;
        rotuloEndereco.textContent = ehProfissional
            ? 'Região onde você atende'
            : 'Endereço de referência';
        ajudaEndereco.textContent = ehProfissional
            ? 'Informe o bairro ou a região para aparecer nas buscas de quem está perto.'
            : 'Usamos para mostrar profissionais perto de você.';
    }
 
    form.querySelectorAll('input[name="tipo"]').forEach(radio => {
        radio.addEventListener('change', atualizarTipo);
    });
    atualizarTipo();
 
    /* ---------- Máscara de telefone: (86) 99999-9999 ---------- */
    telefone.addEventListener('input', () => {
        const d = telefone.value.replace(/\D/g, '').slice(0, 11);
        let formatado = d;
 
        if (d.length > 10) {
            formatado = `(${d.slice(0, 2)}) ${d.slice(2, 7)}-${d.slice(7)}`;
        } else if (d.length > 6) {
            formatado = `(${d.slice(0, 2)}) ${d.slice(2, 6)}-${d.slice(6)}`;
        } else if (d.length > 2) {
            formatado = `(${d.slice(0, 2)}) ${d.slice(2)}`;
        } else if (d.length > 0) {
            formatado = `(${d}`;
        }
 
        telefone.value = formatado;
    });
 
    /* ---------- Confirmação de senha ---------- */
    function validarConfirmacao() {
        confirmar.setCustomValidity(
            confirmar.value !== senha.value ? 'As senhas precisam ser iguais.' : ''
        );
    }
    senha.addEventListener('input', validarConfirmacao);
    confirmar.addEventListener('input', validarConfirmacao);

 
    /* ---------- Contador da descrição ---------- */
    function atualizarContador() {
        contador.textContent = descricao.value.length;
    }
    descricao.addEventListener('input', atualizarContador);
    atualizarContador();
 
    /* ---------- Envio ---------- */
    form.addEventListener('submit', (e) => {
        validarConfirmacao();
 
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
            form.classList.add('was-validated');
 
            // Leva o foco para o primeiro campo com problema
            const primeiroInvalido = form.querySelector(':invalid');
            if (primeiroInvalido) primeiroInvalido.focus();
            return;
        }
 
        // Evita enviar duas vezes se a pessoa clicar de novo
        botaoCriar.disabled = true;
        botaoCriar.textContent = 'Criando conta...';
    });
})();