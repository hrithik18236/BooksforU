let delbtns = document.querySelectorAll(".delbtn");

delbtns.forEach(function (currBtn){
	currBtn.addEventListener("click", function () {
		alert("Deletion succesful!");
	});
})

let editBtns = document.querySelectorAll(".editbtn, .24");

console.log(editBtns);
