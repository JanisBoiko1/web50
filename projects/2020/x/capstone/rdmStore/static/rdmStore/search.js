document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#search-btn').addEventListener('click', () => search());
    var HttpClient = function () {
        this.get = function (aUrl, aCallback) {
            var anHttpRequest = new XMLHttpRequest();
            anHttpRequest.onreadystatechange = function () {
                if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                    aCallback(anHttpRequest.responseText);
            }

            anHttpRequest.open("GET", aUrl, true);
            anHttpRequest.send(null);
        }
    }
    console.log(HttpClient)
})

function search() {
    // selecionar valor do form
    var content = document.querySelector('#search-form').value;
    const request = require("request");
    document.querySelector('#conteudo').textContent = request

    //usar fetch para comparar com categorias, nomes e descrições de produtos
    //carregar pagina de seleção com o <string=elemento> "busca" e os resultados da busca por Api
    //editar o views.py e a categoriasEBusca.html para mostrar o resultado

}