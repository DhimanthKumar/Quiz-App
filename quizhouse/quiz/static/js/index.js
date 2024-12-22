
// 
function update(){
    const radios= document.querySelectorAll('.radio');
    const answer = document.getElementById('id_answer');
    answer.readOnly=true;
    radios.forEach( (value) =>{ 
        if (value.checked){
            const val = value.parentElement.querySelectorAll('[id^="id_form-"]')[0];
            answer.value=val.value;
            answer.style.backgroundColor="limegreen";
        }
    })

}
document.addEventListener("keyup" , ()=> {
    update();
})
document.body.addEventListener('change', (event) => {
    // Check if the target is a radio button
    if (event.target.classList.contains('radio')) {
        update();
    }
});
