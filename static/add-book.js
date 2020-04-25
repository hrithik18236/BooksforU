console.log("Hello World")

let formbtn = document.querySelector("button");
let textfields = document.querySelectorAll(".textfield");

console.log(textfields);

formbtn.addEventListener("click", (e) => {
	textfields.forEach((textfield) => {
		textfield.value = textfield.value.replace("'", "''");
	});
});

///////////////////////

let exchangeRadio = document.getElementById("exchange")
let lendRadio = document.getElementById("lend")
let sellRadio = document.getElementById("sell")


exchangeRadio.addEventListener("click", function() {
	if (exchangeRadio.checked) {
		console.log(exchangeRadio.value)
		// lendRadio.style.display = "none";

		document.querySelector(".price").innerHTML = "";

		document.querySelector(".num-of-days").innerHTML = "";

		document.querySelector(".exchange-description").innerHTML = '<label for="exchange-description"><b>Tell us briefly about the condition of the book and what you want to exchange it for</b></label> <input type="text" placeholder="Enter description" name="exchange-description" required> <br>';
	}
});

lendRadio.addEventListener("click", function() {
	if (lendRadio.checked) {
		console.log(lendRadio.value)
	}
	
	document.querySelector(".price").innerHTML = '<label for="price"><b>Price</b></label> <input type="number" placeholder="Enter price" name="price" required> <br> <br>';

	document.querySelector(".num-of-days").innerHTML = '<label for="num-of-days"><b>No. of days</b></label> <input type="number" placeholder="Enter no. of days" name="num-of-days" required> <br>';

	document.querySelector(".exchange-description").innerHTML = "";

});

sell.addEventListener("click", function() {
	console.log("clicked on sell");
	

	if (sellRadio.checked) {
		console.log(sellRadio.value)
	}

	document.querySelector(".price").innerHTML = '<label for="price"><b>Price</b></label> <input type="number" placeholder="Enter price" name="price" required> <br> <br>';

	document.querySelector(".num-of-days").innerHTML = "";

	document.querySelector(".exchange-description").innerHTML = "";

});