function hideContentAndShowLoadingGif(){
    let content = document.getElementById('main-content')
    let gif = document.getElementById('gif')
    gif.classList.remove('d-none')
    content.classList.add('d-none')
}

function showContentAndHideLoadingGif(){
    let content = document.getElementById('main-content')
    let gif = document.getElementById('gif')
    gif.classList.add('d-none')
    content.classList.remove('d-none')
}

function showCIPSOCCrosswalk(){
    hideContentAndShowLoadingGif()
    const req = new XMLHttpRequest();
    const url='/cipsoc';
    req.open("GET", url);
    req.send();
    req.onreadystatechange=function(){
        if(this.readyState===4 && this.status===200){
            document.getElementById('main-content').innerHTML=req.responseText
        }
        showContentAndHideLoadingGif();
    }
}