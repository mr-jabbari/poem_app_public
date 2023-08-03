const tabButtons = document.querySelectorAll(".tab-button");
const tabContents = document.querySelectorAll(".tab-content");

function showTab(tabIndex) {
	tabButtons.forEach((button) => {
		button.classList.remove("active");
	});
	tabContents.forEach((content) => {
		content.classList.remove("active");
	});
	tabButtons[tabIndex].classList.add("active");
	tabContents[tabIndex].classList.add("active");
}

showTab(0);

tabButtons.forEach((button, index) => {
	button.addEventListener("click", () => {
		showTab(index);
	});
});