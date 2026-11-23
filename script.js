const accountOptions = document.querySelectorAll(".account-option");
const accountLabel = document.querySelector("#account-label");
const passwordToggle = document.querySelector(".password-toggle");
const passwordInput = document.querySelector('input[name="password"]');
const form = document.querySelector(".auth-panel");

accountOptions.forEach((option) => {
  option.addEventListener("click", () => {
    accountOptions.forEach((item) => {
      item.classList.remove("active");
      item.setAttribute("aria-selected", "false");
    });

    option.classList.add("active");
    option.setAttribute("aria-selected", "true");
    accountLabel.textContent = `${option.dataset.account} account`;
  });
});

passwordToggle.addEventListener("click", () => {
  const showing = passwordInput.type === "text";
  passwordInput.type = showing ? "password" : "text";
  passwordToggle.setAttribute("aria-label", showing ? "Show password" : "Hide password");
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
});
