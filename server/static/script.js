const FORMAT_ERROR = "CIP code has to be of format XX, XX.XX or XX.XXXX."
const CIP_DOES_NOT_EXIST = "CIP code does not exist."
const SOC_DOES_NOT_EXIST = "No SOC codes found for this CIP code."
const SOC_DATA_KEYS = ['soc_code', 'soc_title', 'total_employed', 'annual_mean']

function handleTableView(){
    let tableViewBtn = document.getElementById('table-view')
    let visViewBtn = document.getElementById('vis-view')
    let tableRow = document.getElementById('table-row')
    let visRow = document.getElementById('vis-row')
    tableViewBtn['aria-pressed'] = true
    tableViewBtn.classList.add('active')
    visViewBtn['aria-pressed'] = false
    visViewBtn.classList.remove('active')
    tableRow.classList.remove('d-none')
    visRow.classList.add('d-none')
}

function handleVisView(){
    let tableViewBtn = document.getElementById('table-view')
    let visViewBtn = document.getElementById('vis-view')
    let tableRow = document.getElementById('table-row')
    let visRow = document.getElementById('vis-row')
    tableViewBtn['aria-pressed'] = false
    tableViewBtn.classList.remove('active')
    visViewBtn['aria-pressed'] = true
    visViewBtn.classList.add('active')
    tableRow.classList.add('d-none')
    visRow.classList.remove('d-none')

}

function hideVis(){
    let content = document.getElementById('visualization')
    content.classList.add('d-none')
    document.getElementById('table-row').classList.remove('d-none')
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
    
function showVisHideLoadingGif(showTable=true){
    showVis()
    hideLoadingGif()
    if (showTable !== null && showTable !== undefined && !showTable){
        let tableRow = document.getElementById('table-row')
        tableRow.classList.add('d-none')
    }
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

function handleCIPInfo(cip_info, cip_type, no_soc_links){
    let cipCard = document.getElementById('cip-info')
    cipCard.innerHTML='\n'

    let cipHeader = document.createElement('div')
    cipHeader.classList.add('card-header')
    const cipTitle = cip_info[`cip${cip_type}title`]
    const cipCode = cip_info[`cip${cip_type}code`]
    cipHeader.innerText = 'CIP Information Card'
    
    let cipBody = document.createElement('div')
    cipBody.classList.add('card-body')
    let header5 = document.createElement('h5')
    header5.innerText = `${cipCode} - ${cipTitle}`
    cipBody.appendChild(header5)

    let list = document.createElement('ul')
    list.classList.add('list-group', 'list-group-flush')
    const itemList = ['cip2010title',
        'cip2020title', 'action', 'textchange']
    for(let i = 0; i < itemList.length; i++){
        const keyValue = cip_info[itemList[i]].length > 0 ?  cip_info[itemList[i]] : 'None'
        let listItem = document.createElement('li')
        listItem.classList.add('list-group-item')
        switch(itemList[i]) {
            case 'cip2010title':
                listItem.innerHTML = `<strong>CIP 2010 Title</strong>: ${keyValue}`
                list.appendChild(listItem)
                break
            case 'cip2020title':
                listItem.innerHTML = `<strong>CIP 2020 Title</strong>: ${keyValue}`
                list.appendChild(listItem)
                break
            case 'action':
                listItem.innerHTML = `<strong>Action</strong>: ${keyValue}`
                list.appendChild(listItem)
                break
            case 'textchange':
                listItem.innerHTML = `<strong>Any changes</strong>: ${keyValue}`
                list.appendChild(listItem)
                break
            default:
                break
        }   
    }
    let cipFooter = document.createElement('div')
    cipFooter.classList.add('card-footer', 'form-text', 'text-danger')
    cipFooter.innerText = SOC_DOES_NOT_EXIST
    cipCard.appendChild(cipHeader)
    cipCard.appendChild(cipBody)
    cipCard.appendChild(list)
    if(no_soc_links){
        cipCard.appendChild(cipFooter)
        showVisHideLoadingGif(false)
    }else{
        showVisHideLoadingGif()
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
    let req = new XMLHttpRequest()
    let req_ = new XMLHttpRequest()
    req.responseType = 'json'
    req_.responseType = 'json'
    const cipType2010 = document.getElementById('cip2010Radio')
    const cipType2020 = document.getElementById('cip2020Radio')
    const cipType = cipType2010.checked ? cipType2010.value : cipType2020.value
    const url=`/api/cip/${cip}/soc/?cip_code_kind=${cipType}`;
    const url_ = `/api/cip/${cip}`

    req.open("GET", url)
    req_.open("GET", url_)
    req.onreadystatechange=function(){
        if(req.readyState === XMLHttpRequest.DONE) {
            const status = req.status
            if (status == 0 || status >= 200 && status < 400){
                req_.onreadystatechange=function(){
                    if(req_.readyState === XMLHttpRequest.DONE) {
                        const status = req_.status
                        if (status == 0 || status >= 200 && status < 400){
                            handleCIPInfo(req_.response, cipType, req.response.length === 0)
                        }
                    }
                }
                req_.send()
                if (req.response.length === 0){
                    // showError(SOC_DOES_NOT_EXIST)
                    // hideLoadingGif()
                    return
                }
                removeAllItemsFromTable()
                addItemsToTable(req.response)
                // showVisHideLoadingGif()
            }else{
                showError(CIP_DOES_NOT_EXIST)
                hideLoadingGif()
            }
        }
    }
    // req_.onreadystatechange=function(){
    //     if(req_.readyState === XMLHttpRequest.DONE) {
    //         const status = req_.status
    //         if (status == 0 || status >= 200 && status < 400){
    //             handleCIPInfo(req_.response, cipType)
    //         }
    //     }
    // }
    req.send()
    // req_.send()
}