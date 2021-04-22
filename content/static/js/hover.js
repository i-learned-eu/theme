const card = document.querySelector(".preview-card");
const links = document.querySelectorAll("section a");

for (var i = 0; i < links.length; i++) {
    var link = links[i]
    console.log(link)
    if (link.href !== "mailto:contact+blog@eban.bzh"){
        fetch("https://preview.eban.bzh/?key=f359aff157616dc2ee1008888bc5cbf8&q=" + link.href)
        .then(response => response.json())
        .then(jsonResponse => {
            console.log(link)
            link.setAttribute("data-image", jsonResponse.image)
            link.setAttribute("data-title", jsonResponse.title)
            link.setAttribute("data-text", jsonResponse.description)
	    console.log(link)
        })
    }
}
const hideLinkPreview = () => {
    return card.style.display = 'none';
};

const showLinkPreview = event => {
    const image = event.currentTarget.getAttribute("data-image");
    card.querySelector('img').setAttribute("src", image);

    const title = event.currentTarget.getAttribute("data-title");
    card.querySelector('h5').textContent = title;

    const text = event.currentTarget.getAttribute("data-text");
    card.querySelector('p').textContent = text;

    event.currentTarget.appendChild(card);

    return card.style.display = 'inline-block';
};

document.querySelectorAll("section a").forEach(el => {
    el.addEventListener("mouseover", showLinkPreview);
    el.addEventListener("mouseleave", hideLinkPreview)
});

