document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#search-btn').addEventListener('click', () => search());
})

function search() {
    // selecionar valor do form
    content = document.querySelector('#search-form').value;
    document.querySelector('#conteudo').textContent = content

    //usar fetch para comparar com categorias, nomes e descrições de produtos
    //carregar pagina de seleção com o <string=elemento> "busca" e os resultados da busca por Api
    //editar o views.py e a categoriasEBusca.html para mostrar o resultado

}