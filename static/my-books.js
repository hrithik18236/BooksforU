let btns = document.querySelectorAll(".delbtn");

btns.forEach(function (currBtn){
	currBtn.addEventListener("click", function () {
		alert("Deletion succesful!");
	});
})