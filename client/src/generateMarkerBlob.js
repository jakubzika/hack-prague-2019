
let containerInfo = {
    1: 'Colored glass',
    2: 'Electric devices',
    3: 'Metals',
    4: 'Beverage cartons',
    5: 'Paper',
    6: 'Plastic',
    7: 'Clear glass',
    8: 'Textile',
}

export function generateMarkerBlob(container) {
    console.log('blob',container);
    let blob = '<div>';
    blob += `<div class="header">Containers `
    blob += `<span class="distance">${container.distance}</span> meters away</div>`
    for(let i =0; i < container.types.length;i++) {
        console.log(container.types[i]);
        blob += '<div>'
        blob += `<div class="item">- ${containerInfo[container.types[i]]}</div>`
        blob += '</div>'
    }
    blob+= `<span>${container.public}</span>`
    console.log(container);

    return blob+"</div>";
}