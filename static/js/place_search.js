 let places_list_in_js=[]
    {% for place in place_list %}
    places_list_in_js.push(place)
    {% endfor %}
    console.log(places_list_in_js)


    searchBtn=document.getElementByID('searchTxt')
    console.log(searchBtn)
    searchBtn.addEventListener('input',function(){
        textTyped=searchBtn.innerText

        if places_list_in_js.includes(textTyped){
        console.log('yes')
        }

    })