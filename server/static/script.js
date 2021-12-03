const FORMAT_ERROR = "CIP code has to be of format XX, XX.XX or XX.XXXX."
const CIP_DOES_NOT_EXIST = "CIP code does not exist."
const SOC_DOES_NOT_EXIST = "No SOC codes found for this CIP code."
const SOC_DATA_KEYS = ['soc_code', 'soc_title', 'total_employed', 'annual_mean']

function hideVis(){
    let content = document.getElementById('visualization')
    content.classList.add('d-none')
}

function showVis(){
    let content = document.getElementById('visualization')
    content.classList.remove('d-none')
}

function hideLoadingGif(){
    let gif = document.getElementById('gif')
    gif.classList.add('d-none')
}

function showLoadingGif(){
    let gif = document.getElementById('gif')
    gif.classList.remove('d-none')
}

function hideVisShowLoadingGif(){
    hideVis()
    showLoadingGif()
}
    
function showVisHideLoadingGif(){
    showVis()
    hideLoadingGif()
}

function hideVisHideLoadingGif(){
    hideVis()
    hideLoadingGif()
}

function showError(message){
    let cipHelp = document.getElementById('cipHelp')
    cipHelp.innerText = message
    cipHelp.classList.remove('d-none')
}

function hideError(){
    let cipHelp = document.getElementById('cipHelp')
    cipHelp.classList.add('d-none')
}

function validateCIPCode(){
    let re = /^\d{2}(\.(\d{2}|\d{4}))?$/
    const cip = document.getElementById('cip_code_input').value
    return re.test(cip) ? cip : null
}

function removeAllItemsFromTable(){
    let tableBodyObject = document.getElementById('only-table').lastElementChild
    tableBodyObject.innerHTML = '\n'
}

function addItemsToTable(soc_data){
    let tableBodyObject = document.getElementById('only-table').lastElementChild
    for (let i = 0; i < soc_data.length; i++){
        let row = tableBodyObject.insertRow()
        for (let j = 0; j < SOC_DATA_KEYS.length; j++){
            let cell = row.insertCell()
            cell.innerText = soc_data[i][SOC_DATA_KEYS[j]]
        }
    }
}

function getSOCDataForCIPCode(){
    const cip = validateCIPCode()
    if (cip === null){
        showError(FORMAT_ERROR)
        return
    }
    hideError()
    hideVisShowLoadingGif()
    let req = new XMLHttpRequest();
    req.responseType = 'json'
    const cipType2010 = document.getElementById('cip2010Radio')
    const cipType2020 = document.getElementById('cip2020Radio')
    const cipType = cipType2010.checked ? cipType2010.value : cipType2020.value
    const url=`/api/cip/${cip}/soc/?cip_code_kind=${cipType}`;
    req.open("GET", url);
    req.onreadystatechange=function(){
        if(this.readyState === XMLHttpRequest.DONE) {
            const status = this.status
            if (status == 0 || status >= 200 && status < 400){
                if (req.response.length === 0){
                    showError(SOC_DOES_NOT_EXIST)
                    hideLoadingGif()
                    return
                }
                removeAllItemsFromTable()
                addItemsToTable(req.response)
                showVisHideLoadingGif()
            }else{
                showError(CIP_DOES_NOT_EXIST)
                hideLoadingGif()
            }
        }
    }
    req.send()
}