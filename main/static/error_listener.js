const inputs = document.querySelectorAll("input, select, textarea");
let btn = document.getElementById('submit-button')

document.addEventListener('invalid', (function () {
  return function (e) {
    e.preventDefault();
    document.getElementById("name").focus();
  };
})(), true)

btn.addEventListener('click', event  => {
  inputs.forEach(input => {
    input.classList.remove('error');
  })
});

inputs.forEach(input => {
  input.addEventListener(
    "invalid",
    event => {
      input.classList.add("error");
    },
    false
  );
});
