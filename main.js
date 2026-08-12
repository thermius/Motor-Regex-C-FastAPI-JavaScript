	/*Função que é chamada ao clicar em "analisar"*/
async function Analisar() 
{
	/*Obtem os elementos limpando todos os espaços no começo e fim*/
	const elemento_regex	= document.getElementById ("regex").value.trim();
	const elemento_string	= document.getElementById ("string").value.trim();

	/*Testa se existe elementos*/
	if (elemento_regex == ""|| elemento_string == "") 
	{
		alert ("Sem regex ou string para analise");
		return;
	}

	/*Tenta chamar API python e espera pela promisse*/
	try {
		const resposta			= await fetch ("http://127.0.0.1:8000/motor_regex",
		{

			method: "POST",
			headers :
			{
			"Content-Type": "application/json"
			},
			body: JSON.stringify(
			{
				regex: elemento_regex,
				string: elemento_string
			})
		})

		/*Obtem o resultado em json*/
		const resultado = await resposta.json();

		/*Tenta pegar a textare de saida ou o botão finalizar*/
		let saida 			= document.getElementById("saida_regex");
		let botao_finalizar	= document.getElementById("botao_finalizar");

		/*Se não existir, cria a text area*/
		if (!saida)
		{
			/*Cria a saida*/
			saida = document.createElement("textarea");
			
			/*Marca atributos da text area*/
			saida.id 		= "saida_regex";
			saida.readOnly	= true;
			saida.rows 		= 5;
			saida.cols 		= 50;
			
			/*Insere a text area no body do documento*/
			document.body.appendChild(saida);
		}

		/*Se não existir, cria o botão*/
		if (!botao_finalizar)
		{
			/*Cria o botão*/
			botao_finalizar = document.createElement("button");
			
			/*Marca atributos do botão*/
			botao_finalizar.id 			= "botao_finalizar";
			botao_finalizar.textContent	= "Finalizar";
			
			/*Insere o botão areá no body do documento*/
			document.body.appendChild(botao_finalizar);
			
			/*Adciona ao botão a função para destruir a text area e o botão*/
			botao_finalizar.addEventListener("click", function()
			{
				saida.remove();
				botao_finalizar.remove();
			});
		}

		/*Escreve a resposta da api na text area*/
		saida.value = resultado.status;
		if (resultado.status == "falha") { saida.value += " em posição: " + 	(resultado.posicao + 1) + ", caractrere " + resultado.caractere;}


	}

	/*Trata erros de forma totalmente generica*/
	catch (erro) 
	{
   		alert ("Sem respota da API");
		return;
	}

}
