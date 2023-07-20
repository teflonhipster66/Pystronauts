function back(){
    window.history.go(-1)
  }


window.addEventListener("DOMContentLoaded", function(event){
  var list2 = [25, 50, 75]
  var progress = document.getElementById("progress").value;
  console.log(progress)
  for (let i = 0; i < 3; i++) {
    if (progress >= list2[i]) {

      document.getElementById(`pic${i}`).className = "rotate3 linear infinite"
      document.getElementById(`pic${i}`).src = `static/planet${i + 2}.png`;
    }
    if (progress < list2[i]) {
      document.getElementById(`link${i}`).href = "#0"
    }
  }

}) 


// const list = [1,2,3,4,5] 
// Quiz code 

function Quiz(){
  for (let i = 0; i < 3; i++) {       
    const radioButtons = document.querySelectorAll(`input[name="q${list[i]}"]`);
    let choice;
    for (const radioButton of radioButtons) {
        if (radioButton.checked) {
            choice = radioButton.value;
            break;
        }
    }
    // show the output:
       
    if (choice == "Correct") {  
      document.getElementById(`head${list[i]}`).style.color = "green";
  }
    else {
      document.getElementById(`a${list[i]}`).style.color = "green"; 
      document.getElementById(`head${list[i]}`).style.color = "red";
        
        }
    };
  }