async function getStaffData() {
    const params = window.location.search;
    params_list = params.split('=');
    role=params_list[1]

    const token = localStorage.getItem("token");
    const response = await fetch(`/api/staff/${role}`, {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    });
    
    const result = await response.json();
        
    if (response.ok){
        const tbody = document.querySelector("#staffTableBody");
        
        const staffList = result.data; 
        tbody.innerHTML = ""; 

        staffList.forEach(staff => {
            const div = document.createElement("div");
            div.innerHTML = `
                <span class="tag">${staff[1]}<span class="remove-tag">&times;</span></span>
                <div class="option" data-value="${staff[1]}">${staff[1]}</div>
            `;
            
            tbody.appendChild(tr);
        });
    } else {
        console.error("無法取得員工資料");
    }
}
getStaffData();

//https://blog.shiangsoft.com/javascript-multiselector/
function initMultiElement() {
  //產生div.dropdown 和 label區塊
  var multiElement = document.createElement('div'); 
  multiElement.setAttribute('class', 'dropdown');
  var html = `<div class="item text">
    <label></label>
  </div>`;

  //forEach 原本的 ListBox (剛剛有先設class="multi-selector"), 取出option value 在寫成新的結構
  document.querySelectorAll('.multi-selector option').forEach(function(optionItem){
  	html += `<div class="item">
    <input type="checkbox" value="${optionItem.value}"/>
    <span>${optionItem.text}</span>
  </div>`
	})
  multiElement.innerHTML = html;
	document.querySelector('.multi-selector').parentElement.appendChild(multiElement);
  setMultiElementEvent(); //設定點擊事件
}

function setMultiElementEvent()
{
  // foreach checkbox 設定 click 事件
  document.querySelectorAll('.item input[type="checkbox"]').forEach(function(checkItem){
    checkItem.addEventListener("click", function(e){
      //紀錄有被選到的選項value
      let resultText = ''; 
      let checkedItems = document.querySelectorAll('.item input:checked[type="checkbox"]')
      checkedItems.forEach(function(selectItem){
        if(resultText !== '')
          resultText += ','
        resultText += selectItem.value
      })

      //把被勾選的value寫入Label
      document.querySelector('.dropdown .text label').innerText = resultText    
      //找原本的ListBox value相等的元素，同時做勾選或取消
      document.querySelector('.multi-selector option[value="'+e.srcElement.value+'"]').selected = e.srcElement.checked
    });
  })
}

window.onload = function() {
  initMultiElement();
}